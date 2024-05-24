"""PV-Logik
Die Leistung, die die PV-Module liefern, kann nicht komplett für das Laden und SmartHome verwendet werden.
Davon ab geht z.B. noch der Hausverbrauch. Für das Laden mit PV kann deshalb nur der Strom verwendet werden,
der sonst in das Netz eingespeist werden würde.
"""

from dataclasses import dataclass, field
import logging

from control import data
from helpermodules.constants import NO_ERROR

log = logging.getLogger(__name__)


@dataclass
class Config:
    configured: bool = field(default=False, metadata={"topic": "config/configured", "subscribe_only": False})


def config_factory() -> Config:
    return Config()


@dataclass
class Get:
    daily_exported: float = field(default=0, metadata={"topic": "get/daily_exported", "subscribe_only": False})
    fault_str: str = field(default=NO_ERROR, metadata={"topic": "get/fault_str", "subscribe_only": False})
    fault_state: int = field(default=0, metadata={"topic": "get/fault_state", "subscribe_only": False})
    monthly_exported: float = field(
        default=0, metadata={"topic": "get/monthly_exported", "subscribe_only": True})
    yearly_exported: float = field(default=0, metadata={"topic": "get/yearly_exported", "subscribe_only": True})
    exported: float = field(default=0, metadata={"topic": "get/exported", "subscribe_only": False})
    power: float = field(default=0, metadata={"topic": "get/power", "subscribe_only": False})


def get_factory() -> Get:
    return Get()


@dataclass
class PvAllData:
    config: Config = field(default_factory=config_factory)
    get: Get = field(default_factory=get_factory)


class PvAll:
    """
    """

    def __init__(self):
        self.data = PvAllData()

    def calc_power_for_all_components(self) -> None:
        try:
            if len(data.data.pv_data) >= 1:
                # Summe von allen konfigurierten Modulen
                exported = 0
                power = 0
                fault_state = 0
                for module in data.data.pv_data:
                    try:
                        if "pv" in module:
                            module_data = data.data.pv_data[module].data
                            if module_data.get.fault_state < 2:
                                power += module_data.get.power
                                exported += module_data.get.exported
                            else:
                                if fault_state < module_data.get.fault_state:
                                    fault_state = module_data.get.fault_state
                    except Exception:
                        log.exception("Fehler im allgemeinen PV-Modul für "+str(module))
                if fault_state == 0:
                    self.data.get.exported = exported
                    self.data.get.fault_state = 0
                    self.data.get.fault_str = NO_ERROR
                else:
                    self.data.get.fault_state = fault_state
                    self.data.get.fault_str = ("Bitte die Statusmeldungen der Wechselrichter prüfen. Es konnte kein "
                                               "aktueller Zählerstand ermittelt werden, da nicht alle Module Werte "
                                               "liefern.")
                self.data.get.power = power
                self.data.config.configured = True
            else:
                self.data.config.configured = False
                self.data.get = Get()
        except Exception:
            log.exception("Fehler im allgemeinen PV-Modul")
