from dataclasses import dataclass

from dao.basic.skills import Skill, FuryPunch, HardShot


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill


WarriorClass = UnitClass(name='Варвар', max_health=200, max_stamina=60, attack=2, stamina=6, armor=3, skill=FuryPunch())

ThiefClass = UnitClass(name='Убийца', max_health=160, max_stamina=50, attack=3, stamina=4, armor=1, skill=HardShot())

unit_classes = {
    ThiefClass.name: ThiefClass,
    WarriorClass.name: WarriorClass
}
