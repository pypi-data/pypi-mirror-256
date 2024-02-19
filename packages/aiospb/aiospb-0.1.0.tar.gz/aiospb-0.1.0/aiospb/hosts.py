import asyncio
from typing import Callable, Coroutine

from aiospb import get_timestamp
from aiospb.data import Metric, MetricChangeRequest, ValueType
from aiospb.groups import MqttServer
from aiospb.messages import (
    Message,
    NbirthMessage,
    NcmdMessage,
    NdataMessage,
    NdeathMessage,
    StateMessage,
)
from aiospb.mqtt import Will


class EdgeNodeView:
    """Show current metrics of an edge node"""

    def __init__(self, node_name: str):
        self._name = node_name
        self.metrics_by_alias: dict[int, Metric] = {}
        self.metrics_by_name: dict[str, Metric] = {}
        self.state = "offline"

    @property
    def name(self) -> str:
        return self._name

    async def aprocess_message(self, message: Message, node_name: str):
        if self._name != node_name:
            return

        if type(message) is NbirthMessage:
            self.metrics_by_alias = {}
            self.metrics_by_name = {}
            for metric in message.metrics:
                self._add_metric(metric)
            self.state = "publishing"
        elif type(message) is NdataMessage:
            for change in message.changes:
                metric = (
                    self.metrics_by_name[change.metric_name]
                    if change.alias is None
                    else self.metrics_by_alias[change.alias]
                )
                self._add_metric(change.update_metric(metric))
        elif type(message) is NdeathMessage:
            self.state = "offline"

    def _add_metric(self, metric):
        if metric.alias is not None:
            self.metrics_by_alias[metric.alias] = metric

        if metric.name:
            self.metrics_by_name[metric.name] = metric


class HostApplication:
    """Implementation of Host Application"""

    def __init__(
        self,
        hostname: str,
        mqtt_server: MqttServer,
        *node_groups: str,
        clock: Callable[[], int] | None = None,
    ):
        self._client = mqtt_server.create_client()
        self._hostname = hostname
        self._groups = node_groups
        self._callbacks = {}
        self._task = None
        self._nodes = {}
        self._clock = clock if clock else get_timestamp

    @property
    def hostname(self) -> str:
        """Name of the host application"""
        return self._hostname

    async def establish_session(self):
        """Init session to listen edge nodes"""
        await self._client.connect(
            self._hostname,
            will=Will(
                f"spBv1.0/STATE/{self._hostname}", StateMessage(online=False), 1, True
            ),
        )
        if self._groups:
            for group in self._groups:
                await self._client.subscribe(f"spBv1.0/{group}/#", qos=0)
        else:
            await self._client.subscribe("spBv1.0/+/+/+/#", qos=0)

        await self._client.publish(
            f"spBv1.0/STATE/{self._hostname}",
            StateMessage(online=True),
            qos=1,
            retain=True,
        )
        self._task = asyncio.create_task(self._recieve_node_messages())

    def done(self):
        return self._task is None or self._task.done()

    def listen_nodes(
        self,
        callback: Callable[[Message, str], Coroutine[None, None, None]],
        node_filter: str | None = None,
    ) -> None:
        """Add one callable observer when it rece"""
        if node_filter not in self._callbacks:
            self._callbacks[node_filter] = []

        self._callbacks[node_filter].append(callback)

    async def _recieve_node_messages(self):
        while True:
            component_name, message = await self._client.deliver_message()
            if component_name in self._nodes:
                self._nodes[component_name].process_message(message)

            awaitables = [
                callback(message, component_name) for callback in self._callbacks[None]
            ]
            if component_name in self._callbacks:
                awaitables.extend(
                    [
                        callback(message, component_name)
                        for callback in self._callbacks[component_name]
                    ]
                )
            await asyncio.gather(*awaitables)

    async def send_node_command(self, command: NcmdMessage, node_name: str):
        group, node = node_name.split("/")
        await self._client.publish(
            f"spBv1.0/{group}/NCMD/{node}", command, qos=0, retain=False
        )

    async def terminate_session(self):
        """Close cleanly a session"""
        if self._task:
            self._task.cancel()

        await self._client.publish(
            f"spBv1.0/STATE/{self._hostname}",
            StateMessage(online=False),
            qos=1,
            retain=True,
        )
        await self._client.disconnect()
