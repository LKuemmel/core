import logging
from typing import List, Optional

from control.algorithm import common
from control.loadmanagement import LimitingValue, Loadmanagement
from control.counter import Counter
from control.chargepoint import Chargepoint
from control.algorithm.filter_chargepoints import get_chargepoints_by_mode_and_counter, get_preferenced_chargepoint_with_set_current_and_charging
from modules.common.utils.component_parser import get_component_name_by_id

log = logging.getLogger(__name__)


class AdditionalCurrent:
    def __init__(self) -> None:
        pass

    def set_additional_current(self, mode_range: List[int]) -> None:
        for mode_tuple, counter in common.mode_and_counter_generator(mode_range):
            preferenced_chargepoints = get_preferenced_chargepoint_with_set_current_and_charging(
                get_chargepoints_by_mode_and_counter(mode_tuple, f"counter{counter.num}"))
            if preferenced_chargepoints:
                common.update_raw_data(preferenced_chargepoints)
                log.debug(f"Mode-Tuple {mode_tuple}, Zähler {counter.num}")
                chargepoints = len(preferenced_chargepoints)
                for i in range(chargepoints):
                    missing_currents, counts = common.get_missing_currents_left(preferenced_chargepoints)
                    available_currents, limit = Loadmanagement().get_available_currents(missing_currents, counter)
                    available_for_cp = common.available_current_for_cp(
                        preferenced_chargepoints[-1], counts, available_currents)
                    current = common.get_current_to_set(
                        preferenced_chargepoints[-1].data.set.current, available_for_cp, preferenced_chargepoints[-1].data.set.target_current)
                    self._set_loadmangement_message(current, limit, preferenced_chargepoints[-1], counter)
                    common.set_current_counterdiff(
                        current - preferenced_chargepoints[-1].data.set.charging_ev_data.ev_template.data.min_current,
                        current,
                        preferenced_chargepoints[-1])
                    preferenced_chargepoints.pop(-1)

    # tested
    def _set_loadmangement_message(self,
                                   current: float,
                                   limit: Optional[LimitingValue],
                                   chargepoint: Chargepoint,
                                   counter: Counter) -> None:
        # Strom muss an diesem Zähler geändert werden
        if (current != chargepoint.data.set.current and
                # Strom erreicht nicht die vorgegebene Stromstärke
                chargepoint.data.set.current != max(chargepoint.data.set.charging_ev_data.data.control_parameter.required_currents)):
            chargepoint.set_state_and_log(
                f"Es kann nicht mit der vorgegebenen Stromstärke geladen werden{limit.value.format(get_component_name_by_id(counter.num))}")
