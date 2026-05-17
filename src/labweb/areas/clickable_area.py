from typing import Any
from src.labweb.areas.rectangular_area import RectangularArea
from src.labweb.entities.event_sensitive import EventSensitiveEntity
from src.labweb.primitives.color import Color
from src.labweb.system.mouse import Mouse


class ClickableArea(RectangularArea, EventSensitiveEntity):

    def __init__(self, width: int, height: int, color: Color | tuple[int, int, int] | str = "BLACK", corners_radius: tuple[int, int, int, int] | int = 0) -> None:
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
