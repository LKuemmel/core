"""Optionale Module
"""
from dataclasses import dataclass, field
import logging
from math import ceil  # Aufrunden
import threading
from typing import Dict, List

from dataclass_utils.factories import empty_dict_factory
from helpermodules.constants import NO_ERROR
from helpermodules.timecheck import create_unix_timestamp_current_full_hour
from modules.common.configurable_tariff import ConfigurableElectricityTariff
from modules.display_themes.cards.config import CardsDisplayTheme

log = logging.getLogger(__name__)


@dataclass
class EtGet:
    fault_state: int = field(default=0, metadata={"topic": "et/get/fault_state", "subscribe_only": False})
    fault_str: str = field(default=NO_ERROR, metadata={"topic": "et/get/fault_str", "subscribe_only": False})
    prices: Dict = field(default_factory=empty_dict_factory, metadata={
                         "topic": "et/get/prices", "subscribe_only": False})


def get_factory() -> EtGet:
    return EtGet()


@dataclass
class Et:
    get: EtGet = field(default_factory=get_factory)


def et_factory() -> Et:
    return Et()


def cards_display_theme_factory() -> CardsDisplayTheme:
    return CardsDisplayTheme()


@dataclass
class InternalDisplay:
    active: bool = field(default=False, metadata={"topic": "int_display/active", "subscribe_only": True})
    on_if_plugged_in: bool = field(default=True, metadata={
                                   "topic": "int_display/on_if_plugged_in", "subscribe_only": True})
    pin_active: bool = field(default=False, metadata={"topic": "int_display/pin_active", "subscribe_only": True})
    pin_code: str = field(default="0000", metadata={"topic": "int_display/pin_code", "subscribe_only": True})
    standby: int = field(default=60, metadata={"topic": "int_display/standby", "subscribe_only": True})
    theme: CardsDisplayTheme = field(default_factory=cards_display_theme_factory, metadata={
                                     "topic": "int_display/theme", "subscribe_only": True})


def int_display_factory() -> InternalDisplay:
    return InternalDisplay()


@dataclass
class Led:
    active: bool = False


def led_factory() -> Led:
    return Led()


@dataclass
class Rfid:
    active: bool = field(default=False, metadata={"topic": "rfid/active", "subscribe_only": True})


def rfid_factory() -> Rfid:
    return Rfid()


@dataclass
class OptionalData:
    et: Et = field(default_factory=et_factory)
    int_display: InternalDisplay = field(default_factory=int_display_factory)
    led: Led = field(default_factory=led_factory)
    rfid: Rfid = field(default_factory=rfid_factory)


@dataclass
class Optional:
    def __init__(self):
        try:
            self.data = OptionalData()
            self.et_module: ConfigurableElectricityTariff = field(
                default=None, metadata={"topic": "optional/et/provider", "subscribe_only": True})
        except Exception:
            log.exception("Fehler im Optional-Modul")

    def et_provider_availble(self) -> bool:
        return self.et_module is not None and self.data.et.get.fault_state != 2

    def et_price_lower_than_limit(self, max_price: float):
        """ prüft, ob der aktuelle Strompreis unter der festgelegten Preisgrenze liegt.

        Return
        ------
        True: Preis liegt darunter
        False: Preis liegt darüber
        """
        try:
            if self.et_get_current_price() <= max_price:
                return True
            else:
                return False
        except KeyError:
            log.exception("Fehler beim strompreisbasierten Laden")
            self.et_get_prices()
        except Exception:
            log.exception("Fehler im Optional-Modul")
            return False

    def et_get_current_price(self):
        return self.data.et.get.prices[str(create_unix_timestamp_current_full_hour())]

    def et_get_loading_hours(self, duration: float, remaining_time: float) -> List[int]:
        """ geht die Preise der nächsten 24h durch und liefert eine Liste der Uhrzeiten, zu denen geladen werden soll

        Parameter
        ---------
        duration: float
            benötigte Ladezeit

        Return
        ------
        list: Key des Dictionary (Unix-Sekunden der günstigen Stunden)
        """
        try:
            prices = self.data.et.get.prices
            prices_in_scheduled_time = {}
            i = 0
            for timestamp, price in prices.items():
                if i < ceil((duration+remaining_time)/3600):
                    prices_in_scheduled_time.update({timestamp: price})
                    i += 1
                else:
                    break
            ordered = sorted(prices_in_scheduled_time.items(), key=lambda x: x[1])
            return [int(i[0]) for i in ordered][:ceil(duration/3600)]
        except Exception:
            log.exception("Fehler im Optional-Modul")
            return []

    def et_get_prices(self):
        try:
            if self.et_module:
                for thread in threading.enumerate():
                    if thread.name == "electricity tariff":
                        log.debug("Don't start multiple instances of electricity tariff thread.")
                        return
                threading.Thread(target=self.et_module.update, args=(), name="electricity tariff").start()
            else:
                # Wenn kein Modul konfiguriert ist, Fehlerstatus zurücksetzen.
                self.data.et.get.fault_state = 0
                self.data.et.get.fault_str = NO_ERROR
        except Exception:
            log.exception("Fehler im Optional-Modul")
