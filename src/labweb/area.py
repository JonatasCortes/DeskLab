from typing import Any

from src.labweb.system.mouse import Mouse
from src.labweb.color import Color
from src.labweb.entities import ContainableEntity, DisplayableEntity, ColorableEntity, CopiableEntity, EventSensitiveEntity
from src.labweb.utils import is_inside_circle
from pygame import Surface
import pygame


class Area(ContainableEntity, DisplayableEntity, ColorableEntity, CopiableEntity):

    def __init__(self, width: int, height: int, color: Color | tuple[int, int, int] | str = "BLACK") -> None:
        super().__init__(x=0, y=0, width=width, height=height, color=color)

    def contains(self, coordinates: tuple[int, int]) -> bool:
        error = "ERROR: contains method must be implemented by subclasses"
        raise NotImplementedError(error)

    def get_rect(self) -> tuple[int, int, int, int]:
        return (self.get_x(), self.get_y(),
                self.get_width(), self.get_height())

    def set_color(self, color: Color | tuple[int, ...] | str) -> None:
        self._set_color(color)


class RectangularArea(Area):

    def __init__(self,
                 width: int,
                 height: int,
                 color: Color | tuple[int, int, int] | str = "BLACK",
                 corners_radius: tuple[int, int, int, int] | int = 0) -> None:
        super().__init__(width, height, color)
        self.set_corners_radius(corners_radius)

    def set_corners_radius(self, corners_radius: tuple[int, int, int, int] | int) -> None:
        if isinstance(corners_radius, int):
            corners = (corners_radius, ) * 4
        else:
            corners = corners_radius

        if any(c < 0 for c in corners):
            error = "corners_radius only accepts positive values"
            raise ValueError(error)

        if len(corners) != 4:
            error = "corners_radius must have exactly four (4) positive integers."
            raise ValueError()

        self.__set_corners_radius(corners)

    def __set_corners_radius(self, corners: tuple[int, ...]) -> None:
        self.__corners_radius = corners

    def get_corners_radius(self) -> tuple[int, int, int, int]:
        assert len(self.__corners_radius) == 4
        return self.__corners_radius

    def contains(self, coordinates: tuple[int, int]) -> bool:
        x, y = coordinates
        self_x, self_y, self_w, self_h = self.get_rect()
        if not (self_x <= x <= self_x + self_w and
                self_y <= y <= self_y + self_h):
            return False
        return not self.__exceeds_corners(coordinates)

    def __exceeds_corners(self, coordinates: tuple[int, int]) -> bool:
        x, y = coordinates
        rx, ry, w, h = self.get_rect()
        r_tl, r_tr, r_bl, r_br = self.get_corners_radius()

        # top-left
        if r_tl > 0 and x < rx + r_tl and y < ry + r_tl:
            if not is_inside_circle((x, y), (rx + r_tl, ry + r_tl), r_tl):
                return True

        # top-right
        if r_tr > 0 and x > rx + w - r_tr and y < ry + r_tr:
            if not is_inside_circle((x, y), (rx + w - r_tr, ry + r_tr), r_tr):
                return True

        # bottom-left
        if r_bl > 0 and x < rx + r_bl and y > ry + h - r_bl:
            if not is_inside_circle((x, y), (rx + r_bl, ry + h - r_bl), r_bl):
                return True

        # bottom-right
        if r_br > 0 and x > rx + w - r_br and y > ry + h - r_br:
            if not is_inside_circle((x, y), (rx + w - r_br, ry + h - r_br), r_br):
                return True

        return False

    def display(self, screen: Surface) -> None:
        corners = self.get_corners_radius()
        pygame.draw.rect(screen,
                         self.get_color_tuple(),
                         self.get_rect(),
                         border_top_left_radius=corners[0],
                         border_top_right_radius=corners[1],
                         border_bottom_left_radius=corners[2],
                         border_bottom_right_radius=corners[3])

    def copy(self) -> "RectangularArea":
        return self.__class__(self.get_width(), self.get_height(),
                              self.get_color(), self.get_corners_radius())


class ClickableArea(RectangularArea, EventSensitiveEntity):

    def __init__(self, width: int, height: int, color: Color | tuple[int, int, int] | str = "BLACK", corners_radius: tuple[int, int, int, int] | int = 0) -> None:
        super().__init__(width, height, color, corners_radius)
        self.__is_clicked = False
        self.__is_held = False

    def is_clicked(self) -> bool:
        return self.__is_clicked

    def is_held(self) -> bool:
        return self.__is_held

    def handle_event(self, *args: Any, **kwargs: Any) -> None:
        super().handle_event(*args, **kwargs)
        mouse = kwargs.get("mouse")
        if not isinstance(mouse, Mouse):
            self._raise_for_missing_parameter("mouse", Mouse.__name__)

        inside = self.contains(mouse.get_position())

        self.__is_clicked = mouse.is_clicked() and inside
        self.__is_held = mouse.is_held() and inside

    def copy(self) -> "ClickableArea":
        return self.__class__(
            self.get_width(),
            self.get_height(),
            self.get_color(),
            self.get_corners_radius()
        )


class HoverEmphasizingArea(RectangularArea, EventSensitiveEntity):

    def __init__(self,
                 width: int,
                 height: int,
                 color: Color | tuple[int, int, int] | str = "BLACK",
                 corners_radius: tuple[int, int, int, int] | int = 0,
                 hover_emphasis_intensity: int = 100) -> None:
        self.set_color(color)
        self.__hover_emphasis_intensity = self._ensure_not_negative(
            hover_emphasis_intensity)
        super().__init__(width, height, color, corners_radius)

    def __add_hover_listener(self, mouse_pos: tuple[int, int]) -> None:

        hovered = self.contains(mouse_pos)
        color = self.get_color()

        if hovered:
            color = color.luminance_emphasized(
                self.__hover_emphasis_intensity)

        super().set_color(color)

    def handle_event(self, *args: Any, **kwargs: Any) -> None:
        super().handle_event(*args, **kwargs)
        mouse = kwargs.get("mouse")
        if not isinstance(mouse, Mouse):
            self._raise_for_missing_parameter("mouse", Mouse.__name__)
        self.__add_hover_listener(mouse.get_position())

    def set_color(self, color: Color | tuple[int, ...] | str):
        if not isinstance(color, Color):
            color = Color(color)
        self.__default_background_color = color
        return super().set_color(color)

    def get_color(self) -> Color:
        return self.__default_background_color.copy()

    def get_emphasis_intensity(self) -> int:
        return self.__hover_emphasis_intensity

    def copy(self) -> "HoverEmphasizingArea":
        new_instance = self.__class__(self.get_width(),
                                      self.get_height(),
                                      self.get_color(),
                                      self.get_corners_radius(),
                                      self.get_emphasis_intensity())
        return new_instance
