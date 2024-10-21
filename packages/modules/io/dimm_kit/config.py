from typing import Dict, Optional

from helpermodules.auto_str import auto_str
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


@auto_str
class IoLan(IoDeviceSetup[IoLanRcrConfiguration]):
    def __init__(self,
                 name: str = "openWB Dimm- & Control-Kit",
                 type: str = "dimm_kit",
                 id: int = 0,
                 configuration: Optional[IoLanRcrConfiguration] = None,
                 analog_input: Optional[Dict[int, float]] = None,
                 digital_input: Optional[Dict[int, bool]] = None,
                 digital_output: Optional[Dict[int, bool]] = None) -> None:
        if analog_input is None:
            analog_input = analog_input_init()
        if digital_input is None:
            digital_input = digital_input_init()
        if digital_output is None:
            digital_output = digital_output_init()
        super().__init__(name, type, id, configuration or IoLanRcrConfiguration(), analog_input=analog_input,
                         digital_input=digital_input, digital_output=digital_output)
