import logging

from control.algorithm import common
from control.loadmanagement import Loadmanagement
from control.algorithm.filter_chargepoints import get_chargepoints_by_mode_and_counter

log = logging.getLogger(__name__)


class MinCurrent:
    def __init__(self) -> None:
        pass

    def set_min_current(self) -> None:
        for mode_tuple, counter in common.mode_and_counter_generator():
            preferenced_chargepoints = get_chargepoints_by_mode_and_counter(mode_tuple, f"counter{counter.num}")
            if preferenced_chargepoints:
                log.debug(f"Mode-Tuple {mode_tuple}, Zähler {counter.num}")
                chargepoints = len(preferenced_chargepoints)
                for i in range(chargepoints):
                    missing_currents, counts = common.get_min_current(preferenced_chargepoints[0])
                    available_currents, limit = Loadmanagement().get_available_currents(missing_currents, counter)
                    available_for_cp = common.available_current_for_cp(
                        preferenced_chargepoints[0], counts, available_currents)
                    if available_for_cp < preferenced_chargepoints[0].data.set.charging_ev_data.ev_template.data.min_current:
                        common.set_current_counterdiff(-preferenced_chargepoints[0].data.set.current,
                                                       0,
                                                       preferenced_chargepoints[0])
                        preferenced_chargepoints[0].set_state_and_log(
                            f"Ladung kann nicht gestartet werden{limit.value.format(counter.num)}")
                    else:
                        common.set_current_counterdiff(available_for_cp-preferenced_chargepoints[0].data.set.current,
                                                       available_for_cp,
                                                       preferenced_chargepoints[0])
                    preferenced_chargepoints.pop(0)
