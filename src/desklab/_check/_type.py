import inspect
from typing import Any, Callable, Type, get_origin, get_args, Union, TypeVar, overload
from types import UnionType
from desklab._check._parameter import parameter_validator
from desklab._check._class import class_validator
from desklab.exceptions import InvalidParameterType, InvalidDecorationTarget

T = TypeVar("T", bound=Callable[..., Any])
C = TypeVar("C", bound=type)


def check_type_recursively(parameter_name: str, parameter_value: Any, expected_type: Type[Any]):
    if expected_type is Any or expected_type == inspect.Parameter.empty:
        return

    origin = get_origin(expected_type)

    if expected_type.__class__ is UnionType or origin is Union:
        sub_types = get_args(expected_type)

        for sub_type in sub_types:
            try:
                check_type_recursively(
                    parameter_name, parameter_value, sub_type)
                return
            except InvalidParameterType:
                continue

        raise InvalidParameterType(parameter_name,
                                   expected_type,
                                   parameter_value.__class__)

    type_to_check = origin if origin is not None else expected_type

    if not isinstance(parameter_value, type_to_check):
        raise InvalidParameterType(parameter_name,
                                   expected_type,
                                   parameter_value.__class__)


def type_check_logic(param_name: str, param_value: Any, signature: inspect.Signature):
    expected_type = signature.parameters[param_name].annotation
    check_type_recursively(param_name, param_value, expected_type)


def _parameter_type_check():
    return parameter_validator(type_check_logic)


def _class_full_type_check():
    return class_validator(type_check_logic)


@overload
def type_check(target: C) -> C: ...


@overload
def type_check(target: T) -> T: ...


def type_check(target: Any) -> Any:
    if isinstance(target, type):
        return _class_full_type_check()(target)
    if callable(target):
        return _parameter_type_check()(target)

    raise InvalidDecorationTarget("type_check",
                                  [type, Type[Callable[..., Any]]],
                                  target)
