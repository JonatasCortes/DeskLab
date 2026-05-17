from src.labweb.system.mouse import Mouse
from src.labweb.primitives.color import Color
from src.labweb.areas.interface import AreaInterface
from typing import Any
from src.labweb.listeners.protected_change import ProtectedChangeListener


class HoverColorListener(ProtectedChangeListener):

    def __init__(self, area: AreaInterface, hover_color: Color | tuple[int, int, int] | str) -> None:
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
