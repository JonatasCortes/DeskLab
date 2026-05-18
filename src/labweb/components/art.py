from typing import Any
from src.labweb.system.mouse import Mouse
from src.labweb.primitives.color import Color
from src.labweb.areas.rectangular_area import RectangularArea
from src.labweb.entities.event_sensitive import EventSensitiveEntity
from pygame import Surface
import pygame
from src.labweb.utils import point_to_segment_distance
from enum import Enum


class _DrawingMode(Enum):
    DRAWING = 1
    ERASING = 2
    FILLING = 3


class _ExecutionState(Enum):
    PAUSED = 0
    RUNNING = 1


class DrawingArea(RectangularArea, EventSensitiveEntity):

    def __init__(self,
                 width: int,
                 height: int,
                 corners_radius: tuple[int, int, int, int] | int = 0,
                 background_color: Color | tuple[int,
                                                 int, int] | str = "WHITE",
                 brush_color: Color | tuple[int, int, int] | str = "BLACK",
                 brush_width: int = 10,
                 eraser_width: int = 10) -> None:

        super().__init__(width, height, background_color, corners_radius)
        self.set_brush_color(brush_color)
        self.set_brush_width(brush_width)
        self.set_eraser_width(eraser_width)
        self.__mouse_positions: list[tuple[int, int]] = []
        self.__drawn_chunks: list[tuple[Color, list[tuple[int, int]]]] = []
        self.__drawing_mode = _DrawingMode.DRAWING
        self.__execution_state = _ExecutionState.PAUSED

    def clear(self):
        self.__mouse_positions = []
        self.__drawn_chunks = []

    def fill(self):
        self.__drawing_mode = _DrawingMode.FILLING

    def is_filling(self) -> bool:
        return self.__drawing_mode == _DrawingMode.FILLING

    def erase(self):
        self.__drawing_mode = _DrawingMode.ERASING

    def is_erasing(self) -> bool:
        return self.__drawing_mode == _DrawingMode.ERASING

    def is_paused(self) -> bool:
        return self.__execution_state == _ExecutionState.PAUSED

    def draw(self):
        self.__drawing_mode = _DrawingMode.DRAWING

    def is_drawing(self) -> bool:
        return self.__drawing_mode == _DrawingMode.DRAWING

    def copy(self) -> "DrawingArea":
        return self.__class__(self.get_width(), self.get_height(),
                              self.get_corners_radius(),
                              self.get_color(), self.get_brush_color(),
                              self.get_brush_width(), self.get_eraser_width())

    def __pause(self):
        self.__execution_state = _ExecutionState.PAUSED

    def __unpause(self):
        self.__execution_state = _ExecutionState.RUNNING

    def set_brush_width(self, width: int):
        self.__brush_width = self._ensure_not_negative(width)

    def set_eraser_width(self, width: int):
        self.__eraser_width = self._ensure_not_negative(width)

    def set_brush_color(self, color: Color | tuple[int, int, int] | str = "BLACK"):
        if isinstance(color, Color):
            self.__brush_color = color
            return
        self.__brush_color = Color(color)

    def get_brush_width(self) -> int:
        return self.__brush_width

    def get_eraser_width(self) -> int:
        return self.__eraser_width

    def get_brush_color(self) -> Color:
        return self.__brush_color

    def get_drawing_state(self) -> _DrawingMode:
        return self.__drawing_mode

    def handle_event(self, *args: Any, **kwargs: Any) -> None:
        super().handle_event(*args, **kwargs)
        mouse = kwargs.get("mouse")

        if not isinstance(mouse, Mouse):
            self._raise_for_missing_parameter("mouse", Mouse.__name__)

        self.__current_mouse_pos = mouse.get_position()
        self.__add_drawing_listener(mouse)
        self.__add_erasing_listener(mouse)
        self.__add_filling_listener(mouse)

    def __draw_cursor(self, screen: Surface, mouse_pos: tuple[int, int]):
        if not self.contains(mouse_pos):
            return
        if self.is_erasing():
            pygame.draw.circle(screen, self.get_color().luminance_emphasized().get_tuple(),
                               mouse_pos, self.get_eraser_width()//2)
        elif self.is_drawing():
            pygame.draw.circle(screen, self.get_brush_color().get_tuple(), mouse_pos,
                               self.get_brush_width()//2)

    def __update_drawing_state_based_on_mouse_behavior(self, mouse: Mouse):
        if self.is_paused() and mouse.is_clicked() and self.contains(mouse.get_position()):
            self.__unpause()
        elif mouse.is_released() or not self.contains(mouse.get_position()):
            self.__pause()

    def __add_drawing_listener(self, mouse: Mouse):

        self.__update_drawing_state_based_on_mouse_behavior(mouse)

        if self.is_drawing() and not self.is_paused():
            self.__mouse_positions.append(mouse.get_position())
        elif self.__mouse_positions:
            self.__drawn_chunks.append((self.__brush_color,
                                        self.__mouse_positions))
            self.__mouse_positions = []

    def __add_erasing_listener(self, mouse: Mouse):

        self.__update_drawing_state_based_on_mouse_behavior(mouse)
        if not self.is_erasing() or self.is_paused():
            return

        new_chunks: list[tuple[Color, list[tuple[int, int]]]] = []

        for brush_color, chunk in self.__drawn_chunks:

            split_index = None

            for i in range(len(chunk) - 1):
                p1 = chunk[i]
                p2 = chunk[i + 1]

                dist = point_to_segment_distance(mouse.get_position(), p1, p2)

                eraser_width = self.get_eraser_width()
                if eraser_width > 0 and dist - self.get_brush_width()//2 <= eraser_width // 2:
                    split_index = i
                    break

            if split_index is None:
                new_chunks.append((brush_color, chunk))
                continue

            left = chunk[:split_index + 1]
            right = chunk[split_index + 1:]

            if len(left) >= 2:
                new_chunks.append((brush_color, left))

            if len(right) >= 2:
                new_chunks.append((brush_color, right))

        self.__drawn_chunks = new_chunks

    def __add_filling_listener(self, mouse: Mouse):
        if self.is_filling() and mouse.is_clicked() and self.contains(mouse.get_position()):
            self.__fill()

    def __fill(self):
        self.clear()
        self.set_color(self.get_brush_color())

    def __draw(self, screen: Surface):
        if not self.__drawn_chunks and not self.__mouse_positions:
            return
        drawing_chunks = []
        if self.__drawn_chunks:
            drawing_chunks = self.__drawn_chunks
        if self.__mouse_positions:
            drawing_chunks = [*drawing_chunks, (self.__brush_color,
                                                self.__mouse_positions)]

        for brush_color, chunk in drawing_chunks:
            previous = chunk[0]
            for position in chunk[1:]:
                pygame.draw.line(screen, brush_color.get_tuple(),
                                 previous, position,
                                 width=self.get_brush_width())
                pygame.draw.circle(screen, brush_color.get_tuple(),
                                   previous, (self.get_brush_width()//2)-1)
                previous = position

    def display(self, screen: Surface) -> None:
        super().display(screen)

        clipping_mask = pygame.Rect(self.get_rect())

        previous_mask = screen.get_clip()
        screen.set_clip(clipping_mask)

        self.__draw(screen)
        self.__draw_cursor(screen, self.__current_mouse_pos)

        screen.set_clip(previous_mask)
