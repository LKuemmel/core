import logging
from typing import Iterable, List, Optional, Tuple

from control import data
from control.chargemode import Chargemode
from control.chargepoint import Chargepoint
from control.counter import Counter
from modules.common.component_type import ComponentType

log = logging.getLogger(__name__)

# Lademodi in absteigender Priorität
# Tupel-Inhalt:(eingestellter Modus, tatsächlich genutzter Modus, Priorität)
CHARGEMODES = ((Chargemode.SCHEDULED_CHARGING, Chargemode.INSTANT_CHARGING, True),
               (Chargemode.SCHEDULED_CHARGING, Chargemode.INSTANT_CHARGING, False),
               (None, Chargemode.TIME_CHARGING, True),
               (None, Chargemode.TIME_CHARGING, False),
               (Chargemode.INSTANT_CHARGING, Chargemode.INSTANT_CHARGING, True),
               (Chargemode.INSTANT_CHARGING, Chargemode.INSTANT_CHARGING, False),
               (Chargemode.PV_CHARGING, Chargemode.INSTANT_CHARGING, True),
               (Chargemode.PV_CHARGING, Chargemode.INSTANT_CHARGING, False),
               (Chargemode.SCHEDULED_CHARGING, Chargemode.PV_CHARGING, True),
               (Chargemode.SCHEDULED_CHARGING, Chargemode.PV_CHARGING, False),
               (Chargemode.PV_CHARGING, Chargemode.PV_CHARGING, True),
               (Chargemode.PV_CHARGING, Chargemode.PV_CHARGING, False),
               (None, Chargemode.STANDBY, True),
               (None, Chargemode.STANDBY, False),
               (None, Chargemode.STOP, True),
               (None, Chargemode.STOP, False))

# tested


def reset_current():
    for cp in data.data.cp_data.values():
        try:
            cp.data.set.current = 0
        except Exception:
            log.exception(f"Fehler im Algorithmus-Modul für Ladepunkt{cp.num}")


def mode_and_counter_generator(mode_range: List[int] = [0, -1]) -> Iterable[Tuple[Tuple[Optional[str], str, bool], Counter]]:
    for mode_tuple in CHARGEMODES[mode_range[0]: mode_range[1]]:
        levels = data.data.counter_all_data.get_list_of_elements_per_level()
        for level in reversed(levels):
            for element in level:
                if element["type"] == ComponentType.COUNTER.value:
                    counter = data.data.counter_data[f"counter{element['id']}"]
                    yield mode_tuple, counter

# tested


def get_min_current(chargepoint: Chargepoint) -> Tuple[List[float], List[int]]:
    min_currents = [0.0]*3
    counts = [0]*3
    charging_ev_data = chargepoint.data.set.charging_ev_data
    required_currents = charging_ev_data.data.control_parameter.required_currents
    for i in range(3):
        if required_currents[i] != 0:
            counts[i] += 1
            min_currents[i] = charging_ev_data.ev_template.data.min_current
        else:
            min_currents[i] = 0
    return min_currents, counts

# tested


def set_current_counterdiff(diff: float, current: float, chargepoint: Chargepoint) -> None:
    required_currents = chargepoint.data.set.charging_ev_data.data.control_parameter.required_currents
    diffs = [diff if required_currents[i] != 0 else 0 for i in range(3)]
    if max(diffs) > 0:
        counters = data.data.counter_all_data.get_counters_to_check(chargepoint.num)
        for counter in counters:
            data.data.counter_data[counter].update_values_left(diffs)

        chargepoint.data.set.current = current
        log.debug(f"LP{chargepoint.num}: Stromstärke {current}A")

# tested


def get_current_to_set(set_current: float, diff: float, prev_current: float) -> float:
    new_current = prev_current + diff
    if new_current > set_current and set_current != prev_current:
        log.debug("Neuer Sollstrom darf nicht höher als bisher gesetzter sein: "
                  f"bisher {set_current}A, neuer {new_current}")
        return set_current
    else:
        return new_current

# tested


def available_current_for_cp(chargepoint: Chargepoint,
                             counts: List[int],
                             available_currents: List[float]) -> float:
    charging_ev_data = chargepoint.data.set.charging_ev_data
    required_currents = charging_ev_data.data.control_parameter.required_currents

    counts_cp = [1 if required_currents[i] != 0 else 0 for i in range(3)]
    available_current = float("inf")
    for i in range(0, 3):
        if counts_cp[i] != 0:
            available_current = min(available_current, available_currents[i]/counts[i])
    return available_current


def update_raw_data(preferenced_chargepoints: List[Chargepoint]) -> None:
    """alle CP, die schon einen Sollstrom haben, wieder rausrechnen, da dieser neu gesetzt wird
        und die neue Differenz bei den Zählern eingetragen wird."""
    for chargepoint in preferenced_chargepoints:
        charging_ev_data = chargepoint.data.set.charging_ev_data
        required_currents = charging_ev_data.data.control_parameter.required_currents

        if charging_ev_data.ev_template.data.min_current < chargepoint.data.set.current:
            diffs = [charging_ev_data.ev_template.data.min_current -
                     chargepoint.data.set.current if required_currents[i] != 0 else 0 for i in range(3)]
            counters = data.data.counter_all_data.get_counters_to_check(chargepoint.num)
            for counter in counters:
                data.data.counter_data[counter].update_values_left(diffs)

# tested


def get_missing_currents_left(preferenced_chargepoints: List[Chargepoint]) -> Tuple[List[float], List[int]]:
    missing_currents = [0.0]*3
    counts = [0]*3
    for chargepoint in preferenced_chargepoints:
        charging_ev_data = chargepoint.data.set.charging_ev_data
        required_currents = charging_ev_data.data.control_parameter.required_currents
        for i in range(0, 3):
            if required_currents[i] != 0:
                counts[i] += 1
                try:
                    missing_currents[i] += required_currents[i] - charging_ev_data.ev_template.data.min_current
                except KeyError:
                    missing_currents[i] += max(required_currents) - charging_ev_data.ev_template.data.min_current
            else:
                missing_currents[i] += 0
    return missing_currents, counts