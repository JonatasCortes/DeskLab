from src.desklab.system import Mouse
from ._system_listener import SystemListener


class _MouseListener(SystemListener):
    _system_input_class = Mouse


class MouseClickListener(_MouseListener):
    _condition_function = "is_clicked"


class MouseHoldListener(_MouseListener):
    _condition_function = "is_held"


class MouseReleaseListener(_MouseListener):
    _condition_function = "is_released"


class MouseMotionListener(_MouseListener):
    _condition_function = "is_moving"


class FileDropListener(_MouseListener):
    _condition_function = "is_dropping_file"
