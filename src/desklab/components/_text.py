# fmt: off
from desklab.areas import ClickableArea
from desklab.primitives import Color, Font
from typing import Any, Optional, Self
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import Surface
# fmt: on


class Text(ClickableArea):

    __MAX_WIDTH_DEFAULT_VALUE = 150000
    __MAX_HEIGHT_DEFAULT_VALUE = 2000

    def __init__(self,
                 text: str,
                 font: Optional[Font] = None,
                 color: Color | tuple[int, ...] | str = "BLACK"):

        self.__text = text
        self.set_font(font)

        super().__init__(self.get_width(), self.get_height(), color, 0)

    def __add__(self, other: str | Self):
        if isinstance(other, Text):
            other = other.get_text()
        return self.copy(text=self.get_text() + other)

    def __sub__(self, other: str | Self):
        if isinstance(other, Text):
            other = other.get_text()
        raw_text = self.get_text()
        text = raw_text.replace(other, "")
        return self.copy(text=text)

    def __len__(self):
        return len(self.get_text())

    def __bool__(self):
        return not self.is_empty()

    def __getitem__(self, key: int | slice):
        return self.copy(text=self.get_text()[key])

    def get_text(self) -> str: return self.__text
    def __fix_x(self, x: int) -> int: return x + self.get_width()//2
    def __fix_y(self, y: int) -> int: return y + self.get_height()//2
    def set_x(self, x: int) -> None: super().set_x(self.__fix_x(x))
    def set_y(self, y: int) -> None: super().set_y(self.__fix_y(y))
    def is_empty(self) -> bool: return self.get_text() == ""
    def get_font(self) -> Font: return self.__font

    def set_font(self, font: Optional[Font] = None):
        self.__font = font if font else Font()
        self.__update_dimensions()

    def set_text(self, text: str) -> None:
        self.__text = text
        self.__update_dimensions()

    def __update_dimensions(self) -> None:
        new_width, new__height = self.__font.measure_text(self.__text)
        self._set_width(new_width)
        self._set_height(new__height)

    def contains(self, coordinates: tuple[int, int]) -> bool:
        x, y = coordinates
        half_width = self.get_width()//2
        half_height = self.get_height()//2
        within_horizontal_bounds = self.get_x() - half_width <= x <= self.get_x() + half_width
        within_vertical_bounds = self.get_y() - half_height <= y <= self.get_y() + half_height
        return within_horizontal_bounds and within_vertical_bounds

    def fitted_within(self, max_width: Optional[int] = None, max_height: Optional[int] = None) -> Self:
        if max_width is None and max_height is None:
            error = "'maximize' expects at least one of the following parameters: max_width, max_height"
            raise ValueError(error)
        if max_width is None:
            max_width = self.__MAX_WIDTH_DEFAULT_VALUE
        if max_height is None:
            max_height = self.__MAX_HEIGHT_DEFAULT_VALUE

        low = Font.MIN_FONT_SIZE
        high = Font.MAX_FONT_SIZE
        font: Optional[Font] = None

        while low <= high:
            mid = (low + high) // 2

            font = self.get_font().copy(replace_size=mid)
            width, height = font.measure_text(self.__text)

            if width <= max_width and height <= max_height:
                low = mid + 1
            else:
                high = mid - 1

        return self.copy(replace_font=font)

    def display(self, screen: Surface) -> None:
        text_surface = self.__font.render(self.__text, self.get_color_tuple())
        text_rect = text_surface.get_rect(center=(self.get_x(), self.get_y()))
        screen.blit(text_surface, text_rect)

    def _get_copy_replacement_map(self) -> dict[str, Any]:
        return {
            "text": self.get_text(),
            "font": self.get_font(),
            "color": self.get_color()
        }

    def sub(self, start: int | None = None, end: int | None = None) -> Self:
        return self.copy(text=self.get_text()[start:end])
