from modules.common.component_state import IoState
from modules.common.fault_state import FaultState
from modules.common.store import ValueStore
from modules.common.store._api import LoggingValueStore
from modules.common.store._broker import pub_to_broker


class IoValueStoreBroker(ValueStore[IoState]):
    def __init__(self, component_num: int) -> None:
        self.num = component_num

    def set(self, state: IoState) -> None:
        self.state = state

    def update(self):
        try:
            pub_to_broker(f"openWB/set/io/{self.num}/get/input", self.state.input)
        except Exception as e:
            raise FaultState.from_exception(e)


def get_io_value_store() -> ValueStore[IoState]:
    return LoggingValueStore(IoValueStoreBroker())
