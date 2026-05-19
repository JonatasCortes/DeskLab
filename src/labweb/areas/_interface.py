from src.labweb.entity_types import ContainableEntity, DisplayableEntity, CopiableEntity, ColorableEntity
from src.labweb._primitives import Color


class Area(ContainableEntity, DisplayableEntity, ColorableEntity, CopiableEntity):

    def __init__(self, width: int, height: int, color: Color | tuple[int, ...] | str = "BLACK") -> None:
        super().__init__(x=0, y=0, width=width, height=height, color=color)

    def contains(self, coordinates: tuple[int, int]) -> bool:
        error = "ERROR: contains method must be implemented by subclasses"
        raise NotImplementedError(error)

    def get_rect(self) -> tuple[int, int, int, int]:
        return (self.get_x(), self.get_y(),
                self.get_width(), self.get_height())
