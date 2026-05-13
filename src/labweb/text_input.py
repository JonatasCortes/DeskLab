import pygame
import time
import re
from typing import Any, Optional, Union, Tuple
from pygame import Surface, Rect
from src.labweb.color import Color
from src.labweb.system.mouse import Mouse
from src.labweb.system.keyboard import KeyBoard
from src.labweb.system.clipboard import ClipBoard
from src.labweb.area import ClickableArea
from src.labweb.text import Text


class TextInput(ClickableArea):
    def __init__(self,
                 width: int,
                 height: int,
                 corners_radius: Union[Tuple[int, int, int, int], int] = 0,
                 background_color: Union[Color,
                                         Tuple[int, int, int], str] = "WHITE",
                 text_color: Union[Color, Tuple[int, int, int], str] = "BLACK") -> None:

        super().__init__(width, height, background_color, corners_radius)

        text = Text("", color=text_color, font="arial")
        self.__text: Text = text.maximize(99999, int(height*0.5))

        if isinstance(text_color, Color):
            self.__text_color: Color = text_color
        else:
            self.__text_color: Color = Color(text_color)

        # Índices e Seleção
        self.__cursor_index: int = 0
        self.__selection_anchor: Optional[int] = None
        self.__is_focused: bool = False

        # Visual e Scroll
        self.__scroll_offset: int = 0
        self.__last_cursor_toggle: float = time.time()
        self.__cursor_blink_speed: float = 0.5

        # Timers para cliques múltiplos
        self.__last_click_time: float = 0.0
        self.__click_count: int = 0

    def _set_width(self, width: int):
        if width < 30:
            error = f"ERROR: minimum width for {self.__class__.__name__} is {30}"
            raise ValueError(error)
        return super()._set_width(width)

    def _set_height(self, height: int):
        if height < 20:
            error = f"ERROR: minimum height for {self.__class__.__name__} is {20}"
            raise ValueError(error)
        return super()._set_height(height)

    def __get_x_at_index(self, index: int) -> int:
        substring: str = self.__text.get_text()[:index]
        return self.__text.get_font().size(substring)[0]

    def __get_index_from_pos(self, mouse_x: int) -> int:
        """Retorna o índice do caractere mais próximo da posição X do mouse."""
        relative_x: int = mouse_x - self.get_x() + self.__scroll_offset

        best_index: int = 0
        min_diff: float = float('inf')

        for i in range(len(self.__text.get_text()) + 1):
            char_x: int = self.__get_x_at_index(i)
            diff: float = abs(char_x - relative_x)
            if diff < min_diff:
                min_diff = diff
                best_index = i
        return best_index

    def handle_event(self, *args: Any, **kwargs: Any) -> None:

        super().handle_event(*args, **kwargs)

        mouse = kwargs.get("mouse")
        keyboard = kwargs.get("keyboard")
        clipboard = kwargs.get("clipboard")

        if not isinstance(mouse, Mouse) or not isinstance(keyboard, KeyBoard) or not isinstance(clipboard, ClipBoard):
            raise RuntimeError(f"Expected a {Mouse.__name__} instance in kwargs with key 'mouse'",
                               f"Expected a {KeyBoard.__name__} instance in kwargs with key 'keyboard'",
                               f"Expected a {ClipBoard.__name__} instance in kwargs with key 'clipboard'")

        if not all([mouse, keyboard, clipboard]):
            return

        # 1. Gerenciar Foco
        if self.is_clicked():
            self.__is_focused = True
            self.__handle_click_logic(mouse)
        elif mouse.is_clicked():
            self.__is_focused = False

        if not self.__is_focused:
            return

        # 2. Seleção via Mouse (Drag)
        if mouse.is_held() and not self.is_clicked():
            self.__cursor_index = self.__get_index_from_pos(
                mouse.get_position()[0])
            if self.__selection_anchor is None:
                self.__selection_anchor = self.__cursor_index

        # 3. Teclado
        if keyboard.any_key_pressed():
            self.__handle_keyboard(keyboard, clipboard)
            self.__reset_cursor_blink()

        self.__update_scroll()

    def __handle_click_logic(self, mouse: Mouse) -> None:
        now: float = time.time()
        idx: int = self.__get_index_from_pos(mouse.get_position()[0])

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
            if kb.key_down("a"):
                self.__select_all()
            elif kb.key_down("c"):
                self.__copy(cb)
            elif kb.key_down("v"):
                self.__paste(cb)
            elif kb.key_down("x"):
                self.__cut(cb)
            elif kb.key_down("left"):
                self.__move_cursor_word(-1, shift_active)
            elif kb.key_down("right"):
                self.__move_cursor_word(1, shift_active)
            return

        if kb.key_down("left"):
            self.__move_cursor(-1, shift_active)
        elif kb.key_down("right"):
            self.__move_cursor(1, shift_active)
        elif kb.key_down("backspace"):
            self.__delete_text()
        elif kb.any_text_input() and (text := kb.last_input()):
            self.__insert_text(text)

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

    def __move_cursor(self, delta: int, shift: bool) -> None:
        if not shift:
            self.__selection_anchor = None
        elif self.__selection_anchor is None:
            self.__selection_anchor = self.__cursor_index

        self.__cursor_index = max(
            0, min(len(self.__text), self.__cursor_index + delta))

    def __move_cursor_word(self, direction: int, shift: bool) -> None:
        if not shift:
            self.__selection_anchor = None
        elif self.__selection_anchor is None:
            self.__selection_anchor = self.__cursor_index

        if direction > 0:
            match = re.search(r'\w\W', self.__text.get_text()
                              [self.__cursor_index:])
            self.__cursor_index += (match.end()
                                    if match else len(self.__text) - self.__cursor_index)
        else:
            match = re.search(r'\w\W', self.__text.get_text()
                              [:self.__cursor_index][::-1])
            self.__cursor_index -= (match.end()
                                    if match else self.__cursor_index)

    def __select_word_at(self, index: int) -> None:
        # Busca limites de espaços ou pontuação ao redor do índice
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
            cb.put_text(self.__text.sub(start, end))

    def __paste(self, cb: ClipBoard) -> None:
        self.__insert_text(cb.get_text())

    def __cut(self, cb: ClipBoard) -> None:
        self.__copy(cb)
        self.__remove_selected_region()

    def __update_scroll(self) -> None:
        cursor_x: int = self.__get_x_at_index(self.__cursor_index)
        total_text_width: int = self.__get_x_at_index(
            len(self.__text.get_text()))
        padding: int = 20
        view_width: int = self.get_width()

        if cursor_x - self.__scroll_offset > view_width - padding:
            self.__scroll_offset = cursor_x - view_width + padding

        elif cursor_x - self.__scroll_offset < padding:
            self.__scroll_offset = max(0, cursor_x - padding)

        if total_text_width - self.__scroll_offset < view_width:
            self.__scroll_offset = max(
                0, total_text_width - view_width + padding)

    def display(self, screen: Surface) -> None:
        super().display(screen)

        margin_x = 10

        # Clip para evitar que o texto vaze o container
        text_area: Rect = Rect(self.get_x(), self.get_y(),
                               self.get_width(), self.get_height())
        old_clip: Optional[Rect] = screen.get_clip()
        screen.set_clip(text_area)

        # Desenhar Seleção
        if self.__selection_anchor is not None and self.__selection_anchor != self.__cursor_index:
            start_x: int = self.__get_x_at_index(
                min(self.__selection_anchor, self.__cursor_index))
            end_x: int = self.__get_x_at_index(
                max(self.__selection_anchor, self.__cursor_index))
            sel_rect: Rect = Rect(self.get_x() + margin_x + start_x - self.__scroll_offset,
                                  self.get_y(), end_x - start_x, self.get_height())
            pygame.draw.rect(screen, (173, 216, 230), sel_rect)

        # Desenhar Texto Principal
        text_surf: Surface = self.__text.get_font().render(
            self.__text.get_text(), True, self.__text_color.get_tuple())
        screen.blit(text_surf, (self.get_x() + margin_x - self.__scroll_offset,
                    self.get_y() + (self.get_height() - text_surf.get_height()) // 2))

        # Desenhar Cursor
        if self.__is_focused:
            now: float = time.time()
            if int((now - self.__last_cursor_toggle) / self.__cursor_blink_speed) % 2 == 0:
                cx: int = self.get_x() + margin_x + self.__get_x_at_index(self.__cursor_index) - \
                    self.__scroll_offset
                pygame.draw.line(screen, (0, 0, 0), (cx, self.get_y(
                ) + 5), (cx, self.get_y() + self.get_height() - 5), 2)

        screen.set_clip(old_clip)

    def __reset_cursor_blink(self) -> None:
        self.__last_cursor_toggle = time.time()

    def get_text(self) -> str:
        """Requisito da Issue: Permitir ao desenvolvedor recuperar o texto a qualquer momento."""
        return self.__text.get_text()
