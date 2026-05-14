import logging
from typing import Literal


class Color:

    def __init__(self, color: tuple[int, ...] | str) -> None:
        self.__set_color(color)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.get_tuple() == other.get_tuple()
        elif isinstance(other, str):
            return self == self.__class__(other)
        return NotImplemented

    def copy(self) -> "Color":
        return self.__class__(self.get_tuple())

    def __assert_in_range(self, value: int) -> None:
        if not (0 <= value <= 255):
            error = "ERROR: Color value must be between 0 and 255."
            raise ValueError(error)

    def __set_color(self, color: tuple[int, ...] | str):
        if isinstance(color, str):
            color = self.__get_tuple_from_color_name(color)
        self.__set_tuple(color)

    def __set_tuple(self, color: tuple[int, ...]):
        if len(color) != 3:
            error = "ERROR: Color tuple must have exactly 3 values (R, G, B)."
            raise ValueError(error)
        for channel in color:
            self.__assert_in_range(channel)
        self.__tuple = color

    def __get_tuple_from_color_name(self, color: str):

        positive_count = color.count("+")
        negative_count = color.count("-")
        raw_color = color.replace("+", "").replace("-", "")
        color_tuple = _ColorMap.get(raw_color)

        for _ in range(positive_count):
            color_tuple = self.__increase_tuple_channels(color_tuple,
                                                         intensity=5)
        for _ in range(negative_count):
            color_tuple = self.__decrease_tuple_channels(color_tuple,
                                                         intensity=5)
        return color_tuple

    def __alter_brightness(self, _tuple: tuple[int, int, int], intensity: int, operation: Literal["+", "-"]) -> tuple[int, int, int]:
        abs_intensity = abs(intensity)
        true_intensity = abs_intensity if operation == "+" else -abs_intensity
        new_r = min(255, max(0, _tuple[0] + true_intensity))
        new_g = min(255, max(0, _tuple[1] + true_intensity))
        new_b = min(255, max(0, _tuple[2] + true_intensity))
        return (new_r, new_g, new_b)

    def __decrease_tuple_channels(self, _tuple: tuple[int, int, int], intensity: int) -> tuple[int, int, int]:
        return self.__alter_brightness(_tuple, intensity, "-")

    def __increase_tuple_channels(self, _tuple: tuple[int, int, int], intensity: int) -> tuple[int, int, int]:
        return self.__alter_brightness(_tuple, intensity, "+")

    def get_luminance(self) -> float:
        r, g, b = self.__tuple
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    def luminance_emphasized(self, intensity: int = 100) -> "Color":
        lum = self.get_luminance()

        if lum < 128:
            factor = (128 - lum) / 128
            return self.lightened(int((40 + 60 * factor) * (intensity / 100)))
        else:
            factor = (lum - 128) / 127
            return self.darkened(int((30 + 70 * factor) * (intensity / 100)))

    def lightened(self, intensity: int) -> 'Color':
        new_tuple = self.__increase_tuple_channels(self.__tuple, intensity)
        return Color(new_tuple)

    def darkened(self, intensity: int) -> 'Color':
        new_tuple = self.__decrease_tuple_channels(self.__tuple, intensity)
        return Color(new_tuple)

    def get_tuple(self) -> tuple[int, int, int]:
        return self.__tuple

    @classmethod
    def get_options(cls) -> list[str]:
        return _ColorMap.get_options()


class _ColorMap:

    __color_map: dict[str, tuple[int, int, int]] = {
        "BLACK": (0, 0, 0),
        "DARK_GRAY": (64, 64, 64),
        "GRAY": (128, 128, 128),
        "LIGHT_GRAY": (192, 192, 192),
        "WHITE": (255, 255, 255),
        "MAROON": (128, 0, 0),
        "RED": (255, 0, 0),
        "BROWN": (165, 42, 42),
        "ORANGE": (255, 165, 0),
        "GOLD": (255, 215, 0),
        "YELLOW": (255, 255, 0),
        "OLIVE": (128, 128, 0),
        "LIME": (0, 255, 0),
        "GREEN": (0, 255, 0),
        "TEAL": (0, 128, 128),
        "TURQUOISE": (64, 224, 208),
        "CYAN": (0, 255, 255),
        "NAVY": (0, 0, 128),
        "BLUE": (0, 0, 255),
        "INDIGO": (75, 0, 130),
        "PURPLE": (128, 0, 128),
        "MAGENTA": (200, 0, 100),
        "VIOLET": (238, 130, 238),
        "PINK": (255, 192, 203),
        "SILVER": (192, 192, 192),
    }

    __default_color = "WHITE"

    @classmethod
    def get(cls, color: str) -> tuple[int, int, int]:
        try:
            return cls.__color_map[color.upper().strip()]

        except KeyError:
            warning = (f"\nWARNING: Invalid color {color} will be defaulted to {cls.__default_color}."
                       f"\n         Please replace the given value with a valid one, acording to the availuable color map.\n")
            logging.warning(warning)
            return cls.__color_map["WHITE"]

    @classmethod
    def get_options(cls) -> list[str]:
        return list(cls.__color_map.keys())
