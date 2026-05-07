import os
import pygame


class SoundManager:
    def __init__(self):
        try:
            pygame.mixer.init()
            self.enabled = True
        except pygame.error:
            self.enabled = False

        self.base_path = os.path.join("assets")

        self.button_click = self.load_sound("button_click.wav", 0.5)
        self.puzzle_error = self.load_sound("puzzle_error.wav", 0.5)
        self.puzzle_success = self.load_sound("puzzle_success.wav", 0.5)

    def load_sound(self, filename, volume=1.0):
        if not self.enabled:
            return None

        path = os.path.join(self.base_path, filename)
        if not os.path.exists(path):
            return None

        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(volume)
            return sound
        except pygame.error:
            return None

    def play(self, sound):
        if self.enabled and sound:
            sound.play()

    def play_music(self, filename, volume=0.25, loop=True):
        if not self.enabled:
            return

        path = os.path.join(self.base_path, filename)
        if not os.path.exists(path):
            print(f"Lipsește fișierul: {path}")
            return

        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1 if loop else 0, fade_ms=1000)
        except pygame.error as e:
            print(f"Eroare la redarea muzicii: {e}")


    def stop_music(self):
        if self.enabled:
            pygame.mixer.music.stop()