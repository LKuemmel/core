from requests import Session
from helpermodules.scale_metric import scale_metric
from modules.devices.fems.config import FemsCounterSetup
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.store import get_counter_value_store
from modules.devices.fems.version import FemsVersion, get_version


class FemsCounter:
    def __init__(self, ip_address: str, component_config: FemsCounterSetup, session: Session) -> None:
        self.ip_address = ip_address
        self.component_config = component_config
        self.session = session
        self.store = get_counter_value_store(self.component_config.id)
        self.fault_state = FaultState(ComponentInfo.from_component_config(self.component_config))
        self.version = get_version(self.get_data_by_multiple_segement_regex_query)

    def get_data_by_multiple_segement_regex_query(self):
        return self.session.get('http://' + self.ip_address +
                                ':8084/rest/channel/(meter0|_sum)/' +
                                '(ActivePower.*|VoltageL.|Frequency|Grid.+ActiveEnergy)',
                                timeout=6).json()

    def update(self) -> None:
        try:
            # ATTENTION: Recent FEMS versions started using the "unit" field (see example response below) and
            #            kind-of arbitrarily return either Volts, Kilowatthours or Hz or Millivolts, Watthours or
            #            Millihertz
            #            Others units (kW, kV) have not yet been observed but are coded just to be future-proof.
            self.counter_state = CounterState()
            if self.version == FemsVersion.MULTIPLE_SEGMENT_REGEX_QUERY:
                # Grid meter values and grid total energy sums
                response = self.get_data_by_multiple_segement_regex_query()

                self._set_response_values_to_counter_state(response)
            else:
                # Grid meter values
                response = self.session.get('http://' + self.ip_address +
                                            ':8084/rest/channel/meter0/(ActivePower.*|VoltageL.|Frequency)',
                                            timeout=1).json()
                self._set_response_values_to_counter_state(response)

                # Grid total energy sums
                response = self.session.get(
                    'http://'+self.ip_address+':8084/rest/channel/_sum/Grid.+ActiveEnergy',
                    timeout=1).json()
                self._set_response_values_to_counter_state(response)
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            # nicht alle FEMS-Module unterstützen Regex-Requests
            def get_value(url):
                response = self.session.get('http://x:'+self.password+'@'+self.ip_address +
                                            ':8084/rest/channel/'+url, timeout=2).json()
                return response["value"]

            self.counter_state.power = get_value('meter0/ActivePower')
            self.counter_state.imported = get_value('_sum/GridBuyActiveEnergy')
            self.counter_state.exported = get_value('_sum/GridSellActiveEnergy')
            self.counter_state.voltages = [get_value('meter0/VoltageL1'),
                                           get_value('meter0/VoltageL2'), get_value('meter0/VoltageL3')]
            self.counter_state.currents = [get_value('meter0/CurrentL1'),
                                           get_value('meter0/CurrentL2'), get_value('meter0/CurrentL3')]
            self.counter_state.powers = [get_value('meter0/ActivePowerL1'), get_value('meter0/ActivePowerL2'),
                                         get_value('meter0/ActivePowerL3')]

        self.store.set(self.counter_state)

    def _set_response_values_to_counter_state(self, response):
        for singleValue in response:
            address = singleValue['address']
            if (address == 'meter0/Frequency'):
                self.counter_state.frequency = scale_metric(singleValue['value'], singleValue.get('unit'), 'Hz')
            elif (address == 'meter0/ActivePower'):
                self.counter_state.power = scale_metric(singleValue['value'], singleValue.get('unit'), 'W')
            elif (address == 'meter0/ActivePowerL1'):
                self.counter_state.powers[0] = scale_metric(singleValue['value'], singleValue.get('unit'), 'W')
            elif (address == 'meter0/ActivePowerL2'):
                self.counter_state.powers[1] = scale_metric(singleValue['value'], singleValue.get('unit'), 'W')
            elif (address == 'meter0/ActivePowerL3'):
                self.counter_state.powers[2] = scale_metric(singleValue['value'], singleValue.get('unit'), 'W')
            elif (address == 'meter0/VoltageL1'):
                self.counter_state.voltages[0] = scale_metric(singleValue['value'], singleValue.get('unit'), 'V')
            elif (address == 'meter0/VoltageL2'):
                self.counter_state.voltages[1] = scale_metric(singleValue['value'], singleValue.get('unit'), 'V')
            elif (address == 'meter0/VoltageL3'):
                self.counter_state. voltages[2] = scale_metric(singleValue['value'], singleValue.get('unit'), 'V')
            elif (address == '_sum/GridBuyActiveEnergy'):
                self.counter_state.imported = scale_metric(singleValue['value'], singleValue.get('unit'), 'Wh')
            elif (address == '_sum/GridSellActiveEnergy'):
                self.counter_state.exported = scale_metric(singleValue['value'], singleValue.get('unit'), 'Wh')


component_descriptor = ComponentDescriptor(configuration_factory=FemsCounterSetup)
