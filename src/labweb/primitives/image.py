from src.labweb.entities.displayable import DisplayableEntity
from src.labweb.entities.containable import ContainableEntity
from src.labweb.entities.copiable import CopiableEntity
import numpy as np
from PIL import Image as PilImage
from pygame import Surface
import pygame


class Image(DisplayableEntity, ContainableEntity, CopiableEntity):

    def __init__(self, image: str | np.ndarray) -> None:
        self.__set_image_surface(image)
        super().__init__(width=self.get_matrix().shape[0],
                         height=self.get_matrix().shape[0])

    def get_matrix(self) -> np.ndarray: return self.__image_matrix

    def __extract_image_data_from_path(self, image_path: str) -> np.ndarray:
        if not image_path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
            raise ValueError(f"Unsupported file format: {image_path}")

        img = PilImage.open(image_path).convert("RGB")
        return np.array(img)

    def __set_image_surface(self, image: str | np.ndarray) -> None:

        if isinstance(image, str):
            image = self.__extract_image_data_from_path(image)

        if image.ndim != 3 or image.shape[2] != 3:
            raise ValueError("Image must be RGB (H, W, 3)")

        image = np.transpose(image, (1, 0, 2))
        image = np.ascontiguousarray(image)

        self.__image_matrix = image
        self.__image_surface = pygame.surfarray.make_surface(image)

    def rescale(self, width: int, height: int) -> None:
        self.__image_surface = pygame.transform.scale(
            self.__image_surface, (width, height))
        self._set_width(width)
        self._set_height(height)

    def display(self, screen: Surface) -> None:
        screen.blit(self.__image_surface, (self.get_x(), self.get_y()))

    def copy(self) -> "Image":
        return self.__class__(self.get_matrix().copy())
