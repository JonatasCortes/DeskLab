from pygame.event import Event
from src.labweb.color import Color
from src.labweb.entities import Entity, DisplayableEntity, EventSensitiveEntity, CopiableEntity
from src.labweb.area import RectangularArea
from pygame import Surface
from typing import Any, Optional, Union
from abc import abstractmethod
from src.labweb.constants import VerticalAlignment, HorizontalAlignment, FlexDirection


class FlexContainerInterface(RectangularArea, EventSensitiveEntity):
    def __init__(self,
                 width: int,
                 height: int,
                 padding: int = 0,
                 space_between: int = 0,
                 flex_direction: str | FlexDirection = FlexDirection.COLUMN,
                 horizontal_alignment: str | HorizontalAlignment = HorizontalAlignment.CENTER,
                 vertical_alignment: str | VerticalAlignment = VerticalAlignment.CENTER,
                 corners_radius: tuple[int, int, int, int] | int = 0,
                 color: Union[Color, tuple[int, int, int], str] = "BLACK",
                 bounded: bool = True) -> None:

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

    def _set_horizontal_alignment(self, horizontal_alignment: HorizontalAlignment = HorizontalAlignment.CENTER) -> None:
        self._horizontal_alignment = horizontal_alignment
        self._align()

    def _set_vertical_alignment(self, vertical_alignment: VerticalAlignment = VerticalAlignment.CENTER) -> None:
        self._vertical_alignment = vertical_alignment
        self._align()

    def _switch_direction(self) -> None:
        if self._flex_direction == FlexDirection.COLUMN:
            self._flex_direction = FlexDirection.ROW
        else:
            self._flex_direction = FlexDirection.COLUMN
        self._align()

    def display(self, screen: Surface) -> None:
        super().display(screen)
        for child in self._get_children():
            if isinstance(child, DisplayableEntity):
                child.display(screen)

    def handle_event(self, event: Event, *args: Any, **kwargs: Any) -> None:
        for child in self._get_children():
            if isinstance(child, EventSensitiveEntity):
                child.handle_event(event, *args, **kwargs)

    def _add(self, entity: Union[Entity, list[Entity]]) -> None:
        if isinstance(entity, list):
            self.__children.extend(entity)
        else:
            self.__children.append(entity)
        self._align()

    def _set_children(self, children: list[Entity]) -> None:
        self.__children = children
        self._align()

    def _insert(self, index: int, entity: Entity) -> None:
        self.__children.insert(index, entity)
        self._align()

    def _copy(self) -> 'FlexContainerInterface':
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
        for children in self._get_children():
            if isinstance(children, CopiableEntity):
                new_container._add(children.copy())
            else:
                new_container._add(children)
        return new_container

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
