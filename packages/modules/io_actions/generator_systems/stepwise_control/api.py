from control import data
from modules.common.abstract_device import DeviceDescriptor
from modules.io_actions.generator_systems.stepwise_control.api_eebus import StepwiseControlEebus
from modules.io_actions.generator_systems.stepwise_control.api_io import StepwiseControlIo
from modules.io_actions.generator_systems.stepwise_control.config import StepwiseControlSetup


def create_action(config: StepwiseControlSetup):
    if data.data.system_data[f"io{config.configuration.io_device}"].config.type == "eebus":
        return StepwiseControlEebus(config=config)
    else:
        return StepwiseControlIo(config=config)


device_descriptor = DeviceDescriptor(configuration_factory=StepwiseControlSetup)
