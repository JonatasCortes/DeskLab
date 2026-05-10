from src.labweb.color import Color
from src.labweb.constants import VerticalAlignment, HorizontalAlignment, FlexDirection
from src.labweb.containers.protected_flexbox import ProtectedFlexBox
from src.labweb.area import HoverEmphasizingArea


class HoverEmphasizingFlexBox(ProtectedFlexBox, HoverEmphasizingArea):

    def __init__(self,
                 width: int,
                 height: int,
                 padding: int = 0,
                 space_between: int = 0,
                 flex_direction: str | FlexDirection = FlexDirection.COLUMN,
                 horizontal_alignment: str | HorizontalAlignment = HorizontalAlignment.CENTER,
                 vertical_alignment: str | VerticalAlignment = VerticalAlignment.CENTER,
                 corners_radius: tuple[int, int, int, int] | int = 0,
                 color: Color | tuple[int, int, int] | str = "BLACK",
                 hover_emphasis_intensity: int = 100,
                 bounded: bool = True) -> None:
        super().__init__(width=width,
                         height=height,
                         padding=padding,
                         space_between=space_between,
                         flex_direction=flex_direction,
                         horizontal_alignment=horizontal_alignment,
                         vertical_alignment=vertical_alignment,
                         corners_radius=corners_radius,
                         color=color,
                         hover_emphasis_intensity=hover_emphasis_intensity,
                         bounded=bounded)

    def copy(self) -> "HoverEmphasizingFlexBox":
        new_instance = self.__class__(self.get_width(), self.get_height(),
                                      self._get_padding(), self._get_space_between(),
                                      self._get_flex_direction(), self._get_horizontal_alignment(),
                                      self._get_vertical_alignment(), self.get_corners_radius(),
                                      self.get_color(), self.get_emphasis_intensity(), self._is_bounded())
        self._migrate_children(new_instance)
        return new_instance
