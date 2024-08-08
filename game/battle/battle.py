import random
import configparser
from game.character.character import Character
from .attack import *
from game.core.display import scr_turn
from game.core.mechanics import playerChoice

# Prepare config file
config = configparser.ConfigParser()
config.read('config.ini')


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
        
        print(f"~ {[member.name for member in party]}  VS. {[member.name for member in enemies]} ~")
        print(f"  LV. {[member.stats.lvl for member in party]}    LV. {[member.stats.lvl for member in enemies]}")
        
        self.turnNum = 0
        
        while self.active == True:
            self.turn()
    
    def turn(self):
        self.turnNum += 1
        for member in self.party + self.enemies:
            self.applyDamageStates(member)
        speedOrderedMembers = sorted(self.party + self.enemies, key=lambda member: member.stats.spd, reverse=True)
        for member in speedOrderedMembers:
            if self.active == True:
                self.action(member)
        for member in self.party + self.enemies:
            self.decreaseStatusDuration(member)
    
    def action(self, char:Character):
        scr_turn(self.turnNum, self.party, self.enemies)
        if char.player == True:
            choice = playerChoice([action.name for action in self.battleActions], entry=f"{char.name}'s turn: ")
            self.battleActions[choice].do(self, char, self.playerChooseTarget())
        else:
            target = random.choice(self.party)
            char.knownSkills[0].do(char, target)
    
    def playerChooseTarget(self):
        if len(self.enemies) > 1:
            if config['options_battle']['autoTargeting'] == "true":
                return random.choice(self.enemies)
            else:
                print("Available targets:")
                choice = playerChoice([enemy.name for enemy in self.enemies], entry="Which enemy: ")
                return self.enemies[choice]
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
            if char.stats.hp == 0:
                char.addStatus(KO())
            
    def decreaseStatusDuration(self, char:Character):
        for status in char.activeStates[:]:
            if isinstance(status, Status_Damage) or isinstance(status, Status_State):
                status.duration -= 1
                if status.duration < 1:
                    char.removeStatus(status)
    
    def specialAtkMenu(self, char1:Character, char2:Character):
        if len(char1.knownSkills) >= 2:
            print("Your skills:")
            choice = playerChoice([skill.name for skill in char1.knownSkills[1:]], entry="Which special move: ")
            char1.knownSkills[choice+1].do(char1, char2)
    
    def calcBattleExp(self, char:Character):
        return round(120*(char.stats.lvl**(2/3)) + (400 * len(char.modifiers)))

    def calcBattleGold(self, char:Character):
        return round(10*(char.stats.lvl**0.5) + (30 * len(char.modifiers)))
    
    def end(self, outcome:int):
        self.active = False
        scr_turn(self.turnNum, self.party, self.enemies)
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
        return
        


class Act:
    
    def __init__(self, name:str):
        self.name = name
        
    def do(self):
        pass

    
class Act_Attack(Act):
    
    def __init__(self):
        super().__init__("Attack")
    
    def do(self, battle:Battle, char:Character, target:Character):
        char.knownSkills[0].do(char, target)


class Act_Special(Act):
    
    def __init__(self):
        super().__init__("Special")
    
    def do(self, battle:Battle, char:Character, target:Character):
        battle.specialAtkMenu(char, target)


class Act_Escape(Act):
    
    def __init__(self):
        super().__init__("Escape")
    
    def do(self, battle:Battle, char:Character, target:Character):
        battle.end(1)