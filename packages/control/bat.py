from dataclasses import dataclass, field
import logging
from typing import List

from dataclass_utils.factories import currents_list_factory
from helpermodules.constants import NO_ERROR

log = logging.getLogger(__name__)


@dataclass
class Get:
    currents: List[float] = field(default_factory=currents_list_factory, metadata={
                                  "topic": "get/currents", "subscribe_only": True})
    soc: float = field(default=0, metadata={"topic": "get/soc", "subscribe_only": True})
    daily_exported: float = field(default=0, metadata={"topic": "get/daily_exported", "subscribe_only": False})
    daily_imported: float = field(default=0, metadata={"topic": "get/daily_imported", "subscribe_only": False})
    imported: float = field(default=0, metadata={"topic": "get/imported", "subscribe_only": True})
    exported: float = field(default=0, metadata={"topic": "get/exported", "subscribe_only": True})
    fault_state: int = field(default=0, metadata={"topic": "get/fault_state", "subscribe_only": False})
    fault_str: str = field(default=NO_ERROR, metadata={"topic": "get/fault_str", "subscribe_only": False})
    power: float = field(default=0, metadata={"topic": "get/power", "subscribe_only": True})


def get_factory() -> Get:
    return Get()


@dataclass
class BatData:
    get: Get = field(default_factory=get_factory)


class Bat:

    def __init__(self, index):
        self.data = BatData()
        self.num = index
