# fmt: off
from src.desklab.areas import ClickableArea
from src.desklab._primitives import Color
from typing import Any, Optional, Self
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame import Surface
# fmt: on


class _FontMapper:

    __FONT_MAP: dict[str, list[str]] = {
        "times": ["timesnewroman", "times", "liberation serif", "georgia"],
        "georgia": ["georgia", "timesnewroman", "palatino"],
        "arial": ["arial", "helvetica", "liberation sans", "ubuntu", "roboto"],
        "verdana": ["verdana", "geneva", "dejavu sans"],
        "trebuchet": ["trebuchetms", "tahoma", "arial"],
        "tahoma": ["tahoma", "verdana", "geneva"],
        "helvetica": ["helvetica", "arial", "liberation sans"],
        "courier": ["couriernew", "courier", "liberation mono", "dejavu sans mono"],
        "consolas": ["consolas", "lucidaconsole", "monaco", "monospace"],
        "monospace": ["monospace", "dejavu sans mono", "couriernew"],
        "comic": ["comicsansms", "comic sans", "cursive"],
        "impact": ["impact", "charcoal", "helvetica inset"]
    }

    @classmethod
    def get_font_path(cls, font_name: str) -> str:

        clean_name = font_name.lower().strip()

        if clean_name in cls.__FONT_MAP:
            for fallback in cls.__FONT_MAP[clean_name]:
                path = pygame.font.match_font(fallback)
                if path:
                    return path

        path = pygame.font.match_font(clean_name)
        if path:
            return path

        error = (f"\nERROR: Font '{font_name}' not found."
                 f"\nChoose one of the availuable options or include the fonte file path."
                 f"\nAvailuable font options are: {cls.get_available_fonts()}.\n")
        raise ValueError(error)

    @classmethod
    def get_available_fonts(cls) -> list[str]:
        return list(cls.__FONT_MAP.keys())


class Text(ClickableArea):

    def __init__(self, text: str, size: int = 25, color: Color | tuple[int, ...] | str = "WHITE",
                 font: str | None = None, bold: bool = False, italic: bool = False):

        self.__text = text
        self.__size = size
        self.set_bold_status(bold)
        self.set_italic_status(italic)
        self.set_font(font)

        super().__init__(self.get_width(), self.get_height(), color, 0)

    def __add__(self, other: str | Self):
        if isinstance(other, Text):
            other = other.get_text()
        return self.copy(self.get_text() + other)

    def __sub__(self, other: str | Self):
        if isinstance(other, Text):
            other = other.get_text()
        raw_text = self.get_text()
        text = raw_text.replace(other, "")
        return self.copy(text)

    def __len__(self):
        return len(self.get_text())

    def __bool__(self):
        return not self.is_empty()

    def __getitem__(self, key: int | slice):
        return self.copy(self.get_text()[key])

    def get_text(self) -> str: return self.__text
    def get_size(self) -> int: return self.__size
    def __fix_x(self, x: int) -> int: return x + self.get_width()//2
    def __fix_y(self, y: int) -> int: return y + self.get_height()//2
    def set_x(self, x: int) -> None: super().set_x(self.__fix_x(x))
    def set_y(self, y: int) -> None: super().set_y(self.__fix_y(y))
    def is_empty(self) -> bool: return self.get_text() == ""
    def get_font_path(self) -> Optional[str]: return self.__font_path
    def get_font(self) -> pygame.font.Font: return self.__font
    def is_bold(self) -> bool: return self.__bold
    def is_italic(self) -> bool: return self.__italic

    def set_font(self, font_path: str | None):
        self.__font_name = font_path
        if font_path and os.path.exists(font_path):
            self.__font_path = font_path
        elif font_path is not None:
            self.__font_path = _FontMapper.get_font_path(font_path)
        else:
            self.__font_path = None
        self.__update_font()

    def contains(self, coordinates: tuple[int, int]) -> bool:
        x, y = coordinates
        half_width = self.get_width()//2
        half_height = self.get_height()//2
        within_horizontal_bounds = self.get_x() - half_width <= x <= self.get_x() + half_width
        within_vertical_bounds = self.get_y() - half_height <= y <= self.get_y() + half_height
        return within_horizontal_bounds and within_vertical_bounds

    def __update_font(self) -> None:
        self.__font = pygame.font.Font(self.get_font_path(), self.__size)
        self.__update_dimensions()

    def __update_dimensions(self) -> None:
        new_width, new__height = self.__font.size(self.__text)
        self._set_width(new_width)
        self._set_height(new__height)

    def set_bold_status(self, status: bool) -> None:
        self.__bold = status
        self.__font.set_bold(status)
        self.__update_dimensions()

    def set_italic_status(self, status: bool) -> None:
        self.__italic = status
        self.__font.set_italic(status)
        self.__update_dimensions()

    def set_text(self, text: str) -> None:
        self.__text = text
        self.__update_font()

    def set_size(self, size: int) -> None:
        self._ensure_not_negative(size)
        self.__size = size
        self.__update_font()

    def maximize(self, max_width: int, max_height: int) -> Self:
        low = 1
        high = 500
        optimal_size = 1

        new_instance = self.copy()

        while low <= high:
            mid = (low + high) // 2
            new_instance.set_size(mid)

            if new_instance.get_width() <= max_width and new_instance.get_height() <= max_height:
                optimal_size = mid
                low = mid + 1
            else:
                high = mid - 1

        new_instance.set_size(optimal_size)
        return new_instance

    def display(self, screen: Surface) -> None:
        text_surface = self.__font.render(self.__text, True,
                                          self.get_color_tuple())
        text_rect = text_surface.get_rect(center=(self.get_x(), self.get_y()))
        screen.blit(text_surface, text_rect)

    def copy(self, replace_text: str | None = None, *args: Any, **kwargs: Any) -> Self:
        text = replace_text if replace_text is not None else self.get_text()
        return self.__class__(text=text,
                              size=self.get_size(),
                              color=self.get_color(),
                              font=self.__font_name,
                              bold=self.is_bold(),
                              italic=self.is_italic())

    def sub(self, start: int | None = None, end: int | None = None) -> Self:
        end = end+1 if end else None
        return self.copy(self.get_text()[start:end])
