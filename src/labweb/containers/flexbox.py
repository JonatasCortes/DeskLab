from src.labweb.containers.protected_flexbox import ProtectedFlexBox
from src.labweb.entities import Entity
from typing import Optional, Union
from src.labweb.constants import VerticalAlignment, HorizontalAlignment, FlexDirection


class FlexBox(ProtectedFlexBox):

    def get_children(self) -> list[Entity]: return self._get_children()
    def get_padding(self) -> int: return self._get_padding()
    def get_space_between(self) -> int: return self._get_space_between()
    def is_bounded(self) -> bool: return self._is_bounded()
    def switch_direction(self) -> None: self._switch_direction()
    def remove(self, entity: Entity) -> None: self._remove(entity)
    def pop(self) -> Optional[Entity]: return self._pop()
    def clear(self) -> None: return self._clear()
    def length(self) -> int: return self._length()
    def is_empty(self) -> bool: return self._is_empty()
    def index(self, entity: Entity) -> int: return self._index(entity)

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

    def add(self, entity: Union[Entity, list[Entity]]) -> None:
        self._add(entity)

    def set_children(self, children: list[Entity]) -> None:
        self._set_children(children)

    def insert(self, index: int, entity: Entity) -> None:
        self._insert(index, entity)
