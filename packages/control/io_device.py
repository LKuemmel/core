from dataclasses import dataclass, field
from typing import Dict, List, Union
from modules.io_actions.dimming.api import Dimming
from modules.io_actions.dimming_direct_control.api import DimmingDirectControl
from modules.io_actions.ripple_control_receiver.api import RippleControlReceiver


@dataclass
class Get:
    analog_input: List[bool] = False
    digital_input: List[bool] = False
    analog_output: List[bool] = False
    digital_output: List[bool] = False


def get_factory():
    return Get()


@dataclass
class IoDeviceData:
    get: Get = field(default_factory=get_factory)


class IoDevice:
    def __init__(self):
        self.data = IoDeviceData()


class IoActions:
    def __init__(self):
        self.actions: Dict[int, Union[Dimming, DimmingDirectControl, RippleControlReceiver]] = {}

    # def parse_actions_to_dataclass(self, action_config: Dict):
    #     for index, action in enumerate(action_config):
    #         action_class = globals()[action["action"]]
    #         action_instance = dataclass_from_dict(action_class, action["action_parameters"])
    #         action_instance.input = index
    #         self.actions.append(action_instance)

    def dimming_get_import_power_left(self, cp_num: int) -> float:
        for action in self.actions.values():
            if isinstance(action, Dimming):
                if cp_num in action.config.cp_ids:
                    return action.dimming_get_import_power_left(cp_num)

    def dimming_via_direct_control(self, cp_num: int) -> float:
        for action in self.actions.values():
            if isinstance(action, DimmingDirectControl):
                if cp_num == action.config.cp_id:
                    return action.dimming_via_direct_control(cp_num)

    def ripple_control_receiver(self, cp_num: int) -> float:
        for action in self.actions.values():
            if isinstance(action, RippleControlReceiver):
                if cp_num in action.config.cp_ids:
                    return action.ripple_control_receiver(cp_num)
