from src.labweb.entities.entity import Entity
from src.labweb.primitives.color import Color
from typing import Any


class ColorableEntity(Entity):

    def __init__(self, color: Color | tuple[int, ...] | str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._set_color(color)

    def _set_color(self, color: Color | tuple[int, ...] | str):
        if isinstance(color, Color):
            self.__color = color
        else:
            self.__color = Color(color)

    def get_color(self) -> Color:
        return self.__color.copy()

    def get_color_tuple(self) -> tuple[int, ...]:
        return self.__color.get_tuple()

    def color_is(self, color: Color | tuple[int, ...] | str) -> bool:
        color = color if isinstance(color, Color) else Color(color)
        return self.get_color() == color
