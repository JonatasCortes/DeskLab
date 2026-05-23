from ._entity import Entity
from abc import abstractmethod
from typing import Any, Self


class CopiableEntity(Entity):

    @abstractmethod
    def _get_copy_replacement_map(self) -> dict[str, Any]:
        pass

    def copy(self, **kwargs: Any) -> Self:
        params = self._get_copy_replacement_map()

        for key, value in kwargs.items():
            if value is not None:
                params[key] = value

        return self.__class__(**params)
