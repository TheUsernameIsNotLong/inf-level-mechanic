import random
import copy
import configparser
from game.character.status import *
from game.core.mechanics import playerChoice

# Prepare config file
config = configparser.ConfigParser()
config.read('config.ini')

class TargetSelector:
    def __init__(self, battle, user):
        self.battle = battle
        self.user = user

    def chooseTarget(self, group, num=1):
        if len(group) > 1:
            if (group == self.battle.enemies) and (config['options_battle']['autoTargeting'] == "true"):
                return [random.choice(self.battle.enemies)]
            else:
                targetGroup = []
                for i in range(num, 0, -1):
                    if num > 1:
                        print(f"{i} more target(s)")
                    print("Available targets:")
                    choice = playerChoice([member.name for member in group], entry="Which member: ")
                    targetGroup.append(group[choice])
                return targetGroup
        else:
            return [group[0]]

    def getTargets(self, targetType):
        enemiesAlive = [enemy for enemy in self.battle.enemies if enemy.stats.hp > 0]
        partyAlive = [member for member in self.battle.party if member.stats.hp > 0]
        try:
            match targetType:
                case "enemy1":
                    return self.chooseTarget(enemiesAlive)
                case "enemy2":
                    return self.chooseTarget(enemiesAlive, num=2)
                case "enemyA":
                    return enemiesAlive
                case "enemy1Rand":
                    return [random.choice(enemiesAlive)]
                case "enemy2Rand":
                    return random.choices(enemiesAlive, k=2)
                case "ally1":
                    return self.chooseTarget(partyAlive)
                case "ally2":
                    return self.chooseTarget(partyAlive, num=2)
                case "allyO":
                    return [member for member in partyAlive if member != self.user]
                case "allyA":
                    return partyAlive
                case "user":
                    return [self.user]
                case "all":
                    return partyAlive + enemiesAlive
                case _:
                    print("Invalid target type")
                    return None
        except:
            return [] # Default to user if something goes wrong - only seen happening so far when random.choices checks an empty list

class Skill:
    
    def __init__(self, name:str, desc:str, mpCost:int, segments:list):
        self.name = name
        self.desc = desc
        self.mpCost = mpCost
        self.segments = segments
        
    def checkValid(self, user):
        if self.mpCost <= user.stats.mp:
            user.battle.pendingAction = False
            return True
        else:
            print(f"{user.name} does not have the required MP!")
            input()
        return False
    
    def readSkill(self):
        print(f"~ ~ {self.name.upper()} ~ ~")
        print(f"POWER: {self.power} --- HITS: {self.instances}")
        print(self.desc)
    
    def do(self, user):
        if self.checkValid(user):
            user.stats.mp -= self.mpCost
            battle = user.battle
            if battle != None:
                scr_turn(battle.turnNum, battle.party, battle.enemies)
            print(f"{user.name} used {self.name}!")
            input()
            for segment in self.segments:
                segment.do(user, battle)


# The skill_segment class links damage/heals and status inflictions to certain target groups, meaning several different groups can now be affected by a single skill

