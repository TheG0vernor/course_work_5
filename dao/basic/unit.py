from __future__ import annotations

import random
from abc import ABC, abstractmethod

from dao.equipment import Weapon, Armor
from dao.classes import UnitClass


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """
    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = None
        self.armor = None
        self._is_skill_used = False  # использован ли скилл

    @property
    def health_points(self):
        return round(self.hp)  # возвращает аттрибут hp

    @property
    def stamina_points(self):
        return round(self.stamina)  # возвращает аттрибут stamina

    def equip_weapon(self, weapon: Weapon):
        """Присваиваем нашему герою новое оружие"""
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> int:
        damage = round(self.weapon.damage * self.unit_class.attack)
        self.stamina -= self.weapon.stamina_per_hit
        if target.stamina < target.armor.stamina_per_turn * target.unit_class.stamina:
            target.hp -= damage
        else:
            damage = round(damage - target.armor.defence * target.unit_class.armor)
            target.get_damage(damage)
            target.stamina -= round(target.armor.stamina_per_turn * target.unit_class.stamina)
        return damage

    def get_damage(self, damage: int) -> None:
        """Получение урона целью"""
        if damage > 0:
            self.hp -= damage

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        этот метод будет переопределен ниже
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """Использование умения"""
        if self._is_skill_used:
            return 'Умение использовано'
        self._is_skill_used = True
        return self.unit_class.skill.use(user=self, target=target)



class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """Атака игрока"""
        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        damage = self._count_damage(target)
        damage = round(damage)
        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."
        else:
            return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """Атака противника"""

        # использование умения
        if not self._is_skill_used:
            int_ = random.uniform(0.1, 1)
            if round(int_, 1) == 0.5:
                return self.use_skill(target)

        # обычный бой
        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        damage = self._count_damage(target)
        damage = round(damage)
        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит Вам {damage} урона."
        else:
            return f"{self.name} используя {self.weapon.name} наносит удар, но Ваш(а) {target.armor.name} его останавливает."
