from .status import *
from .stats import *
from ..core.mechanics import playerConfirm
from ..battle.attack import *

class Character:

    def __init__(self, name:str, stats, player:bool):
        self.name = name
        self.stats = stats
        self.stats.char = self # im not sure how i feel about this lol
        self.player = player
        self.knownSkills = [atkDefault] # All characters start with a default attack
        self.activeStates = []
        self.modifiers = []
        # VVV Passive States VVV
        self.canHeal = True # Can recieve healing from any healing source
        self.disabled = False # Is able to have turns in battle
        # VVV Current Actions VVV
        self.battle = None # Is this character currently in a battle?
        
        # VVV A character's learnable skills by level VVV
        self.lvlSkills = {5:atkPsnSlash,
                          11:atkBurnBlade,
                          17:atkToxSpore,
                          24:atkFlamethrower}
    
    def harm(self, hp):
        self.stats.hp -= hp
        if self.stats.hp <= 0:
            self.stats.hp = 0 # Do not allow negative health
    
    def heal(self, hp):
        self.stats.hp += hp
        if self.stats.hp > self.stats.maxhp:
            self.stats.hp = self.stats.maxhp
            
    def checkDead(self):
        if self.stats.hp == 0:
            self.addStatus(KO())
            
    def addStatus(self, status):
        if self.battle != None:
            scr_turn(self.battle.turnNum, self.battle.party, self.battle.enemies)
        print(f"{self.name} is inflicted with {status.name}!")
        self.activeStates.append(status) # This may replace statuses with lower duration/lvl
        input()
        if isinstance(status, KO): # Run status effect immediately if defeated
            status.apply(self)
    
    def removeStatus(self, status):
        if self.battle != None:
            scr_turn(self.battle.turnNum, self.battle.party, self.battle.enemies)
        try:
            self.activeStates.remove(status)
            if not (self.checkStatus(status) or isinstance(status, KO)):
                print(f"{self.name} is no longer inflicted with {status.name}!")
        except:
            print(f"{self.name} is not inflicted with {status.name}!")
        input()

    def checkStatus(self, status):
        return any(isinstance(instance, type(status)) for instance in self.activeStates)
    
    def applyStatus(self):
        for s in self.activeStates:
            if isinstance(s, Status_Damage):
                s.apply()
    
    def addSkill(self, skill, alert=True):
        # This does not check if they already have it!
        self.knownSkills.append(skill)
        if alert == True:
            print(f"{self.name} has learnt the skill {skill.name}!")
            if config['options_game']['announceLearntSkillRead'] == "true":
                if playerConfirm(question="Would you like to read about the new skill?") == True:
                    skill.readSkill()
                    input()
    
    def printStats(self):
        print("~ CHARACTER SHEET ~")
        print(f"NAME:\t{self.name}")
        print(f"LVL:\t{self.stats.lvl}")
        print(f"EXP:\t{self.stats.exp}/{self.stats.calc_expGoal(self.stats.lvl)}")
        print(f"HP:\t{self.stats.hp}")
        print(f"MP:\t{self.stats.mp}")
        print(f"ATK:\t{self.stats.atk}")
        print(f"DFC:\t{self.stats.dfc}")
        print(f"M.ATK:\t{self.stats.mAtk}")
        print(f"M.DFC:\t{self.stats.mDfc}")
        print(f"SPD:\t{self.stats.spd}")