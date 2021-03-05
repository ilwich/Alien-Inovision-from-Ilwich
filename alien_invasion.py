import sys
from time import sleep

from random import randint
import pygame
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star
from rockets import Rocket
from settings import Settings
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


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
        # Создание экземпляра для хранения игровой статистики.
        # и панели результатов.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        # Назначение цвета фона.
        self.bg_color = self.settings.bg_color
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.rockets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self._create_university()
        self._create_fleet()
        # Создание кнопки Play.
        self.play_button = Button(self, "Play")
        #Создание кнопок выбора сложности
        self.easy_buttom = Button(self, "Easy")
        self.normal_buttom = Button(self, "Normal")
        self.hard_buttom = Button(self, "Hard")
        self._create_menu()

    def run_game(self):
        # """Запуск основного цикла игры."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()
                self.rockets.update()
                self._update_bullets()
                self._update_rockets()
                self._update_aliens()
                self._update_university()
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #инициализация скорости
            self.settings.initialize_dynamic_settings()
            self._start_game()
        if not self.stats.game_active:
            if self.easy_buttom.rect.collidepoint(mouse_pos):
                self.settings.speedup_scale = 1.1
                self.ship.rect.y = self.easy_buttom.rect.y
            if self.normal_buttom.rect.collidepoint(mouse_pos):
                self.settings.speedup_scale = 1.2
                self.ship.rect.y = self.normal_buttom.rect.y
            if self.hard_buttom.rect.collidepoint(mouse_pos):
                self.settings.speedup_scale = 1.4
                self.ship.rect.y = self.hard_buttom.rect.y

    def _start_game(self):
        # Сброс игровой статистики.
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        # Очистка списков пришельцев и снарядов ракет.
        self.aliens.empty()
        self.bullets.empty()
        self.rockets.empty()
        # Создание нового флота и размещение корабля в центре.
        self._create_fleet()
        self.stats.ships_left = self.settings.ship_limit
        self.ship.center_ship()
        # Сброс игровых настроек.
        self.settings.initialize_dynamic_settings()
        # Указатель мыши скрывается.
        pygame.mouse.set_visible(False)

    def _create_menu(self):
        """Создаем меню из кнопок выбора сложности"""
        if not self.stats.game_active:
            self.easy_buttom.rect.y = self.play_button.rect.y + self.play_button.rect.height * 2
            self.normal_buttom.rect.y = self.easy_buttom.rect.y + self.play_button.rect.height * 2
            self.hard_buttom.rect.y = self.normal_buttom.rect.y + self.play_button.rect.height * 2

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

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление флота."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_university(self):
        star = Star(self)
        star_width, star_height = star.rect.size
        available_space_x = self.settings.screen_width
        number_stars_x = available_space_x // (6 * star_width)
        """Определяет количество рядов, помещающихся на экране."""
        available_space_y = self.settings.screen_height - star_height
        number_rows = available_space_y // (6 * star_height)
        # Создание вселенной.
        for row_number in range(number_rows):
            # Создание первого ряда звезд.
            for star_number in range(number_stars_x):
                # Создание звезды и размещение её в ряду.
                self._create_star(star_number, row_number)


    def _create_star(self, star_number, row_number):
        #"""Создание звезды и размещение её в ряду."""
        star = Star(self)
        star_width, star_height = star.rect.size
        star.x = randint(star_width, star_width * 6) + 6 * star_width * star_number
        star.y = randint(-star_height*6, 0) + 6 * star_height * row_number
        star.rect.x = star.x
        star.rect.y = star.y
        self.stars.add(star)

    def _check_star_edges(self):
        """Реагирует на достижение звезды края экрана."""
        for star in self.stars.sprites():
            if star.check_edges():
                star.y = star.rect.height+randint(-star.rect.height, star.rect.height*3)

    def _update_screen(self):
        # При каждом проходе цикла перерисовывается экран.
        self.screen.fill(self.bg_color)
        self.stars.draw(self.screen)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for rocket in self.rockets.sprites():
            rocket.draw_rocket()
        self.aliens.draw(self.screen)
        # Вывод информации о счете.
        self.sb.show_score()
        # Кнопка Play отображается в том случае, если игра неактивна.
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.easy_buttom.draw_button()
            self.normal_buttom.draw_button()
            self.hard_buttom.draw_button()
            self.ship.rect.x = self.easy_buttom.rect.x - self.ship.rect.width
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
        if event.key == pygame.K_q:
            self.stats.high_score_save()
            sys.exit()
        if event.key == pygame.K_p:
            if not self.stats.game_active:
                self._start_game()
        if event.key == pygame.K_SPACE:
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
        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        """Обработка коллизий снарядов с пришельцами."""
        # Проверка попаданий в пришельцев.
        # При обнаружении попадания удалить снаряд и пришельца.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, False)
        # Удаление снарядов и пришельцев, участвующих в коллизиях.
        count_collisions = 0
        if collisions:
            for element in collisions.values():
                count_collisions += len(element)
                for el in element:
                    el.is_explois = 1
            self.stats.score += self.settings.alien_points * count_collisions
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self.settings.increase_speed()
            self._create_fleet()
            # Увеличение уровня.
            self.stats.level += 1
            self.sb.prep_level()


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
        self._check_rockets_alien_collision()


    def _check_rockets_alien_collision(self):
        # Проверка попаданий в пришельцев.
        # При обнаружении попадания удалить пришельца.
        collisions = pygame.sprite.groupcollide(self.rockets, self.aliens, False, False)
        count_collisions = 0
        if collisions:
            for element in collisions.values():
                count_collisions += len(element)
                for el in element:
                    el.is_explois = 1
            self.stats.score += self.settings.alien_points * count_collisions
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
        # Уничтожение существующих снарядов и создание нового флота.
            self.bullets.empty()
            self.settings.increase_speed()
            self._create_fleet()
            # Увеличение уровня.
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """Обновляет позиции всех пришельцев во флоте."""
        self._check_fleet_edges()
        self.aliens.update()
        self._check_aliens_explois()
        # Проверка коллизий "пришелец — корабль".
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Проверить, добрались ли пришельцы до нижнего края экрана.
        self._check_aliens_bottom()

    def _check_aliens_explois(self):
        for alien in self.aliens.sprites():
            if alien.is_explois >=30:
                alien.kill()


    def _check_aliens_bottom(self):
        """Проверяет, добрались ли пришельцы до нижнего края экрана."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Происходит то же, что при столкновении с кораблем.
                self._ship_hit()
                break

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцем."""
        # Уменьшение ships_left.
        if self.stats.ships_left > 1:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.ship.rockets = self.settings.rocket_number
            # Очистка списков пришельцев и снарядов.
            self.aliens.empty()
            self.bullets.empty()
            self.rockets.empty()
            # Создание нового флота и размещение корабля в центре.
            self._create_fleet()
            self.ship.center_ship()
            # Пауза.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_university(self):
        """Обновляет позиции всех звезд на экране."""
        self._check_star_edges()
        self.stars.update()

if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
