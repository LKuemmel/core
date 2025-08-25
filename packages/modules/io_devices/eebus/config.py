from helpermodules.auto_str import auto_str
from modules.common.io_setup import IoDeviceSetup


class EebusConfiguration:
    def __init__(self, ski: str):
        self.ski = ski


@auto_str
class Eebus(IoDeviceSetup[EebusConfiguration]):
    def __init__(self,
                 name: str = "Steuerbox mit EEbus-Schnittstelle",
                 type: str = "eebus",
                 id: int = 0,
                 configuration: EebusConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or EebusConfiguration())
