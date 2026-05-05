from typing import Any
from src.labweb.constants import FlexDirection, HorizontalAlignment, VerticalAlignment
from src.labweb.containers.hover_emphasizing_flexbox import HoverEmphasizingFlexBox
from src.labweb.color import Color
from pygame.event import Event
from labweb.system_input.mouse import Mouse


class ClickableFlexBox(HoverEmphasizingFlexBox):

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

        super().__init__(width, height, padding,
                         space_between, flex_direction,
                         horizontal_alignment,
                         vertical_alignment,
                         corners_radius, color,
                         hover_emphasis_intensity, bounded)
        self.__is_clicked = False
        self.set_color(color)

    def __add_click_listener(self, mouse: Mouse):
        if mouse.is_clicked() and self.contains(mouse.get_position()):
            self.__is_clicked = True
            return
        self.__is_clicked = False

    def is_clicked(self) -> bool:
        return self.__is_clicked

    def handle_event(self, event: Event, *args: Any, **kwargs: Any) -> None:
        mouse = kwargs.get("mouse")
        if not isinstance(mouse, Mouse):
            error = "Expected a Mouse instance in kwargs with key 'mouse'"
            raise ValueError(error)
        self.__add_click_listener(mouse)
        super().handle_event(event, *args, **kwargs)

    def copy(self) -> "ClickableFlexBox":
        instance = self._copy()
        assert isinstance(instance, self.__class__)
        return instance
