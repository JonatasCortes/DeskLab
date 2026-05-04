from typing import Any, Callable
from src.labweb.constants import FlexDirection, HorizontalAlignment, VerticalAlignment
from src.labweb.containers.hover_emphasizing_flexbox import HoverEmphasizingFlexBox
from src.labweb.color import Color
from pygame.event import Event
from src.labweb.mouse import Mouse
from src.labweb.entities import CopiableEntity


class ClickableFlexBox(HoverEmphasizingFlexBox):

    def __init__(self,
                 width: int,
                 height: int,
                 actions: Callable[..., Any] | list[Callable[..., Any]] = [],
                 padding: int = 0,
                 space_between: int = 0,
                 flex_direction: str | FlexDirection = FlexDirection.COLUMN,
                 horizontal_alignment: str | HorizontalAlignment = HorizontalAlignment.CENTER,
                 vertical_alignment: str | VerticalAlignment = VerticalAlignment.CENTER,
                 corners_radius: tuple[int, int, int, int] | int = 0,
                 color: Color | tuple[int, int, int] | str = "BLACK",
                 bounded: bool = True) -> None:

        super().__init__(width, height, padding,
                         space_between, flex_direction,
                         horizontal_alignment, vertical_alignment,
                         corners_radius, color, 100, bounded)
        self.__actions: list[Callable[..., Any]] = []
        self.add_actions(actions)
        self.set_color(color)

    def __add_click_listener(self, mouse: Mouse):
        if mouse.is_clicked() and self.contains(mouse.get_position()):
            for action in self.get_actions():
                action()

    def add_actions(self, action: Callable[..., Any] | list[Callable[..., Any]]):
        if isinstance(action, list):
            self.__actions = [*self.__actions, *action]
            return
        self.__actions.append(action)

    def get_actions(self) -> list[Callable[..., Any]]:
        return self.__actions

    def handle_event(self, event: Event, *args: Any, **kwargs: Any) -> None:
        mouse = kwargs.get("mouse")
        if not isinstance(mouse, Mouse):
            error = "Expected a Mouse instance in kwargs with key 'mouse'"
            raise ValueError(error)
        self.__add_click_listener(mouse)
        super().handle_event(event, *args, **kwargs)

    def copy(self) -> "ClickableFlexBox":
        new_instance = self.__class__(self.get_width(), self.get_height(), self.get_actions(),
                                      self.get_padding(), self.get_space_between(),
                                      self.get_flex_direction(), self.get_horizontal_alignment(),
                                      self.get_vertical_alignment(), self.get_corners_radius(),
                                      self.get_color(), self.is_bounded())
        for children in self._get_children():
            if isinstance(children, CopiableEntity):
                new_instance._add(children.copy())
            else:
                new_instance._add(children)
        return new_instance
