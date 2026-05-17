from src.labweb.entities.dimensionable import DimensionableEntity
from src.labweb.entities.positionable import PositionableEntity
from typing import Any


class ContainableEntity(PositionableEntity, DimensionableEntity):

    def __init__(self, x: int = 0, y: int = 0, width: int = 0, height: int = 0, **kwargs: Any):
        super().__init__(x=x, y=y, width=width, height=height, **kwargs)

    def set_x(self, x: int) -> None: return self._set_x(x)
    def set_y(self, y: int) -> None: return self._set_y(y)
