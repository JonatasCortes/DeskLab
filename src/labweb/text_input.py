from typing import Any, Optional
from src.labweb.entities import Entity
from src.labweb.text import Text
from src.labweb.color import Color
from src.labweb.containers.protected_flexslot import ProtectedFlexSlot
from src.labweb.containers.flexbox import FlexBox
from src.labweb.containers.clickable_flexbox import ClickableFlexBox
from src.labweb.system_input.mouse import Mouse
from src.labweb.system_input.keyboard import KeyBoard


class _TextInputCell(ClickableFlexBox):

    def __init__(self, value: str | Text, max_width: int, max_height: int, background_color: Color | tuple[int, int, int] | str, text_color: Color | tuple[int, int, int] | str) -> None:
        text = value if isinstance(value, Text) else Text(value,
                                                          color=text_color)
        text = text.maximize(max_width, max_height)
        super().__init__(text.get_width(), text.get_height(), 0, 0, "ROW",
                         "CENTER", "CENTER", 0, background_color, 0, True)
        self.add(text)


class TextInput(ProtectedFlexSlot):

    __HORIZONTAL_PADDING_PERCENTAGE = 5
    __VERTICAL_PADDING_PERCENTAGE = 33

    def __init__(self,
                 width: int,
                 height: int,
                 corners_radius: tuple[int, int, int, int] | int = 0,
                 background_color: Color | tuple[int,
                                                 int, int] | str = "WHITE",
                 text_color: Color | tuple[int, int, int] | str = "BLACK") -> None:

        super().__init__(width, height, 0, "CENTER", "CENTER",
                         corners_radius, background_color, True)
        self.set_text_color(text_color)
        self.__is_focused = False
        self.__text = ""
        self.__set_text_container()

    def is_focused(self) -> bool:
        return self.__is_focused

    def set_text_color(self, color: Color | tuple[int, int, int] | str = "BLACK"):
        self.__text_color = color if isinstance(color, Color) else Color(color)

    def get_text_color(self) -> Color:
        return self.__text_color

    def __set_text_container(self, ) -> None:
        self.__text_container = FlexBox(self.get_width() - self.__calcuate_horizontal_padding(),
                                        self.get_height() - self.__calculate_vertical_padding(),
                                        0, 0, "ROW", "LEFT", "CENTER", self.get_corners_radius(),
                                        self.get_color(), True)
        self._add(self.__text_container)

    def __calcuate_horizontal_padding(self) -> int:
        return self.__HORIZONTAL_PADDING_PERCENTAGE*self.get_width()//100

    def __calculate_vertical_padding(self) -> int:
        return self.__VERTICAL_PADDING_PERCENTAGE*self.get_height()//100

    def handle_event(self, *args: Any, **kwargs: Any):
        mouse = kwargs.get("mouse")
        keyboard = kwargs.get("keyboard")
        if not isinstance(mouse, Mouse) or not isinstance(keyboard, KeyBoard):
            raise ValueError(f"Expected a {Mouse.__name__} instance in kwargs with key 'mouse'",
                             f"Expected a {KeyBoard.__name__} instance in kwwargs with key 'keyboard'")
        self.__add_focus_listener(mouse)
        self.__add_typing_listener(keyboard)
        self.__add_delete_listener(keyboard)

    def __add_focus_listener(self, mouse: Mouse):
        if not mouse.is_clicked():
            return
        if self.contains(mouse.get_position()):
            self.__is_focused = True
            return
        self.__is_focused = False

    def __add_typing_listener(self, keyboard: KeyBoard):
        if not self.is_focused():
            return
        if keyboard.any_text_input():
            text = keyboard.last_input()
            if not text:
                return
            self.__text += text
            cell = _TextInputCell(text, self.__text_container.get_width(),
                                  self.__text_container.get_height(),
                                  self.get_color(), self.get_text_color())
            self.__text_container.add(cell)

    def __add_delete_listener(self, keyboard: KeyBoard):

        if not self.is_focused() or not keyboard.key_down("backspace"):
            return

        if not keyboard.ctrl_active() and not keyboard.meta_active():
            self.__text_container.pop()
            return

        removed_cell = self.__text_container.pop()
        removed_character = self.__retrieve_character_from_cell(removed_cell)

        while removed_character != " ":
            removed_cell = self.__text_container.pop()
            removed_character = self.__retrieve_character_from_cell(
                removed_cell)
            if removed_character is None:
                return

    def __retrieve_character_from_cell(self, cell: Optional[Entity]) -> Optional[str]:
        if not isinstance(cell, _TextInputCell):
            return

        removed_text_instance = cell.pop()
        if not isinstance(removed_text_instance, Text):
            return

        return removed_text_instance.get_text()
