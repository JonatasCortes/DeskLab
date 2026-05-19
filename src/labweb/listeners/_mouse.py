from typing import Callable, Any
from src.labweb.system import Mouse
from src.labweb.areas import Area
from ._protected_interface import ProtectedListener


class _MouseListener(ProtectedListener):

    _condition_function: str = ""

    def __init__(self, area: Area, actions: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        self.__area = area
        super().__init__(self.__check_mouse_condition, actions)

    def __check_mouse_condition(self, **kwargs: Any) -> bool:
        mouse = kwargs.get("mouse")
        if not isinstance(mouse, Mouse):
            self._raise_for_missing_parameter("mouse", Mouse.__name__)

        mouse_condition = getattr(mouse, self._condition_function)()
        return mouse_condition and self.__area.contains(mouse.get_position())

    def get_actions(self) -> list[Callable[..., Any]]:
        return self._get_actions()

    def set_actions(self, actions: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        return self._set_actions(actions)

    def add_actions(self, actions: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        return self._add_actions(actions)


class MouseClickListener(_MouseListener):
    _condition_function = "is_clicked"


class MouseHoldListener(_MouseListener):
    _condition_function = "is_held"


class MouseReleaseListener(_MouseListener):
    _condition_function = "is_released"


class MouseMotionListener(_MouseListener):
    _condition_function = "is_moving"


class FileDropListener(_MouseListener):
    _condition_function = "is_dropping_file"
