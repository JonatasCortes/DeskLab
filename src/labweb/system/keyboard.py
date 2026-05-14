from typing import Optional, Set
from src.labweb.system.system_listener import SystemListener
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

        lower_key_name = key_name.lower()

        if key_value := self.__SPECIAL_KEYS.get(lower_key_name):
            return key_value

        if key_value := self.__key_map.get(lower_key_name):
            return [key_value]

        error = f"{key_name} is not recognised as a valid key name"
        raise ValueError(error)


class KeyBoard(SystemListener):
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

    def last_input(self) -> Optional[str]:
        if not self.__buffer:
            return None
        return self.__buffer[-1]

    def key_pressed(self, key: str) -> bool:
        key_values = self.__key_mapper.get_key(key)
        return any(k in self.__pressed_keys for k in key_values)

    def __key_events(self, key: str, event_type: int) -> bool:
        key = key.lower()
        key_values = self.__key_mapper.get_key(key)
        return (
            self.__event is not None and
            self.__event.type == event_type and
            any(k == self.__event.key for k in key_values)
        )

    def key_down(self, key: str) -> bool:
        return self.__key_events(key, KEYDOWN)

    def key_up(self, key: str) -> bool:
        return self.__key_events(key, KEYUP)

    def __is_event_type(self, type: int) -> bool:
        if self.__event and self.__event.type == type:
            return True
        return False

    def any_key_pressed(self) -> bool:
        return len(self.__pressed_keys) != 0

    def any_key_down(self) -> bool:
        return self.__is_event_type(KEYDOWN)

    def any_key_up(self) -> bool:
        return self.__is_event_type(KEYUP)

    def any_text_input(self) -> bool:
        return self.__is_event_type(TEXTINPUT)

    def ctrl_active(self) -> bool:
        return bool(self.__mod & KMOD_CTRL)

    def shift_active(self) -> bool:
        return bool(self.__mod & KMOD_SHIFT)

    def alt_active(self) -> bool:
        return bool(self.__mod & KMOD_ALT)

    def meta_active(self) -> bool:
        return bool(self.__mod & KMOD_META)
