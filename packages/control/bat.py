from dataclasses import dataclass, field
import logging
from typing import List

from dataclass_utils.factories import currents_list_factory
from helpermodules.constants import NO_ERROR

log = logging.getLogger(__name__)


@dataclass
class Get:
    currents: List[float] = field(default_factory=currents_list_factory, metadata={
                                  "topic": "get/currents", "mutable_by_algorithm": False})
    soc: float = field(default=0, metadata={"topic": "get/soc", "mutable_by_algorithm": False})
    daily_exported: float = field(default=0, metadata={"topic": "get/daily_exported", "mutable_by_algorithm": True})
    daily_imported: float = field(default=0, metadata={"topic": "get/daily_imported", "mutable_by_algorithm": True})
    imported: float = field(default=0, metadata={"topic": "get/imported", "mutable_by_algorithm": False})
    exported: float = field(default=0, metadata={"topic": "get/exported", "mutable_by_algorithm": False})
    fault_state: int = field(default=0, metadata={"topic": "get/fault_state", "mutable_by_algorithm": True})
    fault_str: str = field(default=NO_ERROR, metadata={"topic": "get/fault_str", "mutable_by_algorithm": True})
    power: float = field(default=0, metadata={"topic": "get/power", "mutable_by_algorithm": False})


def get_factory() -> Get:
    return Get()


@dataclass
class BatData:
    get: Get = field(default_factory=get_factory)


class Bat:

    def __init__(self, index):
        self.data = BatData()
        self.num = index
