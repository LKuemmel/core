#!/usr/bin/env python3
from typing import Any, Optional, TypedDict
import logging
from modules.devices.sonnen.sonnenbatterie.config import SonnenbatterieInverterSetup
from modules.common.store import get_inverter_value_store
from modules.common.simcount import SimCounter
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.component_type import ComponentDescriptor
from modules.common.component_state import InverterState
from modules.common.abstract_device import AbstractInverter
from modules.common import req


log = logging.getLogger(__name__)


class KwargsDict(TypedDict):
    api_v2_token: str
    device_id: int
    device_address: str
    device_variant: int


class SonnenbatterieInverter(AbstractInverter):
    def __init__(self, component_config: SonnenbatterieInverterSetup, **kwargs: Any) -> None:
        self.component_config = component_config
        self.kwargs: KwargsDict = kwargs

    def initialize(self) -> None:
        self.__device_id: int = self.kwargs['device_id']
        self.__device_address: str = self.kwargs['device_address']
        self.__device_variant: int = self.kwargs['device_variant']
        self.__api_v2_token: Optional[str] = self.kwargs.get('api_v2_token')
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="pv")
        self.store = get_inverter_value_store(self.component_config.id)
        self.fault_state = FaultState(ComponentInfo.from_component_config(self.component_config))

    def __read_variant_1(self, api: str = "v1"):
        return req.get_http_session().get(
            "http://" + self.__device_address + "/api/" + api + "/status",
            timeout=5,
            headers={"Auth-Token": self.__api_v2_token} if api == "v2" else None
        ).json()

    def __update_variant_1(self, api: str = "v1") -> InverterState:
        # Auslesen einer Sonnenbatterie 8 oder 10 über die integrierte JSON-API v1/v2 des Batteriesystems
        '''
        example data:
        {
            "Apparent_output": 225,
            "BackupBuffer": "0",
            "BatteryCharging": false,
            "BatteryDischarging": false,
            "Consumption_Avg": 2114,
            "Consumption_W": 2101,
            "Fac": 49.97200393676758,
            "FlowConsumptionBattery": false,
            "FlowConsumptionGrid": true,
            "FlowConsumptionProduction": false,
            "FlowGridBattery": false,
            "FlowProductionBattery": false,
            "FlowProductionGrid": false,
            "GridFeedIn_W": -2106,
            "IsSystemInstalled": 1,
            "OperatingMode": "2",
            "Pac_total_W": -5,
            "Production_W": 0,
            "RSOC": 6,
            "RemainingCapacity_Wh": 2377,
            "Sac1": 75,
            "Sac2": 75,
            "Sac3": 75,
            "SystemStatus": "OnGrid",
            "Timestamp": "2021-12-13 07:54:48",
            "USOC": 0,
            "Uac": 231,
            "Ubat": 48,
            "dischargeNotAllowed": true,
            "generator_autostart": false,
            "NVM_REINIT_STATUS": 0
        }
        '''
        inverter_state = self.__read_variant_1(api)
        pv_power = -inverter_state["Production_W"]
        log.debug('Speicher PV Leistung: ' + str(pv_power))
        _, exported = self.sim_counter.sim_count(pv_power)
        return InverterState(
            exported=exported,
            power=pv_power
        )

    def __read_variant_2_element(self, element: str) -> str:
        response = req.get_http_session().get('http://' + self.__device_address +
                                              ':7979/rest/devices/battery/' + element, timeout=5)
        response.encoding = 'utf-8'
        return response.text.strip(" \n\r")

    def __update_variant_2(self) -> InverterState:
        # Auslesen einer Sonnenbatterie Eco 6 über die integrierte REST-API des Batteriesystems
        pv_power = -int(float(self.__read_variant_2_element("M03")))
        log.debug('Speicher PV Leistung: ' + str(pv_power))
        _, exported = self.sim_counter.sim_count(pv_power)
        return InverterState(
            exported=exported,
            power=pv_power
        )

    def update(self) -> None:
        log.debug("Variante: " + str(self.__device_variant))
        if self.__device_variant == 0:
            log.debug("Die Variante '0' bietet keine PV Daten!")
        elif self.__device_variant == 1:
            state = self.__update_variant_1()
        elif self.__device_variant == 2:
            state = self.__update_variant_2()
        elif self.__device_variant == 3:
            state = self.__update_variant_1("v2")
        else:
            raise ValueError("Unbekannte Variante: " + str(self.__device_variant))
        self.store.set(state)


component_descriptor = ComponentDescriptor(configuration_factory=SonnenbatterieInverterSetup)
