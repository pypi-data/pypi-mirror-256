import abc
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, Self

from .data import Metric, MetricChange, MetricChangeRequest

if TYPE_CHECKING:  # pragma: no cover
    from aiospb.components import EdgeNode


class Message(abc.ABC):
    """Base of message"""

    @abc.abstractclassmethod
    def get_topic(cls, node: "EdgeNode") -> str:
        """Return the topic where the message should be sent"""

    @abc.abstractclassmethod
    def from_payload(cls, payload: dict[str, Any]) -> Self:
        """Return the topic where the message should be sent"""

    @abc.abstractmethod
    def get_payload(self, clock: Callable[[], int]) -> dict[str, Any]:
        """Return payload to be published"""


@dataclass
class NbirthMessage(Message):
    metrics: list[Metric]
    seq: int
    timestamp: int | None = None

    @classmethod
    def get_topic(cls, node: "EdgeNode") -> str:
        """Return the topic where the message should be sent"""
        return f"spBv1.0/{node.group_name}/NBIRTH/{node.name}"

    @classmethod
    def from_payload(cls, payload: dict[str, Any]):
        """Generate from standard values"""
        metrics = [Metric.from_dict(metric_data) for metric_data in payload["metrics"]]
        return cls(metrics, payload["seq"], payload["timestamp"])

    def get_payload(self, clock: Callable[[], int]) -> dict[str, Any]:
        """Return payload to be published"""
        self.timestamp = clock()
        return {
            "timestamp": self.timestamp,
            "metrics": [metric.to_dict() for metric in self.metrics],
            "seq": self.seq,
        }


@dataclass
class NdeathMessage(Message):
    bd_seq: Metric
    timestamp: int | None = None

    @classmethod
    def get_topic(cls, node: "EdgeNode") -> str:
        """Return the topic where the message should be sent"""
        return f"spBv1.0/{node.group_name}/NDEATH/{node.name}"

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> Self:
        """Return the topic where the message should be sent"""
        bd_seq = Metric.from_dict(payload["metrics"][0])
        return cls(bd_seq, payload["timestamp"])

    def get_payload(self, clock: Callable[[], int]) -> dict[str, Any]:
        """Return payload to be sent from message information"""
        self.timestamp = clock()
        return {"timestamp": self.timestamp, "metrics": [self.bd_seq.to_dict()]}


@dataclass
class NdataMessage(Message):
    seq: int
    changes: list[MetricChange]
    timestamp: int | None = None

    @classmethod
    def get_topic(cls, node: "EdgeNode") -> str:
        """Return the topic where the message should be sent"""
        return f"spBv1.0/{node.group_name}/NDATA/{node.name}"

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> Self:
        """Return the topic where the message should be sent"""
        changes = [MetricChange.from_dict(change) for change in payload["metrics"]]

        return cls(payload["seq"], changes, payload["timestamp"])

    def get_payload(self, clock: Callable[[], int]) -> dict[str, Any]:
        """Return payload to be published(not encoded!)"""
        self.timestamp = clock()
        return {
            "timestamp": self.timestamp,
            "metrics": [change.to_dict() for change in self.changes],
            "seq": self.seq,
        }


@dataclass
class NcmdMessage(Message):
    requests: list[MetricChangeRequest]
    timestamp: int | None = None

    @classmethod
    def get_topic(cls, node: "EdgeNode") -> str:
        """Return the topic where the message should be published"""
        return f"spBv1.0/{node.group_name}/NCMD/{node.name}"

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> Self:
        """Return the topic where the message should be sent"""
        requests = []
        for request in payload["metrics"]:
            requests.append(MetricChangeRequest.from_dict(request))
        return cls(requests, payload["timestamp"])

    def get_payload(self, clock: Callable[[], int]) -> dict[str, Any]:
        """Return payload to be published(not encoded!)"""
        self.timestamp = clock()

        return {
            "timestamp": self.timestamp,
            "metrics": [request.to_dict() for request in self.requests],
        }


@dataclass
class StateMessage(Message):
    online: bool
    timestamp: int | None = None

    @classmethod
    def get_topic(cls, hostname: str) -> str:
        """Return the topic where the message should be published"""
        return f"spBv1.0/STATE/{hostname}"

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> Self:
        """Return the topic where the message should be sent"""
        return cls(payload["online"], payload["timestamp"])

    def get_payload(self, clock: Callable[[], int]) -> dict[str, Any]:
        """Return payload to be published(not encoded!)"""
        self.timestamp = clock()

        return {"timestamp": self.timestamp, "online": self.online}
