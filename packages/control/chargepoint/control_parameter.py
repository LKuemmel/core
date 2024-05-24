from dataclasses import dataclass, field
from typing import List, Optional

from control.chargepoint.chargepoint_state import ChargepointState
from control.chargemode import Chargemode as Chargemode_enum
from control.limiting_value import LimitingValue
from dataclass_utils.factories import currents_list_factory


@dataclass
class ControlParameter:
    chargemode: Chargemode_enum = field(
        default=Chargemode_enum.STOP,
        metadata={"topic": "control_parameter/chargemode", "subscribe_only": False})
    current_plan: Optional[str] = field(
        default=None,
        metadata={"topic": "control_parameter/current_plan", "subscribe_only": False})
    failed_phase_switches: int = field(
        default=0,
        metadata={"topic": "control_parameter/failed_phase_switches", "subscribe_only": False})
    imported_at_plan_start: Optional[float] = field(
        default=None,
        metadata={"topic": "control_parameter/imported_at_plan_start", "subscribe_only": False})
    imported_instant_charging: Optional[float] = field(
        default=None,
        metadata={"topic": "control_parameter/imported_instant_charging", "subscribe_only": False})
    limit: Optional[LimitingValue] = field(
        default=None,
        metadata={"topic": "control_parameter/limit", "subscribe_only": False})
    phases: int = field(
        default=0,
        metadata={"topic": "control_parameter/phases", "subscribe_only": False})
    prio: bool = field(
        default=False,
        metadata={"topic": "control_parameter/prio", "subscribe_only": False})
    required_current: float = field(
        default=0,
        metadata={"topic": "control_parameter/required_current", "subscribe_only": False})
    required_currents: List[float] = field(
        default_factory=currents_list_factory)
    state: ChargepointState = field(
        default=ChargepointState.NO_CHARGING_ALLOWED,
        metadata={"topic": "control_parameter/state", "subscribe_only": False})
    submode: Chargemode_enum = field(
        default=Chargemode_enum.STOP,
        metadata={"topic": "control_parameter/submode", "subscribe_only": False})
    timestamp_auto_phase_switch: Optional[float] = field(
        default=None,
        metadata={"topic": "control_parameter/timestamp_auto_phase_switch", "subscribe_only": False})
    timestamp_perform_phase_switch: Optional[float] = field(
        default=None,
        metadata={"topic": "control_parameter/timestamp_perform_phase_switch", "subscribe_only": False})
    timestamp_switch_on_off: Optional[float] = field(
        default=None,
        metadata={"topic": "control_parameter/timestamp_switch_on_off", "subscribe_only": False})


def control_parameter_factory() -> ControlParameter:
    return ControlParameter()
