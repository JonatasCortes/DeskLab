from src.labweb.color import Color
from abc import ABC, abstractmethod
from pygame import Surface
from pygame.event import Event
from typing import Any


class Entity(ABC):
    pass


class EventSensitiveEntity(Entity):
    @abstractmethod
    def handle_event(self, event: Event, *args: Any, **kwargs: Any) -> None:
        error = f"ERROR: 'handle_event' can't be called directly from {self.__class__.__name__}"
        raise NotImplementedError(error)


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
        return self.__color.get()

    def color_is(self, color: Color | tuple[int, ...] | str) -> bool:
        color = color if isinstance(color, Color) else Color(color)
        return self.get_color() == color


class DefaultEntity(EventSensitiveEntity, DisplayableEntity, ContainableEntity, ColorableEntity, CopiableEntity):

    def __init__(self, x: int, y: int, width: int, height: int, color: Color | tuple[int, ...] | str) -> None:
        super().__init__(x=x, y=y, width=width, height=height, color=color)

    def set_x(self, x: int) -> None: return self._set_x(x)
    def set_y(self, y: int) -> None: return self._set_y(y)

    def set_color(self, color: Color | tuple[int, ...] | str):
        return self._set_color(color)
