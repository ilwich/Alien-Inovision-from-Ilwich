import pygame
from pygame.sprite import Sprite

class Star(Sprite):
    #"""Класс, представляющий одну звезду."""

    def __init__(self, ai_game):
        #"""Инициализирует звезду и задает её начальную позицию."""
        super().__init__()
        self.screen = ai_game.screen
        # Загрузка изображения звезды и назначение атрибута rect.
        self.image = pygame.image.load('images/star.bmp')
        self.rect = self.image.get_rect()
        # Каждая новая звезда появляется в левом верхнем углу экрана.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # Сохранение точной горизонтальной позиции звезды.
        self.x = float(self.rect.x)