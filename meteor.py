import pygame
from pygame.sprite import Sprite

class Meteor(Sprite):
    #"""Класс для управления метеоритами, выпущенными пришельцами."""

    def __init__(self, ai_game, alien):
        #"""Создает объект метеорита в текущей позиции пришельца."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.image.load('images/meteor2.bmp')
        self.shoot_sound = pygame.mixer.Sound('sounds/meteor_shoot.wav')
        self.rect = self.image.get_rect()
        # Каждый новый метеорит появляется в левом верхнем углу экрана.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # Создание метеорита и назначение правильной позиции.
        self.rect.midtop = alien.rect.midtop
        # Сохранение точной горизонтальной позиции метеорита.
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        self.x_step = 0.0
        self.y_step = 0.0
        self.x_aim = ai_game.ship.rect.x
        self.y_aim = ai_game.ship.rect.y
        self._step_calculation()

    def update(self):
        #"""Перемещает метеорит в сторону цели"""
        # Обновление позиции метеорита в вещественном формате.
        self.y += self.y_step
        self.x += self.x_step
        # Обновление позиции прямоугольника.
        self.rect.y = self.y
        self.rect.x = self.x

    def draw_meteor(self):
        #"""Вывод метеорита на экран."""
        self.screen.blit(self.image, self.rect)

    def _step_calculation(self):
        """Вычисление шагов движения метеорита к цели"""
        delta_x = self.x_aim - self.x
        delta_y = self.y_aim - self.y
        delta = (delta_x ** 2 + delta_y ** 2) ** 0.5
        if delta_x:
            self.x_step = (delta_x * 100) / (delta * self.settings.meteor_speed)
        else:
            self.x_step = 0
        if delta_y:
            self.y_step = (delta_y * 100) / (delta * self.settings.meteor_speed)
        else:
            self.y_step = 0


    def check_edges(self):
        """Возвращает True, если метеор находится у края экрана."""
        screen_rect = self.screen.get_rect()
        if self.rect.bottom >= screen_rect.bottom - 40:
            return True
        if self.rect.right >= screen_rect.right:
            return True
        if self.rect.x <= -10 or self.rect.y <= -10:
            return True