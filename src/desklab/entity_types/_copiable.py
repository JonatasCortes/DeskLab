from ._entity import Entity
from abc import abstractmethod
from typing import Self


class CopiableEntity(Entity):

    @abstractmethod
    def copy(self) -> Self:
        error = f"ERROR: 'copy' can't be called directly from {self.__class__.__name__}"
        raise NotImplementedError(error)
