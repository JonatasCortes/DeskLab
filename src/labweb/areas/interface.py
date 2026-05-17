from src.labweb.entities.colorable import ColorableEntity
from src.labweb.entities.containable import ContainableEntity
from src.labweb.entities.copiable import CopiableEntity
from src.labweb.entities.displayable import DisplayableEntity
from src.labweb.primitives.color import Color


class AreaInterface(ContainableEntity, DisplayableEntity, ColorableEntity, CopiableEntity):

    def __init__(self, width: int, height: int, color: Color | tuple[int, int, int] | str = "BLACK") -> None:
        super().__init__(x=0, y=0, width=width, height=height, color=color)

    def contains(self, coordinates: tuple[int, int]) -> bool:
        error = "ERROR: contains method must be implemented by subclasses"
        raise NotImplementedError(error)

    def get_rect(self) -> tuple[int, int, int, int]:
        return (self.get_x(), self.get_y(),
                self.get_width(), self.get_height())

    def set_color(self, color: Color | tuple[int, ...] | str) -> None:
        self._set_color(color)
