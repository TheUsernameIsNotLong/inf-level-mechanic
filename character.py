import math
import status
class Stats:
    def __init__(self, lvl:int, exp:int, maxhp:int, hp:int, atk:int, dfc:int, mAtk:int, mDfc:int, spd:int):
        self.lvl = lvl
        self.exp = exp
        self.maxhp = maxhp
        self.hp = hp
        self.atk = atk
        self.dfc = dfc
        self.mAtk = mAtk
        self.mDfc = mDfc
        self.spd = spd
        self.setStats()

    def setStats(self):
        self.maxhp = calc_hp(self.lvl)
        self.hp = self.maxhp
        self.atk = calc_atk(self.lvl)
        self.dfc = calc_dfc(self.lvl)
        self.mAtk = calc_atk(self.lvl)
        self.mDfc = calc_dfc(self.lvl)
        self.spd = calc_spd(self.lvl)

    def addExp(self, exp):
        self.exp += exp
        while self.exp >= calc_expGoal(self.lvl):
            self.exp -= calc_expGoal(self.lvl)
            self.lvl += 1
        self.setStats()

    def addLvl(self, lvl):
        exp = calc_expTotal(lvl + self.lvl) - calc_expTotal(self.lvl)
        self.addExp(exp)

class Character:

    def __init__(self, name:str, stats:Stats):
        self.name = name
        self.stats = stats
    
    def knockout(self):
        print(f"{self.name} has fallen!")
    
    def harm(self, hp):
        self.stats.hp -= hp
        if self.stats.hp <= 0:
            self.knockout()
            
    def add_status
    
    def printStats(self):
        print("~ CHARACTER SHEET ~")
        print(f"NAME:\t{self.name}")
        print(f"LVL:\t{self.stats.lvl}")
        print(f"EXP:\t{self.stats.exp}/{calc_expGoal(self.stats.lvl)}")
        print(f"HP:\t{self.stats.hp}")
        print(f"ATK:\t{self.stats.atk}")
        print(f"DFC:\t{self.stats.dfc}")
        print(f"M.ATK:\t{self.stats.mAtk}")
        print(f"M.DFC:\t{self.stats.mDfc}")
        print(f"SPD:\t{self.stats.spd}")

def calc_lvl(exp):
    return math.floor((exp/100)**(1/2))

def calc_expTotal(lvl):
    return 100 * lvl**2

def calc_expGoal(lvl):
    return (100 * lvl**2) - (100 * (lvl-1)**2)

def calc_hp(lvl):
    return lvl**2 + 99

def calc_atk(lvl):
    return round((0.2*lvl**2) + 19.8)

def calc_dfc(lvl):
    return round((0.15*lvl**2) + 14.85)

def calc_spd(lvl):
    return round((0.1*lvl**2) + 9.9)