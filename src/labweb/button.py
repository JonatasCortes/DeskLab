from typing import Any, Callable
from src.labweb.constants import FlexDirection, HorizontalAlignment, VerticalAlignment
from src.labweb.containers.clickable_hover_emphasizing_flexbox import ClickableHoverEmphasizingFlexBox
from src.labweb.containers.flexbox import FlexBox
from src.labweb.color import Color


class Button(ClickableHoverEmphasizingFlexBox, FlexBox):

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
                 hover_emphasis_intensity: int = 100,
                 bounded: bool = True) -> None:

        super().__init__(width, height, padding,
                         space_between, flex_direction,
                         horizontal_alignment, vertical_alignment,
                         corners_radius, color,
                         hover_emphasis_intensity, bounded)
        self.__actions: list[Callable[..., Any]] = []
        self.add_actions(actions)

    def __add_click_listener(self):
        if self.is_clicked():
            for action in self.get_actions():
                action()

    def add_actions(self, action: Callable[..., Any] | list[Callable[..., Any]]):
        if isinstance(action, list):
            self.__actions = [*self.__actions, *action]
            return
        self.__actions.append(action)

    def get_actions(self) -> list[Callable[..., Any]]:
        return self.__actions

    def handle_event(self, *args: Any, **kwargs: Any) -> None:
        super().handle_event(*args, **kwargs)
        self.__add_click_listener()

    def copy(self) -> "Button":
        new_instance = self.__class__(self.get_width(), self.get_height(), self.get_actions(),
                                      self.get_padding(), self.get_space_between(),
                                      self.get_flex_direction(), self.get_horizontal_alignment(),
                                      self.get_vertical_alignment(), self.get_corners_radius(),
                                      self.get_color(), self.get_emphasis_intensity(), self.is_bounded())
        self._migrate_children(new_instance)
        return new_instance
