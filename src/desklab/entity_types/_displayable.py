# fmt: off
from abc import abstractmethod
from ._entity import Entity
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import Surface
# fmt: on


class DisplayableEntity(Entity):
    @abstractmethod
    def display(self, screen: Surface) -> None:
        error = f"ERROR: 'display' can't be called directly from {self.__class__.__name__}"
        raise NotImplementedError(error)
