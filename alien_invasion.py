import sys
import pygame
from ship import Ship

from settings import Settings


class AlienInvasion:
    # """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        #    """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        # Назначение цвета фона.
        self.bg_color = self.settings.bg_color
        self.ship = Ship(self)

    def run_game(self):
        # """Запуск основного цикла игры."""
        while True:
            # Отслеживание событий клавиатуры и мыши.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            # При каждом проходе цикла перерисовывается экран.
            self.screen.fill(self.bg_color)
            self.ship.blitme()
            # Отображение последнего прорисованного экрана.
            pygame.display.flip()


if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()