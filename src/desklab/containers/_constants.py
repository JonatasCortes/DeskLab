from enum import Enum


class HorizontalAlignment(Enum):
    LEFT = "LEFT"
    CENTER = "CENTER"
    RIGHT = "RIGHT"


class VerticalAlignment(Enum):
    TOP = "TOP"
    CENTER = "CENTER"
    BOTTOM = "BOTTOM"


class FlexDirection(Enum):
    ROW = "ROW"
    COLUMN = "COLUMN"
