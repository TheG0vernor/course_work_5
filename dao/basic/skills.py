from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dao.basic.unit import BaseUnit


class Skill(ABC):
    """
    Базовый класс умения
    """
    user = None
    target = None

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def stamina(self):
        pass

    @property
    @abstractmethod
    def damage(self):
        pass

    @abstractmethod
    def skill_effect(self) -> str:
        pass

    def _is_stamina_enough(self):
        return self.user.stamina > self.stamina

    def use(self, user: BaseUnit, target: BaseUnit) -> str:
        """
        Проверка, достаточно ли выносливости у игрока для применения умения.
        Для вызова скилла везде используем просто use
        """
        self.user = user
        self.target = target
        if self._is_stamina_enough:
            return self.skill_effect()
        return f"{self.user.name} попытался использовать {self.name} но у него не хватило выносливости."


class FuryPunch(Skill):
    name = 'Fury Punch'
    stamina = 6
    damage = 12

    def skill_effect(self) -> str:
        self.target.hp -= self.damage
        self.user.stamina -= self.stamina
        return f"{self.user.name} использовал {self.name} и атаковал противника."


class HardShot(Skill):
    name = 'Hard Shot'
    stamina = 4
    damage = 8

    def skill_effect(self) -> str:
        self.target.hp -= self.damage
        self.user.stamina -= self.stamina
        return f"{self.user.name} использовал {self.name} и атаковал противника."