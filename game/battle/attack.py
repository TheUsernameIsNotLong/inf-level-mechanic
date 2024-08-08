import random
import copy
import configparser
from game.character.character import Character
from game.character.status import *

config = configparser.ConfigParser()

config.read('config.ini')

class Attack():
    def __init__(self, name:str, desc:str, instances:int, power:float, hitChance:float, status:Status, statusChance:float):
        self.name = name
        self.desc = desc
        self.instances = instances # Number of times an attack can hit
        self.power = power # Affects damage output on each hit
        self.hitChance = hitChance # Chance of an attack hitting
        self.status = status # Status effect an attack can inflict
        self.statusChance = statusChance # Chance of the status effect inflicting
    
class Attack_Physical(Attack):
    def __init__(self, name:str, desc:str, instances:int, power:float, hitChance:float, status:Status, statusChance:float):
        super().__init__(name, desc, instances, power, hitChance, status, statusChance)
    
    def calcDamage(self, attacker:Character, defender:Character):
        totalDmg = 0
        for i in range(self.instances):
            if config['options_game']['damageVarianceEnabled'] == "true":
                randModifier = 0.75 + (random.random()/2)
            else:
                randModifier = 1
            dmg = round(self.power*randModifier*((2*attacker.stats.atk) - (defender.stats.dfc))/200)
            totalDmg += dmg
        return totalDmg
    
    def do(self, attacker:Character, defender:Character):
        battle = attacker.battle
        damage = self.calcDamage(attacker, defender)
        defender.harm(damage)
        if battle != None:
            scr_turn(battle.turnNum, battle.party, battle.enemies)
        print(f"{attacker.name} used {self.name}!")
        print(f"{attacker.name} attacked {defender.name} for {damage} dmg!")
        input()
        if defender.stats.hp == 0:
            defender.addStatus(KO())
        elif self.status is not None:
            if random.random() <= self.statusChance:
                newInstance = copy.deepcopy(self.status)
                defender.addStatus(newInstance)

class Attack_Magical(Attack):
    def __init__(self, name:str, desc:str, instances:int, power:float, hitChance:float, status:Status, statusChance:float):
        super().__init__(name, desc, instances, power, hitChance, status, statusChance)
    
    def calcDamage(self, attacker:Character, defender:Character):
        totalDmg = 0
        for i in range(self.instances):
            if config['options_game']['damageVarianceEnabled'] == "true":
                randModifier = 0.75 + (random.random()/2)
            else:
                randModifier = 1
            dmg = round(self.power*randModifier*((2*attacker.stats.mAtk) - (defender.stats.mDfc))/200)
            totalDmg += dmg
        return totalDmg
    
    def do(self, attacker:Character, defender:Character):
        battle = attacker.battle
        damage = self.calcDamage(attacker, defender)
        defender.harm(damage)
        if battle != None:
            scr_turn(battle.turnNum, battle.party, battle.enemies)
        print(f"{attacker.name} used {self.name}!")
        print(f"{attacker.name} attacked {defender.name} for {damage} dmg!")
        input()
        if defender.stats.hp == 0:
            defender.addStatus(KO())
        elif self.status is not None:
            if random.random() <= self.statusChance:
                newInstance = copy.deepcopy(self.status)
                # vvv Toxic spore has a chance to have double the level - I would rather implement this in a more dynamic way (should I add more with similar effects in the future) but this works for now
                if self.name == "Toxic Spore":
                    newInstance.lvl = random.randint(1,2)
                defender.addStatus(newInstance)

atkDefault = Attack_Physical("Attack", "Perform a weak attack.", 1, 100, 1, None, 0)
atkPsnSlash = Attack_Physical("Poison Slash", "Slash the opponent with a toxic blade. Chance to poison.", 1, 100, 1, Poison(), 0.5)
atkToxSpore = Attack_Magical("Toxic Spore", "Shoot a toxic spore, inflicting poison. Chance to double poison strength.", 1, 0, 1, Poison(), 1)
atkBurnBlade = Attack_Physical("Burning Blade", "Perform a flaming double-slash upon the opponent. Chance to burn.", 2, 60, 1, Burn(), 0.5)
atkFlamethrower = Attack_Magical("Flamethrower", "Spur endless flames towards the oppenent!", 10, 16, 1, Burn(2), 1)