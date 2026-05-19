# fmt: off
from src.labweb._primitives import Color
from typing import Any
from src.labweb.system import Mouse
from src.labweb.containers import FlexBox, FlexDirection, HorizontalAlignment, VerticalAlignment
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame.event import Event
# fmt: on


class DragDrop(FlexBox):

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
                         color, bounded)

    def handle_event(self, *args: Any, **kwargs: Any) -> None:
        super().handle_event(*args, **kwargs)
        mouse = kwargs.get("mouse")
        event = kwargs.get("event")
        if not isinstance(mouse, Mouse):
            self._raise_for_missing_parameter("mouse", Mouse.__name__)
        if event:
            self.__add_file_drop_listener(event, mouse)

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
