from src.desklab.system import Mouse
from src.desklab.areas import Area
from typing import Any, Callable
from ._protected_listener import ProtectedListener


class HoverListener(ProtectedListener):

    def __init__(self,
                 area: Area,
                 actions: Callable[..., Any] | list[Callable[..., Any]],
                 aditional_conditions: Callable[...,
                                                Any] | list[Callable[..., Any]] = [],
                 on_change: bool = False,
                 listen_once: bool = False) -> None:

        self.__area = area

        if isinstance(aditional_conditions, Callable):
            aditional_conditions = [aditional_conditions]

        super().__init__([self.__hover, *aditional_conditions],
                         actions, on_change, listen_once)

    def __hover(self, *args: Any, **kwargs: Any) -> bool:
        mouse = kwargs.get("mouse")
        if not isinstance(mouse, Mouse):
            self._raise_for_missing_parameter("mouse", Mouse.__name__)
        return self.__area.contains(mouse.get_position())
