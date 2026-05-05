from pygame.event import Event
from src.labweb.color import Color
from typing import Any, Union
from src.labweb.constants import VerticalAlignment, HorizontalAlignment, FlexDirection
from src.labweb.system_input.mouse import Mouse
from src.labweb.containers.flexbox import FlexBox


class HoverEmphasizingFlexBox(FlexBox):

    def __init__(self,
                 width: int,
                 height: int,
                 padding: int = 0,
                 space_between: int = 0,
                 flex_direction: str | FlexDirection = FlexDirection.COLUMN,
                 horizontal_alignment: str | HorizontalAlignment = HorizontalAlignment.CENTER,
                 vertical_alignment: str | VerticalAlignment = VerticalAlignment.CENTER,
                 corners_radius: tuple[int, int, int, int] | int = 0,
                 color: Union[Color, tuple[int, int, int], str] = "BLACK",
                 hover_emphasis_intensity: int = 100,
                 bounded: bool = True) -> None:
        self.set_color(color)
        self.__hover_emphasis_intensity = self._ensure_not_negative(
            hover_emphasis_intensity)
        super().__init__(width, height, padding, space_between, flex_direction,
                         horizontal_alignment, vertical_alignment, corners_radius,
                         color, bounded)

    def __add_hover_listener(self, mouse_pos: tuple[int, int]) -> None:

        hovered = self.contains(mouse_pos)
        color = self.get_color()

        if hovered:
            color = color.luminance_emphasized(
                self.__hover_emphasis_intensity)

        super().set_color(color)

    def handle_event(self, event: Event, *args: Any, **kwargs: Any) -> None:
        mouse = kwargs.get("mouse")
        if not isinstance(mouse, Mouse):
            error = "Expected a Mouse instance in kwargs with key 'mouse'"
            raise ValueError(error)
        self.__add_hover_listener(mouse.get_position())
        return super().handle_event(event, *args, **kwargs)

    def set_color(self, color: Color | tuple[int, ...] | str):
        if not isinstance(color, Color):
            color = Color(color)
        self.__default_background_color = color
        return super().set_color(color)

    def get_color(self) -> Color:
        return self.__default_background_color.copy()

    def get_emphasis_intensity(self) -> int:
        return self.__hover_emphasis_intensity

    def copy(self) -> "HoverEmphasizingFlexBox":
        new_instance = self.__class__(self.get_width(), self.get_height(),
                                      self.get_padding(), self.get_space_between(),
                                      self.get_flex_direction(), self.get_horizontal_alignment(),
                                      self.get_vertical_alignment(), self.get_corners_radius(),
                                      self.get_color(), self.get_emphasis_intensity(), self.is_bounded())
        self._migrate_children(new_instance)
        return new_instance
