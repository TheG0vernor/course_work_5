from typing import Optional

from dao.basic.unit import BaseUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False
    battle_result = None

    def start_game(self, player: BaseUnit, enemy: BaseUnit) -> None:
        """Начало игры"""
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self) -> Optional[str]:
        """Проверка здоровья игрока и врага"""
        if self.player.hp > 0 >= self.enemy.hp:
            self.battle_result = 'Игрок выиграл битву'
            self._end_game()
        elif self.player.hp <= 0 < self.enemy.hp:
            self.battle_result = 'Игрок проиграл битву'
            self._end_game()
        elif self.player.hp <= 0 >= self.enemy.hp:
            self.battle_result = 'Ничья'
            self._end_game()
        return self.battle_result

    def _stamina_regeneration(self) -> None:
        """Регенерация выносливости за ход"""
        if self.player.stamina < self.player.unit_class.max_stamina:
            self.player.stamina += self.STAMINA_PER_ROUND

        if self.enemy.stamina < self.enemy.unit_class.max_stamina:
            self.enemy.stamina += self.STAMINA_PER_ROUND


    def next_turn(self):
        """Следующий ход"""
        if self._check_players_hp():
            return self.battle_result
        self._stamina_regeneration()
        return self.enemy.hit(self.player)  # ответный удар

    def _end_game(self) -> str:
        """Конец игры"""
        self.game_is_running = False
        self.enemy = None
        self.player = None
        return self.battle_result

    def player_hit(self) -> str:
        """Удар игрока и противника"""
        if self._check_players_hp():
            return self.battle_result
        result = self.player.hit(self.enemy)
        result2 = self.enemy.hit(self.player)
        self.next_turn()
        return f'{result}<br>' \
               f'{result2}'

    def player_use_skill(self):
        """Использование умения игроком и противником"""
        if self._check_players_hp():
            return self.battle_result
        result = self.player.use_skill(self.enemy)
        result2 = self.enemy.hit(self.player)
        self.next_turn()
        return f'{result}<br>' \
               f'{result2}'
