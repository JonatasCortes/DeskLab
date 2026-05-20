from typing import Callable, Any
from src.desklab.system import KeyBoard
from ._system_listener import SystemListener


class _KeyboardListener(SystemListener):
    _system_input_class = KeyBoard


class _KeyValueDependentListener(_KeyboardListener):
    def __init__(self,
                 keys: str | list[str],
                 actions: Callable[..., Any] | list[Callable[..., Any]],
                 aditional_conditions: Callable[...,
                                                Any] | list[Callable[..., Any]] = [],
                 on_change: bool = False,
                 listen_once: bool = False) -> None:
        self.__keys = keys
        super().__init__(actions, aditional_conditions, on_change, listen_once)

    def handle_event(self, *args: Any, **kwargs: Any) -> None:
        return super().handle_event(*args, **kwargs, keys=self.__keys)


class KeyPressedListener(_KeyValueDependentListener):
    _condition_function = "key_pressed"


class KeyDownListener(_KeyValueDependentListener):
    _condition_function = "key_down"


class KeyUpListener(_KeyValueDependentListener):
    _condition_function = "key_up"


class CtrlActiveListener(_KeyboardListener):
    _condition_function = "ctrl_active"


class ShiftActiveListener(_KeyboardListener):
    _condition_function = "shift_active"


class AltActiveListener(_KeyboardListener):
    _condition_function = "alt_active"


class MetaActiveListener(_KeyboardListener):
    _condition_function = "meta_active"


class AnyKeyPressedListener(_KeyboardListener):
    _condition_function = "any_key_pressed"


class AnyKeyDownListener(_KeyboardListener):
    _condition_function = "any_key_down"


class AnyKeyUpListener(_KeyboardListener):
    _condition_function = "any_key_up"


class AnyTextInputListener(_KeyboardListener):
    _condition_function = "any_text_input"
