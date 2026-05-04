from src.labweb.color import Color
from src.labweb.entities import DefaultEntity
import pygame
from pygame import Surface
from pygame.event import Event
from typing import Any


class Text(DefaultEntity):

    def __init__(self, text: str, size: int = 25, color: Color | tuple[int, ...] | str = "WHITE"):

        self.set_text(text)
        self.set_size(size)
        width, height = self.__get_dimensions()
        super().__init__(0, 0, width, height, color)

    def set_text(self, text: str) -> None:
        self.__text = text

    def get_text(self) -> str:
        return self.__text

    def get_size(self) -> int:
        return self.__size

    def set_size(self, size: int) -> None:
        if size < 0:
            error = f"ERROR: size {size} is invalid."
            raise ValueError(error)
        self.__size = size
        new_width, new_height = self.__get_dimensions()
        self._set_width(new_width)
        self._set_height(new_height)

    def __fix_x(self, x: int) -> int:
        return x + self.get_width()//2

    def __fix_y(self, y: int) -> int:
        return y + self.get_height()//2

    def set_x(self, x: int) -> None:
        super().set_x(self.__fix_x(x))

    def set_y(self, y: int) -> None:
        super().set_y(self.__fix_y(y))

    def maximize(self, max_width: int, max_height: int) -> None:
        size = 0
        while True:
            self.set_size(size)
            if self.get_width() > max_width or self.get_height() > max_height:
                self.set_size(size - 1 if size > 1 else 1)
                break
            size += 1

    def __get_dimensions(self) -> tuple[int, int]:
        font = pygame.font.Font(None, self.get_size())
        return font.size(self.get_text())

    def display(self, screen: Surface) -> None:

        font = pygame.font.Font(None, self.get_size())

        text_surface = font.render(self.get_text(), True,
                                   self.get_color_tuple())
        text_rect = text_surface.get_rect(center=(self.get_x(),
                                                  self.get_y()))

        screen.blit(text_surface, text_rect)

    def handle_event(self, event: Event, *args: Any, **kwargs: Any) -> None:
        pass

    def is_empty(self) -> bool:
        return self.get_text() == ""

    def copy(self) -> "Text":
        return self.__class__(text=self.get_text(),
                              size=self.get_size(),
                              color=self.get_color())
