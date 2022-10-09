from dataclasses import dataclass

from dao.basic.skills import Skill


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill


WarriorClass = UnitClass(name='Teodor', max_health=200, max_stamina=60, attack=6, stamina=6, armor=3, skill=Skill())

ThiefClass = UnitClass(name='Thief', max_health=160, max_stamina=50, attack=8, stamina=4, armor=1, skill=Skill())

unit_classes = {
    ThiefClass.name: ThiefClass,
    WarriorClass.name: WarriorClass
}
