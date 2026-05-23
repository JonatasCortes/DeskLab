import os
from typing import Any, Optional
from desklab.entity_types._copiable import CopiableEntity
import pygame


class Font(CopiableEntity):

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

    MAX_FONT_SIZE: int = 1000
    MIN_FONT_SIZE: int = 1

    def __init__(self, font: Optional[str] = None, size: int = 25, bold: bool = False, italic: bool = False) -> None:
        self.__font_path = self.__deduce_font_path(font)
        self.set_size(size)
        self.__font.set_bold(bold)
        self.__font.set_italic(italic)

    def set_size(self, size: int) -> None:
        self.__assert_size_within_bounds(size)
        self.__size = size
        self.__font = pygame.font.Font(self.__font_path, size)

    def get_size(self) -> int: return self.__size
    def get_bold_status(self) -> bool: return self.__font.get_bold()
    def get_italic_status(self) -> bool: return self.__font.get_italic()

    def set_bold_status(self, bold: bool) -> None:
        self.__font.set_bold(bold)

    def set_italic_status(
        self, italic: bool) -> None: self.__font.set_italic(italic)

    def __assert_size_within_bounds(self, size: int) -> None:
        if self.MIN_FONT_SIZE <= size <= self.MAX_FONT_SIZE:
            return
        error = f"'size' must have a value between {self.MIN_FONT_SIZE} and {self.MAX_FONT_SIZE}"
        raise ValueError(error)

    def measure_text(self, text: str) -> tuple[int, int]:
        return self.__font.size(text)

    def render(self, text: str, color: tuple[int, ...]) -> pygame.Surface:
        return self.__font.render(text, True, color)

    def __deduce_font_path(self, font: Optional[str]) -> Optional[str]:
        if font is None:
            return
        if os.path.exists(font):
            return font
        return self.__search_font_path(font)

    def __search_font_path(self, font_name: str) -> Optional[str]:
        normalized_name = font_name.lower().strip()

        path = ""
        if normalized_name in self.__FONT_MAP:
            for attempt in self.__FONT_MAP[normalized_name]:
                path = pygame.font.match_font(attempt)
                if path:
                    break
        else:
            path = pygame.font.match_font(normalized_name)

        return path if path else None

    @classmethod
    def get_available_fonts(cls) -> list[str]:
        return list(cls.__FONT_MAP.keys())

    def _get_copy_replacement_map(self) -> dict[str, Any]:
        return {
            "font": self.__font_path,
            "size": self.get_size(),
            "bold": self.get_bold_status(),
            "italic": self.get_italic_status()
        }
