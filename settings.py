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
        self.exlois_timer = 30
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
        # Направление движения босса 1- вправо и вниз
        self.boss_direction_x = 1
        self.boss_direction_y = 1
        # Уровень жизни пушки
        self.boss_turrel_health_max = 100
        self.boss_turrel_health_width = 100
        self.boss_turrel_health_height = 15
        # Повреждения пушки от попадания пули
        self.boss_turrel_bullet_damge = 10
        # Параметры отображения здоровья пушек босса
        self.boss_turrel_health_color = (255, 0, 0)
        # Темп ускорения игры
        self.speedup_scale = 1.1
        # Темп роста стоимости пришельцев
        self.score_scale = 1.5
        # Имя файла с рекордами
        self.record_filename = 'records.dat'
        # Параметры метеоритов
        self.meteor_number_max = 5
        self.bossbullet_number_max = 8
        # Сколько шагов на 100 пикселей
        self.meteor_speed = 200
        self.bossbullet_speed = 50
        # Частота выстрела метеоритами
        self.meteor_clock = 500
        self.bossbullet_clock = 250
        # Уровень повреждения от метеорита
        self.meteor_damage = 12
        self.bossbullet_damage = 24
        # Уровень здоровья корабля
        self.ship_health_max = 100
        self.initialize_dynamic_settings()
        # Количество типов бонусов
        self.bonus_type_number = 6

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
        self.bossbullet_timing = 0

    def increase_speed(self):
        """Увеличивает настройки скорости и стоимость пришельцев."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.bossbullet_speed *= self.speedup_scale
        self.rocket_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

    def save_normal_level_setting(self):
        """Сохранение настроек уровня до бонусов"""
        self.normal_alien_speed = self.alien_speed
        self.normal_alien_points = self.alien_points

    def load_normal_level_setting(self):
        """Восстановление настроек уровня после прохождения"""
        self.alien_points = self.normal_alien_points
        self.alien_speed = self.normal_alien_speed

    def save_normal_ship_setting(self):
        """Сохранение настроек для нового корабля до бонусов"""
        self.normal_bullet_heigth = self.bullet_height
        self.normal_bullets_allowed = self.bullets_allowed
        self.normal_rocket_number = self.rocket_number

    def load_normal_ship_setting(self):
        """Восстановление настроек для корабля после гибели"""
        self.rocket_number = self.normal_rocket_number
        self.bullets_allowed = self.normal_bullets_allowed
        self.bullet_heigth = self.normal_bullet_heigth
