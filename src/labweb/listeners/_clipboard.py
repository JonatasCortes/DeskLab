from src.labweb.system import ClipBoard
from ._system_listener import SystemListener


class _ClipBoardListener(SystemListener):
    _system_input_class = ClipBoard


class ClipBoardTextListener(_ClipBoardListener):
    _condition_function = "has_text"


class ClipBoardFilesListener(_ClipBoardListener):
    _condition_function = "has_files"


class ClipBoardImageListener(_ClipBoardListener):
    _condition_function = "has_image"
