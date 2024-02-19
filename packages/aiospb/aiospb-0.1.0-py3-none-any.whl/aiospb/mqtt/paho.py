from typing import Any, Callable

import aiomqtt

from .. import get_timestamp
from ..messages import (
    Message,
    NbirthMessage,
    NcmdMessage,
    NdataMessage,
    NdeathMessage,
    StateMessage,
)
from . import MessageEncoder, MqttClient, MqttConnectionError, Will


class PahoMqttClient(MqttClient):
    _MESSAGES = {
        "NDATA": NdataMessage,
        "NBIRTH": NbirthMessage,
        "NDEATH": NdeathMessage,
        "NCMD": NcmdMessage,
    }

    def __init__(
        self,
        config: dict[str, Any],
        encoder: MessageEncoder,
        clock: Callable[[], int] | None = None,
    ):
        self._config = config
        self._client = None
        self._client_id = None
        self._encoder = encoder
        self._clock = clock if clock else get_timestamp

    async def connect(self, component_name: str, will: Will):
        payload = self._encoder.encode(will.message.get_payload(self._clock))
        will_ = aiomqtt.Will(will.topic, payload, qos=will.qos, retain=will.retain)
        self._client_id = component_name

        tls_pars = None
        if self._config["ca_certs"]:
            tls_pars = aiomqtt.TLSParameters(ca_certs=self._config["ca_certs"])

        self._client = aiomqtt.Client(
            self._config["hostname"],
            int(self._config["port"]),
            identifier=component_name,
            username=self._config["username"],
            password=self._config["password"],
            will=will_,
            tls_params=tls_pars,
            keepalive=30,
        )

        await self._client.__aenter__()  # Connect with aiomqtt

    async def publish(self, topic: str, message: Message, qos: int, retain: bool):
        if not self._client or not self._client_id:
            raise MqttConnectionError("Client not connected to Mqtt Server")

        payload = self._encoder.encode(message.get_payload(self._clock))
        await self._client.publish(topic, payload, qos=qos, retain=retain)

    async def subscribe(self, topic: str, qos: int):
        if not self._client or not self._client_id:
            raise MqttConnectionError("Client not connected to Mqtt Server")

        await self._client.subscribe(topic, qos=qos)

    async def deliver_message(self) -> tuple[str, Message]:
        # if self._client is None:
        #     raise MqttConnectionError(f"Client is not connected, so no messages")

        message = await anext(self._client.messages)

        topic_words = message.topic.value.split("/")
        payload = self._encoder.decode(message.payload.decode())
        if "STATE" in topic_words:
            hostname = topic_words[-1]
            print(f"detected State {payload}")
            return (hostname, StateMessage.from_payload(payload))
        else:  #  Node message
            node_name = f"{topic_words[1]}/{topic_words[3]}"
            NodeMessage = self._MESSAGES[topic_words[2]]
            return (node_name, NodeMessage.from_payload(payload))

    async def disconnect(self):
        if self._client is None:
            return

        await self._client.__aexit__(None, None, None)
