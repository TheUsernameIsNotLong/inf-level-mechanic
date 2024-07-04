import random
from character import Character
from attack import *



def healthBar(char:Character):
    hp_Bars_Default = 20
    hp_Bars = hp_Bars_Default + (2*char.stats.prof.hp)
    hp_Remaining = round(hp_Bars*char.stats.hp/char.stats.maxhp)
    hp_Lost = hp_Bars-hp_Remaining
    hp_all = "|" + "█" * hp_Remaining + "_" * hp_Lost + "|"
    print(hp_all)

class Battle:
    def __init__(self, char1:Character, char2:Character):
        self.char1 = char1
        self.char2 = char2
        
        self.active = True
        
        self.char1.battle = self
        self.char2.battle = self
        
        self.battleActions = ["Attack",
                              "Special",
                              "Escape"]
        
        print(f"~ {char1.name}  VS. {char2.name} ~")
        print(f"  LV. {char1.stats.lvl}    LV. {char2.stats.lvl}")
        
        self.turnNum = 0
        
        while self.active == True:
            self.turn(char1, char2)
    
    def turn(self, char1:Character, char2:Character):
        self.turnNum += 1
        print(f"Turn {self.turnNum}...")
        print()
        self.applyDamageStates(char1)
        self.applyDamageStates(char2)
        print()
        print(f"{char2.name}")
        print(f"HP: {char2.stats.hp}/{char2.stats.maxhp}")
        healthBar(char2)
        print()
        print(f"{char1.name}")
        print(f"HP: {char1.stats.hp}/{char1.stats.maxhp}")
        healthBar(char1)
        print()
        if char1.stats.spd >= char2.stats.spd:
            self.action(char1, char2)
            self.action(char2, char1)
        else:
            self.action(char2, char1)
            self.action(char1, char2)
        self.decreaseStatusDuration(char1)
        self.decreaseStatusDuration(char2)
    
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
    
    def specialAtkMenu(self, char1:Character, char2:Character):
        if len(char1.knownSkills) >= 2:
            print("Your skills:")
            for i in range(len(char1.knownSkills)-1):
                print(f"{i+1}. {char1.knownSkills[i+1].name}")
            while True:
                try:
                    choice = int(input("Which special move: "))
                    if (choice >= 1) and (choice <= len(char1.knownSkills)-1):
                        char1.knownSkills[choice].do(char1, char2)
                        break
                except:
                    print("You can't do that!")
    
    def action(self, char1:Character, char2:Character):
        if self.active != True:
            return #Exit the battle
        if char1.player == True:
            for i in range(len(self.battleActions)):
                print(f"{i+1}. {self.battleActions[i]}")
            while True:
                try:
                    choice = int(input("Your turn: "))
                    if (choice >= 1) and (choice <= len(self.battleActions)):
                        match choice:
                            case 1:
                                char1.knownSkills[0].do(char1, char2)
                                break
                            case 2:
                                self.specialAtkMenu(char1, char2)
                                break
                            case 3:
                                self.escape()
                                break
                            case _:
                                print("You can't do that!")
                except:
                    print("You can't do that!")
        else:
            char1.knownSkills[0].do(char1, char2)
    
    def end(self, outcome:int):
        self.active = False
        self.char1.battle = None
        self.char2.battle = None
        if outcome == 0: # Loss
            print("Game over!")
        elif outcome == 1: # Escape
            print("You fled the battle!")
        elif outcome == 2: # Win
            battleExp = self.calcBattleExp(self.char2)
            battleGold = self.calcBattleGold(self.char2)
            print("Battle is over!")
            print("Rewards:")
            print(f"Exp.\t{battleExp}")
            print(f"Gold\t{battleGold}")
            self.char1.stats.addExp(battleExp)
        else:
            print("The battle ended unnaturally...?")
    
    # def attack(self, attacker:Character, defender:Character):
    #     randModifier = 0.75 + (random.random()/2)
    #     damage = round(randModifier*((2*attacker.stats.atk) - (defender.stats.dfc)))
    #     print(f"{attacker.name} attacked {defender.name} for {damage} dmg!")
    #     defender.harm(damage)
    
    def escape(self):
        self.end(1)
    
    def calcBattleExp(self, char:Character):
        return round(120*(char.stats.lvl**(2/3)))

    def calcBattleGold(self, char:Character):
        return round(10*(char.stats.lvl**0.5))