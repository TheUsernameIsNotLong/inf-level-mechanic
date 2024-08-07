from status import *
from proficiency import *
from stats import *

class Character:

    def __init__(self, name:str, stats:Stats, player:bool):
        self.name = name
        self.stats = stats
        self.player = player
        self.knownSkills = []
        self.activeStates = []
        self.modifiers = []
        # VVV Passive States VVV
        self.canHeal = True # Can recieve healing from any healing source
        # VVV Current Actions VVV
        self.battle = None # Is this character currently in a battle?
    
    def harm(self, hp):
        self.stats.hp -= hp
        if self.stats.hp <= 0:
            self.stats.hp = 0 # Do not allow negative health
    
    def heal(self, hp):
        self.stats.hp += hp
        if self.stats.hp > self.stats.maxhp:
            self.stats.hp = self.stats.maxhp
            
    def addStatus(self, status:Status):
        if self.battle != None:
            scr_turn(self.battle.turnNum, self.battle.party, self.battle.enemies)
        print(f"{self.name} is inflicted with {status.name}!")
        self.activeStates.append(status) # This may replace statuses with lower duration/lvl
        input()
        if isinstance(status, KO): # Run status effect immediately if defeated
            status.apply(self)
    
    def removeStatus(self, status:Status):
        if self.battle != None:
            scr_turn(self.battle.turnNum, self.battle.party, self.battle.enemies)
        try:
            self.activeStates.remove(status)
            if not (self.checkStatus(status) or isinstance(status, KO)):
                print(f"{self.name} is no longer inflicted with {status.name}!")
        except:
            print(f"{self.name} is not inflicted with {status.name}!")
        input()

    def checkStatus(self, status:Status):
        return any(isinstance(instance, type(status)) for instance in self.activeStates)
    
    def applyStatus(self):
        for s in self.activeStates:
            if isinstance(s, Status_Damage):
                s.apply()
    
    def printStats(self):
        print("~ CHARACTER SHEET ~")
        print(f"NAME:\t{self.name}")
        print(f"LVL:\t{self.stats.lvl}")
        print(f"EXP:\t{self.stats.exp}/{self.stats.calc_expGoal(self.stats.lvl)}")
        print(f"HP:\t{self.stats.hp}")
        print(f"ATK:\t{self.stats.atk}")
        print(f"DFC:\t{self.stats.dfc}")
        print(f"M.ATK:\t{self.stats.mAtk}")
        print(f"M.DFC:\t{self.stats.mDfc}")
        print(f"SPD:\t{self.stats.spd}")