"""Allgemeine Einstellungen
"""
from dataclasses import dataclass, field
from enum import Enum
import logging
import random
from typing import List, Optional

from control import data
from control.bat_all import BatConsiderationMode
from helpermodules.constants import NO_ERROR
from helpermodules import timecheck
from modules.common.configurable_ripple_control_receiver import ConfigurableRcr
from modules.ripple_control_receivers.gpio.config import GpioRcr
from modules.ripple_control_receivers.gpio.ripple_control_receiver import create_ripple_control_receiver

log = logging.getLogger(__name__)


@dataclass
class InstantCharging:
    phases_to_use: int = field(default=1, metadata={
        "topic": "chargemode_config/instant_charging/phases_to_use", "mutable_by_algorithm": False})


def instant_charging_factory() -> InstantCharging:
    return InstantCharging()


def control_range_factory() -> List:
    return [0, 230]


@dataclass
class PvCharging:
    bat_power_reserve: int = field(default=2000, metadata={
        "topic": "chargemode_config/pv_charging/bat_power_reserve", "mutable_by_algorithm": False})
    bat_power_reserve_active: bool = field(default=False, metadata={
        "topic": "chargemode_config/pv_charging/bat_power_reserve_active", "mutable_by_algorithm": False})
    control_range: List = field(default_factory=control_range_factory, metadata={
        "topic": "chargemode_config/pv_charging/control_range", "mutable_by_algorithm": False})
    feed_in_yield: int = field(default=15000, metadata={
        "topic": "chargemode_config/pv_charging/feed_in_yield", "mutable_by_algorithm": False})
    phase_switch_delay: int = field(default=7, metadata={
        "topic": "chargemode_config/pv_charging/phase_switch_delay", "mutable_by_algorithm": False})
    phases_to_use: int = field(default=1, metadata={
        "topic": "chargemode_config/pv_charging/phases_to_use", "mutable_by_algorithm": False})
    bat_power_discharge: int = field(default=1500, metadata={
        "topic": "chargemode_config/pv_charging/bat_power_discharge", "mutable_by_algorithm": False})
    bat_power_discharge_active: bool = field(default=False, metadata={
        "topic": "chargemode_config/pv_charging/bat_power_discharge_active", "mutable_by_algorithm": False})
    min_bat_soc: int = field(default=50, metadata={
        "topic": "chargemode_config/pv_charging/min_bat_soc", "mutable_by_algorithm": False})
    bat_mode: BatConsiderationMode = field(default=BatConsiderationMode.EV_MODE.value, metadata={
        "topic": "chargemode_config/pv_charging/bat_mode", "mutable_by_algorithm": False})
    switch_off_delay: int = field(default=60, metadata={
                                  "topic": "chargemode_config/pv_charging/switch_off_delay", "mutable_by_algorithm": False})
    switch_off_threshold: int = field(default=5, metadata={
        "topic": "chargemode_config/pv_charging/switch_off_threshold", "mutable_by_algorithm": False})
    switch_on_delay: int = field(default=30, metadata={
        "topic": "chargemode_config/pv_charging/switch_on_delay", "mutable_by_algorithm": False})
    switch_on_threshold: int = field(default=1500, metadata={
        "topic": "chargemode_config/pv_charging/switch_on_threshold", "mutable_by_algorithm": False})


def pv_charging_factory() -> PvCharging:
    return PvCharging()


@dataclass
class ScheduledCharging:
    phases_to_use: int = field(default=0, metadata={
        "topic": "chargemode_config/scheduled_charging/phases_to_use", "mutable_by_algorithm": False})


def scheduled_charging_factory() -> ScheduledCharging:
    return ScheduledCharging()


@dataclass
class TimeCharging:
    phases_to_use: int = field(default=1, metadata={
        "topic": "chargemode_config/time_charging/phases_to_use", "mutable_by_algorithm": False})


def time_charging_factory() -> TimeCharging:
    return TimeCharging()


@dataclass
class ChargemodeConfig:
    instant_charging: InstantCharging = field(default_factory=instant_charging_factory)
    pv_charging: PvCharging = field(default_factory=pv_charging_factory)
    retry_failed_phase_switches: bool = field(
        default=False,
        metadata={"topic": "chargemode_config/retry_failed_phase_switches", "mutable_by_algorithm": False})
    scheduled_charging: ScheduledCharging = field(default_factory=scheduled_charging_factory)
    time_charging: TimeCharging = field(default_factory=time_charging_factory)
    unbalanced_load_limit: int = field(
        default=18, metadata={"topic": "chargemode_config/unbalanced_load_limit", "mutable_by_algorithm": False})
    unbalanced_load: bool = field(default=False, metadata={
                                  "topic": "chargemode_config/unbalanced_load", "mutable_by_algorithm": False})


def chargemode_config_factory() -> ChargemodeConfig:
    return ChargemodeConfig()


@dataclass
class RippleControlReceiverGet:
    fault_state: int = field(default=0, metadata={
                             "topic": "ripple_control_receiver/get/fault_state", "mutable_by_algorithm": True})
    fault_str: str = field(default=NO_ERROR, metadata={
                           "topic": "ripple_control_receiver/get/fault_str", "mutable_by_algorithm": True})
    override_value: float = field(default=100, metadata={
        "topic": "ripple_control_receiver/get/override_value", "mutable_by_algorithm": True})


