from typing import Any
from ._rectangular_area import RectangularArea
from src.desklab.entity_types import EventSensitiveEntity
from src.desklab._primitives import Color
from src.desklab.system import Mouse


class ClickableArea(RectangularArea, EventSensitiveEntity):

    def __init__(self, width: int, height: int, color: Color | tuple[int, ...] | str = "BLACK", corners_radius: tuple[int, int, int, int] | int = 0) -> None:
        super().__init__(width, height, color, corners_radius)
        self.__is_clicked = False
        self.__is_held = False

    def is_clicked(self) -> bool:
        return self.__is_clicked

    def is_held(self) -> bool:
        return self.__is_held

    def handle_event(self, *args: Any, **kwargs: Any) -> None:
        super().handle_event(*args, **kwargs)
        mouse = kwargs.get("mouse")
        if not isinstance(mouse, Mouse):
            self._raise_for_missing_parameter("mouse", Mouse.__name__)

        inside = self.contains(mouse.get_position())

        self.__is_clicked = mouse.is_clicked() and inside
        self.__is_held = mouse.is_held() and inside
