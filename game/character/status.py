import random
from math import floor, ceil
from game.core.display import scr_turn

class Status:
    def __init__(self, tag:str, name:str, desc:str):
        self.tag = tag
        self.name = name
        self.desc = desc
    
    def apply(self, char):
        pass
    
class Status_Special(Status):
    def __init__(self, tag:str, name:str, desc:str):
        super().__init__(tag, name, desc)

class Status_Damage(Status):
    def __init__(self, tag:str, name:str, desc:str, lvl:float, duration:int, stackable:bool):
        super().__init__(tag, name, desc)
        self.lvl = lvl
        self.duration = duration
        self.stackable = stackable
    
    def lvlRound(self):
        lvlLower = int(self.lvl)
        lvlPart = self.lvl - lvlLower
        if random.random() > lvlPart:
            self.lvl = lvlLower
        else:
            self.lvl = lvlLower + 1
    
    def printDamage(self, char, damage):
        battle = char.battle
        if battle != None:
            scr_turn(battle.turnNum, battle.party, battle.enemies)
        print(f"{char.name} took {damage} {self.name} damage!")
        input()
    
    def apply(self):
        if not self.lvl.is_integer():
            self.lvlRound()
        
class Status_State(Status):
    def __init__(self, tag:str, name:str, desc:str, duration:int):
        super().__init__(tag, name, desc)
        self.duration = duration

class KO(Status_Special):
    def __init__(self):
        super().__init__("KO", "Knocked Out", "No health remaining.")
    
    def apply(self, char):
        print(f"{char.name} has been knocked out!")
        char.canHeal = False
        if char.battle != None:
            if char.player == True:
                char.battle.end(0)
            else:
                char.battle.end(2)
            char.removeStatus(self)
    
class Poison(Status_Damage):
    def __init__(self, lvl:float=1, duration:int=4):
        super().__init__("PSN", "Poison", "Take reccuring damage.", lvl, duration, True)
        
    def apply(self, char):
        super().apply()
        damage = floor(char.stats.hp*(1-(1-0.05)**self.lvl))
        char.harm(damage)
        self.printDamage(char, damage)

class Burn(Status_Damage):
    def __init__(self, lvl:float=1):
        super().__init__("BRN", "Burn", "Take reccuring flat damage.", lvl, 1, False)
        self.duration += self.lvl
        
    def apply(self, char):
        super().apply()
        damage = floor(char.stats.maxhp*0.08)
        char.harm(damage)
        self.printDamage(char, damage)

class Radiation(Status_Damage):
    def __init__(self, lvl:float=1):
        super().__init__("RAD", "Radiation", "Take reccuring damage.", lvl, 5, True)
        
    def apply(self, char):
        super().apply()
        damage = floor(self.lvl * 0.125 * char.stats.hp)
        char.harm(damage)
        self.printDamage(char, damage)
        self.lvl /= 2

class Paralysis(Status_State):
    def __init__(self, duration:int=3):
        super().__init__("PAR", "Paralysed", "Unable to use physical attacks.", duration)
        
    def apply(self, char):
        print("Paralysed!")
        
class Silence(Status_State):
    def __init__(self, duration:int=2):
        super().__init__("SIL", "Silenced", "Unable to use magic attacks.", duration)
        
    def apply(self, char):
        print("Silenced!")
        
class Lock(Status_State):
    def __init__(self, duration:int=2):
        super().__init__("LOK", "Locked", "Unable to move.", duration)
        
    def apply(self, char):
        print("Locked!")

availableStates = {
    "KO": KO,
    "PSN": Poison,
    "BRN": Burn,
    "RAD": Radiation,
    "PAR": Paralysis,
    "SIL": Silence,
    "LOK": Lock
}