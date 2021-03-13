import pygame
from pygame.sprite import Sprite

class Bossstation(Sprite):
    #"""Класс, представляющий станцию боса."""

    def __init__(self, ai_game):
        #"""Инициализирует станцию и задает его начальную позицию."""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.explois_sound = pygame.mixer.Sound('sounds/Explosion3.wav')
        # Загрузка изображения станции и назначение атрибута rect.
        self.image = pygame.image.load('images/bossstation.bmp')
        self.image_explois = pygame.image.load('images/ship_destroy.bmp')
        self.is_explois = 0
        self.rect = self.image.get_rect()
        # Каждый новый босс появляется в центре экрана.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery
        # Сохранение точной горизонтальной позиции боса.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        # Точки размещения башен
        self.turrel_list = [(210, 300), (390, 300), ]

    def check_edges(self):
        """Возвращает True, если босс находится у краев экрана."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.x <= -10:
            return True

    def _explois(self):
        """Отрисовываем взрыв"""
        rect_explois = self.image_explois.get_rect()
        rect_explois.center = (self.rect.width / 2, self.rect.height / 2)
        self.image.blit(self.image_explois, rect_explois)


    def update(self):
        """Перемещает станции вправо и вниз."""
        self.x += (self.settings.alien_speed * 0.2 * self.settings.boss_direction_x)
        self.rect.x = self.x
        self.rect.y = self.y
        if self.is_explois >= 1:
            self._explois()
            self.is_explois += 1

    def blitme(self):
        #"""Рисует станцию в текущей позиции."""
        self.screen.blit(self.image, self.rect)


