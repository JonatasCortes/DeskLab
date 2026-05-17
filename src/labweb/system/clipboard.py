import pygame
import numpy as np
import io
import os
import sys
import pyperclip
import subprocess
import tempfile
from urllib.parse import quote
from PIL import Image as PilImage
from typing import Optional, List, Final, no_type_check
from src.labweb.system.system_listener import SystemListener
from src.labweb.primitives.text import Text
from src.labweb.primitives.image import Image
from typing import no_type_check
from abc import ABC, abstractmethod


class _ClipBoardBackend(ABC):

    _TEXT_FORMAT: Final = pygame.SCRAP_TEXT
    _FILE_FORMAT: Final = "text/uri-list" if os.name != 'nt' else "FileNameW"
    _BMP_FORMAT: Final = "image/bmp"

    def __raise_not_implemented_error(self, method_name: str) -> None:
        error = f"method '{method_name}' can't be called directly from {self.__class__.__name__}"
        raise NotImplementedError(error)

    def has_text(self) -> bool:
        if pyperclip.paste():
            return True
        return pygame.scrap.contains(self._TEXT_FORMAT)

    @abstractmethod
    def has_files(self) -> bool:
        self.__raise_not_implemented_error("has_files")

    @abstractmethod
    def has_image(self) -> bool:
        self.__raise_not_implemented_error("has_image")

    def put_text(self, text: str | Text) -> None:
        content = text.get_text() if isinstance(text, Text) else text
        try:
            pygame.scrap.put(self._TEXT_FORMAT, content.encode('utf-8'))
        except pygame.error:
            pass
        finally:
            pyperclip.copy(content)

    @abstractmethod
    def put_files(self, file_paths: List[str]) -> None:
        self.__raise_not_implemented_error("put_files")

    @abstractmethod
    def put_image(self, image: np.ndarray) -> None:
        self.__raise_not_implemented_error("put_image")

    def get_text(self) -> str:
        text = pyperclip.paste()
        if text:
            return text

        data = pygame.scrap.get(self._TEXT_FORMAT)
        if data:
            return data.decode('utf-8').rstrip('\x00')
        return ""

    @abstractmethod
    def get_files(self) -> List[str]:
        self.__raise_not_implemented_error("get_files")

    @abstractmethod
    def get_image(self) -> Optional[Image]:
        self.__raise_not_implemented_error("get_image")

    @abstractmethod
    def clear(self) -> None:
        self.__raise_not_implemented_error("clear")

    def _search_paths_within_clipboard_text(self) -> list[str]:
        text_content = self.get_text()
        lines = text_content.splitlines()
        potential_paths = [l.strip()
                           for l in lines if os.path.exists(l.strip())]
        return potential_paths if potential_paths else []


class _DefaultClipBoardBackend(_ClipBoardBackend):

    def has_files(self) -> bool:
        return pygame.scrap.contains(self._FILE_FORMAT)

    def has_image(self) -> bool:
        if pygame.scrap.contains(self._BMP_FORMAT):
            return True
        return False

    def put_files(self, file_paths: List[str]) -> None:
        uris: List[str] = []
        for path in file_paths:
            abs_path = os.path.abspath(path)
            encoded_path = quote(abs_path.replace("\\", "/"))
            if not encoded_path.startswith("/"):
                encoded_path = "/" + encoded_path
            uris.append(f"file://{encoded_path}")

        data = "\r\n".join(uris).encode('utf-8')
        pygame.scrap.put(self._FILE_FORMAT, data)
        self.put_text("\n".join(file_paths))

    def put_image(self, image: np.ndarray) -> None:
        temp_surface = pygame.surfarray.make_surface(image)
        image_buffer = io.BytesIO()
        pygame.image.save(temp_surface, image_buffer, "BMP")
        pygame.scrap.put(self._BMP_FORMAT, image_buffer.getvalue())

    def get_files(self) -> List[str]:
        data = pygame.scrap.get(self._FILE_FORMAT)
        if not data:
            return self._search_paths_within_clipboard_text()

        raw_list = data.decode(
            'utf-8', errors='ignore').rstrip('\x00').splitlines()
        paths: List[str] = []
        for line in raw_list:
            if "file://" in line:
                paths.append(self.__normaliza_file_path(line))
        return paths

    def __normaliza_file_path(self, path: str) -> str:
        path = path.split("file://")[-1].strip()
        if os.name == 'nt' and path.startswith("/") and ":" in path:
            path = path[1:]
        return path

    def get_image(self) -> Optional[Image]:
        data = pygame.scrap.get(self._BMP_FORMAT)
        if not data:
            return None
        try:
            image_buffer = io.BytesIO(data)
            surface = pygame.image.load(image_buffer)
            array = pygame.surfarray.array3d(surface)
            array_for_init = np.transpose(array, (1, 0, 2))
            return Image(image=array_for_init)
        except pygame.error:
            return None

    def clear(self) -> None:
        pygame.scrap.put(self._TEXT_FORMAT, b"")
        pyperclip.copy("")


