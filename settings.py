class Settings():
#"""Класс для хранения всех настроек игры Alien Invasion."""

    def __init__(self):
        #"""Инициализирует настройки игры."""
        """Инициализирует статические настройки игры."""
        # Параметры экрана
        self.screen_width = 1200
        self.screen_height = 750
        self.bg_color = (143, 85, 201)
        self.ship_limit = 5
        # Параметры снаряда
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        self.rocket_number = 5
        self.fleet_drop_speed = 10
        # fleet_direction = 1 обозначает движение вправо; а -1 - влево.
        self.fleet_direction = 1
        self.university_drop_speed = 0.5
        # Темп ускорения игры
        self.speedup_scale = 1.1
        # Темп роста стоимости пришельцев
        self.score_scale = 1.5
        # Имя файла с рекордами
        self.record_filename = 'records.dat'
        # Параметры метеоритов
        self.meteor_number_max = 5
        # Сколько шагов на 100 пикселей
        self.meteor_speed = 200
        # Частота выстрела метеоритами
        self.meteor_clock = 500
        # Уровень повреждения от метеорита
        self.meteor_damage = 12
        # Уровень здоровья корабля
        self.ship_health_max = 100
        self.initialize_dynamic_settings()
        # Количество типов бонусов
        self.bonus_type_number = 5

    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры."""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.rocket_speed = 4.5
        self.alien_speed = 1.0
        # fleet_direction = 1 обозначает движение вправо; а -1 - влево.
        self.fleet_direction = 1
        # Подсчет очков
        self.alien_points = 100
        self.meteor_timing = 0

    def increase_speed(self):
        """Увеличивает настройки скорости и стоимость пришельцев."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.rocket_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
