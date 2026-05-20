from typing import Dict, Any, Type, TypeVar, cast
import threading


T = TypeVar("T")


class Singleton(type):
    _instances: Dict[Type[Any], Any] = {}
    _lock = threading.Lock()

    def __call__(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        if cls not in Singleton._instances:
            with Singleton._lock:
                if cls not in Singleton._instances:
                    instance = super().__call__(*args, **kwargs)
                    Singleton._instances[cls] = instance

        return cast(T, Singleton._instances[cls])


class SystemInput(metaclass=Singleton):
    pass
