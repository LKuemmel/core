import pytest

from control import data
from control.algorithm import additional_current
from control.chargemode import Chargemode
from control.chargepoint.chargepoint import Chargepoint, ChargepointData
from control.chargepoint.chargepoint_data import Set
from control.chargepoint.control_parameter import ControlParameter
from control.ev.charge_template import ChargeTemplate
from control.ev.ev import Ev
from control.limiting_value import LoadmanagementLimit
from control.loadmanagement import LimitingValue


@pytest.mark.parametrize(
    "set_current, limit, expected_msg",
    [pytest.param(7, LoadmanagementLimit(None,  None), None, id="unverändert"),
     pytest.param(
        6, LoadmanagementLimit(LimitingValue.CURRENT.value.format('Garage'), LimitingValue.CURRENT),
        f"Es kann nicht mit der vorgegebenen Stromstärke geladen werden{LimitingValue.CURRENT.value.format('Garage')}",
         id="begrenzt durch Strom"),
     pytest.param(
        6, LoadmanagementLimit(LimitingValue.POWER.value.format('Garage'), LimitingValue.POWER),
        f"Es kann nicht mit der vorgegebenen Stromstärke geladen werden{LimitingValue.POWER.value.format('Garage')}",
         id="begrenzt durch Leistung"),
     pytest.param(
        6, LoadmanagementLimit(LimitingValue.UNBALANCED_LOAD.value.format('Garage'), LimitingValue.UNBALANCED_LOAD),
        f"Es kann nicht mit der vorgegebenen Stromstärke geladen werden"
        f"{LimitingValue.UNBALANCED_LOAD.value.format('Garage')}",
        id="begrenzt durch Schieflast"),
     ])
def test_set_loadmangement_message(set_current, limit, expected_msg, monkeypatch):
    # setup
    ev = Ev(0)
    ev.charge_template = ChargeTemplate()
    cp1 = Chargepoint(1, None)
    cp1.data = ChargepointData(set=Set(current=set_current),
                               control_parameter=ControlParameter(required_currents=[8]*3))

    # execution
    additional_current.AdditionalCurrent()._set_loadmangement_message(7, limit, cp1)

    # evaluation
    assert cp1.data.get.state_str == expected_msg


@pytest.mark.parametrize("phases", [1, 2, 3])
def test_additional_current_preserves_target_across_counter_levels(phases):
    """The previous stage's allocation may differ from the configured minimum."""
    cp = data.data.cp_data["cp4"]
    cp.data.control_parameter.chargemode = Chargemode.INSTANT_CHARGING
    cp.data.control_parameter.submode = Chargemode.INSTANT_CHARGING
    cp.data.control_parameter.min_current = 6
    cp.data.control_parameter.required_current = 16
    cp.data.control_parameter.required_currents = [16]*phases + [0]*(3-phases)
    cp.data.get.charge_state = True
    cp.data.get.voltages = [230]*3
    cp.data.set.target_current = 10
    for counter in data.data.counter_data.values():
        counter.data.set.raw_currents_left = [100]*3
        counter.data.set.raw_power_left = 40000

    additional_current.AdditionalCurrent().set_additional_current([cp])

    assert cp.data.set.current == 16
    for counter in data.data.counter_data.values():
        assert counter.data.set.raw_power_left == pytest.approx(40000 - 6*phases*230)
        assert counter.data.set.raw_currents_left == [94]*phases + [100]*(3-phases)
