from requests import Session
from helpermodules.scale_metric import scale_metric
from modules.devices.fems.config import FemsInverterSetup
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.store import get_inverter_value_store
from modules.devices.fems.version import FemsVersion, get_version


class FemsInverter:
    def __init__(self, ip_address: str, component_config: FemsInverterSetup, session: Session) -> None:
        self.ip_address = ip_address
        self.component_config = component_config
        self.session = session
        self.store = get_inverter_value_store(self.component_config.id)
        self.fault_state = FaultState(ComponentInfo.from_component_config(self.component_config))
        self.version = get_version(self.get_data_by_multiple_segement_regex_query)

    def get_data_by_multiple_segement_regex_query(self):
        return self.session.get(
            'http://'+self.ip_address+':8084/rest/channel/_sum/(ProductionActivePower|ProductionActiveEnergy)',
            timeout=2).json()

    def update(self) -> None:
        self.inverter_state = InverterState(None, None)
        if self.version == FemsVersion.MULTIPLE_SEGMENT_REGEX_QUERY:
            response = self.get_data_by_multiple_segement_regex_query()
            self._set_response_values_to_inverter_state(response)
        else:
            response = self.session.get(
                'http://'+self.ip_address+':8084/rest/channel/_sum/ProductionActivePower',
                timeout=2).json()
            self._set_response_values_to_inverter_state(response)
            response = self.session.get(
                'http://'+self.ip_address+':8084/rest/channel/_sum/ProductionActiveEnergy',
                timeout=2).json()
            self._set_response_values_to_inverter_state(response)

        self.store.set(self.inverter_state)

    def _set_response_values_to_inverter_state(self, response):
        for singleValue in response:
            address = singleValue["address"]
            if address == "_sum/ProductionActivePower":
                self.inverter_state.power = scale_metric(singleValue['value'], singleValue.get('unit'), 'W') * -1
            elif address == "_sum/ProductionActiveEnergy":
                self.inverter_state.exported = scale_metric(singleValue['value'], singleValue.get('unit'), 'Wh')


component_descriptor = ComponentDescriptor(configuration_factory=FemsInverterSetup)
