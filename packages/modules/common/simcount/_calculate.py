import logging
from typing import Union, Tuple


Number = Union[int, float]


def calculate_import_export(time_since_previous: Number, power1: Number, power2: Number) -> Tuple[float, float]:
    power_low = min(power1, power2)
    power_high = max(power1, power2)
    gradient = (power_high - power_low) / time_since_previous
    # Berechnung der Gesamtfläche (ohne Beträge, Fläche unterhalb der x-Achse reduziert die Fläche oberhalb der
    # x-Achse)
    def energy_function(seconds): return .5 * gradient * seconds ** 2 + power_low * seconds

    energy_total = energy_function(time_since_previous)
    if power_low < 0 < power_high:
        # Berechnung der Fläche im vierten Quadranten -> Export
        power_zero_seconds = -power_low / gradient
        energy_exported = energy_function(power_zero_seconds)
        # Betragsmäßige Gesamtfläche: oberhalb der x-Achse = Import, unterhalb der x-Achse: Export
        return energy_total - energy_exported, energy_exported * -1
    return (energy_total, 0) if energy_total >= 0 else (0, -energy_total)
