from typing import Any, Self
from src.labweb.system.mouse import Mouse
from src.labweb.primitives.color import Color
from src.labweb.areas.rectangular_area import RectangularArea
from src.labweb.entities.event_sensitive import EventSensitiveEntity
from pygame import Surface
import pygame
from enum import Enum
import math


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
        self._set_canvas(width, height)
        self.__last_mouse_pos: tuple[int, int] | None = None
        self.__current_mouse_pos: tuple[int, int] = (0, 0)
        self.__drawing_mode = _DrawingMode.DRAWING
        self.__execution_state = _ExecutionState.PAUSED

    def _set_canvas(self, width: int = 0, height: int = 0) -> None:
        self.__canvas = Surface((width, height), pygame.SRCALPHA)
        self.__canvas.fill((0, 0, 0, 0))

    def _put_canvas(self, canvas: Surface) -> None:
        self.__canvas.blit(canvas, (0, 0))

    def clear(self):
        self.__canvas.fill((0, 0, 0, 0))
        self.__last_mouse_pos = None

    def fill(self):
        self.__drawing_mode = _DrawingMode.FILLING

    def is_filling(self) -> bool:
        return self.__drawing_mode == _DrawingMode.FILLING

    def erase(self):
        self.__drawing_mode = _DrawingMode.ERASING

    def is_erasing(self) -> bool:
        return self.__drawing_mode == _DrawingMode.ERASING

    def draw(self):
        self.__drawing_mode = _DrawingMode.DRAWING

    def is_drawing(self) -> bool:
        return self.__drawing_mode == _DrawingMode.DRAWING

    def __unpause(self):
        self.__execution_state = _ExecutionState.RUNNING

    def __pause(self):
        self.__execution_state = _ExecutionState.PAUSED
        self.__last_mouse_pos = None

    def is_paused(self) -> bool:
        return self.__execution_state == _ExecutionState.PAUSED

    def __update_execution_state(self, mouse: Mouse) -> None:
        if self.is_paused() and mouse.is_clicked() and self.contains(self.__current_mouse_pos):
            self.__unpause()
        elif mouse.is_released() or not self.contains(self.__current_mouse_pos):
            self.__pause()

    def copy(self) -> Self:
        new_instance = self.__class__(self.get_width(), self.get_height(),
                                      self.get_corners_radius(),
                                      self.get_color(), self.get_brush_color(),
                                      self.get_brush_width(), self.get_eraser_width())
        new_instance._put_canvas(self.__canvas)
        return new_instance

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

    def handle_event(self, *args: Any, **kwargs: Any) -> None:
        super().handle_event(*args, **kwargs)
        mouse = kwargs.get("mouse")

        if not isinstance(mouse, Mouse):
            self._raise_for_missing_parameter("mouse", Mouse.__name__)

        self.__current_mouse_pos = mouse.get_position()

        self.__update_execution_state(mouse)

        if self.is_paused():
            return

        local_pos = (self.__current_mouse_pos[0] - self.get_x(),
                     self.__current_mouse_pos[1] - self.get_y())

        if self.is_drawing():
            self.__draw_to_canvas(local_pos, self.get_brush_color().get_tuple(),
                                  self.get_brush_width())
        elif self.is_erasing():
            self.__draw_to_canvas(local_pos, (0, 0, 0, 0),
                                  self.get_eraser_width())
        elif self.is_filling():
            if mouse.is_clicked():
                self.__canvas.fill(self.get_brush_color().get_tuple())

        self.__last_mouse_pos = local_pos

    def __draw_to_canvas(self, current_pos: tuple[int, int], color: tuple[int, ...], width: int):
        start_pos = self.__last_mouse_pos if self.__last_mouse_pos is not None else current_pos

        radius = max(1, width // 2)

        pygame.draw.circle(self.__canvas, color, start_pos, radius)
        pygame.draw.circle(self.__canvas, color, current_pos, radius)

        if start_pos == current_pos:
            return
        edges = self.__calculate_polygon_edges(current_pos, start_pos, radius)
        pygame.draw.polygon(self.__canvas, color, edges)

    def __calculate_polygon_edges(self, current_pos: tuple[int, ...], start_pos: tuple[int, ...], radius: int) -> tuple[tuple[float, ...], ...]:
        delta_x = current_pos[0] - start_pos[0]
        delta_y = current_pos[1] - start_pos[1]
        angle = math.atan2(delta_y, delta_x)

        perpendicular_angle = angle + math.pi / 2

        offset_x = radius * math.cos(perpendicular_angle)
        offset_y = radius * math.sin(perpendicular_angle)

        e1 = (start_pos[0] + offset_x, start_pos[1] + offset_y)
        e2 = (start_pos[0] - offset_x, start_pos[1] - offset_y)
        e3 = (current_pos[0] - offset_x, current_pos[1] - offset_y)
        e4 = (current_pos[0] + offset_x, current_pos[1] + offset_y)
        return (e1, e2, e3, e4)

    def __draw_cursor(self, screen: Surface, mouse_pos: tuple[int, int]):
        if not self.contains(mouse_pos):
            return
        if self.is_erasing():
            pygame.draw.circle(screen, self.get_color().luminance_emphasized().get_tuple(),
                               mouse_pos, self.get_eraser_width() // 2, 1)
        elif self.is_drawing():
            pygame.draw.circle(screen, self.get_brush_color().get_tuple(), mouse_pos,
                               self.get_brush_width() // 2)

    def display(self, screen: Surface) -> None:
        super().display(screen)
        clipping_mask = pygame.Rect(self.get_rect())
        previous_mask = screen.get_clip()
        screen.set_clip(clipping_mask)
        screen.blit(self.__canvas, (self.get_x(), self.get_y()))
        self.__draw_cursor(screen, self.__current_mouse_pos)
        screen.set_clip(previous_mask)
