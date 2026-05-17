from src.labweb.primitives.color import Color
from src.labweb.entities.entity import Entity
from src.labweb.entities.containable import ContainableEntity
from src.labweb.entities.displayable import DisplayableEntity
from src.labweb.entities.event_sensitive import EventSensitiveEntity
from src.labweb.entities.copiable import CopiableEntity
from src.labweb.areas.rectangular_area import RectangularArea
from pygame import Surface
from typing import Any, Optional, Union, Self
from abc import abstractmethod
from src.labweb.constants import VerticalAlignment, HorizontalAlignment, FlexDirection


class FlexBoxInterface(RectangularArea, EventSensitiveEntity):
    def __init__(self,
                 width: int,
                 height: int,
                 padding: int = 0,
                 space_between: int = 0,
                 flex_direction: str | FlexDirection = "COLUMN",
                 horizontal_alignment: str | HorizontalAlignment = "CENTER",
                 vertical_alignment: str | VerticalAlignment = "CENTER",
                 corners_radius: tuple[int, int, int, int] | int = 0,
                 color: Union[Color, tuple[int, int, int], str] = "BLACK",
                 bounded: bool = True, *args: Any, **kwargs: Any) -> None:

        self.__children: list[Entity] = []
        self._bounded = bounded
        self._padding = padding
        self._space_between = space_between

        if isinstance(flex_direction, str):
            flex_direction = flex_direction.upper()
        self._flex_direction = FlexDirection(flex_direction)

        if isinstance(horizontal_alignment, str):
            horizontal_alignment = horizontal_alignment.upper()
        self._horizontal_alignment = HorizontalAlignment(horizontal_alignment)

        if isinstance(vertical_alignment, str):
            vertical_alignment = vertical_alignment.upper()
        self._vertical_alignment = VerticalAlignment(vertical_alignment)

        super().__init__(width, height, color, corners_radius)

    def _get_padding(self) -> int: return self._padding
    def _get_space_between(self) -> int: return self._space_between
    def _get_flex_direction(self) -> FlexDirection: return self._flex_direction
    def _is_bounded(self) -> bool: return self._bounded

    def _get_children(self) -> list[Entity]:
        return self.__children.copy()

    def _get_horizontal_alignment(self) -> HorizontalAlignment:
        return self._horizontal_alignment

    def _get_vertical_alignment(self) -> VerticalAlignment:
        return self._vertical_alignment

    def _set_horizontal_alignment(self, horizontal_alignment: HorizontalAlignment | str) -> None:
        self._horizontal_alignment = HorizontalAlignment(horizontal_alignment)
        self._align()

    def _set_vertical_alignment(self, vertical_alignment: VerticalAlignment | str) -> None:
        self._vertical_alignment = VerticalAlignment(vertical_alignment)
        self._align()

    def _set_flex_direction(self, flex_direction: FlexDirection | str) -> None:
        self._flex_direction = FlexDirection(flex_direction)
        self._align()

    def _switch_direction(self) -> None:
        if self._flex_direction == FlexDirection.COLUMN:
            self._set_flex_direction("ROW")
        else:
            self._set_flex_direction("COLUMN")

    def display(self, screen: Surface) -> None:
        super().display(screen)
        for child in self._get_children():
            if isinstance(child, DisplayableEntity):
                child.display(screen)

    def handle_event(self, *args: Any, **kwargs: Any) -> None:
        super().handle_event(*args, **kwargs)
        for child in self._get_children():
            if isinstance(child, EventSensitiveEntity):
                child.handle_event(*args, **kwargs)

    def _add(self, entity: Union[Entity, list[Entity]]) -> None:
        if not isinstance(entity, list):
            entity = [entity]
        try:
            self.__children.extend(entity)
            self._align()
        except ValueError as error:
            for e in entity:
                self.__children.remove(e)
            raise error

    def _set_children(self, children: list[Entity]) -> None:
        self.__children = children
        self._align()

    def _insert(self, index: int, entity: Entity) -> None:
        self.__children.insert(index, entity)
        self._align()

    def _index(self, entity: Entity) -> int:
        return self.__children.index(entity)

    def _copy(self) -> Self:
        new_container = self.__class__(
            width=self.get_width(),
            height=self.get_height(),
            padding=self._get_padding(),
            space_between=self._get_space_between(),
            flex_direction=self._get_flex_direction(),
            horizontal_alignment=self._get_horizontal_alignment(),
            vertical_alignment=self._get_vertical_alignment(),
            corners_radius=self.get_corners_radius(),
            color=self.get_color(),
            bounded=self._is_bounded()
        )
        self._migrate_children(new_container)
        return new_container

    def _migrate_children(self, new_instance: "FlexBoxInterface") -> None:
        for children in self._get_children():
            if isinstance(children, CopiableEntity):
                new_instance._add(children.copy())
            else:
                new_instance._add(children)

    def _remove(self, entity: Entity) -> None:
        self.__children.remove(entity)
        self._align()

    def _pop(self) -> Optional[Entity]:
        if not self.__children:
            return None
        entity = self.__children.pop()
        self._align()
        return entity

    def _clear(self) -> None:
        self.__children.clear()
        self._align()

    def _length(self) -> int:
        return len(self.__children)

    def _count_containable_children(self) -> int:
        count = 0
        for c in self._get_children():
            if isinstance(c, ContainableEntity):
                count += 1
        return count

    def _is_empty(self) -> bool:
        return not self.__children

    def set_x(self, x: int) -> None:
        super().set_x(x)
        self._align()

    def set_y(self, y: int) -> None:
        super().set_y(y)
        self._align()

    @abstractmethod
    def _align(self) -> None:
        raise NotImplementedError(
            "ERROR: _align method must be implemented by subclasses")
