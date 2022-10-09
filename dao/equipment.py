from dataclasses import dataclass
from typing import List
from random import uniform
import marshmallow_dataclass
import marshmallow
import json

from constants import WEAPONS_and_ARMORS


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class Weapon:
    """Описание экземпляра оружия"""
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self):
        """Расчёт урона"""
        return round(uniform(self.min_damage, self.max_damage), 1)


@dataclass
class EquipmentData:
    """Содержит 2 списка - с оружием и с броней"""
    weapons: List[Weapon]
    armors: List[Armor]


class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name) -> Weapon:
        """Возвращает объект оружия по имени"""
        weapons = self.equipment.weapons
        for w in weapons:
            if w.name == weapon_name:
                return w
            else:
                raise ValueError
        # return self.equipment.weapons[self.equipment.weapons.index(weapon_name)]

    def get_armor(self, armor_name) -> Armor:
        """Возвращает объект брони по имени"""
        armors = self.equipment.armors
        for a in armors:
            if a.name == armor_name:
                return a
            else:
                raise ValueError

    def get_weapons_names(self) -> list:
        """Возвращает список с оружием"""
        weapons = self.equipment.weapons
        weapons = [w.name for w in weapons]
        return weapons

    def get_armors_names(self) -> list:
        """Возвращает список с броней"""
        armors = self.equipment.armors
        armors = [a.name for a in armors]
        return armors

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        """Метод загружает json в переменную EquipmentData"""
        equipment_file = open(WEAPONS_and_ARMORS, encoding='utf-8')
        data = json.load(equipment_file)
        equipment_file.close()
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError
