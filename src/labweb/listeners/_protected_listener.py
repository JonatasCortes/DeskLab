from typing import Callable, Any
from src.labweb.entity_types import EventSensitiveEntity
from typing import Any, Callable


class ProtectedListener(EventSensitiveEntity):

    def __init__(self,
                 condition: Callable[..., Any] | list[Callable[..., Any]],
                 actions: Callable[..., Any] | list[Callable[..., Any]],
                 on_change: bool = False, listen_once: bool = False) -> None:
        self.__listen_once = listen_once
        self.__has_triggered = False
        self.__on_change = on_change
        self.__previous_state = None
        self._set_actions(actions)
        self._set_conditions(condition)

    def handle_event(self, *args: Any, **kwargs: Any) -> None:
        super().handle_event(*args, **kwargs)

        if self.__listen_once and self.__has_triggered:
            return

        condition_value = self._trigger_conditions(*args, **kwargs)
        should_trigger = False

        if self.__on_change and self.__previous_state is not None and condition_value != self.__previous_state:
            should_trigger = True
        elif condition_value:
            should_trigger = True

        self.__previous_state = condition_value

        if should_trigger:
            self._trigger_actions(*args, **kwargs)
            if self.__listen_once:
                self.__has_triggered = True

    def _get_conditions(self) -> list[Callable[..., Any]]:
        return self.__conditions

    def _set_conditions(self, conditions: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        if isinstance(conditions, Callable):
            conditions = [conditions]
        self.__conditions = conditions

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

    def _trigger_conditions(self, *args: Any, **kwargs: Any) -> bool:
        for condition in self._get_conditions():
            try:
                result = condition(*args, **kwargs)
            except TypeError:
                result = condition()
            if not result:
                return False
        return True

    def _trigger_actions(self, *args: Any, **kwargs: Any) -> None:
        for action in self._get_actions():
            try:
                action(*args, **kwargs)
            except TypeError:
                return action()
