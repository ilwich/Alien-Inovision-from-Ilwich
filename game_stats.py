class GameStats():
    """Отслеживание статистики для игры Alien Invasion."""

    def __init__(self, ai_game):
        """Инициализирует статистику."""
        self.settings = ai_game.settings
        self.reset_stats()
        # Игра запускается в неактивном состоянии.
        self.game_active = False
        # Рекорд не должен сбрасываться.
        self._high_score_init()

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def _high_score_init(self):
        with open(self.settings.record_filename, 'r') as file_object:
            self.high_score = int(file_object.read())

    def high_score_save(self):
        with open(self.settings.record_filename, 'w') as file_object:
            file_object.write(str(self.high_score))