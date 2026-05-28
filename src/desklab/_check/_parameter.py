import inspect
from functools import wraps
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")


def parameter_validator(validation_logic: Callable[..., None]):
    def decorator(function: Callable[P, R]) -> Callable[P, R]:
        signature = inspect.signature(function)

        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            bound_arguments = signature.bind(*args, **kwargs)
            bound_arguments.apply_defaults()

            for param_name, param_value in bound_arguments.arguments.items():
                if param_name in ("self", "cls"):
                    continue
                validation_logic(param_name, param_value, signature=signature)

            return function(*args, **kwargs)
        return wrapper
    return decorator
