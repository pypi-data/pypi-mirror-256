import json
from typing import Any

from .. import messages as m
from . import MessageEncoder


class JsonEncoder(MessageEncoder):
    """Encoder of messages for testing purposes"""

    _MESSAGES = {"NBIRTH": m.NbirthMessage}

    def encode(self, payload: dict[str, Any]) -> str:
        """Convert a payload dict to a string for publishing"""

        return json.dumps(payload, sort_keys=True)

    def decode(self, payload: str) -> dict[str, Any]:
        """Convert payload to a payload dict"""
        return json.loads(payload)
