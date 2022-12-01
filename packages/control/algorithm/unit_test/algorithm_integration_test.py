import pytest

from control.chargemode import Chargemode
from control import data
from control.algorithm.algorithm import Algorithm


@pytest.fixture()
def all_cp_instant_charging():
    for i in range(3, 6):
        data.data.cp_data[f"cp{i}"].data.set.charging_ev_data.data.control_parameter.required_currents = [0]*3
        data.data.cp_data[f"cp{i}"].data.set.charging_ev_data.data.control_parameter.required_currents[i-3] = 16
        data.data.cp_data[f"cp{i}"].data.set.charging_ev_data.data.control_parameter.chargemode = Chargemode.INSTANT_CHARGING
        data.data.cp_data[f"cp{i}"].data.set.charging_ev_data.data.control_parameter.submode = Chargemode.INSTANT_CHARGING
    data.data.cp_data["cp3"].data.get.currents = [10, 0, 0]
    data.data.cp_data["cp4"].data.get.currents = [6, 0, 0]
    data.data.cp_data["cp5"].data.get.currents = [6, 0, 0]


def test_start_instant_charging(all_cp_instant_charging):
    # alle 3 im Sofortladen, keine Ladung aktiv -> dürfen nur Mindeststrom zugeteilt kriegen
    # setup
    data.data.counter_data["counter0"].data["set"]["raw_power_left"] = 21310
    data.data.counter_data["counter0"].data["set"]["raw_currents_left"] = [32, 30, 31]
    data.data.counter_data["counter6"].data["set"]["raw_currents_left"] = [16, 12, 14]
    # execution
    Algorithm().calc_current()

    # evaluation
    assert data.data.cp_data["cp3"].data.set.current == 10
    assert data.data.cp_data["cp4"].data.set.current == 6
    assert data.data.cp_data["cp5"].data.set.current == 6
    assert data.data.counter_data["counter0"].data["set"]["raw_power_left"] == 16250
    assert data.data.counter_data["counter0"].data["set"]["raw_currents_left"] == [22, 24, 25]
    assert data.data.counter_data["counter6"].data["set"]["raw_currents_left"] == [4, 0, 2]

# Lastmanagement
# alle 3 im Sofortladen, 3 Ladung aktiv -> alle 3 reduziert wg Strom
# alle 3 im Sofortladen, 3 Ladung aktiv -> alle 3 reduziert wg Leistung
# alle 3 im Sofortladen, 3 Ladung aktiv -> alle 3 reduziert wg Schieflast
# alle 3 im Sofortladen, 3 Ladung aktiv -> 1 wird höher priorisiert, lädt mit Sollstrom
# alle 3 im Sofortladen, 3 Ladung aktiv -> 1 wird niedriger priorisiert, lädt mit Minstrom
# alle 3 im Sofortladen, 3 Ladung aktiv -> 1 wird höherer LM, lädt mit Sollstrom
# alle 3 im Sofortladen, 3 Ladung aktiv -> 1 wird niedrigerer LM, lädt mit Minstrom

# PV-geführt
# alle 3 im PV-laden, keine Ladung -> bei zweien die Verz starten, für den 3 reichts nicht
# alle 3 im PV-laden, keine Ladung -> bei einem die Verz abgelaufen, erhält minstrom
# alle 3 im PV-laden, Ladung -> raw_power_left positiv
# alle 3 im PV-laden, Ladung -> raw_power_left negativ, Reduktion reicht
# alle 3 im PV-laden, Ladung -> raw_power_left negativ, Phasenumschaltung 3 -> 1
# alle 3 im PV-laden, Ladung -> raw_power_left positiv, Phasenumschaltung 1 -> 3
# alle 3 im PV-laden, Ladung -> raw_power_left negativ, zwei abschalten, einer darf weiter laden

# deprecated
# @pytest.mark.parametrize("required_currents, expected_set_current, expected_raw_power_left, expected_raw_currents_left_0, expected_raw_currents_left_6",
#                          [pytest.param([16]*3, 6.0, 650, [2, 0, 1], [18, 14, 16], id="start charging, 3 phases"),
#                           ]
#                          )
# def test_instant_charging_cp_3(required_currents, expected_set_current, expected_raw_power_left, expected_raw_currents_left_0, expected_raw_currents_left_6):
#     # setup
#     data.data.cp_data["cp3"].data.get.plug_state = True
#     data.data.cp_data["cp3"].data.set.charging_ev = 0
#     data.data.cp_data["cp3"].data.set.charging_ev_data = Ev(0)
#     data.data.cp_data["cp3"].data.set.charging_ev_data.data.control_parameter.required_currents = required_currents
#     data.data.cp_data["cp3"].data.set.charging_ev_data.data.control_parameter.chargemode = Chargemode.INSTANT_CHARGING
#     data.data.cp_data["cp3"].data.set.charging_ev_data.data.control_parameter.submode = Chargemode.INSTANT_CHARGING
#     data.data.counter_data["counter0"].data["set"]["raw_power_left"] = 10310
#     data.data.counter_data["counter0"].data["set"]["raw_currents_left"] = [16, 14, 15]
#     data.data.counter_data["counter6"].data["set"]["raw_currents_left"] = [32, 28, 30]

#     # execution
#     Algorithm().calc_current()

#     # evaluation
#     assert data.data.cp_data["cp3"].data.set.current == expected_set_current
#     assert data.data.counter_data["counter0"].data["set"]["raw_power_left"] == expected_raw_power_left
#     assert data.data.counter_data["counter0"].data["set"]["raw_currents_left"] == expected_raw_currents_left_0
#     assert data.data.counter_data["counter6"].data["set"]["raw_currents_left"] == expected_raw_currents_left_6
