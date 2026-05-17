from src.labweb.listeners.interface import Listener
from src.labweb.listeners.protected_change import ProtectedChangeListener


class ChangeListener(ProtectedChangeListener, Listener):
    pass
