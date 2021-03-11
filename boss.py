import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2

class Boss(Sprite):
    #"""Класс, представляющий одного боса."""

    def __init__(self, ai_game):
        #"""Инициализирует боса и задает его начальную позицию."""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.explois_sound = pygame.mixer.Sound('sounds/Explosion3.wav')
        # Загрузка изображения боса и назначение атрибута rect.
        self.image_norm = pygame.image.load('images/turrel.bmp')
        self.rect_norm = self.image_norm.get_rect()
        self.image = self.image_norm
        self.image_explois = pygame.image.load('images/explois.bmp')
        self.is_explois = 0
        self.rect = self.image.get_rect()
        # Каждый новый босс появляется в центре экрана.
        self.rect.x = self.screen_rect.centerx
        self.rect.y = self.screen_rect.centery

        # Сохранение точной горизонтальной позиции боса.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.x_aim = ai_game.ship.rect.x
        self.y_aim = ai_game.ship.rect.y

    def check_edges(self):
        """Возвращает True, если босс находится у края экрана."""
        screen_rect = self.screen.get_rect()
        if self.rect.bottom >= screen_rect.bottom:
            return True
        if self.rect.right >= screen_rect.right:
            return True
        if self.rect.x <= -10 or self.rect.y <= -10:
            return True

    def update(self):
        #"""Перемещает боса вправо и вниз."""
        # self.x += (self.settings.alien_speed * self.settings.boss_direction_x)
        # self.y += (self.settings.alien_speed * self.settings.boss_direction_y)
        self.rect.x = self.x
        self.rect.y = self.y

        self._rotate_to_ship()
        if self.is_explois >= 1:
            self.image = self.image_explois
            self.is_explois += 1
        else:
            self.aim_turel_rect.center = self.rect.center
            self.image = self.aim_turel_image
            self.rect = self.image.get_rect()
            self.rect.centerx = self.x + self.rect_norm.width / 2
            self.rect.centery = self.y + self.rect_norm.height / 2


    def _rotate_to_ship(self):
        """Вращает в сторону корабля"""
        turrel_ship_diff = pygame.Vector2(self.x_aim, self.y_aim) - pygame.Vector2(self.rect.center)
        radius, angle = pygame.math.Vector2.as_polar(turrel_ship_diff)
        self.aim_turel_image = self._rotate(90 - angle)
        self.aim_turel_rect = self.aim_turel_image.get_rect()

    def _rotate(self, angle):
        w, h = self.image_norm.get_size()
        img2 = pygame.Surface((w, h), pygame.SRCALPHA)
        img2.blit(self.image_norm, (0, 0))
        return pygame.transform.rotate(img2, angle)
