from src.labweb.listeners.protected_interface import ProtectedListener
from typing import Callable, Any
from typing import Any, Callable


class ProtectedChangeListener(ProtectedListener):

    def __init__(self, condition: Callable[..., bool], actions: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        self.__previous_state = None
        super().__init__(condition, actions)

    def handle_event(self, *args: Any, **kwargs: Any) -> None:
        condition_value = self._trigger_condition(*args, **kwargs)
        if self.__previous_state is not None and condition_value != self.__previous_state:
            self._trigger_actions(*args, **kwargs)

        self.__previous_state = condition_value
