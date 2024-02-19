"""Main components of sparkplug standard"""
import abc
import asyncio
import logging
from functools import singledispatchmethod
from queue import Queue
from typing import Callable, Literal

from aiospb.mqtt import MqttClient, Will

from . import get_timestamp
from . import messages as m
from .data import DataType, Metric, MetricChange, MetricChangeRequest, ValueType

logging.basicConfig(level=logging.DEBUG)

_NODES_STATES = Literal["online", "offline", "publishing"]


class DeviceConnectionError(Exception):
    ...


class DeviceDriver(abc.ABC):
    """Connection to real devices or direct interfaces"""

    @abc.abstractmethod
    async def connect(self, node: "EdgeNode"):
        """Connect node to real device"""

    @abc.abstractmethod
    async def load_metrics(self):
        """Load metrics from system"""

    @abc.abstractmethod
    async def scan_metrics_changes(
        self, is_historical: bool = False
    ) -> list[MetricChange]:
        """Return changes in a list of metrics"""

    @abc.abstractmethod
    async def write_metric(self, request: MetricChangeRequest) -> MetricChange:
        """Write metric to system"""


class EdgeNode:
    """Gateway connected to mqtt and to one or more hardware devices"""

    def __init__(
        self,
        name: str,
        group_name: str,
        mqtt_client: MqttClient,
        device_driver: DeviceDriver,
        primary_hostname: str = "",
        scan_rate: float = 60.0,  # Scan every 1 minute
        clock: None | Callable[[], int] = None,
    ):
        self._name = name
        self._group_name = group_name
        self._primary_hostname = primary_hostname
        self._clock = clock if clock else get_timestamp

        self._driver = device_driver
        self._client = mqtt_client

        self._seq = 255
        self._inner_metrics = {
            "bdSeq": m.Metric("bdSeq", self._clock(), 255, data_type=DataType.Int64),
            "Node Control/Rebirth": m.Metric(
                "Node Control/Rebirth", self._clock(), False, data_type=DataType.Boolean
            ),
            "Node Control/Reboot": m.Metric(
                "Node Control/Reboot", self._clock(), False, data_type=DataType.Boolean
            ),
            "Node Control/Scan Rate": m.Metric(
                "Node Control/Scan Rate",
                self._clock(),
                scan_rate,
                data_type=DataType.Float,
            ),
        }
        self._metrics_by_name: dict[str, Metric] = {}
        self._metrics_by_alias: dict[int, Metric] = {}

        self._incomings_task = None
        self._outcomings_task = None
        self._scanning_task = None
        self._changes_queue = Queue()
        self._state: _NODES_STATES = "offline"
        self._is_connected_to_gateway = False

    @property
    def name(self) -> str:
        """Return name of edge of network node"""
        return self._name

    @property
    def group_name(self) -> str:
        """Return the name of the group of nodes it beyong to"""
        return self._group_name

    @property
    def state(self) -> _NODES_STATES:
        """Return the current state of node"""
        return self._state

    @property
    def primary_hostname(self) -> str:
        """Name of primary host application"""
        return self._primary_hostname

    @property
    def metrics(self) -> dict[str, Metric]:
        """Return a dict with all the metrics of the node"""
        metrics = self._inner_metrics.copy()
        metrics.update(self._metrics_by_name)
        return metrics

    def clear_metrics(self):
        """Remove all not internal metrics"""
        self._metrics_by_name.clear()
        self._metrics_by_alias.clear()

    def add_metric(self, metric: Metric):
        """Add new metric in node"""
        self._metrics_by_name[metric.name] = metric
        if metric.alias:
            self._metrics_by_alias[metric.alias] = metric

    def _get_seq(self):
        self._seq = self._seq + 1 if self._seq != 255 else 0
        return self._seq

    def _get_bd_seq(self):
        bd_seq = self._inner_metrics["bdSeq"]
        value = int(bd_seq.value) + 1 if bd_seq.value != 255 else 0
        bd_seq = Metric("bdSeq", self._clock(), value, data_type=DataType.Int64)
        self._inner_metrics["bdSeq"] = bd_seq
        return value

    async def _publish_data_messages(self):
        while True:
            await asyncio.sleep(0.1)  # Capture commands each 0.1 s
            if self._state == "publishing":
                # Publish Ndata messages
                changes = []
                while not self._changes_queue.empty():
                    changes.append(self._changes_queue.get())

                if not changes:
                    continue

                await self._client.publish(
                    f"spBv1.0/{self.group_name}/NDATA/{self.name}",
                    m.NdataMessage(self._get_seq(), changes),
                    qos=0,
                    retain=False,
                )
            else:
                await asyncio.sleep(1)

    async def _scan_metrics(self):
        if type(self._inner_metrics["Node Control/Scan Rate"].value) is not float:
            raise ValueError(f"Scan rate shall be a float!")

        scan_period = int(self._inner_metrics["Node Control/Scan Rate"].value * 1000)
        while True and scan_period:
            now = self._clock()
            next_scan_time = (now // scan_period + 1) * scan_period

            await asyncio.sleep((next_scan_time - now) / 1000)

            if self._is_connected_to_gateway:
                is_historical = self._state != "publishing"
                changes = await self._driver.scan_metrics_changes(
                    is_historical=is_historical
                )
                for change in changes:
                    if not change.alias and not change.metric_name:
                        continue

                    metric = (
                        self._metrics_by_alias[change.alias]
                        if change.alias is not None
                        else self.metrics[change.metric_name]
                    )
                    self._changes_queue.put(change)
                    self.add_metric(change.update_metric(metric))

    async def _handle_incomming_messages(self):
        while True:
            topic, message = await self._client.deliver_message()
            await self._handle_message(message, topic)

    @singledispatchmethod
    async def _handle_message(self, message: m.Message, topic: str):
        raise NotImplementedError(
            f"Message type {type(message)} is not managed by a Edge Node"
        )

    @_handle_message.register
    async def _handle_state_message(self, message: m.StateMessage, topic: str):
        if message.online:
            if not self._is_connected_to_gateway:
                await self._driver.connect(self)
                self._is_connected_to_gateway = True

            self._state = "publishing"
            await self._publish_birth_certificate()
        else:
            self._state = "online"

    @_handle_message.register
    async def _handle_command(self, message: m.NcmdMessage, topic: str):
        topic = f"spBv1.0/{self.group_name}/NDATA/{self.name}"
        for request in message.requests:
            if request.metric_name == "Node Control/Rebirth" and request.value is True:
                self._state = "online"  # Stops sending data
                await self._client.publish(
                    topic,
                    m.NdataMessage(
                        self._get_seq(),
                        [
                            MetricChange(
                                self._clock(),
                                True,
                                DataType.Boolean,
                                metric_name="Node Control/Rebirth",
                            )
                        ],
                    ),
                    qos=0,
                    retain=False,
                )
                await self._publish_birth_certificate()
            if request.metric_name == "Node Control/Reboot" and request.value is True:
                await self.terminate_session()
                await self.establish_session()
            else:
                loop = asyncio.get_event_loop()
                loop.create_task(self._process_metric_change(request))

    async def _process_metric_change(self, request: MetricChangeRequest):
        change = await self._driver.write_metric(request)
        metric = (
            self._metrics_by_alias[change.alias]
            if change.alias
            else self._metrics_by_name[change.metric_name]
        )
        self.add_metric(change.update_metric(metric))
        self._changes_queue.put(change)

    async def _publish_birth_certificate(self):
        self.clear_metrics()
        await self._driver.load_metrics()

        await self._client.publish(
            f"spBv1.0/{self.group_name}/NBIRTH/{self.name}",
            m.NbirthMessage(
                list(self.metrics.values()),
                self._get_seq(),
            ),
            qos=0,
            retain=False,
        )
        self._state = "publishing"

    async def establish_session(self):
        """Create a session"""

        self._get_bd_seq()
        await self._client.connect(
            f"{self.group_name}/{self.name}",
            will=Will(
                f"spBv1.0/{self.group_name}/NDEATH/{self.name}",
                m.NdeathMessage(self._inner_metrics["bdSeq"]),
                0,
                False,
            ),
        )
        await self._client.subscribe("spBv1.0/STATE/+", qos=1)
        await self._client.subscribe(
            f"spBv1.0/{self._group_name}/NCMD/{self._name}", qos=0
        )

        self._state = "online"

        self._outcomings_task = asyncio.create_task(self._publish_data_messages())
        self._incomings_task = asyncio.create_task(self._handle_incomming_messages())
        self._scanning_task = asyncio.create_task(self._scan_metrics())

    async def terminate_session(self):
        """Finish a session cleanly, leaving the node clean"""
        if self._outcomings_task is not None:
            self._outcomings_task.cancel()
            self._outcomings_task = None
        if self._scanning_task is not None:
            self._scanning_task.cancel()
            self._scanning_task = None
        if self._incomings_task is not None:
            self._incomings_task.cancel()
            self._incomings_task = None

        self._state = "offline"
        if self._client:
            await self._client.publish(
                f"spBv1.0/{self.group_name}/NDEATH/{self.name}",
                m.NdeathMessage(self._inner_metrics["bdSeq"]),
                0,
                False,
            )

        await self._client.disconnect()
