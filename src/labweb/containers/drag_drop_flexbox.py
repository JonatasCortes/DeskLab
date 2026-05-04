from src.labweb.containers.hover_emphasizing_flexbox import HoverEmphasizingFlexBox
from src.labweb.mouse import Mouse
from pygame.event import Event
from typing import Any
from src.labweb.constants import FlexDirection, HorizontalAlignment, VerticalAlignment
from src.labweb.color import Color
from src.labweb.entities import CopiableEntity


class DragDropFlexBox(HoverEmphasizingFlexBox):

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
                 bounded: bool = True) -> None:

        self.__files: list[str] = []
        super().__init__(width, height, padding, space_between, flex_direction,
                         horizontal_alignment, vertical_alignment, corners_radius,
                         color, 20, bounded)

    def handle_event(self, event: Event, *args: Any, **kwargs: Any) -> None:
        mouse = kwargs.get("mouse")
        if not isinstance(mouse, Mouse):
            error = "Expected a Mouse instance in kwargs with key 'mouse'"
            raise ValueError(error)
        self.__add_file_drop_listener(event, mouse)
        return super().handle_event(event, *args, **kwargs)

    def __add_file_drop_listener(self, event: Event, mouse: Mouse) -> None:
        if mouse.is_dropping_file() and self.contains(mouse.get_position()):
            file_path = event.file
            self.__files.append(file_path)

    def get_files(self) -> list[str]:
        return self.__files.copy()

    def pop_file(self) -> str:
        if not self.__files:
            raise IndexError("No files to pop")
        return self.__files.pop()

    def clear_files(self) -> None:
        self.__files.clear()

    def has_files(self) -> bool:
        return len(self.__files) > 0

    def count_files(self) -> int:
        return len(self.__files)

    def copy(self) -> "DragDropFlexBox":
        new_instance = self.__class__(self.get_width(), self.get_height(), self.get_padding(),
                                      self.get_space_between(), self.get_flex_direction(),
                                      self.get_horizontal_alignment(), self.get_vertical_alignment(),
                                      self.get_corners_radius(), self.get_color(), self.is_bounded())
        for children in self._get_children():
            if isinstance(children, CopiableEntity):
                new_instance._add(children.copy())
            else:
                new_instance._add(children)
        return new_instance
