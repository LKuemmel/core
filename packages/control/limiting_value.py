from enum import Enum


class LimitingValue(Enum):
    CURRENT = ", da der Maximal-Strom an Zähler {} erreicht ist."
    POWER = ", da die maximale Leistung an Zähler {} erreicht ist."
    UNBALANCED_LOAD = ", da die maximale Schieflast an Zähler {} erreicht ist."
    DIMMING_VIA_DIRECT_CONTROL = ", da die Dimmung per Direkt-Steuerung an Zähler {} erreicht ist."
