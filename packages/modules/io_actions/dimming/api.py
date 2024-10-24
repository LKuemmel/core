from dataclasses import dataclass
from typing import List
from control import data
from dataclass_utils.factories import empty_list_factory
from modules.common.abstract_device import DeviceDescriptor
from modules.io_actions.groups import ActionGroup


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
        self.group = ActionGroup.CONTROLLABLE_CONSUMERS_ACTIONS.value
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


device_descriptor = DeviceDescriptor(configuration_factory=Dimming)
