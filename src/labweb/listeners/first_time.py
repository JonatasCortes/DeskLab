from src.labweb.listeners.interface import Listener
from src.labweb.listeners.protected_first_time import ProtectedFirstTimeListener


class FirstTimeListener(ProtectedFirstTimeListener, Listener):
    pass
