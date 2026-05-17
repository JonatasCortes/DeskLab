from src.labweb.entities.entity import Entity
from src.labweb.entities.containable import ContainableEntity
from src.labweb.constants import VerticalAlignment, HorizontalAlignment, FlexDirection
from src.labweb.containers.flexbox_interface import FlexBoxInterface


class ProtectedFlexBox(FlexBoxInterface):

    def __get_main_dimension(self, entity: ContainableEntity) -> int:
        if self._get_flex_direction() == FlexDirection.COLUMN:
            return entity.get_height()
        else:
            return entity.get_width()

    def __get_secondary_dimension(self, entity: ContainableEntity) -> int:
        if self._get_flex_direction() == FlexDirection.COLUMN:
            return entity.get_width()
        else:
            return entity.get_height()

    def _align(self) -> None:
        if self._is_empty():
            return

        main_dimension_sum = self.__get_main_dimension_sum()
        secondary_dimension_max = self.__get_secondary_dimension_max()
        total_space_between = self.__calculate_total_space_between()

        if self._is_bounded():
            self.__validate_bounds(main_dimension_sum,
                                   secondary_dimension_max,
                                   total_space_between)

        free_space = self.__calculate_free_space(main_dimension_sum,
                                                 total_space_between)
        start_pos = self.__calculate_main_start_position(free_space)
        self.__distribute_children(self._get_children(), start_pos)

    def __get_main_dimension_sum(self) -> int:
        return sum(self.__get_main_dimension(c) for c in self._get_children()
                   if isinstance(c, ContainableEntity))

    def __get_secondary_dimension_max(self) -> int:
        return max((self.__get_secondary_dimension(c)
                    for c in self._get_children()
                    if isinstance(c, ContainableEntity)), default=0)

    def __calculate_total_space_between(self) -> int:
        return self._get_space_between() * (self._count_containable_children() - 1)

    def __validate_bounds(self, main_sum: int, secondary_max: int, total_space_between: int) -> None:
        padding = self._get_padding()
        main_limit = self.__get_main_dimension(self) - 2 * padding
        cross_limit = self.__get_secondary_dimension(self) - 2 * padding

        main_axis = "width"
        secondary_axis = "height"

        if self._get_flex_direction() == FlexDirection.COLUMN:
            main_axis, secondary_axis = secondary_axis, main_axis

        if main_sum + total_space_between > main_limit:
            raise ValueError(f"ERROR: children exceed {main_axis} limit")

        if secondary_max > cross_limit:
            raise ValueError(f"ERROR: children exceed {secondary_axis} limit")

    def __calculate_free_space(self, main_dimension_sum: int, total_space_between: int):
        return (self.__get_main_dimension(self) -
                2 * self._get_padding() -
                main_dimension_sum - total_space_between)

    def __calculate_main_start_position(self, free_space: int) -> int:
        if self._get_flex_direction() == FlexDirection.ROW:
            alignment = self._get_horizontal_alignment()
            base_coordinate = self.get_x()
        else:
            alignment = self._get_vertical_alignment()
            base_coordinate = self.get_y()

        start_pos = base_coordinate + self._get_padding()

        if alignment == HorizontalAlignment.CENTER or alignment == VerticalAlignment.CENTER:
            start_pos += free_space // 2
        elif alignment in (HorizontalAlignment.RIGHT, VerticalAlignment.BOTTOM):
            start_pos += free_space

        return start_pos

    def __distribute_children(self, children: list[Entity], start_pos: int) -> None:

        current_main_axis_pos = start_pos

        for child in children:
            if not isinstance(child, ContainableEntity):
                continue

            secondary_axis_pos = self.__calculate_secondary_axis_pos(child)

            if self._get_flex_direction() == FlexDirection.ROW:
                child.set_x(current_main_axis_pos)
                child.set_y(secondary_axis_pos)
            else:
                child.set_x(secondary_axis_pos)
                child.set_y(current_main_axis_pos)

            current_main_axis_pos += (self.__get_main_dimension(child) +
                                      self._get_space_between())

    def __calculate_secondary_axis_pos(self, child: ContainableEntity) -> int:

        padding = self._get_padding()

        if self._get_flex_direction() == FlexDirection.COLUMN:
            align = self._get_horizontal_alignment()
            base_pos = self.get_x()
        else:
            align = self._get_vertical_alignment()
            base_pos = self.get_y()

        container_dim = self.__get_secondary_dimension(self)
        child_dim = self.__get_secondary_dimension(child)

        safe_area_start = base_pos + padding
        safe_area_dim = container_dim - 2 * padding

        if align == HorizontalAlignment.CENTER or align == VerticalAlignment.CENTER:
            return safe_area_start + (safe_area_dim - child_dim) // 2

        if align in (VerticalAlignment.BOTTOM, HorizontalAlignment.RIGHT):
            return safe_area_start + (safe_area_dim - child_dim)

        return safe_area_start
