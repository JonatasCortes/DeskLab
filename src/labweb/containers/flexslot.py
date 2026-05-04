from src.labweb.containers.flex_container_interface import FlexContainerInterface
from src.labweb.color import Color
from src.labweb.entities import Entity, ContainableEntity, CopiableEntity
from typing import Optional
from src.labweb.constants import VerticalAlignment, HorizontalAlignment, FlexDirection


class FlexSlot(FlexContainerInterface):

    def __init__(self,
                 width: int,
                 height: int,
                 horizontal_alignment: str | HorizontalAlignment = HorizontalAlignment.CENTER,
                 vertical_alignment: str | VerticalAlignment = VerticalAlignment.CENTER,
                 corners_radius: tuple[int, int, int, int] | int = 0,
                 color: Color | tuple[int, int, int] | str = "BLACK",
                 bounded: bool = True) -> None:

        super().__init__(width, height, 0, 0, FlexDirection.COLUMN,
                         horizontal_alignment, vertical_alignment,
                         corners_radius, color, bounded)

    def set_child(self, child: Entity) -> None:
        self._clear()
        self._add(child)

    def get_child(self) -> Optional[Entity]:
        if self.is_empty():
            return None
        return self._get_children()[0]

    def pop(self) -> Optional[Entity]: return self._pop()
    def clear(self) -> None: self._clear()
    def is_empty(self) -> bool: return self._is_empty()
    def is_bounded(self) -> bool: return self._is_bounded()
    def switch_direction(self) -> None: self._switch_direction()

    def get_horizontal_alignment(self) -> HorizontalAlignment:
        return self._get_horizontal_alignment()

    def get_vertical_alignment(self) -> VerticalAlignment:
        return self._get_vertical_alignment()

    def set_horizontal_alignment(self, horizontal_alignment: HorizontalAlignment = HorizontalAlignment.CENTER) -> None:
        self._set_horizontal_alignment(horizontal_alignment)

    def set_vertical_alignment(self, vertical_alignment: VerticalAlignment = VerticalAlignment.CENTER) -> None:
        self._set_vertical_alignment(vertical_alignment)

    def copy(self) -> 'FlexSlot':
        new_slot = self.__class__(self.get_width(), self.get_height(),
                                  self.get_horizontal_alignment(),
                                  self.get_vertical_alignment(),
                                  self.get_corners_radius(),
                                  self.get_color(), self.is_bounded())
        child = self.get_child()
        assert child
        if isinstance(child, CopiableEntity):
            new_slot.set_child(child.copy())
        else:
            new_slot.set_child(child)
        return new_slot

    def _align(self) -> None:
        if self.is_empty():
            return
        child = self.get_child()
        if not isinstance(child, ContainableEntity):
            return

        available_width, available_height = self.__get_available_space()
        child_width, child_height = child.get_width(), child.get_height()

        if self._is_bounded():
            self.__validate_bounds(child_width, child_height,
                                   available_width, available_height)

        x = self.__calculate_horizontal_position(child_width, available_width)
        y = self.__calculate_vertical_position(child_height, available_height)

        child.set_x(x)
        child.set_y(y)

    def __get_available_space(self) -> tuple[int, int]:
        padding = self._get_padding()
        width = self.get_width() - 2 * padding
        height = self.get_height() - 2 * padding
        return width, height

    def __validate_bounds(self, child_width: int, child_height: int, available_width: int, available_height: int) -> None:
        if child_width > available_width:
            raise ValueError("ERROR: child exceeds width limit")

        if child_height > available_height:
            raise ValueError("ERROR: child exceeds height limit")

    def __calculate_horizontal_position(self, child_width: int, available_width: int) -> int:
        align = self._get_horizontal_alignment()
        base = self.get_x() + self._get_padding()

        if align == HorizontalAlignment.CENTER:
            return base + (available_width - child_width) // 2

        if align == HorizontalAlignment.RIGHT:
            return base + (available_width - child_width)

        return base

    def __calculate_vertical_position(self, child_height: int, available_height: int) -> int:
        align = self._get_vertical_alignment()
        base = self.get_y() + self._get_padding()

        if align == VerticalAlignment.CENTER:
            return base + (available_height - child_height) // 2

        if align == VerticalAlignment.BOTTOM:
            return base + (available_height - child_height)

        return base
