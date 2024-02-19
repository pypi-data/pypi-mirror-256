import abc
import asyncio

from aiospb.mqtt import MqttClient
from aiospb.mqtt.encoding import JsonEncoder
from aiospb.mqtt.paho import PahoMqttClient
from aiospb.nodes import DeviceDriver, EdgeNode


class DeviceDriverFactory(abc.ABC):
    """Create connections to device from Nodes/Devices"""

    @abc.abstractmethod
    def get_all_node_names(self, nodes_filter: str = "") -> list[str]:
        """Return all name of nodes available to connect by"""

    @abc.abstractmethod
    def create_device_driver(self) -> DeviceDriver:
        """Create a device connection"""


class MqttServer:
    """Create mqtt clients working asyncronously"""

    def __init__(self, mqtt_config: dict[str, str]):
        self._config = mqtt_config
        self._encoder = JsonEncoder()

    def create_client(self) -> MqttClient:
        """Create an asyncronous mqtt client"""
        return PahoMqttClient(self._config, self._encoder)


class NodesGroup:
    """Runnable class which manage a group of edge nodes"""

    def __init__(
        self,
        name: str,
        mqtt_server: MqttServer,
        device_driver_fry: DeviceDriverFactory,
        primary_hostname: str,
        scan_rate: str | float = 0.1,
    ):
        self._name = name
        self._mqtt_server = mqtt_server
        self._driver_fry = device_driver_fry
        self._primary_hostname = primary_hostname
        try:
            self._scan_rate = (
                scan_rate if type(scan_rate) is float else float(scan_rate)
            )
        except ValueError:
            self._scan_rate = 60.0
        self._filter = None
        self._nodes = {}

    @property
    def name(self) -> str:
        """Return the name of the group"""
        return self._name

    @property
    def nodes(self) -> dict[str, EdgeNode]:
        """Return all executable nodes."""
        return self._nodes.copy()

    def setup(self, boxes_filter: str | None = None):
        self._filter = boxes_filter

        node_names = self._driver_fry.get_all_node_names(boxes_filter)
        for name in node_names:
            self._nodes[name] = EdgeNode(
                name,
                self._name,
                mqtt_client=self._mqtt_server.create_client(),
                device_driver=self._driver_fry.create_device_driver(),
                primary_hostname=self._primary_hostname,
                scan_rate=self._scan_rate,
            )

    async def _start_all_nodes(self, cycles):
        for node in self._nodes.values():
            await node.establish_session()

        counter = 0
        while True:
            counter += 1
            if node.state == "crashed":
                await node.terminate_session()
                await node.establish_session()
            if cycles and counter == cycles:
                break
            await asyncio.sleep(2)

    def run(self, cycles: int | None = None):
        """Run the group as an application in the OS"""
        asyncio.run(self._start_all_nodes(cycles))
        # loop = asyncio.get_event_loop()
        # loop.create_task(self._start_all_nodes(cycles))
        # loop.run_forever()
