from requests import Session

from modules.common.abstract_device import AbstractCounter
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.store import get_counter_value_store
from modules.devices.discovergy.discovergy import api
from modules.devices.discovergy.discovergy.config import DiscovergyCounterSetup


class DiscovergyCounter(AbstractCounter):
    def __init__(self, component_config: DiscovergyCounterSetup) -> None:
        self.component_config = component_config

    def initialize(self) -> None:
        self.store = get_counter_value_store(self.component_config.id)
        self.fault_state = FaultState(ComponentInfo.from_component_config(self.component_config))

    def update(self, session: Session):
        self.store.set(api.get_last_reading(session, self.component_config.configuration.meter_id))


component_descriptor = ComponentDescriptor(configuration_factory=DiscovergyCounterSetup)
