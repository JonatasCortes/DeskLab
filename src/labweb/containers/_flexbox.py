from src.labweb.entity_types import Entity
from typing import Callable, Optional, Self, Union, TypeVar
from ._constants import VerticalAlignment, HorizontalAlignment, FlexDirection
from ._protected_flexbox import ProtectedFlexBox

T = TypeVar("T")


class FlexBox(ProtectedFlexBox):

    def get_children(self) -> list[Entity]: return self._get_children()
    def get_padding(self) -> int: return self._get_padding()
    def get_space_between(self) -> int: return self._get_space_between()
    def is_bounded(self) -> bool: return self._is_bounded()
    def switch_direction(self) -> None: self._switch_direction()
    def pop_child(self) -> Optional[Entity]: return self._pop_child()
    def clear_children(self) -> None: return self._clear_children()
    def count_children(self) -> int: return self._count_children()
    def copy(self) -> Self: return super()._copy()

    def cascade(self, function: Callable[[Entity], T]) -> list[T]:
        return self._cascade(function)

    def remove_children(self, entity: Entity) -> None:
        self._remove_children(entity)

    def count_containable_children(self) -> int:
        return self._count_containable_children()

    def is_childless(self) -> bool: return self._is_childless()

    def get_child_index(self, entity: Entity) -> int:
        return self._get_child_index(entity)

    def get_horizontal_alignment(self) -> HorizontalAlignment:
        return self._get_horizontal_alignment()

    def get_vertical_alignment(self) -> VerticalAlignment:
        return self._get_vertical_alignment()

    def get_flex_direction(self) -> FlexDirection:
        return self._get_flex_direction()

    def set_horizontal_alignment(self, horizontal_alignment: HorizontalAlignment = HorizontalAlignment.CENTER) -> None:
        self._set_horizontal_alignment(horizontal_alignment)

    def set_vertical_alignment(self, vertical_alignment: VerticalAlignment = VerticalAlignment.CENTER) -> None:
        self._set_vertical_alignment(vertical_alignment)

    def add_children(self, entity: Union[Entity, list[Entity]]) -> None:
        self._add_children(entity)

    def set_children(self, children: list[Entity]) -> None:
        self._set_children(children)

    def insert_children(self, index: int, entity: Entity) -> None:
        self._insert_children(index, entity)
