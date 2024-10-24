from dataclasses import dataclass
from typing import List
from control import data
from dataclass_utils.factories import empty_list_factory
from modules.common.abstract_device import DeviceDescriptor
from modules.io_actions.groups import ActionGroup


@dataclass
class RippleControlReceiverConfig:
    io_device: int = 0
    digital_input: int = 0
    cp_ids: List[int] = empty_list_factory


class RippleControlReceiver:
    def __init__(self, name: str = "ripple_control_receiver", id: int = 0, config: RippleControlReceiverConfig = None):
        self.name = name
        self.id = id
        self.config = config or RippleControlReceiverConfig()
        self.group = ActionGroup.CONTROLLABLE_CONSUMERS_ACTIONS.value

    def ripple_control_receiver(self, cp_num: int) -> None:
        if cp_num in self.config.cp_ids:
            if data.data.io_devices[self.config.io_device].get.digital_input[self.config.digital_input]:
                return 0
            else:
                return None
        else:
            return None


device_descriptor = DeviceDescriptor(configuration_factory=RippleControlReceiver)
