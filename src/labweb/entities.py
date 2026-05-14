from src.labweb.color import Color
from abc import ABC, abstractmethod
from pygame import Surface
from typing import Any


class Entity(ABC):
    pass


class EventSensitiveEntity(Entity):
    @abstractmethod
    def handle_event(self, *args: Any, **kwargs: Any) -> None:
        pass

    def _raise_for_missing_parameter(self, parameter_key: str, parameter_class_name: str):
        error = f"Expected a {parameter_class_name} instance in kwargs with key '{parameter_key}'"
        raise RuntimeError(error)


class DisplayableEntity(Entity):
    @abstractmethod
    def display(self, screen: Surface) -> None:
        error = f"ERROR: 'display' can't be called directly from {self.__class__.__name__}"
        raise NotImplementedError(error)


class CopiableEntity(Entity):

    @abstractmethod
    def copy(self) -> "CopiableEntity":
        error = f"ERROR: 'copy' can't be called directly from {self.__class__.__name__}"
        raise NotImplementedError(error)


class PositionableEntity(Entity):

    def __init__(self, x: int = 0, y: int = 0, **kwargs: Any):
        super().__init__(**kwargs)
        self._set_x(x)
        self._set_y(y)

    def _set_x(self, x: int):
        self.__x = x

    def get_x(self) -> int:
        return self.__x

    def _set_y(self, y: int):
        self.__y = y

    def get_y(self) -> int:
        return self.__y


class DimensionableEntity(Entity):

    def __init__(self, width: int = 0, height: int = 0, **kwargs: Any):
        super().__init__(**kwargs)
        self._set_width(width)
        self._set_height(height)

    def _ensure_not_negative(self, pos: int):
        return pos if pos >= 0 else 0

    def _set_width(self, width: int):
        self.__width = self._ensure_not_negative(width)

    def get_width(self) -> int:
        return self.__width

    def _set_height(self, height: int):
        self.__height = self._ensure_not_negative(height)

    def get_height(self) -> int:
        return self.__height


class ContainableEntity(PositionableEntity, DimensionableEntity):

    def __init__(self, x: int = 0, y: int = 0, width: int = 0, height: int = 0, **kwargs: Any):
        super().__init__(x=x, y=y, width=width, height=height, **kwargs)

    def set_x(self, x: int) -> None: return self._set_x(x)
    def set_y(self, y: int) -> None: return self._set_y(y)


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
