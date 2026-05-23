# fmt: off
from desklab._utils import is_inside_circle
from ._interface import Area
from desklab.primitives import Color
from typing import Any
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame import Surface
# fmt: on


class RectangularArea(Area):

    def __init__(self,
                 width: int,
                 height: int,
                 color: Color | tuple[int, ...] | str = "BLACK",
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
        rect_x, rect_y, rect_width, rect_height = self.get_rect()
        radius_top_left, radius_top_right, radius_bottom_left, radius_bottom_right = self.get_corners_radius()

        corners_geometry_map = [
            (radius_top_left, rect_x + radius_top_left,
             rect_y + radius_top_left, True, True),  # Top-Left
            (radius_top_right, rect_x + rect_width - radius_top_right,
             rect_y + radius_top_right, False, True),  # Top-Right
            (radius_bottom_left, rect_x + radius_bottom_left, rect_y +
             rect_height - radius_bottom_left, True,  False),  # Bottom-Left
            (radius_bottom_right, rect_x + rect_width - radius_bottom_right,
             rect_y + rect_height - radius_bottom_right, False, False)  # Bottom-Right
        ]

        for corner_radius, arc_center_x, arc_center_y, check_left, check_top in corners_geometry_map:
            if corner_radius <= 0:
                continue

            if self.__is_point_inside_corner_bounding_box(coordinates, arc_center_x, arc_center_y, check_left, check_top):
                if not is_inside_circle(coordinates, (arc_center_x, arc_center_y), corner_radius):
                    return True

        return False

    def __is_point_inside_corner_bounding_box(self, coordinates: tuple[int, int], arc_center_x: int, arc_center_y: int, check_left: bool, check_top: bool) -> bool:
        point_x, point_y = coordinates
        is_within_horizontal_boundary = point_x < arc_center_x if check_left else point_x > arc_center_x
        is_within_vertical_boundary = point_y < arc_center_y if check_top else point_y > arc_center_y
        return is_within_horizontal_boundary and is_within_vertical_boundary

    def display(self, screen: Surface) -> None:
        corners = self.get_corners_radius()
        pygame.draw.rect(screen,
                         self.get_color_tuple(),
                         self.get_rect(),
                         border_top_left_radius=corners[0],
                         border_top_right_radius=corners[1],
                         border_bottom_left_radius=corners[2],
                         border_bottom_right_radius=corners[3])

    def _get_copy_replacement_map(self) -> dict[str, Any]:
        return {
            "width": self.get_width(),
            "height": self.get_height(),
            "color": self.get_color(),
            "corners_radius": self.get_corners_radius()
        }
