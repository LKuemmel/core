from enum import Enum

import requests


class FemsVersion(Enum):
    ONE_SEGMENT_REGEX_QUERY = 0
    MULTIPLE_SEGMENT_REGEX_QUERY = 1


def get_version(multiple_segement_regex_query_func):
    try:
        multiple_segement_regex_query_func()
        return FemsVersion.MULTIPLE_SEGMENT_REGEX_QUERY
    # FEMS, die Regex-Abfragen über mehrere Segmente unterstützen, dürfen nicht zu häufig abgefragt werden.
    # Alle Werte müssen auf einmal abgefragt werden.
    except requests.exceptions.HTTPError:
        return FemsVersion.ONE_SEGMENT_REGEX_QUERY
