from control import data
from modules.common.abstract_device import DeviceDescriptor
from modules.io_actions.controllable_consumers.dimming.api_eebus import DimmingEebus
from modules.io_actions.controllable_consumers.dimming.api_io import DimmingIo
from modules.io_actions.controllable_consumers.dimming.config import DimmingSetup


def create_action(config: DimmingSetup):
    return DimmingEebus(config=config)
    # if data.data.system_data[f"io{config.configuration.io_device}"].config.type == "eebus":

    # else:
    #     return DimmingIo(config=config)


device_descriptor = DeviceDescriptor(configuration_factory=DimmingSetup)