def rcr_get_factory() -> RippleControlReceiverGet:
    return RippleControlReceiverGet()


def gpio_rcr_factory() -> ConfigurableRcr:
    return create_ripple_control_receiver(GpioRcr())


class OverrideReference(Enum):
    EVU = "evu"
    CHARGEPOINT = "chargepoint"


@dataclass
class RippleControlReceiver:
    get: RippleControlReceiverGet = field(default_factory=rcr_get_factory)
    module: ConfigurableRcr = field(default_factory=gpio_rcr_factory, metadata={
                                    "topic": "ripple_control_receiver/module", "mutable_by_algorithm": False})
    overrice_reference: OverrideReference = OverrideReference.CHARGEPOINT


def ripple_control_receiver_factory() -> RippleControlReceiver:
    return RippleControlReceiver()


@dataclass
class Prices:
    bat: float = field(default=0.0002, metadata={"topic": "prices/bat", "mutable_by_algorithm": False})
    cp: float = field(default=0, metadata={"topic": "prices/cp", "mutable_by_algorithm": False})
    grid: float = field(default=0.0003, metadata={"topic": "prices/grid", "mutable_by_algorithm": False})
    pv: float = field(default=0.00015, metadata={"topic": "prices/pv", "mutable_by_algorithm": False})


def prices_factory() -> Prices:
    return Prices()


@dataclass
class GeneralData:
    chargemode_config: ChargemodeConfig = field(default_factory=chargemode_config_factory)
    control_interval: int = field(default=10, metadata={"topic": "control_interval", "mutable_by_algorithm": False})
    extern_display_mode: str = field(default="primary", metadata={
                                     "topic": "extern_display_mode", "mutable_by_algorithm": False})
    extern: bool = field(default=False, metadata={"topic": "extern", "mutable_by_algorithm": False})
    external_buttons_hw: bool = field(
        default=False, metadata={"topic": "external_buttons_hw", "mutable_by_algorithm": False})
    grid_protection_active: bool = field(
        default=False, metadata={"topic": "grid_protection_active", "mutable_by_algorithm": True})
    grid_protection_configured: bool = field(
        default=True, metadata={"topic": "grid_protection_configured", "mutable_by_algorithm": False})
    grid_protection_random_stop: int = field(
        default=0, metadata={"topic": "grid_protection_random_stop", "mutable_by_algorithm": True})
    grid_protection_timestamp: Optional[float] = field(
        default=None, metadata={"topic": "grid_protection_timestamp", "mutable_by_algorithm": True})
    mqtt_bridge: bool = False
    prices: Prices = field(default_factory=prices_factory)
    range_unit: str = "km"
    ripple_control_receiver: RippleControlReceiver = field(default_factory=ripple_control_receiver_factory)


class General:
    """
    """

    def __init__(self):
        self.data: GeneralData = GeneralData()

    def get_phases_chargemode(self, chargemode: str) -> Optional[int]:
        """ gibt die Anzahl Phasen zurück, mit denen im jeweiligen Lademodus geladen wird.
        Wenn der Lademodus Stop oder Standby ist, wird 0 zurückgegeben, da in diesem Fall
        die bisher genutzte Phasenzahl weiter genutzt wird, bis der Algorithmus eine Umschaltung vorgibt.
        """
        try:
            if chargemode == "stop" or chargemode == "standby":
                # bei diesen Lademodi kann die bisherige Phasenzahl beibehalten werden.
                return None
            else:
                return getattr(self.data.chargemode_config, chargemode).phases_to_use
        except Exception:
            log.exception("Fehler im General-Modul")
            return 1

    def grid_protection(self):
        """ Wenn der Netzschutz konfiguriert ist, wird geprüft, ob die Frequenz außerhalb des Normalbereichs liegt
        und dann der Netzschutz aktiviert. Bei der Ermittlung des benötigten Stroms im EV-Modul wird geprüft, ob
        der Netzschutz aktiv ist und dann die Ladung gestoppt.
        """
        try:
            evu_counter = data.data.counter_all_data.get_evu_counter_str()
            if self.data.grid_protection_configured:
                frequency = data.data.counter_data[evu_counter].data.get.frequency * 100
                grid_protection_active = self.data.grid_protection_active
                if not grid_protection_active:
                    if 4500 < frequency < 4920:
                        self.data.grid_protection_random_stop = random.randint(
                            1, 90)
                        self.data.grid_protection_timestamp = timecheck.create_timestamp(
                        )
                        self.data.grid_protection_active = True
                        log.info("Netzschutz aktiv! Frequenz: " +
                                 str(data.data.counter_data[evu_counter].data.get.frequency)+"Hz")
                    if 5180 < frequency < 5300:
                        self.data.grid_protection_random_stop = 0
                        self.data.grid_protection_timestamp = None
                        self.data.grid_protection_active = True
                        log.info("Netzschutz aktiv! Frequenz: " +
                                 str(data.data.counter_data[evu_counter].data.get.frequency)+"Hz")
                else:
                    if 4962 < frequency < 5100:
                        self.data.grid_protection_active = False
                        log.info("Netzfrequenz wieder im normalen Bereich. Frequenz: " +
                                 str(data.data.counter_data[evu_counter].data.get.frequency)+"Hz")
                        self.data.grid_protection_timestamp = None
                        self.data.grid_protection_random_stop = 0
        except Exception:
            log.exception("Fehler im General-Modul")
