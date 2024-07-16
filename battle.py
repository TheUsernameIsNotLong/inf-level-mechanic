import random
import configparser
from character import Character
from attack import *

# Prepare config file
config = configparser.ConfigParser()
config.read('config.ini')

def healthBar(char:Character):
    hp_Bars_Default = 20
    hp_Bars = hp_Bars_Default + (2*char.stats.prof.hp)
    hp_Remaining = round(hp_Bars*char.stats.hp/char.stats.maxhp)
    hp_Lost = hp_Bars-hp_Remaining
    hp_all = "|" + "█" * hp_Remaining + "_" * hp_Lost + "|"
    print(hp_all)

class Battle:
    def __init__(self, party:list, enemies:list):
        self.party = party
        self.enemies = enemies
        
        self.active = True
        
        for member in self.party + self.enemies:
            member.battle = self
        
        self.battleActions = [Act_Attack(),
                              Act_Special(),
                              Act_Escape()]
        
        print(f"~ {party}  VS. {enemies} ~")
        print(f"  LV. {[member.stats.lvl for member in party]}    LV. {[member.stats.lvl for member in enemies]}")
        
        self.turnNum = 0
        
        while self.active == True:
            self.turn()
    
    def turn(self):
        self.turnNum += 1
        print(f"Turn {self.turnNum}...")
        print()
        for member in self.party + self.enemies:
            self.applyDamageStates(member)
        print()
        for member in self.party + self.enemies:
            print(f"{member.name}")
            print(f"HP: {member.stats.hp}/{member.stats.maxhp}")
            healthBar(member)
            print()
        speedOrderedMembers = sorted(self.party+self.enemies,key=lambda member: member.stats.spd, reverse=True)
        for member in speedOrderedMembers:
            self.action(member)
        for member in self.party + self.enemies:
            self.decreaseStatusDuration(member)
    
    def action(self, char:Character):
        if self.active != True:
            return #Exit the battle
        if char.player == True:
            for i in range(len(self.battleActions)):
                print(f"{i+1}. {self.battleActions[i].name}")
            while True:
                try:
                    choice = int(input(f"{char.name}'s turn: "))
                    if (choice >= 1) and (choice <= len(self.battleActions)):
                        target = self.playerChooseTarget()
                        self.battleActions[choice-1].do(char, target)
                        break
                except:
                    print("You can't do that!")
        else:
            target = random.choice(self.party)
            char.knownSkills[0].do(char, target)
    
    def playerChooseTarget(self):
        if len(self.enemies) > 1:
            if config['battle']['autoTargeting'] == "true":
                return random.choice(self.enemies)
            else:
                print("Available targets:")
                for i in range(len(self.enemies)):
                    print(f"{i+1}. {self.enemies[i].name}")
                while True:
                    try:
                        choice = int(input("Which enemy: "))
                        if (choice >= 1) and (choice <= len(self.enemies)):
                            return self.enemies[choice-1]
                    except:
                        print("You can't do that!")
        else:
            return self.enemies[0]
    
    def applyDamageStates(self, char:Character):
        groupedStates = {}
        
        for status in char.activeStates:
            if isinstance(status, Status_Damage):
                if status.stackable:
                    if type(status) not in groupedStates:
                        groupedStates[type(status)] = 0
                    groupedStates[type(status)] += status.lvl
                else:
                    if type(status) not in groupedStates:
                        groupedStates[type(status)] = status.lvl
                    
        for statusType, lvl in groupedStates.items():
            tempStatus = statusType(lvl=lvl)
            tempStatus.apply(char)
            
    def decreaseStatusDuration(self, char:Character):
        for status in char.activeStates[:]:
            if isinstance(status, Status_Damage) or isinstance(status, Status_State):
                status.duration -= 1
                if status.duration < 1:
                    char.removeStatus(status)
    
    def escape(self):
        self.end(1)
    
    def calcBattleExp(self, char:Character):
        return round(120*(char.stats.lvl**(2/3)) + (400 * len(char.modifiers)))

    def calcBattleGold(self, char:Character):
        return round(10*(char.stats.lvl**0.5) + (30 * len(char.modifiers)))
    
    def end(self, outcome:int):
        self.active = False
        if outcome == 0: # Loss
            print("Game over!")
        elif outcome == 1: # Escape
            print("You fled the battle!")
        elif outcome == 2: # Win
            totalBattleExp = 0
            totalBattleGold = 0
            for member in self.enemies:
                battleExp = self.calcBattleExp(member)
                totalBattleExp += battleExp
                battleGold = self.calcBattleGold(member)
                totalBattleGold += battleGold
            print("Battle is over!")
            print("Rewards:")
            print(f"Exp.\t{totalBattleExp}")
            print(f"Gold\t{totalBattleGold}")
            memberBattleExp = (2*totalBattleExp)/len(self.party)
            for member in self.party:
                member.stats.addExp(memberBattleExp)
        else:
            print("The battle ended unnaturally...?")
        for member in self.party + self.enemies:
            member.battle = None


class Act:
    
    def __init__(self, name:str):
        self.name = name
        
    def do(self):
        pass

    
class Act_Attack(Act):
    
    def __init__(self):
        super().__init__("Attack")
    
    def do(self, char:Character, target:Character):
        char.knownSkills[0].do(char, target)


class Act_Special(Act):
    
    def __init__(self):
        super().__init__("Special")
    
    def do(self, char:Character, target:Character):
        specialAtkMenu(char, target)


class Act_Escape(Act):
    
    def __init__(self):
        super().__init__("Escape")
    
    def do(self, char:Character, target:Character):
        self.escape()


def specialAtkMenu(char1:Character, char2:Character):
    if len(char1.knownSkills) >= 2:
        print("Your skills:")
        for i in range(len(char1.knownSkills)-1): # The character's default attack is first in the list
            print(f"{i+1}. {char1.knownSkills[i+1].name}")
        while True:
            try:
                choice = int(input("Which special move: "))
                if (choice >= 1) and (choice <= len(char1.knownSkills)-1):
                    char1.knownSkills[choice].do(char1, char2)
                    break
            except:
                print("You can't do that!")