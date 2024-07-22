import logging
import operator
from typing import List, Optional, Tuple

from control import data
from control.counter import Counter
from control.limiting_value import LimitingValue


log = logging.getLogger(__name__)


class Loadmanagement:
    def get_available_currents(self,
                               missing_currents: List[float],
                               counter: Counter,
                               max_power_dynamic_loadsharing: Optional[float],
                               feed_in: int = 0) -> Tuple[List[float], Optional[LimitingValue]]:
        raw_currents_left = counter.data.set.raw_currents_left
        available_currents, limit = self._limit_by_current(missing_currents, raw_currents_left)
        available_currents, limit_power = self._limit_by_power(
            available_currents, counter.data.set.raw_power_left, feed_in)
        if limit_power is not None:
            limit = limit_power
        if f"counter{counter.num}" == data.data.counter_all_data.get_evu_counter_str():
            available_currents, limit_unbalanced_load = self._limit_by_unbalanced_load(
                counter, available_currents, raw_currents_left)
            if limit_unbalanced_load is not None:
                limit = limit_unbalanced_load
        available_currents, limit_dynamic_loadsharing = self._limit_by_dynamic_loadsharing(
            counter, available_currents, max_power_dynamic_loadsharing)
        if limit_dynamic_loadsharing is not None:
            limit = limit_dynamic_loadsharing
        return available_currents, limit

    def get_available_currents_surplus(self,
                                       missing_currents: List[float],
                                       counter: Counter,
                                       max_power_dynamic_loadsharing: Optional[float],
                                       feed_in: int = 0) -> Tuple[List[float], Optional[LimitingValue]]:
        raw_currents_left = counter.data.set.raw_currents_left
        available_currents, limit = self._limit_by_current(missing_currents, raw_currents_left)
        available_currents, limit_power = self._limit_by_power(
            available_currents, counter.data.set.surplus_power_left, feed_in)
        if limit_power is not None:
            limit = limit_power
        if f"counter{counter.num}" == data.data.counter_all_data.get_evu_counter_str():
            available_currents, limit_unbalanced_load = self._limit_by_unbalanced_load(
                counter, available_currents, raw_currents_left)
            if limit_unbalanced_load is not None:
                limit = limit_unbalanced_load
        available_currents, limit_dynamic_loadsharing = self._limit_by_dynamic_loadsharing(
            counter, available_currents, max_power_dynamic_loadsharing)
        if limit_dynamic_loadsharing is not None:
            limit = limit_dynamic_loadsharing
        return available_currents, limit

    def _limit_by_unbalanced_load(self,
                                  counter: Counter,
                                  available_currents: List[float],
                                  raw_currents_left: List[float]) -> Tuple[List[float], Optional[LimitingValue]]:
        raw_currents_left_charging = list(map(operator.sub, raw_currents_left, available_currents))
        max_exceeding = counter.get_unbalanced_load_exceeding(raw_currents_left_charging)
        limit = None
        if max(max_exceeding) > 0:
            available_currents = list(map(operator.sub, available_currents, max_exceeding))
            log.debug(f"Schieflast {max_exceeding}A korrigieren: {available_currents}")
            limit = LimitingValue.UNBALANCED_LOAD
        return available_currents, limit

    # tested
    def _limit_by_power(self,
                        available_currents: List[float],
                        raw_power_left: Optional[float],
                        feed_in: Optional[float]) -> Tuple[List[float], Optional[LimitingValue]]:
        currents = available_currents.copy()
        limit = None
        if raw_power_left:
            if feed_in:
                raw_power_left = raw_power_left - feed_in
                log.debug(f"Verbleibende Leistung unter Berücksichtigung der Einspeisegrenze: {raw_power_left}W")
            if sum(available_currents)*230 > raw_power_left:
                for i in range(0, 3):
                    # Am meisten belastete Phase trägt am meisten zur Leistungsreduktion bei.
                    currents[i] = available_currents[i] / sum(available_currents) * raw_power_left / 230
                log.debug(f"Leistungsüberschreitung auf {raw_power_left}W korrigieren: {available_currents}")
                limit = LimitingValue.POWER
        return currents, limit

    # tested
    def _limit_by_current(self,
                          missing_currents: List[float],
                          raw_currents_left: List[float]) -> Tuple[List[float], Optional[LimitingValue]]:
        available_currents = [0.0]*3
        limit = None
        for i in range(0, 3):
            available_currents[i] = min(missing_currents[i], raw_currents_left[i])
        if available_currents != missing_currents:
            log.debug(f"Stromüberschreitung {missing_currents}W korrigieren: {available_currents}")
            limit = LimitingValue.CURRENT
        return available_currents, limit

    def _limit_by_dynamic_loadsharing(self,
                                      available_currents: List[float],
                                      max_power_dynamic_loadsharing: Optional[float]
                                      ) -> Tuple[List[float], Optional[LimitingValue]]:
        currents = available_currents.copy()
        limit = None
        if max_power_dynamic_loadsharing:
            log.debug("Verbleibende Leistung unter Berücksichtigung der dynamischen Lastverteilung: "
                      f"{max_power_dynamic_loadsharing}W")
            if sum(available_currents)*230 > max_power_dynamic_loadsharing:
                for i in range(0, 3):
                    # Am meisten belastete Phase trägt am meisten zur Leistungsreduktion bei.
                    currents[i] = available_currents[i] / sum(available_currents) * max_power_dynamic_loadsharing / 230
                log.debug(
                    f"Leistungsüberschreitung auf {max_power_dynamic_loadsharing}W korrigieren: {available_currents}")
                limit = LimitingValue.POWER
        return currents, limit
