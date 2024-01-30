from requests import Session
from helpermodules.scale_metric import scale_metric
from modules.devices.fems.config import FemsBatSetup
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.store import get_bat_value_store
from modules.devices.fems.version import FemsVersion, get_version


class FemsBat:
    def __init__(self, ip_address: str, component_config: FemsBatSetup, session: Session) -> None:
        self.ip_address = ip_address
        self.component_config = component_config
        self.session = session
        self.store = get_bat_value_store(self.component_config.id)
        self.fault_state = FaultState(ComponentInfo.from_component_config(self.component_config))
        if self.component_config.configuration.num == 1:
            self._data = "ess0"
        else:
            self._data = "ess2"
        self.version = get_version(self.get_data_by_multiple_segement_regex_query)

    def get_data_by_multiple_segement_regex_query(self):
        return self.session.get(
            (f"http://{self.ip_address}:8084/rest/channel/{self._data}|_sum)/"
             "(Soc|DcChargeEnergy|DcDischargeEnergy|GridActivePower|ProductionActivePower|ConsumptionActivePower)"),
            timeout=2).json()

    def update(self) -> None:
        self.bat_state = BatState()
        if self.version == FemsVersion.MULTIPLE_SEGMENT_REGEX_QUERY:
            response = self.get_data_by_multiple_segement_regex_query(self.session)
            self._set_response_values_to_bat_state(response)
        else:
            response = self.session.get(
                f"http://{self.ip_address}:8084/rest/channel/{self.data}/(Soc|DcChargeEnergy|DcDischargeEnergy)",
                timeout=2).json()
            self._set_response_values_to_bat_state(response)

            response = self.session.get(
                (f"http://{self.ip_address}:8084/rest/channel/_sum/(GridActivePower|ProductionActivePower|"
                 "ConsumptionActivePower)"),
                timeout=2).json()
            self._set_response_values_to_bat_state(response)

        self.store.set(self.bat_state)

    def _set_response_values_to_bat_state(self, response):
        for singleValue in response:
            address = singleValue["address"]
            if (address == self._data+"/Soc"):
                self.bat_state.soc = singleValue["value"]
            elif address == self._data+"/DcChargeEnergy":
                self.bat_state.imported = scale_metric(singleValue['value'], singleValue.get('unit'), 'Wh')
            elif address == self._data+"/DcDischargeEnergy":
                self.bat_state.exported = scale_metric(singleValue['value'], singleValue.get('unit'), 'Wh')
            elif address == "_sum/GridActivePower":
                grid = scale_metric(singleValue['value'], singleValue.get('unit'), 'W')
            elif address == "_sum/ProductionActivePower":
                pv = scale_metric(singleValue['value'], singleValue.get('unit'), 'W')
            elif address == "_sum/ConsumptionActivePower":
                haus = scale_metric(singleValue['value'], singleValue.get('unit'), 'W')
        # keine Berechnung im Gerät, da grid nicht der Leistung aus der Zählerkomponente entspricht.
        self.bat_state.power = grid + pv - haus


component_descriptor = ComponentDescriptor(configuration_factory=FemsBatSetup)
