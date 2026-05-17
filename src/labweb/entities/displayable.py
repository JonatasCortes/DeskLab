from src.labweb.entities.entity import Entity
from abc import abstractmethod
from pygame import Surface


class DisplayableEntity(Entity):
    @abstractmethod
    def display(self, screen: Surface) -> None:
        error = f"ERROR: 'display' can't be called directly from {self.__class__.__name__}"
        raise NotImplementedError(error)
