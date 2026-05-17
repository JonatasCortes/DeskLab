from src.labweb.listeners.protected_interface import ProtectedListener
from typing import Callable, Any
from typing import Any, Callable


class Listener(ProtectedListener):

    def get_condition(self) -> Callable[..., bool]:
        return self._get_condition()

    def set_condition(self, condition: Callable[..., bool]) -> None:
        return self._set_condition(condition)

    def get_actions(self) -> list[Callable[..., Any]]:
        return self._get_actions()

    def set_actions(self, actions: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        return self._set_actions(actions)

    def add_actions(self, actions: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        self._add_actions(actions)
