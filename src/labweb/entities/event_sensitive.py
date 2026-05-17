from src.labweb.entities.entity import Entity
from abc import abstractmethod
from typing import Any


class EventSensitiveEntity(Entity):
    @abstractmethod
    def handle_event(self, *args: Any, **kwargs: Any) -> None:
        pass

    def _raise_for_missing_parameter(self, parameter_key: str, parameter_class_name: str):
        error = f"Expected a {parameter_class_name} instance in kwargs with key '{parameter_key}'"
        raise RuntimeError(error)
