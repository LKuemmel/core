from modules.common.io_setup import IoDeviceSetup


class AddOnConfiguration:
    def __init__(self):
        pass


class AddOn(IoDeviceSetup[AddOnConfiguration]):
    def __init__(self,
                 name: str = "GPIOs auf der AddOn-Platine",
                 type: str = "add_on",
                 configuration: AddOnConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.configuration = configuration or AddOnConfiguration()
        super().__init__(name, type, id, configuration or AddOnConfiguration())
        self.digital_input = {i: False for i in range(1, 9)}
        self.digital_output = {i: False for i in range(1, 9)}
