from typing import Iterable

from pygame.locals import QUIT
from src.labweb.color import Color
from src.labweb.containers.flexbox import FlexBox
from src.labweb.constants import FlexDirection, HorizontalAlignment, VerticalAlignment
from src.labweb.mouse import Mouse
from pygame._sdl2 import Window as PygameWindow
import pygame
import sys


class Window(FlexBox):

    __is_set_up = False

    def __init__(self,
                 padding: int = 0,
                 space_between: int = 0,
                 flex_direction: str | FlexDirection = FlexDirection.COLUMN,
                 horizontal_alignment: str | HorizontalAlignment = HorizontalAlignment.CENTER,
                 vertical_alignment: str | VerticalAlignment = VerticalAlignment.CENTER,
                 color: Color | tuple[int, int, int] | str = "BLACK") -> None:

        if not self.__is_set_up:
            error = f"ERROR: {self.__class__.__name__} must be set up using the 'setup' class method before instantiation."
            raise RuntimeError(error)

        super().__init__(self.__width, self.__height, padding, space_between,
                         flex_direction, horizontal_alignment, vertical_alignment,
                         corners_radius=0, color=color, bounded=True)

    @classmethod
    def setup(cls, width: int = 640, height: int = 480, caption: str = "PyPaint") -> None:
        pygame.init()
        cls.__screen = pygame.display.set_mode((width, height))
        cls.__clock = pygame.time.Clock()
        cls.__width = width
        cls.__height = height
        pygame.display.set_caption(caption)
        cls.__is_set_up = True
        cls.__window = PygameWindow.from_display_module()

    def get_window_coordinates(self):
        window_coordinates = self.__window.position
        assert isinstance(window_coordinates, Iterable)
        return tuple(window_coordinates)

    def open(self) -> None:

        mouse = Mouse()

        self.__running = True
        while self.__running:

            for event in pygame.event.get():

                mouse.update_event(event)
                mouse.update_refference_origin(*self.get_window_coordinates())

                if event.type == QUIT:
                    sys.exit()
                self.handle_event(event, mouse=mouse,
                                  screen=self.__screen)

            self.__screen.fill((0, 0, 0))

            self.display(self.__screen)

            pygame.display.update()
            self.__clock.tick(60)

    def close(self) -> None:
        self.__running = False
