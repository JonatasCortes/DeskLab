from src.labweb.area import ClickableArea
from src.labweb.containers.protected_flexbox import ProtectedFlexBox


class ClickableFlexBox(ProtectedFlexBox, ClickableArea):

    def copy(self) -> "ClickableFlexBox":
        instance = self._copy()
        assert isinstance(instance, self.__class__)
        return instance
