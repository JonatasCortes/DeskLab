# fmt: off
import sys
from pygame._sdl2 import Window as PygameWindow
from src.labweb.system import Mouse, KeyBoard, ClipBoard
from src.labweb.containers import FlexBox, FlexDirection, HorizontalAlignment, VerticalAlignment
from src.labweb._primitives import Color
from pygame.locals import QUIT
from typing import Iterable
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from importlib import resources
# fmt: on


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
    def setup(cls, width: int = 640, height: int = 480, caption: str = "LabWeb", icon: str | None = None) -> None:
        if icon is None:
            assets = resources.files('labweb._assets')
            icon_path = assets.joinpath('labweb.png')
            with resources.as_file(icon_path) as labweb_icon:
                icon = str(labweb_icon)
        pygame.display.set_icon(pygame.image.load(icon))
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
        keyboard = KeyBoard()
        clipboard = ClipBoard()
        self.__running = True
        while self.__running:
            mouse.update_refference_origin(
                *self.get_window_coordinates())

            if events := pygame.event.get():
                for event in events:

                    keyboard.update_event(event)
                    mouse.update_event(event)

                    if event.type == QUIT:
                        sys.exit()

                    self.handle_event(event=event, mouse=mouse,
                                      keyboard=keyboard,
                                      clipboard=clipboard,
                                      screen=self.__screen)
            else:
                keyboard.update_event(None)
                mouse.update_event(None)
                self.handle_event(mouse=mouse,
                                  keyboard=keyboard,
                                  clipboard=clipboard,
                                  screen=self.__screen)

            self.__screen.fill((0, 0, 0))

            self.display(self.__screen)

            pygame.display.update()
            self.__clock.tick(60)

    def close(self) -> None:
        self.__running = False
