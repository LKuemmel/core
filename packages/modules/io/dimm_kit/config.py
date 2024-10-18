from typing import Optional

from control.io_device import CONTROLLABLE_CONSUMERS_ACTIONS


class IoLanRcrConfiguration:
    def __init__(self, ip_address: Optional[str] = None, port: int = 8899, modbus_id: int = 1):
        self.ip_address = ip_address
        self.port = port
        self.modbus_id = modbus_id


class IoLan:
    def __init__(self,
                 name: str = "openWB Dimm- & Control-Kit",
                 type: str = "dimm_kit",
                 configuration: IoLanRcrConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.configuration = configuration or IoLanRcrConfiguration()
        self.actions = {i: CONTROLLABLE_CONSUMERS_ACTIONS for i in range(1, 11)}
