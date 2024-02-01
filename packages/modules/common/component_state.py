from dataclasses import dataclass, field
import logging
from typing import Dict, List, Optional, Tuple
from dataclass_utils.factories import empty_three_phase_list_factory, empty_dict_factory, voltages_list_factory
from helpermodules import timecheck


log = logging.getLogger(__name__)


def _calculate_powers_and_currents(currents: Optional[List[float]],
                                   powers: Optional[List[float]],
                                   voltages: Optional[List[float]]) -> Tuple[
        Optional[List[float]], List[float], List[float]]:
    if voltages is None:
        voltages = [230.0]*3
    if powers is None:
        if currents is None:
            powers = [0.0]*3
        else:
            powers = [currents[i]*voltages[i] for i in range(0, 3)]
    if currents is None and powers:
        try:
            currents = [powers[i]/voltages[i] for i in range(0, 3)]
        except ZeroDivisionError:
            # some inverters (Sungrow) report 0V if in standby
            currents = [0.0]*3
    if currents and powers:
        currents = [currents[i]*-1 if powers[i] < 0 and currents[i] > 0 else currents[i] for i in range(0, 3)]
    return currents, powers, voltages


@dataclass
class BatState:
    imported: float = 0
    exported: float = 0
    power: float = 0
    soc: float = 0


@dataclass
class CounterState:
    imported: float = 0
    exported: float = 0
    power: float = 0
    voltages: List[float] = field(default_factory=voltages_list_factory)
    currents: List[float] = field(default_factory=empty_three_phase_list_factory)
    powers: List[float] = field(default_factory=empty_three_phase_list_factory)
    power_factors: List[float] = field(default_factory=empty_three_phase_list_factory)
    frequency: float = 50
    """Args:
            imported: total imported energy in Wh
            exported: total exported energy in Wh
            power: actual power in W
            voltages: actual voltages for 3 phases in V
            currents: actual currents for 3 phases in A
            powers: actual powers for 3 phases in W
            power_factors: actual power factors for 3 phases
            frequency: actual grid frequency in Hz
        """
    @property
    def currents(self) -> str:
        return self._currents

    @currents.setter
    def currents(self, v: str) -> None:
        self._currents, self._powers, self._voltages = _calculate_powers_and_currents(v, self._powers, self._voltages)

    @property
    def powers(self) -> str:
        return self._powers

    @powers.setter
    def powers(self, v: str) -> None:
        self._currents, self._powers, self._voltages = _calculate_powers_and_currents(self._currents, v, self._voltages)

    @property
    def voltages(self) -> str:
        return self._voltages

    @voltages.setter
    def voltages(self, v: str) -> None:
        self._currents, self._powers, self._voltages = _calculate_powers_and_currents(self._currents, self._powers, v)

    def __post_init__(self):
        self._currents, self._powers, self.voltages = _calculate_powers_and_currents(
            self.currents, self.powers, self.voltages)


@dataclass
class InverterState:
    exported: float
    power: float
    currents: List[float] = field(default_factory=empty_three_phase_list_factory)
    dc_power: Optional[float] = None
    """Args:
        exported: total energy in Wh
        power: actual power in W
        currents: actual currents for 3 phases in A
        dc_power: dc power in W
    """

    def _check_currents_sign(self):
        if all(c > 0 for c in self._currents):
            if not ((sum(self._currents) < 0 and self._power < 0) or (sum(self._currents) > 0 and self._power > 0)):
                log.debug(f"currents sign wrong {self._currents}")

    @property
    def currents(self) -> str:
        return self._currents

    @currents.setter
    def currents(self, v: str) -> None:
        self._currents = v
        self._check_currents_sign()

    @property
    def power(self) -> str:
        return self._power

    @power.setter
    def power(self, v: str) -> None:
        self._power = v
        self._check_currents_sign()


@dataclass
class CarState:
    soc: float
    range: Optional[float] = None
    soc_timestamp: float = 0
    """Args:
        soc: actual state of charge in percent
        range: actual range in km
        soc_timestamp: timestamp of last request as unix timestamp
    """


@dataclass
class ChargepointState:
    phases_in_use: int = 0
    imported: float = 0
    exported: float = 0
    power: float = 0
    powers: List[float] = field(default_factory=empty_three_phase_list_factory)
    voltages: List[float] = field(default_factory=voltages_list_factory)
    currents: List[float] = field(default_factory=empty_three_phase_list_factory)
    power_factors: List[float] = field(default_factory=empty_three_phase_list_factory)
    charge_state: bool = False
    plug_state: bool = False
    rfid: Optional[str] = None
    rfid_timestamp: Optional[float] = None
    frequency: float = 50
    soc: Optional[float] = None
    soc_timestamp: Optional[int] = None
    evse_current: Optional[float] = None
    vehicle_id: Optional[str] = None

    @property
    def currents(self) -> str:
        return self._currents

    @currents.setter
    def currents(self, v: str) -> None:
        self._currents, self._powers, self._voltages = _calculate_powers_and_currents(v, self._powers, self._voltages)

    @property
    def powers(self) -> str:
        return self._powers

    @powers.setter
    def powers(self, v: str) -> None:
        self._currents, self._powers, self._voltages = _calculate_powers_and_currents(self._currents, v, self._voltages)

    @property
    def voltages(self) -> str:
        return self._voltages

    @voltages.setter
    def voltages(self, v: str) -> None:
        self._currents, self._powers, self._voltages = _calculate_powers_and_currents(self._currents, self._powers, v)

    def __post_init__(self):
        self._currents, self._powers, self.voltages = _calculate_powers_and_currents(
            self.currents, self.powers, self.voltages)

    @property
    def rfid(self) -> str:
        return self._rfid

    @rfid.setter
    def rfid(self, v: str) -> None:
        self._rfid = v
        if self.rfid_timestamp is None:
            self.rfid_timestamp = timecheck.create_timestamp()


@dataclass
class TariffState:
    prices: Dict[int, float] = field(default_factory=empty_dict_factory)


@dataclass
class RcrState:
    override_value: float = 0
