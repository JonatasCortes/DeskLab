from pynput import mouse
from src.labweb.entities import Entity
from typing import Optional
from pygame.event import Event
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, DROPFILE


class Mouse(Entity):

    def __init__(self) -> None:
        self.__position = (0, 0)
        self.__refference_x = 0
        self.__refference_y = 0
        self.__is_held = False
        self.__event: Optional[Event] = None
        self.__activate_listeners()

    def __matches_current_event(self, event_type: int) -> bool:
        if self.__event and self.__event.type == event_type:
            return True
        return False

    def update_event(self, event: Optional[Event]):
        self.__event = event
        if self.is_clicked():
            self.__is_held = True
        elif self.is_released():
            self.__is_held = False

    def update_refference_origin(self, x: int, y: int):
        self.__refference_x = x
        self.__refference_y = y

    def get_position(self) -> tuple[int, int]:
        return self.__position

    def is_held(self) -> bool:
        return self.__is_held

    def is_clicked(self) -> bool:
        return self.__matches_current_event(MOUSEBUTTONDOWN)

    def is_released(self) -> bool:
        return self.__matches_current_event(MOUSEBUTTONUP)

    def is_moving(self) -> bool:
        return self.__matches_current_event(MOUSEMOTION)

    def is_dropping_file(self) -> bool:
        return self.__matches_current_event(DROPFILE)

    def __position_listener(self, x: int, y: int) -> None:
        self.__position = (x - self.__refference_x, y - self.__refference_y)

    def __activate_listeners(self) -> None:
        self._listener = mouse.Listener(on_move=self.__position_listener)
        self._listener.start()
