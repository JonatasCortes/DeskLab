from typing import Optional

from src.labweb.color import Color
from src.labweb.entities import DisplayableEntity, ContainableEntity, ColorableEntity, CopiableEntity
import pygame
from pygame import Surface
import os


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


class Text(DisplayableEntity, ContainableEntity, ColorableEntity, CopiableEntity):

    def __init__(self, text: str, size: int = 25, color: Color | tuple[int, ...] | str = "WHITE",
                 font: str | None = None, bold: bool = False, italic: bool = False):

        self.__font_name = font
        if font and os.path.exists(font):
            self.__font_path = font
        elif font is not None:
            self.__font_path = _FontMapper.get_font_path(font)
        else:
            self.__font_path = None

        self.__text = text
        self.__size = size
        self.__bold = bold
        self.__italic = italic
        self.__font = pygame.font.Font(None, 0)
        self.__update_font()

        super().__init__(x=0, y=0, width=self.__width, height=self.__height, color=color)

    def __add__(self, other: str | Text):
        copy = self.copy()
        if isinstance(other, Text):
            copy.set_text(copy.get_text() + other.get_text())
        else:
            copy.set_text(copy.get_text() + other)
        return copy

    def __len__(self):
        return len(self.__text)

    def __update_font(self) -> None:
        self.__font = pygame.font.Font(self.get_font_path(), self.__size)
        self.__font.set_bold(self.is_bold())
        self.__font.set_italic(self.is_italic())
        self.__width, self.__height = self.__font.size(self.__text)

    def set_bold_status(self, status: bool) -> None:
        self.__bold = status
        self.__update_font()
        self._set_width(self.__width)
        self._set_height(self.__height)

    def set_italic_status(self, status: bool) -> None:
        self.__italic = status
        self.__update_font()
        self._set_width(self.__width)
        self._set_height(self.__height)

    def is_bold(self) -> bool: return self.__bold
    def is_italic(self) -> bool: return self.__italic

    def set_text(self, text: str) -> None:
        self.__text = text
        self.__update_font()
        self._set_width(self.__width)
        self._set_height(self.__height)

    def get_text(self) -> str: return self.__text
    def get_size(self) -> int: return self.__size
    def __fix_x(self, x: int) -> int: return x + self.get_width()//2
    def __fix_y(self, y: int) -> int: return y + self.get_height()//2
    def set_x(self, x: int) -> None: super().set_x(self.__fix_x(x))
    def set_y(self, y: int) -> None: super().set_y(self.__fix_y(y))
    def is_empty(self) -> bool: return self.get_text() == ""
    def get_font_path(self) -> Optional[str]: return self.__font_path
    def get_font(self) -> pygame.font.Font: return self.__font

    def set_color(self, color: Color | tuple[int, ...] | str):
        return super()._set_color(color)

    def set_size(self, size: int) -> None:
        if size < 0:
            error = f"ERROR: size {size} is invalid."
            raise ValueError(error)
        self.__size = size
        self.__update_font()
        self._set_width(self.__width)
        self._set_height(self.__height)

    def maximize(self, max_width: int, max_height: int) -> "Text":
        size = 0
        new_instance = self.copy()
        while True:
            new_instance.set_size(size)
            if new_instance.get_width() > max_width or new_instance.get_height() > max_height:
                new_instance.set_size(size - 1 if size > 1 else 1)
                break
            size += 1
        return new_instance

    def display(self, screen: Surface) -> None:
        text_surface = self.__font.render(self.__text, True,
                                          self.get_color_tuple())
        text_rect = text_surface.get_rect(center=(self.get_x(), self.get_y()))
        screen.blit(text_surface, text_rect)

    def copy(self) -> "Text":
        return self.__class__(text=self.get_text(),
                              size=self.get_size(),
                              color=self.get_color(),
                              font=self.__font_name,
                              bold=self.is_bold(),
                              italic=self.is_italic())

    def sub(self, start: int | None = None, end: int | None = None) -> "Text":
        copy = self.copy()
        copy.set_text(copy.get_text()[start:end])
        return copy
