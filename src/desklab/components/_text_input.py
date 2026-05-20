# fmt: off
from src.desklab.areas import ClickableArea
from src.desklab.system import Mouse, KeyBoard, ClipBoard
from ._text import Color, Text
from typing import Any, Optional, Union, Tuple, Final
import re
import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame import Surface, Rect
# fmt: on


class TextInput(ClickableArea):

    __MINIMUM_WIDTH: Final[int] = 30
    __MINIMUM_HEIGHT: Final[int] = 20

    __TEXT_PROPORTION_RELATIVE_TO_HEIGHT: Final[float] = 0.5

    __LEFT_MARGIN: Final[int] = 10
    __RIGHT_MARGIN: Final[int] = 20

    __SELECTED_AREA_COLOR: tuple[int, int, int] = (173, 216, 230)

    __CURSOR_BLINK_SPEED: Final[float] = 0.5
    __CURSOR_COLOR_TUPLE: tuple[int, int, int] = (0, 0, 0)
    __CURSOR_WIDTH: Final[int] = 2
    __CURSOR_VERTICAL_MARGIN: Final[int] = 5

    def __init__(self,
                 width: int,
                 height: int,
                 corners_radius: Union[Tuple[int, int, int, int], int] = 0,
                 background_color: Union[Color,
                                         Tuple[int, int, int], str] = "WHITE",
                 text_color: Union[Color, Tuple[int, int, int], str] = "BLACK",
                 text_font: str = "arial") -> None:

        super().__init__(width, height, background_color, corners_radius)

        text = Text("", color=text_color, font=text_font)
        text_height = int(height*self.__TEXT_PROPORTION_RELATIVE_TO_HEIGHT)
        self.__text: Text = text.maximize(99999, text_height)

        if isinstance(text_color, Color):
            self.__text_color: Color = text_color
        else:
            self.__text_color: Color = Color(text_color)

        self.__cursor_index: int = 0
        self.__selection_anchor: Optional[int] = None
        self.__is_focused: bool = False

        self.__scroll_offset: int = 0
        self.__last_cursor_toggle: float = time.time()

        self.__last_click_time: float = 0.0
        self.__click_count: int = 0

    def _set_width(self, width: int):
        if width < self.__MINIMUM_WIDTH:
            error = f"ERROR: minimum width for {self.__class__.__name__} is {self.__MINIMUM_WIDTH}"
            raise ValueError(error)
        return super()._set_width(width)

    def _set_height(self, height: int):
        if height < self.__MINIMUM_HEIGHT:
            error = f"ERROR: minimum height for {self.__class__.__name__} is {self.__MINIMUM_HEIGHT}"
            raise ValueError(error)
        return super()._set_height(height)

    def __get_width_up_to_index(self, index: int) -> int:
        sub_text = self.__text.sub(end=index)
        return self.__text.get_font().size(sub_text.get_text())[0]

    def __get_closest_index_from_mouse_pos(self, mouse_x: int) -> int:
        width_up_to_mouse_x: int = mouse_x - self.get_x() + self.__scroll_offset
        best_index: int = 0
        min_distance: float = width_up_to_mouse_x

        for i in range(len(self.__text) + 1):
            width_up_to_index = self.__get_width_up_to_index(i) + \
                self.__LEFT_MARGIN
            distance_to_mouse = abs(width_up_to_mouse_x - width_up_to_index)
            if distance_to_mouse < min_distance:
                min_distance = distance_to_mouse
                best_index = i
            else:
                break

        return best_index

    def handle_event(self, *args: Any, **kwargs: Any) -> None:

        super().handle_event(*args, **kwargs)

        mouse = kwargs.get("mouse")
        keyboard = kwargs.get("keyboard")
        clipboard = kwargs.get("clipboard")

        if not isinstance(mouse, Mouse):
            self._raise_for_missing_parameter("mouse", Mouse.__name__)

        if not isinstance(keyboard, KeyBoard):
            self._raise_for_missing_parameter("keyboard", KeyBoard.__name__)

        if not isinstance(clipboard, ClipBoard):
            self._raise_for_missing_parameter("clipboard", ClipBoard.__name__)

        self.__handle_focus(mouse)
        if not self.__is_focused:
            return

        self.__handle_mouse_drag_selection(mouse)

        if keyboard.any_key_pressed():
            self.__handle_keyboard(keyboard, clipboard)
            self.__reset_cursor_blink()

        self.__update_scroll()

    def __handle_focus(self, mouse: Mouse) -> None:
        if self.is_clicked():
            self.__is_focused = True
            self.__handle_click_logic(mouse)
        elif mouse.is_clicked():
            self.__is_focused = False

    def __handle_mouse_drag_selection(self, mouse: Mouse) -> None:
        if mouse.is_held() and not self.is_clicked() and self.__click_count == 1:
            self.__cursor_index = self.__get_closest_index_from_mouse_pos(
                mouse.get_position()[0])
            if self.__selection_anchor is None:
                self.__selection_anchor = self.__cursor_index

    def __handle_click_logic(self, mouse: Mouse) -> None:
        now: float = time.time()
        idx: int = self.__get_closest_index_from_mouse_pos(
            mouse.get_position()[0])

        if now - self.__last_click_time < 0.4:
            self.__click_count += 1
        else:
            self.__click_count = 1
        self.__last_click_time = now

        if self.__click_count == 1:
            self.__cursor_index = idx
            self.__selection_anchor = idx
        elif self.__click_count == 2:
            self.__select_word_at(idx)
        elif self.__click_count >= 3:
            self.__select_all()

    def __handle_keyboard(self, kb: KeyBoard, cb: ClipBoard) -> None:
        shift_active: bool = kb.shift_active()

        if kb.ctrl_active() or kb.meta_active():
            self.__handle_keyboard_modifiers(kb, cb)
            return
        elif kb.key_down("left"):
            self.__move_cursor_left(shift_active)
        elif kb.key_down("right"):
            self.__move_cursor_right(shift_active)
        elif kb.key_down("backspace"):
            self.__delete_text()
        elif kb.any_text_input() and (text := kb.last_input()):
            self.__insert_text(text)

    def __handle_keyboard_modifiers(self, keyboard: KeyBoard, clipboard: ClipBoard) -> None:
        shift_active = keyboard.shift_active()
        if keyboard.key_down("a"):
            self.__select_all()
        elif keyboard.key_down("c"):
            self.__copy(clipboard)
        elif keyboard.key_down("v"):
            self.__paste(clipboard)
        elif keyboard.key_down("x"):
            self.__cut(clipboard)
        elif keyboard.key_down("left"):
            self.__move_cursor_skipping_word_left(shift_active)
        elif keyboard.key_down("right"):
            self.__move_cursor_skipping_word_right(shift_active)

    def __insert_text(self, string: str) -> None:
        self.__remove_selected_region()
        self.__text = self.__text.sub(end=self.__cursor_index) + \
            string + self.__text.get_text()[self.__cursor_index:]
        self.__cursor_index += len(string)
        self.__selection_anchor = None

    def __delete_text(self) -> None:
        if self.__selection_anchor is not None and self.__selection_anchor != self.__cursor_index:
            self.__remove_selected_region()
        elif self.__cursor_index > 0:
            self.__text = self.__text.sub(end=self.__cursor_index - 1) + \
                self.__text.get_text()[self.__cursor_index:]
            self.__cursor_index -= 1

    def __remove_selected_region(self) -> None:
        if self.__selection_anchor is None or self.__selection_anchor == self.__cursor_index:
            return
        start, end = sorted((self.__selection_anchor, self.__cursor_index))
        self.__text = self.__text.sub(end=start) + self.__text.get_text()[end:]
        self.__cursor_index = start
        self.__selection_anchor = None

    def __move_cursor(self, delta: int, shift_status: bool) -> None:
        self.__update_selection_anchor_based_of_shift_status(shift_status)
        self.__cursor_index = max(
            0, min(len(self.__text), self.__cursor_index + delta))

    def __move_cursor_left(self, shift_status: bool) -> None:
        self.__move_cursor(-1, shift_status)

    def __move_cursor_right(self, shift_status: bool) -> None:
        self.__move_cursor(1, shift_status)

    def __move_cursor_skipping_word_left(self, shift_status: bool) -> None:
        self.__update_selection_anchor_based_of_shift_status(shift_status)
        match = re.search(r'\w\W', self.__text.get_text()
                          [:self.__cursor_index][::-1])
        decrement = match.end() if match else self.__cursor_index
        self.__cursor_index -= decrement

    def __move_cursor_skipping_word_right(self, shift_status: bool) -> None:
        self.__update_selection_anchor_based_of_shift_status(shift_status)
        match = re.search(r'\w\W', self.__text.get_text()
                          [self.__cursor_index:])
        increment = match.end() if match else len(self.__text) - self.__cursor_index
        self.__cursor_index += increment

    def __update_selection_anchor_based_of_shift_status(self, shift: bool) -> None:
        if not shift:
            self.__selection_anchor = None
        elif self.__selection_anchor is None:
            self.__selection_anchor = self.__cursor_index

    def __select_word_at(self, index: int) -> None:
        text_around: str = self.__text.get_text()
        start: int = index
        while start > 0 and text_around[start-1].isalnum():
            start -= 1
        end: int = index
        while end < len(text_around) and text_around[end].isalnum():
            end += 1
        self.__selection_anchor = start
        self.__cursor_index = end

    def __select_all(self) -> None:
        self.__selection_anchor = 0
        self.__cursor_index = len(self.__text)

    def __copy(self, cb: ClipBoard) -> None:
        if self.__selection_anchor is not None:
            start, end = sorted((self.__selection_anchor, self.__cursor_index))
            cb.put_text(self.__text.sub(start, end).get_text())

    def __paste(self, cb: ClipBoard) -> None:
        self.__insert_text(cb.get_text())

    def __cut(self, cb: ClipBoard) -> None:
        self.__copy(cb)
        self.__remove_selected_region()

    def __update_scroll(self) -> None:
        width_up_to_cursor: int = self.__get_width_up_to_index(
            self.__cursor_index)
        total_text_width: int = self.__get_width_up_to_index(
            len(self.__text))
        padding: int = self.__RIGHT_MARGIN
        view_width: int = self.get_width()

        if width_up_to_cursor - self.__scroll_offset > view_width - padding:
            self.__scroll_offset = width_up_to_cursor - view_width + padding

        elif width_up_to_cursor - self.__scroll_offset < padding:
            self.__scroll_offset = max(0, width_up_to_cursor - padding)

        if total_text_width - self.__scroll_offset < view_width:
            self.__scroll_offset = max(
                0, total_text_width - view_width + padding)

    def display(self, screen: Surface) -> None:
        super().display(screen)

        text_area: Rect = Rect(self.get_x(), self.get_y(),
                               self.get_width(), self.get_height())
        old_clip = screen.get_clip()
        screen.set_clip(text_area)

        self.__display_selected_background(screen)
        self.__display_text(screen)
        self.__display_cursor(screen)
        screen.set_clip(old_clip)

    def __display_selected_background(self, screen: Surface) -> None:

        if self.__selection_anchor is None or self.__selection_anchor == self.__cursor_index:
            return
        start_x: int = self.__get_width_up_to_index(
            min(self.__selection_anchor, self.__cursor_index))
        end_x: int = self.__get_width_up_to_index(
            max(self.__selection_anchor, self.__cursor_index))
        sel_rect: Rect = Rect(self.get_x() + self.__LEFT_MARGIN + start_x -
                              self.__scroll_offset, self.get_y(), end_x - start_x,
                              self.get_height())
        pygame.draw.rect(screen, self.__SELECTED_AREA_COLOR, sel_rect)

    def __display_text(self, screen: Surface) -> None:
        font = self.__text.get_font()
        text = self.__text.get_text()
        color = self.__text_color.get_tuple()
        text_surface: Surface = font.render(text, True, color)
        text_surface_x = self.get_x() + self.__LEFT_MARGIN - self.__scroll_offset
        text_surface_y = self.get_y() + (self.get_height() - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_surface_x, text_surface_y))

    def __display_cursor(self, screen: Surface) -> None:
        if not self.__is_focused:
            return
        now: float = time.time()
        time_since_last_toggle = now - self.__last_cursor_toggle
        if int(time_since_last_toggle / self.__CURSOR_BLINK_SPEED) % 2 != 0:
            return
        cursor_x: int = (self.get_x() + self.__LEFT_MARGIN +
                         self.__get_width_up_to_index(self.__cursor_index) -
                         self.__scroll_offset)
        vertical_margin = self.__CURSOR_VERTICAL_MARGIN
        start_pos = (cursor_x, self.get_y() + vertical_margin)
        end_pos = (cursor_x, self.get_y() + self.get_height() -
                   vertical_margin)
        pygame.draw.line(screen, self.__CURSOR_COLOR_TUPLE,
                         start_pos, end_pos, self.__CURSOR_WIDTH)

    def __reset_cursor_blink(self) -> None:
        self.__last_cursor_toggle = time.time()

    def get_text(self) -> str:
        return self.__text.get_text()
