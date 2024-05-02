import math

class stats:
    def __init__(self, lvl:int, exp:int, hp:int, atk:int, dfc:int, mAtk:int, mDfc:int, spd:int):
        self.lvl = lvl
        self.exp = exp
        self.hp = hp
        self.atk = atk
        self.dfc = dfc
        self.mAtk = mAtk
        self.mDfc = mDfc
        self.spd = spd

    def setStats(self):
        self.hp = calc_hp(self.lvl)
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

class character:
    def __init__(self, name:str, stats):
        self.name = name
        self.stats = stats
    
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
    return math.floor((exp/20)**(1/3))

def calc_expTotal(lvl):
    return 20 * lvl**3

def calc_expGoal(lvl):
    return (20 * lvl**3) - (20 * (lvl-1)**3)

def calc_hp(lvl):
    return lvl**2 + 99

def calc_atk(lvl):
    return round(lvl**1.7 + 19)

def calc_dfc(lvl):
    return round(lvl**1.5 + 9)

def calc_spd(lvl):
    return round(lvl**1.3 + 4)