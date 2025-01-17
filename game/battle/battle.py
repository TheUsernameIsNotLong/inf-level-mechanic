import random
from .attack import *
from game.core.display import scr_turn
from game.core.mechanics import playerChoice

class Battle:
    
    def __init__(self, party:list, enemies:list):
        
        self.party = party
        self.enemies = enemies
        
        self.active = True
        
        self.pendingAction = False
        
        for member in self.party + self.enemies:
            member.battle = self
        
        print(f"~ {[member.name for member in party]}  VS. {[member.name for member in enemies]} ~")
        print(f"  LV. {[member.stats.lvl for member in party]}    LV. {[member.stats.lvl for member in enemies]}")
        
        self.turnNum = 0
        
        while self.active:
            self.turn()
    
    def turn(self):
        self.turnNum += 1
        self.activeMembers = [member for member in self.party + self.enemies if not member.checkStatus(KO())]
        for member in self.activeMembers:
            self.applyDamageStates(member)
            self.decreaseStatusDuration(member)
        speedOrderedMembers = sorted(self.activeMembers, key=lambda member: member.stats.spd, reverse=True)
        for member in speedOrderedMembers:
            if not member.checkStatus(KO()) and self.active:
                member.changeInHealth = 0
                self.action(member)
            
    
    def action(self, user):
        self.pendingAction = True
        while self.pendingAction:
            scr_turn(self.turnNum, self.party, self.enemies)
            if user.player == True:
                choice = playerChoice([action.name for action in battleActions], entry=f"{user.name}'s turn: ", returnOption=False)
                battleActions[choice].do(self, user)
            else:
                user.knownSkills[0].do(user)
        self.checkWipeout()
    
    def applyDamageStates(self, char):
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
            char.checkDead()
            
    def decreaseStatusDuration(self, char):
        for status in char.activeStates[:]:
            if isinstance(status, Status_Damage) or isinstance(status, Status_State):
                status.duration -= 1
                if status.duration < 1:
                    char.removeStatus(status)
    
    def specialAtkMenu(self, user):
        specialSkills = user.knownSkills[1:]
        if len(specialSkills) >= 1:
            print("Your skills:")
            skillList = [f"{skill.name}  [{skill.mpCost} MP]" for skill in specialSkills]
            choice = playerChoice(skillList, entry="Which special move: ")
            if choice >= 0:
                specialSkills[choice].do(user)
    
    def checkWipeout(self):
        if all(member.stats.hp == 0 for member in self.party):
            self.end(0)
        elif all(member.stats.hp == 0 for member in self.enemies):
            self.end(2)
        else:
            return None
    
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
            scalingMult = expScalingModifier(self.party, self.enemies)
            for member in self.enemies:
                battleExp = calcBattleExp(member, scalingMult)
                totalBattleExp += battleExp
                battleGold = calcBattleGold(member)
                totalBattleGold += battleGold
            print("Battle is over!")
            print("Rewards:")
            print(f"Exp.\t{totalBattleExp}")
            print(f"Gold\t{totalBattleGold}")
            memberBattleExp = (2*totalBattleExp)/len(self.party)
            for member in self.party:
                member.stats.addExp(memberBattleExp)
            input()
        else:
            print("The battle ended unnaturally...?")
        for member in self.party + self.enemies:
            member.battle = None
            member.activeStates.clear()
        return
        


# vvv  i do NOT think im understanding inheritence as much as i think i am...

class Act:
    
    def __init__(self, name:str):
        self.name = name
        
    def do(self):
        pass

    
class Act_Attack(Act):
    
    def __init__(self):
        super().__init__("Attack")
    
    def do(self, battle, char):
        char.knownSkills[0].do(char)

class Act_Special(Act):
    
    def __init__(self):
        super().__init__("Special")
    
    def do(self, battle, char):
        battle.specialAtkMenu(char)

class Act_Escape(Act):
    
    def __init__(self):
        super().__init__("Escape")
    
    def do(self, battle, char):
        battle.pendingAction = False
        battle.end(1)


battleActions = [Act_Attack(),
                Act_Special(),
                Act_Escape()]

def expScalingModifier(party:list, enemies:list):
    if config['options_game']['experienceScalingEnabled'] == "true":
        enemiesLvlSum = sum(member.stats.lvl for member in enemies)
        partyLvlSum = sum(member.stats.lvl for member in party)
        levelRatio = 10*((enemiesLvlSum*len(party)**0.5)/(partyLvlSum*len(enemies)**0.5) - 1)
    else:
        levelRatio = 0
    scalingPower = float(config['options_game']['experienceScalingPower'])
    return 2**(levelRatio*scalingPower)

def calcBattleExp(char, scalingMult):
    return round(scalingMult*(120*(char.stats.lvl**(2/3)) + (400 * len(char.modifiers))))

def calcBattleGold(char):
    return round(10*(char.stats.lvl**0.5) + (30 * len(char.modifiers)))