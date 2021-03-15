import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2

class Boss(Sprite):
    """Класс, представляющий одного боса."""

    def __init__(self, ai_game):
        #"""Инициализирует боса и задает его начальную позицию."""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.explois_sound = pygame.mixer.Sound('sounds/Explosion3.wav')
        # Загрузка изображения боса и назначение атрибута rect.
        self.image_norm = pygame.image.load('images/turrel2.bmp')
        self.image = self.image_norm.copy()
        self.image_explois = pygame.image.load('images/ship_destroy.bmp')
        self.is_explois = 0
        self.rect = self.image.get_rect()
        self.normal_center = self.rect.center
        # Каждый новый босс появляется в центре экрана.
        self.rect.x = self.screen_rect.centerx
        self.rect.y = self.screen_rect.centery
        # Уровень здоровья орудий
        self.boss_turrel_health = self.settings.boss_turrel_health_max
        self.turrel_health_color = self.settings.boss_turrel_health_color
        # Создание полосы здоровья в позиции (0,0) и назначение правильной позиции.
        self.turrel_health_rect = pygame.Rect(0, 0,
                                              self.settings.boss_turrel_health_width,
                                              self.settings.boss_turrel_health_height)
        self.rect_health_heigth = self.settings.boss_turrel_health_height
        self.rect_health_weigth = self.settings.boss_turrel_health_width
        # Сохранение точной горизонтальной позиции боса.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.index_in_station = 0
        self.x_aim = ai_game.ship.rect.x
        self.y_aim = ai_game.ship.rect.y

    def check_edges(self):
        """Возвращает True, если босс находится у краев экрана."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.x <= 10:
            return True

    def _explois(self):
        """Отрисовываем взрыв"""
        rect_explois = self.image_explois.get_rect()
        rect_explois.center = (self.rect.width / 2, self.rect.height / 2)
        self.image.blit(self.image_explois, rect_explois)


    def update(self):
        #"""Перемещает боса вправо и вниз."""

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        if self.is_explois >= 1:
            self._explois()
            self.is_explois += 1
            if self.is_explois >= self.settings.exlois_timer:
                self.boss_turrel_health -= self.settings.boss_turrel_bullet_damge
                if self.boss_turrel_health >= 0:
                    self.is_explois = 0
        else:
            self._rotate_to_ship()
        self._draw_turrel_health()

    def _draw_turrel_health(self):
        """Вывод уровня здоровья пушки на экран."""
        # Расчёт позиции жизни смерти
        kill_level = int(self.boss_turrel_health * self.rect_health_weigth / 100)
        boader = self.settings.boss_turrel_health_boader_thick
        # Параметры прямоугольника бара здороья
        rect_health = (int((self.rect.width / 2) - (self.rect_health_weigth / 2)),
                       int((self.rect.height / 2) - (self.rect_health_heigth / 2)),
                       self.rect_health_weigth,
                       self.rect_health_heigth)
        pygame.draw.rect(self.image, (254, 254, 254), (rect_health[0]-boader, rect_health[1]-boader, rect_health[2]+boader*2, rect_health[3]+boader*2))
        pygame.draw.rect(self.image, self.settings.boss_turrel_health_color, (rect_health[0], rect_health[1], kill_level, rect_health[3]))
        pygame.draw.rect(self.image, pygame.SRCALPHA, (rect_health[0] + kill_level, rect_health[1], rect_health[2], rect_health[3]))

    def draw_boss(self):
        """Вывод босса на экран."""
        self.screen.blit(self.image, self.rect)

    def _rotate_to_ship(self):
        """Вращает в сторону корабля"""
        #Вычисления угла между векторами в позицию башни и в позицию корабля
        turrel_ship_diff = pygame.Vector2(self.x_aim, self.y_aim) - pygame.Vector2(self.rect.center)
        radius, angle = pygame.math.Vector2.as_polar(turrel_ship_diff)
        # Сохранение позиции центра картинки
        self.rect = self.image.copy().get_rect()
        self.center = (int(self.x + self.rect.width / 2), int(self.y + self.rect.height / 2))
        # Поворот изображения
        self.image = self.rotate(self.image_norm, self.normal_center, 90 - angle)
        self.rect = self.image.get_rect()
        # Возвращение картинки в изначальный центр после поворота
        self.rect.center = self.center
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)


    def rotate(self, img, pos, angle):
        """Поворот изображения с предварительным увеличением в два раза"""
        w, h = img.get_size()
        img2 = pygame.Surface((w * 2, h * 2), pygame.SRCALPHA)
        img2.blit(img, (w - pos[0], h - pos[1]))
        return pygame.transform.rotate(img2, angle)