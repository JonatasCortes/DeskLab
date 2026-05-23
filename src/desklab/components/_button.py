from typing import Any, Callable
from desklab.containers import (FlexDirection, HorizontalAlignment,
                                VerticalAlignment, FlexBox)
from desklab.areas import ClickableArea
from desklab.primitives import Color


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

    def _get_copy_replacement_map(self) -> dict[str, Any]:
        replace = super()._get_copy_replacement_map()
        replace["actions"] = self.get_actions()
        return replace
