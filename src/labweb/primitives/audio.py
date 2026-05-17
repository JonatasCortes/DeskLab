import pygame
from io import BytesIO
from imageio_ffmpeg import get_ffmpeg_exe  # type: ignore
import subprocess
from src.labweb.entities.entity import Entity


class Audio(Entity):

    def __init__(self, audio: str | BytesIO) -> None:
        self.set(audio)

    def set(self, sound_effect: str | BytesIO, volume: float | None = None):
        if isinstance(sound_effect, str):
            sound_effect = self.__convert_to_wav(sound_effect)
        try:
            self.__sound = pygame.mixer.Sound(sound_effect)
            if volume:
                self.__sound.set_volume(volume)
        except pygame.error as e:
            error = f"ERROR: Unnable to resolve sound effect file. {e}"
            raise RuntimeError(error)

    def play(self):
        self.__sound.play()

    def __convert_to_wav(self, sound_effect: str) -> BytesIO:
        ffmpeg = get_ffmpeg_exe()

        process = subprocess.run([ffmpeg, "-i", sound_effect, "-ac", "1",
                                  "-ar", "16000", "-sample_fmt", "s16",
                                  "-f", "wav", "-"],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.DEVNULL,
                                 check=True)

        wav_buffer = BytesIO(process.stdout)
        wav_buffer.seek(0)
        return wav_buffer
