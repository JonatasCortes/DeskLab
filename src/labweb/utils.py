import threading
from typing import Dict, Any, Type, TypeVar, cast


def point_to_segment_distance(point: tuple[int, int], begin: tuple[int, int], end: tuple[int, int]) -> float:
    # p = mouse, a e b = extremos do segmento
    px, py = point
    ax, ay = begin
    bx, by = end
    # vetor AB
    abx = bx - ax
    aby = by - ay

    # vetor AP
    apx = px - ax
    apy = py - ay

    ab_len_sq = abx * abx + aby * aby
    if ab_len_sq == 0:
        # a == b
        return ((px - ax) ** 2 + (py - ay) ** 2) ** 0.5

    # projeção escalar normalizada (clamp entre 0 e 1)
    t = max(0, min(1, (apx * abx + apy * aby) / ab_len_sq))

    # ponto mais próximo no segmento
    closest_x = ax + abx * t
    closest_y = ay + aby * t

    # distância
    dx = px - closest_x
    dy = py - closest_y
    return (dx * dx + dy * dy) ** 0.5


def is_inside_circle(coordinates: tuple[int, int], circle_center: tuple[int, int], circle_radius: int):
    x, y = coordinates
    cx, cy = circle_center
    return (x - cx)**2 + (y - cy)**2 <= circle_radius**2


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
