import sys
import pygame
from ship import Ship
from bullet import Bullet
from alien import Alien
from rockets import Rocket
from settings import Settings


class AlienInvasion:
    # """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        #    """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        # Назначение цвета фона.
        self.bg_color = self.settings.bg_color
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.rockets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        # """Запуск основного цикла игры."""
        while True:
            self._check_events()
            self.ship.update()
            self.bullets.update()
            self.rockets.update()
            self._update_bullets()
            self._update_rockets()

            self._update_screen()


    def _check_events(self):
        # Отслеживание событий клавиатуры и мыши.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _create_fleet(self):
        #"""Создание флота вторжения."""
        # Создание пришельца.
        # Создание пришельца и вычисление количества пришельцев в ряду
        # Интервал между соседними пришельцами равен ширине пришельца.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        """Определяет количество рядов, помещающихся на экране."""
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        # Создание флота вторжения.
        for row_number in range(number_rows):
            # Создание первого ряда пришельцев.
            for alien_number in range(number_aliens_x):
                # Создание пришельца и размещение его в ряду.
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        #"""Создание пришельца и размещение его в ряду."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.y = alien_height + 2 * alien_height * row_number
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def _update_screen(self):
        # При каждом проходе цикла перерисовывается экран.
        self.screen.fill(self.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for rocket in self.rockets.sprites():
            rocket.draw_rocket()
        self.aliens.draw(self.screen)
        # Отображение последнего прорисованного экрана.
        pygame.display.flip()

    def _check_keydown_events(self, event):
        #"""Реагирует на нажатие клавиш."""
        if event.key == pygame.K_RIGHT:
            # Переместить корабль вправо.
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Переместить корабль влево.
            self.ship.moving_left = True
        if event.key == pygame.K_UP:
            # Переместить корабль вперед.
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            # Переместить корабль влево.
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_LCTRL:
            self._fire_rockets()


    def _check_keyup_events(self, event):
        #"""Реагирует на отпускание клавиш."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        #"""Создание нового снаряда и включение его в группу bullets."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        #"""Обновляет позиции снарядов и уничтожает старые снаряды."""
        # Обновление позиций снарядов.
        # Удаление снарядов, вышедших за край экрана.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _fire_rockets(self):
        #"""Создание новой ракеты и включение её в группу rockets."""
        if len(self.rockets) < self.settings.bullets_allowed and self.ship.rockets > 0:
            new_rocket = Rocket(self)
            self.ship.rockets -= 1
            self.rockets.add(new_rocket)

    def _update_rockets(self):
        #"""Обновляет позиции снарядов и уничтожает стары ракеты."""
        #Обновление позиции ракеты.
        #Удаление ракет улетевших за экран
        for rocket in self.rockets.copy():
            if rocket.rect.bottom <= 0:
                self.rockets.remove(rocket)

if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
