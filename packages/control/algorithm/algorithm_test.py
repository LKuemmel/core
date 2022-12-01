# from unittest.mock import Mock
# import pytest
# from control import data

# from control.algorithm.algorithm import Algorithm
# from control.chargemode import Chargemode
# from control.chargepoint import Chargepoint
# from control.pv import PvAll


# @pytest.fixture(autouse=True)
# def cp() -> None:
#     data.data_init(Mock())
#     data.data.cp_data = {"cp0": Chargepoint(0, None)}
#     data.data.pv_data["all"] = PvAll()


# @pytest.mark.parametrize("submode, charge_state, timer, expected_submode",
#                          [pytest.param(Chargemode.TIME_CHARGING.value, False, False, Chargemode.TIME_CHARGING.value),
#                           pytest.param(Chargemode.PV_CHARGING.value, False, False, Chargemode.PV_CHARGING.value),
#                           pytest.param(Chargemode.PV_CHARGING.value, True, False, Chargemode.PV_CHARGING.value),
#                           pytest.param(Chargemode.PV_CHARGING.value, True, True, Chargemode.STOP.value)])
# def test_stop_after_switch_off_delay(submode: str,
#                                      charge_state: bool,
#                                      timer: bool,
#                                      expected_submode: str,
#                                      monkeypatch):
#     # setup
#     switch_off_check_timer_mock = Mock(return_value=timer)
#     monkeypatch.setattr(PvAll, "switch_off_check_timer", switch_off_check_timer_mock)
#     data.data.cp_data["cp0"].data.set.charging_ev_data.data.control_parameter.submode = submode
#     data.data.cp_data["cp0"].data.set.charging_ev = 0
#     data.data.cp_data["cp0"].data.get.charge_state = charge_state

#     # execution
#     Algorithm()._stop_after_switch_off_delay()

#     # evaluation
#     assert data.data.cp_data["cp0"].data.set.charging_ev_data.data.control_parameter.submode == expected_submode
