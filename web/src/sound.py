try:
    import pygame
    _SOUND_AVAILABLE = True
except Exception:
    pygame = None
    _SOUND_AVAILABLE = False


class Sound:

    def __init__(self, path):
        self.path = path
        self.sound = None
        if _SOUND_AVAILABLE:
            try:
                # Create sound object when pygame is available
                self.sound = pygame.mixer.Sound(path)
            except Exception:
                self.sound = None

    def play(self):
        if _SOUND_AVAILABLE and self.sound:
            try:
                pygame.mixer.Sound.play(self.sound)
            except Exception:
                pass