from desklab._check._parameter import parameter_validator
from typing import Callable


def class_validator(validation_logic: Callable[..., None]):
    def decorator(cls: type) -> type:

        for attr_name in list(cls.__dict__.keys()):
            attr_value = getattr(cls, attr_name)
            if not callable(attr_value) or attr_name.startswith("__"):
                continue
            validator = parameter_validator(validation_logic)
            setattr(cls, attr_name, validator(attr_value))

        return cls
    return decorator