class _MacOsClipBoardBackend(_ClipBoardBackend):

    @no_type_check
    def __init__(self) -> None:
        from AppKit import NSPasteboard, NSPasteboardTypeTIFF  # type: ignore
        from Foundation import NSURL  # type: ignore

        self.__paste_board = NSPasteboard
        self.__paste_board_type = NSPasteboardTypeTIFF

    @no_type_check
    def has_files(self) -> bool:
        try:
            pb = self.__paste_board.generalPasteboard()

            file_types = ["NSFilenamesPboardType",
                          "public.file-url"]

            return any(pb.availableTypeFromArray_([t]) is not None
                       for t in file_types)
        except Exception:
            return False

    @no_type_check
    def has_image(self) -> bool:
        pb = self.__paste_board.generalPasteboard()
        return pb.availableTypeFromArray_([self.__paste_board_type]) is not None

    def put_files(self, file_paths: List[str]) -> None:
        abs_paths = [os.path.abspath(p).replace('"', '\\"')
                     for p in file_paths]
        paths_string = '{"' + '", "'.join(abs_paths) + '"}'

        script = f'''
            set posixPaths to {paths_string}
            set fileList to {{}}
            repeat with aPath in posixPaths
                set end of fileList to (POSIX file aPath) as alias
            end repeat
            tell application "Finder"
                set the clipboard to fileList
            end tell
            '''

        try:
            subprocess.run(["osascript", "-e", script], check=True)
            pyperclip.copy("\n".join(file_paths))
        except subprocess.CalledProcessError as e:
            print(f"Unable to copy files into MacOS clipboard: {e}")

    def put_image(self, image: np.ndarray) -> None:
        img = PilImage.fromarray(np.transpose(image, (1, 0, 2)))
        with tempfile.NamedTemporaryFile(suffix=".tiff", delete=False) as f:
            temp_file = f.name

        try:
            img.save(temp_file, format="TIFF")
            script = f'set the clipboard to (read POSIX file "{temp_file}" as TIFF picture)'
            subprocess.run(["osascript", "-e", script], check=True)
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    @no_type_check
    def get_files(self) -> List[str]:
        try:
            pb = self.__paste_board.generalPasteboard()
            paths = pb.propertyListForType_("NSFilenamesPboardType")
            if paths:
                return list(paths)
            return []
        except Exception:
            return self._search_paths_within_clipboard_text()

    @no_type_check
    def get_image(self) -> Optional[Image]:
        try:
            pasteboard = self.__paste_board.generalPasteboard()
            data = pasteboard.dataForType_(self.__paste_board_type)
            if data is None:
                return None
            image_bytes = bytes(data)
            image_buffer = io.BytesIO(image_bytes)
            pil_image = PilImage.open(image_buffer).convert("RGB")
            array = np.array(pil_image)
            return Image(image=array)
        except Exception:
            return None

    def clear(self) -> None:
        pyperclip.copy("")
        args = ["osascript", "-e", 'set the clipboard to ""']
        subprocess.run(args, check=False)


class ClipBoard(SystemListener):

    def __init__(self) -> None:
        if not pygame.scrap.get_init():
            pygame.scrap.init()
        self.__set_backend()

    def __set_backend(self) -> None:
        if sys.platform == "darwin":
            self.__backend = _MacOsClipBoardBackend()
        else:
            self.__backend = _DefaultClipBoardBackend()

    def has_text(self) -> bool:
        return self.__backend.has_text()

    def has_files(self) -> bool:
        return self.__backend.has_files()

    def has_image(self) -> bool:
        return self.__backend.has_image()

    def put_text(self, text: str | Text) -> None:
        self.__backend.put_text(text)

    def put_files(self, files: str | list[str]) -> None:
        if isinstance(files, str):
            files = [files]
        self.__backend.put_files(files)

    def put_image(self, image: str | np.ndarray | Image) -> None:
        if isinstance(image, str):
            image = Image(image)
        if isinstance(image, Image):
            image = image.get_matrix()

        if image.ndim == 3 and image.shape[-1] == 4:
            image = image[:, :, :3]

        self.__backend.put_image(image)

    def get_text(self) -> str:
        return self.__backend.get_text()

    def get_files(self) -> list[str]:
        return self.__backend.get_files()

    def get_image(self) -> Optional[Image]:
        return self.__backend.get_image()

    def clear(self) -> None:
        self.__backend.clear()
