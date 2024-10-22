from dataclasses import dataclass, field
from typing import Dict, List, Union
from control import data
from dataclass_utils._dataclass_from_dict import dataclass_from_dict
from dataclass_utils.factories import empty_list_factory
from helpermodules.pub import Pub

CONTROLLABLE_CONSUMERS_ACTIONS = [{"action": "Dimming", "io": {"digital_input": [None]}, "action_parameters": ["cps", "max_import_power"]},
                                  {"action": "ripple_control_receiver", "io": {
                                      "digital_input": [None, None, None, None]}, "action_parameters": []},
                                  {"action": "dimming_via_direct_control", "action_parameters": ["cp_num"]}, ]


@dataclass
class DimmingConfig:
    io_device: int = 0
    digital_input: int = 0
    cp_ids: List[int] = empty_list_factory
    max_import_power: int = 0


class Dimming:
    def __init__(self, name: str = "dimming", id: int = 0, config: DimmingConfig = None):
        self.name = name
        self.id = id
        self.config = config or DimmingConfig()
        # wird jeden zyklus kopiert und daher zurückgesetzt
        self.import_power_left = self.config.max_import_power

    def dimming_get_import_power_left(self, cp_num: int) -> None:
        if cp_num in self.config.cp_ids:
            if data.data.io_devices[self.config.io_device].get.digital_input[self.config.digital_input]:
                return self.import_power_left
            else:
                return None
        else:
            return None

    def dimming_set_import_power_left(self, used_power: float, cp_num: int) -> None:
        if cp_num in self.config.cp_ids:
            self.import_power_left -= used_power
            return self.import_power_left
        else:
            return None


@dataclass
class Get:
    analog_input: List[bool] = False
    digital_input: List[bool] = False
    analog_output: List[bool] = False
    digital_output: List[bool] = False


def get_factory():
    return Get()


@dataclass
class Set:
    output: List[bool] = False


def set_factory():
    return Set()


@dataclass
class IoDeviceData:
    get: Get = field(default_factory=get_factory)
    set: Set = field(default_factory=set_factory)


class IoDevice:
    def __init__(self):
        self.data = IoDeviceData()

    def parse_actions_to_dataclass(self, action_config: Dict):
        for index, action in enumerate(action_config):
            action_class = globals()[action["action"]]
            action_instance = dataclass_from_dict(action_class, action["action_parameters"])
            action_instance.input = index
            self.actions.append(action_instance)

    def dimming_via_direct_control(input_state: bool, cp_num: int) -> None:
        pass

    def ripple_control_receiver(input_state: bool) -> None:
        Pub().pub("openWB/set/general/ripple_control_receiver/get/active", input_state)


class IoActions:
    def __init__(self):
        self.actions: Dict[int, Union[Dimming]] = {}

    def parse_actions_to_dataclass(self, action_config: Dict):
        for index, action in enumerate(action_config):
            action_class = globals()[action["action"]]
            action_instance = dataclass_from_dict(action_class, action["action_parameters"])
            action_instance.input = index
            self.actions.append(action_instance)

    def dimming_via_direct_control(input_state: bool, cp_num: int) -> None:
        pass

    def ripple_control_receiver(input_state: bool) -> None:
        Pub().pub("openWB/set/general/ripple_control_receiver/get/active", input_state)
