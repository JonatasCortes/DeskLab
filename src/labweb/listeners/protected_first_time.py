from src.labweb.listeners.protected_interface import ProtectedListener
from typing import Callable, Any
from typing import Any, Callable


class ProtectedFirstTimeListener(ProtectedListener):

    def __init__(self, condition: Callable[..., bool], actions: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        self.__has_triggered = False
        super().__init__(condition, actions)

    def handle_event(self, *args: Any, **kwargs: Any) -> None:
        if not self.__has_triggered and self._trigger_condition(*args, **kwargs):
            self._trigger_actions(*args, **kwargs)
            self.__has_triggered = True
