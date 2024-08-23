from dataclasses import dataclass, field
from typing import Dict, List
from dataclass_utils._dataclass_from_dict import dataclass_from_dict
from dataclass_utils.factories import empty_dict_factory
from helpermodules.pub import Pub

CONTROLLABLE_CONSUMERS_ACTIONS = [{"action": "Dimming", "action_parameters": ["cp_num", "max_import_power"]},
                                  {"action": "ripple_control_receiver", "action_parameters": []},
                                  {"action": "dimming_via_direct_control", "action_parameters": ["cp_num"]}, ]


@dataclass
class Dimming:
    input: int = 0
    cp: int = 0
    max_import_power: int = 0
    # wird jeden zyklus kopiert und daher zurückgesetzt
    import_power_left: float = 0

    def __post_init__(self):
        self.import_power_left = self.max_import_power


@dataclass
class Get:
    input: List[bool] = False


def get_factory():
    return Get()


@dataclass
class Set:
    output: List[bool] = False


def set_factory():
    return Set()


@dataclass
class IoData:
    get: Get = field(default_factory=get_factory)
    set: Set = field(default_factory=set_factory)
    config: Dict = field(default_factory=empty_dict_factory)


class IoDevice:

    def __init__(self, num: int, config: Dict):
        self.num = num
        self.actions: List[Dimming] = self.parse_actions_to_dataclass(config["actions"])
        self.data = IoData()
        self.module = None

    def parse_actions_to_dataclass(self, action_config: Dict):
        for index, action in enumerate(action_config["input"]):
            action_class = globals()[action["action"]]
            action_instance = dataclass_from_dict(action_class, action["action_parameters"])
            action_instance.input = index
            self.actions.append(action_instance)

    def dimming_via_direct_control(input_state: bool, cp_num: int) -> None:
        pass

    def dimming_get_import_power_left(self, cp_num: int) -> None:
        for action in self.actions:
            if isinstance(action, Dimming):
                if action.cp == cp_num:
                    if self.data.get.input[action.input]:
                        return action.import_power_left
                    else:
                        return None
        else:
            return None

    def dimming_set_import_power_left(self, used_power: float, cp_num: int) -> None:
        for action in self.actions:
            if isinstance(action, Dimming):
                if action.cp == cp_num:
                    action.import_power_left -= used_power
                    return action.import_power_left
        else:
            return None

    def ripple_control_receiver(input_state: bool) -> None:
        Pub().pub("openWB/set/general/ripple_control_receiver/get/active", input_state)
