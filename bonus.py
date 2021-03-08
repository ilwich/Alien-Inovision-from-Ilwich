import pygame
from os import path
from pygame.sprite import Sprite

class Bonus(Sprite):
    #"""Класс для управления бонусами, выпущенными метеоритами."""

    def __init__(self, ai_game, meteor, bonus_type):
        #"""Создает объект бонуса в текущей позиции метеорита."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image_file = 'bonus_' + str(bonus_type) + '.bmp'
        self.img_dir = path.join(path.dirname(__file__), 'images')
        self.image = pygame.image.load(path.join(self.img_dir, self.image_file))
        self.upgrade_sound = pygame.mixer.Sound('sounds/Powerup.wav')
        self.rect = self.image.get_rect()
        # Каждый новый бонус появляется в левом верхнем углу экрана.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # Создание бонуса и назначение правильной позиции.
        self.rect.midtop = meteor.rect.midtop
        # Сохранение точной горизонтальной позиции бонуса.
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        self.x_step = meteor.x_step
        self.y_step = meteor.y_step
        self.bonus_type = bonus_type


    def update(self):
        #"""Перемещает бонус в сторону цели"""
        # Обновление позиции бонуса в вещественном формате.
        self.y += self.y_step
        self.x += self.x_step
        # Обновление позиции прямоугольника.
        self.rect.y = self.y
        self.rect.x = self.x


    def draw_bonus(self):
        #"""Вывод бонуса на экран."""
        self.screen.blit(self.image, self.rect)




    def check_edges(self):
        """Возвращает True, если бонус находится у края экрана."""
        screen_rect = self.screen.get_rect()
        if self.rect.bottom >= screen_rect.bottom:
            return True
        if self.rect.right >= screen_rect.right:
            return True
        if self.rect.x <= -10 or self.rect.y <= -10:
            return True