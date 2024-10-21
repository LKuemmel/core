from typing import Dict, Optional

from modules.common.io_setup import IoDeviceSetup


class IoLanRcrConfiguration:
    def __init__(self, ip_address: Optional[str] = None, port: int = 8899, modbus_id: int = 1):
        self.ip_address = ip_address
        self.port = port
        self.modbus_id = modbus_id


def analog_input_init():
    return {i: 0 for i in range(1, 9)}


def digital_input_init():
    return {i: False for i in range(1, 9)}


def digital_output_init():
    return {i: False for i in range(1, 9)}


class IoLan(IoDeviceSetup[IoLanRcrConfiguration]):
    def __init__(self,
                 name: str = "openWB Dimm- & Control-Kit",
                 type: str = "dimm_kit",
                 configuration: IoLanRcrConfiguration = None,
                 analog_input: Dict[int, float] = analog_input_init,
                 digital_input: Dict[int, bool] = digital_input_init,
                 digital_output: Dict[int, bool] = digital_output_init) -> None:
        super().__init__(name, type, id, configuration or IoLanRcrConfiguration(), analog_input=analog_input,
                         digital_input=digital_input, digital_output=digital_output)
