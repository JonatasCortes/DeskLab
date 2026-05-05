from src.labweb.entities import EventSensitiveEntity
from pygame.event import Event
from typing import Any, Callable


class EventListener(EventSensitiveEntity):

    def __init__(self, condition: Callable[..., bool], actions: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        self.set_actions(actions)
        self.set_condition(condition)

    def handle_event(self, event: Event, *args: Any, **kwargs: Any) -> None:
        if self._trigger_condition(*args, **kwargs, event=event):
            self._trigger_actions(*args, **kwargs, event=event)

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

    def handle_event(self, event: Event, *args: Any, **kwargs: Any) -> None:
        if not self.__has_triggered and self._trigger_condition():
            self._trigger_actions()
            self.__has_triggered = True
