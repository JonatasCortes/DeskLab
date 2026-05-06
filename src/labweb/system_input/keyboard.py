from typing import Optional, Set
from src.labweb.entities import Entity
from pygame.event import Event
import pygame
from pygame.constants import (
    K_BACKSPACE, K_ESCAPE, K_LALT, K_LCTRL, K_LSHIFT,
    K_RALT, K_RCTRL, K_RETURN, K_RSHIFT, K_SPACE, K_TAB,
    KEYDOWN, KEYUP, TEXTINPUT, KMOD_CTRL, KMOD_SHIFT,
    KMOD_ALT, KMOD_META
)


class _PygameKeyMapper:

    __SPECIAL_KEYS: dict[str, list[int]] = {
        "esc": [K_ESCAPE],
        "enter": [K_RETURN],
        " ": [K_SPACE],
        "backspace": [K_BACKSPACE],
        "tab": [K_TAB],
        "shift": [K_LSHIFT, K_RSHIFT],
        "ctrl": [K_LCTRL, K_RCTRL],
        "alt": [K_LALT, K_RALT],
    }

    def __init__(self) -> None:
        self.__build_key_map()

    def __build_key_map(self) -> None:
        key_map: dict[str, int] = {}
        for attr in dir(pygame):
            if attr.startswith("K_"):
                key_value: int = getattr(pygame, attr)
                key_name = pygame.key.name(key_value)

                key_map[key_name] = key_value
        self.__key_map = key_map

    def get_key(self, key_name: str) -> list[int]:

        if key_value := self.__SPECIAL_KEYS.get(key_name):
            return key_value

        if key_value := self.__key_map.get(key_name):
            return [key_value]

        error = f"{key_name} is not recognised as a valid key name"
        raise ValueError(error)


class KeyBoard(Entity):
    def __init__(self) -> None:
        self.__event: Optional[Event] = None
        self.__buffer: list[str] = []
        self.__pressed_keys: Set[int] = set()
        self.__mod: int = 0
        self.__key_mapper = _PygameKeyMapper()

    def update_event(self, event: Optional[Event]):
        self.__event = event
        if not event:
            return

        if event.type == KEYDOWN:
            self.__mod = event.mod
            self.__pressed_keys.add(event.key)
        elif event.type == KEYUP:
            self.__mod = event.mod
            self.__pressed_keys.discard(event.key)
        elif event.type == TEXTINPUT:
            self.__buffer.append(event.text)

    def flush(self) -> list[str]:
        buffer = self.peek()
        self.__buffer.clear()
        return buffer

    def peek(self) -> list[str]:
        return self.__buffer.copy()

    def last_input(self) -> str:
        return self.__buffer[-1]

    def key_pressed(self, key: str) -> bool:
        key_values = self.__key_mapper.get_key(key)
        return any(key in self.__pressed_keys for key in key_values)

    def __key_events(self, key: str, event_type: int) -> bool:
        key = key.lower()
        key_values = self.__key_mapper.get_key(key)
        return (
            self.__event is not None and
            self.__event.type == event_type and
            any(k == self.__event.key for k in key_values)
        )

    def key_down_event(self, key: str) -> bool:
        return self.__key_events(key, KEYDOWN)

    def key_up_event(self, key: str) -> bool:
        return self.__key_events(key, KEYUP)

    def ctrl_active(self) -> bool:
        return bool(self.__mod & KMOD_CTRL)

    def shift_active(self) -> bool:
        return bool(self.__mod & KMOD_SHIFT)

    def alt_active(self) -> bool:
        return bool(self.__mod & KMOD_ALT)

    def meta_active(self) -> bool:
        return bool(self.__mod & KMOD_META)
