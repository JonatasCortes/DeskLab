from typing import Callable, Any
from src.labweb.system.mouse import Mouse
from src.labweb.properties.color import Color
from src.labweb.entities import EventSensitiveEntity
from src.labweb.area import Area
from typing import Any, Callable


class _ProtectedEventListener(EventSensitiveEntity):

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


class EventListener(_ProtectedEventListener):

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


class _ProtectedFirstTimeEventListener(_ProtectedEventListener):

    def __init__(self, condition: Callable[..., bool], actions: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        self.__has_triggered = False
        super().__init__(condition, actions)

    def handle_event(self, *args: Any, **kwargs: Any) -> None:
        if not self.__has_triggered and self._trigger_condition(*args, **kwargs):
            self._trigger_actions(*args, **kwargs)
            self.__has_triggered = True


class FirstTimeEventListener(_ProtectedFirstTimeEventListener, EventListener):
    pass


class _ProtectedChangeEventListener(_ProtectedEventListener):

    def __init__(self, condition: Callable[..., bool], actions: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        self.__previous_state = None
        super().__init__(condition, actions)

    def handle_event(self, *args: Any, **kwargs: Any) -> None:
        condition_value = self._trigger_condition(*args, **kwargs)
        if self.__previous_state is not None and condition_value != self.__previous_state:
            self._trigger_actions(*args, **kwargs)

        self.__previous_state = condition_value


class ChangeEventListener(_ProtectedChangeEventListener, EventListener):
    pass


class HoverColorEventListener(_ProtectedChangeEventListener):

    def __init__(self, area: Area, hover_color: Color | tuple[int, int, int] | str) -> None:
        self.__area = area
        self.__default_color = area.get_color()
        self.__hover_color = hover_color
        super().__init__(self.__area_contains_mouse_position, self.__change_area_color)

    def __area_contains_mouse_position(self, *args: Any, **kwargs: Any) -> bool:
        mouse = kwargs.get("mouse")
        if not isinstance(mouse, Mouse):
            self._raise_for_missing_parameter("mouse", Mouse.__name__)
        return self.__area.contains(mouse.get_position())

    def __change_area_color(self) -> None:
        if self.__area.get_color() == self.__default_color:
            self.__area.set_color(self.__hover_color)
            return
        self.__area.set_color(self.__default_color)


class _MouseEventListener(_ProtectedEventListener):

    def __init__(self, area: Area, actions: Callable[..., Any] | list[Callable[..., Any]], condition_func: str) -> None:
        self.__area = area
        super().__init__(lambda *args, **
                         kwargs: self.__check_mouse_condition(condition_func, **kwargs), actions)

    def __check_mouse_condition(self, condition_func: str, **kwargs: Any) -> bool:
        mouse = kwargs.get("mouse")
        if not isinstance(mouse, Mouse):
            self._raise_for_missing_parameter("mouse", Mouse.__name__)

        mouse_condition = getattr(mouse, condition_func)()
        return mouse_condition and self.__area.contains(mouse.get_position())

    def get_actions(self) -> list[Callable[..., Any]]:
        return self._get_actions()

    def set_actions(self, actions: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        return self._set_actions(actions)

    def add_actions(self, actions: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        return self._add_actions(actions)


class MouseClickEventListener(_MouseEventListener):
    def __init__(self, area: Area, actions: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        super().__init__(area, actions, "is_clicked")


class MouseHoldEventListener(_MouseEventListener):
    def __init__(self, area: Area, actions: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        super().__init__(area, actions, "is_held")
