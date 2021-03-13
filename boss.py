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
        self.image_explois = pygame.image.load('images/ship_destroy.bmp')
        self.is_explois = 0
        self.rect = self.image.get_rect()
        # Каждый новый босс появляется в центре экрана.
        self.rect.x = self.screen_rect.centerx
        self.rect.y = self.screen_rect.centery
        # Уровень здоровья орудий
        self.boss_turrel_health = self.settings.boss_turrel_health_max
        self.turrel_health_color = self.settings.boss_turrel_health_color
        # Создание полосы здоровья в позиции (0,0) и назначение правильной позиции.
        self.turrel_health_rect = pygame.Rect(0, 0, self.settings.boss_turrel_health_width, self.settings.boss_turrel_health_height)
        # Сохранение точной горизонтальной позиции боса.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.index_in_station = 0
        self.x_aim = ai_game.ship.rect.x
        self.y_aim = ai_game.ship.rect.y

    def check_edges(self):
        """Возвращает True, если босс находится у краев экрана."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.x <= -10:
            return True

    def _explois(self):
        """Отрисовываем взрыв"""
        rect_explois = self.image_explois.get_rect()
        rect_explois.center = (self.rect_norm.width / 2, self.rect_norm.height / 2)
        self.image.blit(self.image_explois, rect_explois)


    def update(self):
        #"""Перемещает боса вправо и вниз."""

        self.rect.x = self.x
        self.rect.y = self.y
        if self.is_explois >= 1:
            self._explois()
            self.is_explois += 1
            if self.is_explois >= self.settings.exlois_timer:
                self.boss_turrel_health -= self.settings.boss_turrel_bullet_damge
                if self.boss_turrel_health >= 0:
                    self.is_explois = 0
        else:
            self._rotate_to_ship()
            self.aim_turel_rect.center = self.rect.center
            self.image = self.aim_turel_image.copy()
            rect_temp = self.image.get_rect()
            self.rect.width = rect_temp.width
            self.rect.height = rect_temp.height
            self.rect.centerx = self.rect.x + self.rect_norm.width / 2
            self.rect.centery = self.rect.y + self.rect_norm.height / 2
        self._draw_turrel_health()


    def _draw_turrel_health(self):
        """Вывод уровня здоровья пушки на экран."""
        kill_level = self.boss_turrel_health * self.settings.boss_turrel_health_width / 100
        kill_level_rect = self.turrel_health_rect.copy()
        kill_level_rect.width = kill_level
        kill_level_rect.height = self.settings.boss_turrel_health_height
        kill_level_rect.topleft = (int((self.rect.width / 2) - (self.settings.boss_turrel_health_width / 2)), 3)
        heath_level_rect = self.turrel_health_rect.copy()
        heath_level_rect.width = self.settings.boss_turrel_health_width - kill_level
        heath_level_rect.height = self.settings.boss_turrel_health_height
        heath_level_rect.topright = (int((self.rect.width / 2) + (self.settings.boss_turrel_health_width / 2)), 3)
        self.turrel_health_rect.midtop = (int(self.rect.width / 2), 0)
        self.turrel_health_rect.width = self.settings.boss_turrel_health_width + 6
        self.turrel_health_rect.height = self.settings.boss_turrel_health_height + 6
        pygame.draw.rect(self.image, (254, 254, 254), self.turrel_health_rect)
        pygame.draw.rect(self.image, self.settings.boss_turrel_health_color, kill_level_rect)
        pygame.draw.rect(self.image, pygame.SRCALPHA, heath_level_rect)


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

    def draw_boss(self):
        """Вывод босса на экран."""
        self.screen.blit(self.image, self.rect)
