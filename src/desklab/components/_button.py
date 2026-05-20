from typing import Any, Callable, Self
from src.desklab.containers import (FlexDirection, HorizontalAlignment,
                                    VerticalAlignment, FlexBox)
from src.desklab.areas import ClickableArea
from src.desklab._primitives import Color


class Button(FlexBox, ClickableArea):

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
                         corners_radius, color, bounded)
        self.__actions: list[Callable[..., Any]] = []
        self.add_actions(actions)

    def __add_click_listener(self):
        if self.is_clicked():
            for action in self.get_actions():
                action()

    def set_actions(self, actions: Callable[..., Any] | list[Callable[..., Any]]):
        if not isinstance(actions, list):
            actions = [actions]
        self.__actions = actions

    def add_actions(self, actions: Callable[..., Any] | list[Callable[..., Any]]):
        if isinstance(actions, Callable):
            actions = [actions]
        self.__actions.extend(actions)

    def get_actions(self) -> list[Callable[..., Any]]:
        return self.__actions.copy()

    def remove_actions(self, actions: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        if isinstance(actions, Callable):
            actions = [actions]
        for a in actions:
            self.__actions.remove(a)

    def handle_event(self, *args: Any, **kwargs: Any) -> None:
        super().handle_event(*args, **kwargs)
        self.__add_click_listener()

    def copy(self) -> Self:
        new_instance = self.__class__(self.get_width(), self.get_height(), self.get_actions(),
                                      self.get_padding(), self.get_space_between(),
                                      self.get_flex_direction(), self.get_horizontal_alignment(),
                                      self.get_vertical_alignment(), self.get_corners_radius(),
                                      self.get_color(), self.is_bounded())
        self._migrate_children(new_instance)
        return new_instance
