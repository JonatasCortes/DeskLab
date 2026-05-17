from typing import Callable, Any
from src.labweb.system.mouse import Mouse
from src.labweb.areas.interface import AreaInterface
from src.labweb.listeners.protected_interface import ProtectedListener


class _MouseListener(ProtectedListener):

    def __init__(self, area: AreaInterface, actions: Callable[..., Any] | list[Callable[..., Any]], condition_func: str) -> None:
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


class MouseClickListener(_MouseListener):
    def __init__(self, area: AreaInterface, actions: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        super().__init__(area, actions, "is_clicked")


class MouseHoldListener(_MouseListener):
    def __init__(self, area: AreaInterface, actions: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        super().__init__(area, actions, "is_held")
