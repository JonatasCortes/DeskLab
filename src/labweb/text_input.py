from typing import Any, Optional
from src.labweb.entities import Entity
from src.labweb.text import Text
from src.labweb.color import Color
from src.labweb.containers.flexbox.clickable_flexbox import ClickableFlexBox
from src.labweb.containers.flexbox.flexbox import FlexBox
from src.labweb.system_input.mouse import Mouse
from src.labweb.system_input.keyboard import KeyBoard


class _TextInputCell(FlexBox):

    def __init__(self, value: str | Text, max_width: int, max_height: int, background_color: Color | tuple[int, int, int] | str, text_color: Color | tuple[int, int, int] | str) -> None:
        text = value if isinstance(value, Text) else Text(value,
                                                          color=text_color)
        text = text.maximize(max_width, max_height)
        super().__init__(text.get_width(), text.get_height(), 0, 0, "ROW",
                         "CENTER", "CENTER", 0, background_color, True)
        self.add(text)


class _TextInputContainer(FlexBox):

    def __init__(self,
                 width: int,
                 height: int,
                 corners_radius: tuple[int, int, int, int] | int,
                 color: Color | tuple[int, int, int] | str,
                 text_color: Color | tuple[int, int, int] | str) -> None:

        super().__init__(width, height, 0, 0, "ROW", "LEFT",
                         "CENTER", corners_radius, color, True)
        self.set_text_color(text_color)

    def set_text_color(self, color: Color | tuple[int, int, int] | str):
        self.__text_color = color if isinstance(color, Color) else Color(color)

    def get_text_color(self) -> Color:
        return self.__text_color

    def add_cell(self, text: str) -> None:
        cell = _TextInputCell(text, self.get_width(),
                              self.get_height(),
                              self.get_color(),
                              self.get_text_color())
        self.add(cell)

    def force_cell_append(self, text: str):
        while True:
            try:
                self.add_cell(text)
                return
            except ValueError:
                new_cells_list = self.get_children()[1::]
                self.set_children(new_cells_list)

    def delete_last_word(self):
        while len(self.get_children()) > 0:
            removed_cell = self.pop()
            char = self.__retrieve_character_from_cell(removed_cell)
            if char == " ":
                break

    def __retrieve_character_from_cell(self, cell: Optional[Entity]) -> Optional[str]:
        if not isinstance(cell, _TextInputCell):
            return

        removed_text_instance = cell.pop()
        if not isinstance(removed_text_instance, Text):
            return

        return removed_text_instance.get_text()


class TextInput(ClickableFlexBox):

    __HORIZONTAL_PADDING_PERCENTAGE = 5
    __VERTICAL_PADDING_PERCENTAGE = 33

    def __init__(self,
                 width: int,
                 height: int,
                 corners_radius: tuple[int, int, int, int] | int = 0,
                 background_color: Color | tuple[int,
                                                 int, int] | str = "WHITE",
                 text_color: Color | tuple[int, int, int] | str = "BLACK") -> None:

        super().__init__(width, height, 0, 0, "ROW", "CENTER", "CENTER",
                         corners_radius, background_color, True)
        self.__set_text_container(text_color)
        self.__is_focused = False
        self.__text = ""

    def is_focused(self) -> bool:
        return self.__is_focused

    def __set_text_container(self, text_color: Color | tuple[int, int, int] | str) -> None:
        self.__text_container = _TextInputContainer(self.get_width() - self.__calcuate_horizontal_padding(),
                                                    self.get_height() - self.__calculate_vertical_padding(),
                                                    self.get_corners_radius(), self.get_color(), text_color)
        self._add(self.__text_container)

    def __calcuate_horizontal_padding(self) -> int:
        return self.__HORIZONTAL_PADDING_PERCENTAGE*self.get_width()//100

    def __calculate_vertical_padding(self) -> int:
        return self.__VERTICAL_PADDING_PERCENTAGE*self.get_height()//100

    def handle_event(self, *args: Any, **kwargs: Any):
        super().handle_event(*args, **kwargs)
        mouse = kwargs.get("mouse")
        keyboard = kwargs.get("keyboard")
        if not isinstance(mouse, Mouse) or not isinstance(keyboard, KeyBoard):
            raise ValueError(f"Expected a {Mouse.__name__} instance in kwargs with key 'mouse'",
                             f"Expected a {KeyBoard.__name__} instance in kwwargs with key 'keyboard'")
        self.__add_focus_listener(mouse)
        self.__add_typing_listener(keyboard)
        self.__add_delete_listener(keyboard)

    def __add_focus_listener(self, mouse: Mouse):
        if self.is_clicked():
            self.__is_focused = True
            return
        elif mouse.is_clicked():
            self.__is_focused = False

    def __add_typing_listener(self, keyboard: KeyBoard):
        if not self.is_focused():
            return
        if keyboard.any_text_input():
            text = keyboard.last_input()
            if not text:
                return
            self.__text_container.force_cell_append(text)

    def __add_delete_listener(self, keyboard: KeyBoard):

        if not self.is_focused() or not keyboard.key_down("backspace"):
            return

        if not keyboard.ctrl_active() and not keyboard.meta_active():
            self.__text_container.pop()
            return

        self.__text_container.delete_last_word()
