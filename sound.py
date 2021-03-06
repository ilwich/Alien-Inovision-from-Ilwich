import pygame
import random
from os import path

class Sound():
    """Класс для хранения звуковых эффектов игры Alien Invasion."""
    def __init__(self):
        self.snd_dir = path.join(path.dirname(__file__), 'sounds')
        # Загрузка мелодий игры
        self.shoot_sound = pygame.mixer.Sound(path.join(self.snd_dir, 'Laser_Shoot5.wav'))

    def sound_play(self):
        """Проигрывание выстрела"""
        self.play()