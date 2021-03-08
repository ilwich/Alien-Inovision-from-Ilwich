import pygame
from pygame.sprite import Sprite
import  random

class Star(Sprite):
    #"""Класс, представляющий одну звезду."""

    def __init__(self, ai_game):
        #"""Инициализирует звезду и задает её начальную позицию."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # Загрузка изображения звезды и назначение атрибута rect.
        self.image = pygame.image.load('images/star.bmp')
        self.rect = self.image.get_rect()
        # Каждая новая звезда появляется в левом верхнем углу экрана.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # Сохранение точной горизонтальной позиции звезды.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def check_edges(self):
        """Возвращает True, если звезда находится у края экрана."""
        screen_rect = self.screen.get_rect()
        if self.rect.bottom >= screen_rect.bottom:
            return True

    def update(self):
        # """Перемещает звезду вниз"""
        self.y += self.settings.university_drop_speed
        self.rect.y = self.y
