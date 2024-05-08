from math import *

class Status:
    def __init__(self, name:str, desc:str, duration:int):
        self.name = name
        self.desc = desc
        self.duration = duration
    
    def apply(self, char):
        pass

class KO(Status):
    def __init__(self):
        super().__init__("Knocked Out", "No health remaining.", -1)
    
    def apply(self, char):
        print(f"{char.name} has been knocked out!")
        char.canHeal = False
        if char.battle != None:
            if char.player == True:
                char.battle.end(0)
            else:
                char.battle.end(2)
            char.removeStatus(self)
    
class Poison(Status):
    def __init__(self, lvl:int):
        super().__init__("Poisoned", "Take reccuring damage.", 3)
        self.lvl = lvl
        
    def apply(self, char):
        damage = floor(1-(1-char.stats.hp*0.05)**self.lvl)
        char.harm(char.stats.maxhp)

class Burn(Status):
    def __init__(self, lvl:int):
        super().__init__("Burning", "Take reccuring flat damage.", 3)
        self.lvl = lvl
        
    def apply(self, char):
        damage = floor(char.stats.maxhp*0.08)
        char.harm(damage)

class Radiation(Status):
    def __init__(self, lvl:float):
        super().__init__("Radiated", "Take reccuring damage.", 5)
        self.lvl = lvl
        
    def apply(self, char):
        damage = floor(self.lvl * 0.125 * char.stats.hp)
        char.harm(damage)
        self.lvl /= 2

class Paralysis(Status):
    def __init__(self, lvl:int):
        super().__init__("Paralysed", "Unable to use physical attacks.", 3)
        self.lvl = lvl
        
    def apply(self, char):
        print("Paralysed!")
        
class Silence(Status):
    def __init__(self, lvl:int):
        super().__init__("Silenced", "Unable to use magic attacks.", 3)
        self.lvl = lvl
        
    def apply(self, char):
        print("Silenced!")
        
class Lock(Status):
    def __init__(self, lvl:int):
        super().__init__("Locked", "Unable to move.", 3)
        self.lvl = lvl
        
    def apply(self, char):
        print("Locked!")