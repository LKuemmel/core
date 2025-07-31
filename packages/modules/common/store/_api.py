import logging
from abc import abstractmethod
from typing import Generic, TypeVar

from modules.common.component_context import SingleComponentUpdateContext

T = TypeVar("T")


class ValueStore(Generic[T]):
    @abstractmethod
    def set(self, state: T) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass


class LoggingValueStore(Generic[T], ValueStore[T]):
    def __init__(self, delegate: ValueStore[T]):
        self.delegate = delegate

    def set(self, state: T) -> None:
        self.delegate.set(state)

    def update(self) -> None:
        try:
            self.delegate.update()
        except AttributeError:
            # Wenn keine Daten ausgelesen werden, fehlt das state-Attribut.
            pass
        except Exception:
            pass


def update_values(component):
    with SingleComponentUpdateContext(component.fault_state, update_always=False):
        if hasattr(component, "store"):
            try:
                component.store.update()
            except AttributeError:
                # Wenn keine Daten ausgelesen werden, fehlt das state-Attribut. Die eigentliche Fehlermeldung würde
                # dann durch die Attribute-Error-Meldung überschrieben werden.
                pass
