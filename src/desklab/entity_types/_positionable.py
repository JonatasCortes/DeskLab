from ._entity import Entity
from typing import Any


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
