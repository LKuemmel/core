from dataclasses import dataclass, field
import threading
from typing import Dict, List, Optional, Protocol
from control.chargepoint.chargepoint_template import CpTemplate

from control.chargepoint.control_parameter import ControlParameter, control_parameter_factory
from control.ev import Ev
from dataclass_utils.factories import currents_list_factory, empty_dict_factory, voltages_list_factory
from helpermodules.constants import NO_ERROR
from modules.common.abstract_chargepoint import AbstractChargepoint


@dataclass
class ConnectedSoc:
    fault_str: str = NO_ERROR
    fault_state: int = 0
    range_charged: float = 0
    range_unit: str = "km"
    range: float = 0
    soc: int = 0
    timestamp: Optional[str] = None


@dataclass
class ConnectedSocConfig:
    configured: str = ""


@dataclass
class ConnectedInfo:
    id: int = 0
    name: str = "Ladepunkt"


@dataclass
class ConnectedConfig:
    average_consumption: float = 17
    charge_template: int = 0
    chargemode: str = "stop"
    current_plan: Optional[int] = 0
    ev_template: int = 0
    priority: bool = False
    time_charging_in_use: bool = False


def connected_config_factory() -> ConnectedConfig:
    return ConnectedConfig()


def connected_info_factory() -> ConnectedInfo:
    return ConnectedInfo()


def connected_soc_factory() -> ConnectedSoc:
    return ConnectedSoc()


@dataclass
class ConnectedVehicle:
    config: ConnectedConfig = field(default_factory=connected_config_factory, metadata={
                                    "topic": "get/connected_vehicle/config", "subscribe_only": False})
    info: ConnectedInfo = field(default_factory=connected_info_factory, metadata={
                                "topic": "get/connected_vehicle/info", "subscribe_only": False})
    soc: ConnectedSoc = field(default_factory=connected_soc_factory, metadata={
                              "topic": "get/connected_vehicle/soc", "subscribe_only": False})


@dataclass
class Log:
    chargemode_log_entry: str = "_"
    costs: float = 0
    imported_at_mode_switch: float = 0
    imported_at_plugtime: float = 0
    imported_since_mode_switch: float = 0
    imported_since_plugged: float = 0
    range_charged: float = 0
    time_charged: str = "00:00"
    timestamp_start_charging: Optional[float] = None
    ev: int = -1
    prio: bool = False
    rfid: Optional[str] = None
    serial_number: Optional[str] = None


def connected_vehicle_factory() -> ConnectedVehicle:
    return ConnectedVehicle()


@dataclass
class Get:
    charge_state: bool = field(default=False, metadata={"topic": "get/charge_state", "subscribe_only": True})
    connected_vehicle: ConnectedVehicle = field(default_factory=connected_vehicle_factory)
    currents: List[float] = field(default_factory=currents_list_factory, metadata={
                                  "topic": "get/currents", "subscribe_only": True})
    daily_imported: float = field(default=0, metadata={"topic": "get/daily_imported", "subscribe_only": False})
    daily_exported: float = field(default=0, metadata={"topic": "get/daily_exported", "subscribe_only": False})
    evse_current: Optional[float] = field(
        default=None, metadata={"topic": "get/daily_exported", "subscribe_only": True})
    exported: float = field(default=0, metadata={"topic": "get/exported", "subscribe_only": True})
    fault_str: str = field(default=NO_ERROR, metadata={"topic": "get/fault_str", "subscribe_only": False})
    fault_state: int = field(default=0, metadata={"topic": "get/fault_state", "subscribe_only": False})
    imported: float = field(default=0, metadata={"topic": "get/imported", "subscribe_only": True})
    phases_in_use: int = field(default=0, metadata={"topic": "get/phases_in_use", "subscribe_only": True})
    plug_state: bool = field(default=False, metadata={"topic": "get/plug_state", "subscribe_only": True})
    power: float = field(default=0, metadata={"topic": "get/power", "subscribe_only": True})
    rfid_timestamp: Optional[float] = field(
        default=None, metadata={"topic": "get/rfid_timestamp", "subscribe_only": True})
    rfid: Optional[int] = field(default=None, metadata={"topic": "get/rfid", "subscribe_only": True})
    serial_number: Optional[str] = field(
        default=None, metadata={"topic": "get/serial_number", "subscribe_only": True})
    soc: Optional[float] = field(default=None, metadata={"topic": "get/soc", "subscribe_only": True})
    soc_timestamp: Optional[int] = field(
        default=None, metadata={"topic": "get/soc_timestamp", "subscribe_only": True})
    state_str: Optional[str] = field(default=None, metadata={"topic": "get/state_str", "subscribe_only": False})
    vehicle_id: Optional[str] = field(default=None, metadata={"topic": "get/vehicle_id", "subscribe_only": True})
    voltages: List[float] = field(default_factory=voltages_list_factory, metadata={
                                  "topic": "get/voltages", "subscribe_only": True})


