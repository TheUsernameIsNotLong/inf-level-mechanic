import random
import copy
from character import Character
from status import *

class Attack():
    def __init__(self, name:str, desc:str, instances:int, power:float, hitChance:float, status:Status, statusChance:float):
        self.name = name
        self.desc = desc
        self.instances = instances
        self.power = power
        self.hitChance = hitChance
        self.status = status
        self.statusChance = statusChance
    
class Attack_Physical(Attack):
    def __init__(self, name:str, desc:str, instances:int, power:float, hitChance:float, status:Status, statusChance:float):
        super().__init__(name, desc, instances, power, hitChance, status, statusChance)
    
    def do(self, attacker:Character, defender:Character):
        print(f"{attacker.name} used {self.name}!")
        randModifier = 0.75 + (random.random()/2)
        damage = round(self.power*randModifier*((2*attacker.stats.atk) - (defender.stats.dfc))/200)
        print(f"{attacker.name} attacked {defender.name} for {damage} dmg!")
        defender.harm(damage)
        if self.status is not None:
            if random.random() <= self.statusChance:
                newInstance = copy.deepcopy(self.status)
                defender.addStatus(newInstance)

class Attack_Magical(Attack):
    def __init__(self, name:str, desc:str, instances:int, power:float, hitChance:float, status:Status, statusChance:float):
        super().__init__(name, desc, instances, power, hitChance, status, statusChance)
    
    def do(self, attacker:Character, defender:Character):
        print(f"{attacker.name} used {self.name}!")
        randModifier = 0.75 + (random.random()/2)
        damage = round(self.power*randModifier*((2*attacker.stats.mAtk) - (defender.stats.mDfc))/200)
        print(f"{attacker.name} attacked {defender.name} for {damage} dmg!")
        defender.harm(damage)
        if self.status is not None:
            if random.random() <= self.statusChance:
                newInstance = copy.deepcopy(self.status)
                if self.name == "Toxic Spore":
                    newInstance.lvl = random.randint(1,2)
                defender.addStatus(newInstance)

atkDefault = Attack_Physical("Attack", "Perform a weak attack.", 1, 100, 1, None, 0)
atkPsnSlash = Attack_Physical("Poison Slash", "Slash the opponent with a toxic blade. Chance to poison.", 1, 100, 1, Poison(), 0.5)
atkToxSpore = Attack_Magical("Toxic Spore", "Shoot a toxic spore, inflicting poison. Chance to double poison strength.", 1, 0, 1, Poison(), 1)
atkBurnBlade = Attack_Physical("Burning Blade", "Perform a flaming double-slash upon the opponent. Chance to burn.", 2, 60, 1, Burn(), 0.5)
atkFlamethrower = Attack_Magical("Flamethrower", "Spur endless flames towards the oppenent!", 10, 16, 1, Burn(2), 1)