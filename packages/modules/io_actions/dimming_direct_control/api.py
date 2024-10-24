from dataclasses import dataclass
from control import data
from modules.common.abstract_device import DeviceDescriptor
from modules.io_actions.groups import ActionGroup


@dataclass
class DimmingDirectControlConfig:
    io_device: int = 0
    digital_input: int = 0
    cp_id: int = None


class DimmingDirectControl:
    def __init__(self,
                 name: str = "Dimmen per Direktsteuerung",
                 type: str = "dimming_direct_control",
                 id: int = 0,
                 config: DimmingDirectControlConfig = None):
        self.name = name
        self.type = type
        self.id = id
        self.config = config or DimmingDirectControlConfig()
        self.group = ActionGroup.CONTROLLABLE_CONSUMERS_ACTIONS.value

    def dimming_via_direct_control(self, cp_num: int) -> None:
        if cp_num == self.config.cp_id:
            if data.data.io_devices[self.config.io_device].get.digital_input[self.config.digital_input]:
                return 4200
            else:
                return None
        else:
            return None


device_descriptor = DeviceDescriptor(configuration_factory=DimmingDirectControl)