class Skill_Segment:
    
    def __init__(self, magic:bool, targetType, instances:int, power:float, hitChance:float, status, statusChance:float, healing:bool=False):
        self.magic = magic
        self.targetType = targetType
        self.instances = instances # Number of times a skill can hit
        self.power = power # Affects damage/healing output on each hit - 100 is a standard attack when paired up against an opponent of similar stats, or a full heal when healing
        self.hitChance = hitChance # Chance of a skill hitting
        self.status = status # Status effect a skill can inflict
        self.statusChance = statusChance # Chance of the status effect inflicting
        self.healing = healing # Determines whether the attack damages or heals the target
                
    def chooseTarget(self, group:list, battle, num:int=1):
        if len(group) > 1:
            if (group == battle.enemies) and (config['options_battle']['autoTargeting'] == "true"): # Only apply auto targetting to enemies
                return [random.choice(battle.enemies)] # Attacking randomly is a horrible strategy
            else:
                targetGroup = []
                for i in range(num+1, 1, -1):
                    if num > 1:
                        print(f"{i} more target(s)")
                    print("Available targets:")
                    choice = playerChoice([member.name for member in group], entry="Which member: ")
                    targetGroup.append(group[choice])
                return targetGroup
        else:
            return [group[0]] # Don't offer choice if there is only 1 character in group
    
    def calcValue(self, user, target):
        totalValue = 0
        for i in range(self.instances):
            if config['options_game']['damageVarianceEnabled'] == "true":
                randModifier = 0.75 + (random.random()/2) # Random value between -25% and +25% the actual value
            else:
                randModifier = 1
            if self.healing is False:
                if self.magic is False:
                    value = round(self.power*randModifier*((2*user.stats.atk) - (target.stats.dfc))/200)
                else:
                    value = round(self.power*randModifier*((2*user.stats.mAtk) - (target.stats.mDfc))/200)
            else:
                value = round((self.power * target.stats.maxhp)/100)
            totalValue += value
        return totalValue

    def do(self, user, battle):
        targetSelector = TargetSelector(battle, user)
        if user.player is True:
            while True:
                self.target = targetSelector.getTargets(self.targetType)
                if len(self.target) > 0:
                    user.battle.pendingAction = False
                    break
                else:
                    if all(member.stats.hp == 0 for member in battle.party) or all(member.stats.hp == 0 for member in battle.enemies):
                        break
                    else:
                        print(f"There's no one to target!")
                        input()
        else:
            self.target = [random.choice(battle.party)] # Change this before giving enemies healing spells! :)

        if self.power > 0:
            for target in self.target:
                value = self.calcValue(user, target)
                if self.healing is False:
                    target.harm(value)
                    if battle:
                        scr_turn(battle.turnNum, battle.party, battle.enemies)
                    print(f"{user.name} attacked {target.name} for {value} DMG!")
                    input()
                    target.checkDead()
                else:
                    target.heal(value)
                    if battle:
                        scr_turn(battle.turnNum, battle.party, battle.enemies)
                    print(f"{user.name} healed {target.name} for {value} HP!")
                    input()

        if self.status is not None:
            for member in self.target:
                if (member.inflictedThisTurn is False) and (random.random() <= self.statusChance):
                    newInstance = copy.deepcopy(self.status)
                    member.addStatus(newInstance)
                    member.inflictedThisTurn = True # Prevents multiple inflictions on one target
    
    


# ~ SKILL SEGMENTS ~ #

singleHit = Skill_Segment(False, "enemy1", 1, 100, 1, None, 0)
singleHitPsn = Skill_Segment(False, "enemy1", 1, 100, 1, Poison(), 0.5)
singleToxSpore = Skill_Segment(True, "enemy1", 1, 0, 1, Poison(1.5), 1)
singleHitBrn = Skill_Segment(False, "enemy1", 1, 100, 1, Burn(), 0.5)
flame = Skill_Segment(True, "enemy2Rand", 3, 10, 1, Burn(2), 1)

heal = Skill_Segment(True, "user", 1, 40, 1, None, 0, True)

# ~ SKILLS ~ #

sklDefault = Skill("Attack", "Perform a weak attack.", 0, [singleHit])
sklPsnSlash = Skill("Poison Slash", "Slash the opponent with a toxic blade. Chance to poison.", 12, [singleHitPsn])
sklToxSpore = Skill("Toxic Spore", "Shoot a toxic spore, inflicting poison. Chance to double poison strength.", 22, [singleToxSpore])
sklBrnBlade = Skill("Burning Blade", "Perform a flaming double-slash upon the opponent. Chance to burn.", 18, [singleHitBrn])
sklFlamethrower = Skill("Flamethrower", "Spur endless flames towards the oppenents!", 32, [flame, flame, flame, flame])

sklHeal = Skill("Heal", "Heals the user by 40% of their HP", 18, [heal])