from typing import Callable, Any, Type
from desklab.system import SystemInput
from ._protected_listener import ProtectedListener


class SystemListener(ProtectedListener):

    _condition_function: str = ""
    _system_input_class: Type[SystemInput]

    def __init__(self,
                 actions: Callable[..., Any] | list[Callable[..., Any]],
                 aditional_conditions: Callable[...,
                                                Any] | list[Callable[..., Any]] = [],
                 on_change: bool = False,
                 listen_once: bool = False) -> None:

        if isinstance(aditional_conditions, Callable):
            aditional_conditions = [aditional_conditions]
        super().__init__([self._check_condition, *aditional_conditions],
                         actions, on_change, listen_once)

    def _check_condition(self, **kwargs: Any) -> bool:
        class_name = self._system_input_class.__name__
        system_input = kwargs.get(class_name.lower())
        if not isinstance(system_input, self._system_input_class):
            self._raise_for_missing_parameter(class_name,
                                              self._system_input_class.__name__)
        method = getattr(system_input, self._condition_function)
        try:
            return bool(method(**kwargs))
        except TypeError:
            return bool(method())

    def get_actions(self) -> list[Callable[..., Any]]:
        return self._get_actions()

    def set_actions(self, actions: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        return self._set_actions(actions)

    def add_actions(self, actions: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        return self._add_actions(actions)

    def _get_copy_replacement_map(self) -> dict[str, Any]:
        return {
            "actions": self._get_actions(),
            "aditional_conditions": self._get_conditions()[1:],
            "on_change": self._on_change,
            "listen_once": self._listen_once
        }
