#!/usr/bin/env python3
import logging
from html.parser import HTMLParser
from typing import Any, List, Tuple, TypedDict

from modules.devices.byd.byd.config import BYD, BYDBatSetup
from modules.common import req
from modules.common.abstract_device import AbstractBat
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.simcount import SimCounter
from modules.common.store import get_bat_value_store

log = logging.getLogger(__name__)


class KwargsDict(TypedDict):
    device_config: BYD


class BYDBat(AbstractBat):
    def __init__(self, component_config: BYDBatSetup, **kwargs: Any) -> None:
        self.component_config = component_config
        self.kwargs: KwargsDict = kwargs

    def initialize(self) -> None:
        self.device_config: BYD = self.kwargs['device_config']
        self.sim_counter = SimCounter(self.device_config.id, self.component_config.id, prefix="speicher")
        self.store = get_bat_value_store(self.component_config.id)
        self.fault_state = FaultState(ComponentInfo.from_component_config(self.component_config))

    def update(self) -> None:
        power, soc = self.get_values()

        imported, exported = self.sim_counter.sim_count(power)
        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.store.set(bat_state)

    def get_values(self) -> Tuple[float, float]:
        '''BYD Speicher bieten zwei HTML-Seiten, auf denen Informationen abgegriffen werden können:
        /asp/Home.asp und /asp/RunData.asp. Aktuell (2022-03) ist die Leistungsangabe (Power) auf der
        RunData.asp auf ganze kW gerundet und somit für openWB nicht brauchbar.
        '''
        resp = req.get_http_session().get(
            'http://' + self.device_config.configuration.ip_address + '/asp/Home.asp',
            auth=(self.device_config.configuration.user, self.device_config.configuration.password))
        return BydParser.parse(resp.text)


class BydParser(HTMLParser):
    values = {"SOC:": 0, "Power:": 0}
    armed = None

    @staticmethod
    def parse(html: str):
        parser = BydParser()
        parser.feed(html)
        return parser.get_bat_state()

    def handle_starttag(self, tag, attrs: List[Tuple[str, str]]):
        if tag == "input" and self.armed is not None:
            for key, value in attrs:
                if key == "value":
                    self.values[self.armed] = value
                    break
            self.armed = None

    def handle_data(self, data: str):
        if data in self.values:
            self.armed = data

    def get_bat_state(self) -> Tuple[float, float]:
        return float(self.values["Power:"]) * 1000, float(self.values["SOC:"][:-1])


component_descriptor = ComponentDescriptor(configuration_factory=BYDBatSetup)
