from src.labweb.entities import EventSensitiveEntity
from typing import Any, Callable


class EventListener(EventSensitiveEntity):

    def __init__(self, condition: Callable[..., bool], actions: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        self.set_actions(actions)
        self.set_condition(condition)

    def handle_event(self, *args: Any, **kwargs: Any) -> None:
        super().handle_event(*args, **kwargs)
        if self._trigger_condition(*args, **kwargs):
            self._trigger_actions(*args, **kwargs)

    def get_condition(self) -> Callable[..., bool]:
        return self.__condition

    def set_condition(self, condition: Callable[..., bool]) -> None:
        self.__condition = condition

    def get_actions(self) -> list[Callable[..., Any]]:
        return self.__action

    def set_actions(self, action: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        if isinstance(action, list):
            self.__action = action
            return
        self.__action: list[Callable[..., Any]] = [action]

    def _trigger_condition(self, *args: Any, **kwargs: Any) -> bool:
        condition = self.get_condition()
        try:
            return condition(*args, **kwargs)
        except TypeError:
            return condition()

    def _trigger_actions(self, *args: Any, **kwargs: Any) -> None:
        for action in self.get_actions():
            try:
                action(*args, **kwargs)
            except TypeError:
                return action()


class FirstTimeEventListener(EventListener):

    def __init__(self, condition: Callable[..., bool], actions: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        self.__has_triggered = False
        super().__init__(condition, actions)

    def handle_event(self, *args: Any, **kwargs: Any) -> None:
        super().handle_event(*args, **kwargs)
        if not self.__has_triggered and self._trigger_condition():
            self._trigger_actions()
            self.__has_triggered = True


class ChangeEventListener(EventListener):

    def __init__(self, condition: Callable[..., bool], actions: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        self.__previous_state = None
        super().__init__(condition, actions)

    def handle_event(self, *args: Any, **kwargs: Any) -> None:
        super().handle_event(*args, **kwargs)
        condition_value = self._trigger_condition()
        if self.__previous_state is not None and condition_value != self.__previous_state:
            self._trigger_actions()

        self.__previous_state = condition_value
