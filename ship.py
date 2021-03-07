import pygame
from pygame.sprite import Sprite
from os import path


class Ship(Sprite):
    #"""Класс для управления кораблем."""
    def __init__(self, ai_game):
        #"""Инициализирует корабль и задает его начальную позицию."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.img_dir = path.join(path.dirname(__file__), 'images')
        self.destroy_sound = pygame.mixer.Sound('sounds/expl6.wav')
        self.damage_sound = pygame.mixer.Sound('sounds/Ship_Damage.wav')
        # Загружает изображение корабля и получает прямоугольник.
        self.image = pygame.image.load(path.join(self.img_dir, 'ship.bmp'))
        self.image_normal = pygame.image.load(path.join(self.img_dir, 'ship.bmp'))
        self.image_destroy = pygame.image.load(path.join(self.img_dir, 'ship_destroy.bmp'))
        self.image_health = pygame.image.load(path.join(self.img_dir, 'health0.bmp'))
        self.rect_health = self.image_health.get_rect()
        self.is_destroy = 0
        self.rect = self.image.get_rect()
        # Каждый новый корабль появляется у нижнего края экрана.
        self.rect.midbottom = self.screen_rect.midbottom
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.rockets = self.settings.rocket_number
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.health = 0
        self.image_health_list = []
        self._making_image_list(self.image_health)


    def blitme(self):
        #"""Рисует корабль в текущей позиции."""
        if self.is_destroy >= 200 or self.is_destroy == 0:
            self.is_destroy = 0
            self.screen.blit(self.image, self.rect)
            self._draw_image_health()
        if self.is_destroy >= 1:
            self.screen.blit(self.image_destroy, self.rect)
            self.is_destroy += 1


    def update(self):
        #"""Обновляет позицию корабля с учетом флага."""
        # Обновляется атрибут x, не rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect_health.centerx = self.rect.centerx
        self.rect_health.centery = self.rect.centery




    def center_ship(self):
        """Размещает корабль в центре нижней стороны."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.bottom = self.screen_rect.bottom
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def _making_image_list(self, image):
        """Генерируем три дуги повернутые на 90 градусов"""
        resize = 0
        rect = image.get_rect()
        while resize < 60:
            angle = 0
            image_resize = pygame.transform.scale(image, (rect.width - resize, rect.height - resize))
            resize += 27
            while angle < 270:
                image_rotate = pygame.transform.rotate(image_resize, angle * (-1))
                self.image_health_list.append(image_rotate)
                angle += 90

    def _draw_image_health(self):
        """Отрисовываем уровень жизни корабля"""
        centerx = self.rect.centerx
        centery = self.rect.centery
        for image in self.image_health_list[: self.health // 11]:
            rect = image.get_rect()
            rect.centerx = centerx
            rect.centery = centery
            self.screen.blit(image, rect)