import pygame
from pygame.sprite import Sprite

class Rocket(Sprite):
    #"""Класс для управления ракетами, выпущенными кораблем."""

    def __init__(self, ai_game):
        #"""Создает объект ракета в текущей позиции корабля."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.shoot_sound = pygame.mixer.Sound('sounds/Rocket_Shoot1.wav')
        # Загружает изображение ракеты и получает прямоугольник.
        self.image = pygame.image.load('images/rocket.bmp')
        self.rect = self.image.get_rect()
        self.rect.midtop = ai_game.ship.rect.midtop
        # Позиция ракеты хранится в вещественном формате.
        self.y = float(self.rect.y)

    def update(self):
        #"""Перемещает ракеты вверх по экрану."""
        # Обновление позиции ракеты в вещественном формате.
        self.y -= self.settings.rocket_speed
        # Обновление позиции прямоугольника.
        self.rect.y = self.y

    def draw_rocket(self):
        #"""Вывод ракеты на экран."""
        self.screen.blit(self.image, self.rect)