from typing import TypeVar, Generic, Callable

from modules.common import store
from modules.common.component_context import SingleComponentUpdateContext
from modules.common.component_type import ComponentType
from modules.common.fault_state import ComponentInfo, FaultState


T_IO_CONFIG = TypeVar("T_IO_CONFIG")


class ConfigurableIo(Generic[T_IO_CONFIG]):
    def __init__(self,
                 config: T_IO_CONFIG,
                 component_updater: Callable[[], float]) -> None:
        self.config = config
        self.fault_state = FaultState(ComponentInfo(None, self.config.name,
                                      ComponentType.IO.value))
        self.store = store.get_io_value_store()
        with SingleComponentUpdateContext(self.fault_state):
            self.__component_updater = component_updater

    def update(self):
        if hasattr(self, "_component_updater"):
            # Wenn beim Initialisieren etwas schief gelaufen ist, ursprüngliche Fehlermeldung beibehalten
            with SingleComponentUpdateContext(self.fault_state):
                self.store(self.__component_updater())


# {"name": "Dimm-Kit", "type": "dimm_kit", "configuration": {"ip_address": "192.168.1.98",
#                                                            "port": 8899, "modbus_id": 1}, "actions": {"input_1": {"action_parameters": {"cp": 2}, "action": "direct_control_cp"}}}
# openWB/set/io/1/config
# {"name": "openWB Dimm- & Control-Kit", "type": "dimm_kit", "configuration": {"ip_address": null, "port": 8899, "modbus_id": 1},
#     "actions": {"1": {"action": "Dimming", "action_parameters": {"cp_num": [3, 4], "max_import_power": 4200}}}, "id": 1}