def ev_factory() -> Ev:
    return Ev(0)


def log_factory() -> Log:
    return Log()


@dataclass
class Set:
    change_ev_permitted: bool = False
    charging_ev: int = field(default=-1, metadata={"topic": "set/charging_ev", "subscribe_only": False})
    charging_ev_prev: int = field(default=-1, metadata={"topic": "set/charging_ev_prev", "subscribe_only": False})
    current: float = field(default=0, metadata={"topic": "set/current", "subscribe_only": False})
    loadmanagement_available: bool = True
    log: Log = field(default_factory=log_factory, metadata={"topic": "set/log", "subscribe_only": False})
    manual_lock: bool = field(default=False, metadata={"topic": "set/manual_lock", "subscribe_only": False})
    phases_to_use: int = field(default=0, metadata={"topic": "set/phases_to_use", "subscribe_only": False})
    plug_state_prev: bool = field(default=False, metadata={
                                  "topic": "set/plug_state_prev", "subscribe_only": False})
    plug_time: Optional[float] = field(default=None, metadata={"topic": "set/plug_time", "subscribe_only": False})
    required_power: float = 0
    rfid: Optional[str] = field(default=None, metadata={"topic": "set/rfid", "subscribe_only": False})
    target_current: float = 0  # Sollstrom aus fest vorgegebener Stromstärke
    charging_ev_data: Ev = field(default_factory=ev_factory)


@dataclass
class Config:
    configuration: Dict = field(default_factory=empty_dict_factory)
    ev: int = 0
    name: str = "Standard-Ladepunkt"
    type: Optional[str] = None
    template: int = 0
    connected_phases: int = 3
    phase_1: int = 0
    auto_phase_switch_hw: bool = False
    control_pilot_interruption_hw: bool = False
    id: int = 0

    def __post_init__(self):
        self.event_update_state: threading.Event

    @property
    def ev(self) -> int:
        return self._ev

    @ev.setter
    def ev(self, ev: int):
        self._ev = ev
        try:
            self.event_update_state.set()
        except AttributeError:
            pass

    def __getstate__(self):
        state = self.__dict__.copy()
        if state.get('event_update_state'):
            del state['event_update_state']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)


def get_factory() -> Get:
    return Get()


def set_factory() -> Set:
    return Set()


def config_factory() -> Config:
    return Config()


@dataclass
class ChargepointData:
    control_parameter: ControlParameter = field(default_factory=control_parameter_factory)
    get: Get = field(default_factory=get_factory)
    set: Set = field(default_factory=set_factory)
    config: Config = field(default_factory=config_factory, metadata={"topic": "config", "subscribe_only": True})

    def set_event(self, event: Optional[threading.Event] = None) -> None:
        self.event_update_state = event
        if event:
            self.config.event_update_state = event

    def __getstate__(self):
        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()
        # Remove the unpicklable entries.
        if state.get('event_update_state'):
            del state['event_update_state']
        return state

    def __setstate__(self, state):
        # Restore instance attributes (i.e., filename and lineno).
        self.__dict__.update(state)


class ChargepointProtocol(Protocol):
    @property
    def template(self) -> CpTemplate: ...
    @property
    def chargepoint_module(self) -> AbstractChargepoint: ...
    @property
    def num(self) -> int: ...
    @property
    def set_current_prev(self) -> float: ...
    @property
    def data(self) -> ChargepointData: ...
