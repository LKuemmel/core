
from typing import Dict, Generic, TypeVar

from dataclass_utils.factories import empty_dict_factory


T = TypeVar("T")


class IoDeviceSetup(Generic[T]):
    def __init__(self,
                 name: str,
                 type: str,
                 id: int,
                 configuration: T,
                 analog_input: Dict[int: float] = empty_dict_factory,
                 analog_output: Dict[int: float] = empty_dict_factory,
                 digital_input: Dict[int: float] = empty_dict_factory,
                 digital_output: Dict[int: float] = empty_dict_factory) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration
        self.analog_input = analog_input
        self.digital_input = digital_input
        self.analog_output = analog_output
        self.digital_output = digital_output
