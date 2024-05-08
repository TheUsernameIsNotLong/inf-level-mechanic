import random
from character import Character

hp_Bars = 20

def healthBar(char:Character):
    hp_Remaining = round(hp_Bars*char.stats.hp/char.stats.maxhp)
    hp_Lost = hp_Bars-hp_Remaining
    print(f"|{"█"*hp_Remaining}{"_"*hp_Lost}|")
    
def applyStatusEffects(char:Character):
    for status in char.activeStates:
        status.apply(char)
class battle:
    def __init__(self, char1:Character, char2:Character):
        self.char1 = char1
        self.char2 = char2
        
        self.active = True
        
        self.char1.battle = self
        self.char2.battle = self
        
        self.battleActions = ["Attack",
                              "Escape"]
        
        print(f"~ {char1.name}  VS. {char2.name} ~")
        print(f"  LV. {char1.stats.lvl}    LV. {char2.stats.lvl}")
        
        self.turnNum = 0
        
        while self.active == True:
            self.turn(char1, char2)
    
    def turn(self, char1:Character, char2:Character):
        self.turnNum += 1
        print(f"Turn {self.turnNum}:")
        print()
        print(f"{char2.name}")
        print(f"HP: {char2.stats.hp}/{char2.stats.maxhp}")
        healthBar(char2)
        print()
        print(f"{char1.name}")
        print(f"HP: {char1.stats.hp}/{char1.stats.maxhp}")
        healthBar(char1)
        print()
        applyStatusEffects(char1)
        applyStatusEffects(char2)
        self.action(char1, char2)
        self.action(char2, char1)
    
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
                                self.attack(char1, char2)
                                break
                            case 2:
                                self.escape()
                                break
                            case _:
                                print("You can't do that!")
                except:
                    print("You can't do that!")
        else:
            self.attack(char1, char2)
    
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
    
    def attack(self, attacker:Character, defender:Character):
        randModifier = 0.75 + (random.random()/2)
        damage = round(randModifier*((2*attacker.stats.atk) - (defender.stats.dfc)))
        print(f"{attacker.name} attacked {defender.name} for {damage} dmg!")
        defender.harm(damage)
    
    def escape(self):
        self.end(1)
    
    def calcBattleExp(self, char:Character):
        return round(120*(char.stats.lvl**(2/3)))

    def calcBattleGold(self, char:Character):
        return round(10*(char.stats.lvl**0.5))