from src.labweb.entities.entity import Entity
from typing import Any


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
