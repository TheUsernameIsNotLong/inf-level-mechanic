from math import floor, ceil

class Status:
    def __init__(self, name:str, desc:str):
        self.name = name
        self.desc = desc
    
    def apply(self, char):
        pass
    
class Status_Special(Status):
    def __init__(self, name:str, desc:str):
        super().__init__(name, desc)

class Status_Damage(Status):
    def __init__(self, name:str, desc:str, lvl:float, duration:int, stackable:bool):
        super().__init__(name, desc)
        self.lvl = lvl
        self.duration = duration
        self.stackable = stackable
    
    def printDamage(self, char, damage):
        print(f"{char.name} took {damage} {self.name} damage!")
        
class Status_State(Status):
    def __init__(self, name:str, desc:str, duration:int):
        super().__init__(name, desc)
        self.duration = duration

class KO(Status_Special):
    def __init__(self):
        super().__init__("Knocked Out", "No health remaining.")
    
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
    def __init__(self, lvl:float=1, duration:int=3):
        super().__init__("Poison", "Take reccuring damage.", lvl, duration, True)
        
    def apply(self, char):
        damage = floor(char.stats.hp*(1-(1-0.05)**self.lvl))
        self.printDamage(char, damage)
        char.harm(damage)

class Burn(Status_Damage):
    def __init__(self, lvl:float=1):
        super().__init__("Burn", "Take reccuring flat damage.", lvl, 1, False)
        self.duration += self.lvl
        
    def apply(self, char):
        damage = floor(char.stats.maxhp*0.08)
        self.printDamage(char, damage)
        char.harm(damage)

class Radiation(Status_Damage):
    def __init__(self, lvl:float=1):
        super().__init__("Radiation", "Take reccuring damage.", lvl, 5, True)
        
    def apply(self, char):
        damage = floor(self.lvl * 0.125 * char.stats.hp)
        self.printDamage(char, damage)
        char.harm(damage)
        self.lvl /= 2

class Paralysis(Status_State):
    def __init__(self, duration:int=3):
        super().__init__("Paralysed", "Unable to use physical attacks.", duration)
        
    def apply(self, char):
        print("Paralysed!")
        
class Silence(Status_State):
    def __init__(self, duration:int=2):
        super().__init__("Silenced", "Unable to use magic attacks.", duration)
        
    def apply(self, char):
        print("Silenced!")
        
class Lock(Status_State):
    def __init__(self, duration:int=2):
        super().__init__("Locked", "Unable to move.", duration)
        
    def apply(self, char):
        print("Locked!")

def effectPoison(self, char):
        char.harm(floor(1-(1-char.stats.hp*0.05)**self.lvl))

