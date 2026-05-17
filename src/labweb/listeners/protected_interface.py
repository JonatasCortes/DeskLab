from typing import Callable, Any
from src.labweb.entities.event_sensitive import EventSensitiveEntity
from typing import Any, Callable


class ProtectedListener(EventSensitiveEntity):

    def __init__(self, condition: Callable[..., bool], actions: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        self._set_actions(actions)
        self._set_condition(condition)

    def handle_event(self, *args: Any, **kwargs: Any) -> None:
        if self._trigger_condition(*args, **kwargs):
            self._trigger_actions(*args, **kwargs)

    def _get_condition(self) -> Callable[..., bool]:
        return self.__condition

    def _set_condition(self, condition: Callable[..., bool]) -> None:
        self.__condition = condition

    def _get_actions(self) -> list[Callable[..., Any]]:
        return self.__actions

    def _set_actions(self, actions: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        if isinstance(actions, list):
            self.__actions = actions
            return
        self.__actions: list[Callable[..., Any]] = [actions]

    def _add_actions(self, actions: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        if isinstance(actions, Callable):
            self.__actions.append(actions)
            return
        self.__actions.extend(actions)

    def _trigger_condition(self, *args: Any, **kwargs: Any) -> bool:
        condition = self._get_condition()
        try:
            return condition(*args, **kwargs)
        except TypeError:
            return condition()

    def _trigger_actions(self, *args: Any, **kwargs: Any) -> None:
        for action in self._get_actions():
            try:
                action(*args, **kwargs)
            except TypeError:
                return action()
