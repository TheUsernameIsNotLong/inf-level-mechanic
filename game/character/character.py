"""
Modules imported:
- game.character.status: For managing character status effects.
- game.character.stats: For character statistics and leveling.
- game.core.mechanics: For core game mechanics like player confirmation.
- game.battle.attack: For managing character attacks and skills.
"""

from game.character.status import *
from game.character.stats import *
from game.core.mechanics import player_confirm
from game.battle.attack import *

class Character:
    """Class representing a character in the game."""
    def __init__(self, name:str, stats, player:bool):
        self.name = name
        self.stats = stats
        self.stats.char = self # im not sure how i feel about this lol
        self.player = player
        self.known_skills = [sklDefault] # All characters start with a default attack
        self.active_states = []
        self.modifiers = []
        # VVV Passive States VVV
        self.inflicted_this_turn = False # Prevents multiple status inflictions when targetted from a multi-instance skill
        self.change_in_health = 0 # The change in health this turn
        self.can_heal = True # Can recieve healing from any healing source
        self.disabled = False # Is able to have turns in battle
        # VVV Current Actions VVV
        self.battle = None # Is this character currently in a battle?

        # VVV A character's learnable skills by level VVV
        self.lvl_skills = {3:sklHeal,
                          5:sklPsnSlash,
                          11:sklBrnBlade,
                          17:sklToxSpore,
                          24:sklFlamethrower}

        for key, value in self.lvl_skills.items():
            if key <= self.stats.lvl:
                self.add_skill(value)
            else:
                break

    def harm(self, hp):
        """Reduces the character's health by a specified amount."""
        if self.stats.hp - hp < 0:
            hp = self.stats.hp # Do not allow negative health
        self.stats.hp -= hp
        self.change_in_health = -hp

    def heal(self, hp):
        """Increases the character's health by a specified amount."""
        if self.stats.hp + hp > self.stats.maxhp:
            hp = self.stats.maxhp - self.stats.hp # Do not allow overhealing
        self.stats.hp += hp
        self.change_in_health = hp

    def check_dead(self):
        """Checks if the character is dead and applies KO status if so."""
        if self.stats.hp == 0:
            self.add_status(KO())

    def add_status(self, status):
        """Adds a status effect to the character."""
        if self.battle is not None:
            scr_turn(self.battle.turn_num, self.battle.party, self.battle.enemies)
        print(f"{self.name} is inflicted with {status.name}!")
        self.active_states.append(status) # This may replace statuses with lower duration/lvl
        input()
        if isinstance(status, KO): # Run status effect immediately if defeated
            status.apply(self)

    def remove_status(self, status):
        """Removes a status effect from the character."""
        if self.battle is not None:
            scr_turn(self.battle.turn_num, self.battle.party, self.battle.enemies)
        try:
            self.active_states.remove(status)
            if not (self.check_status(status) or isinstance(status, KO)):
                print(f"{self.name} is no longer inflicted with {status.name}!")
        except ValueError:
            print(f"{self.name} is not inflicted with {status.name}!")
        input()

    def check_status(self, status):
        """Checks if the character has a specific status effect."""
        return any(isinstance(instance, type(status)) for instance in self.active_states)

    def apply_status(self):
        """Applies all active status effects to the character."""
        for s in self.active_states:
            if isinstance(s, StatusDamage):
                s.apply()

    def add_skill(self, skill, alert=True):
        """Adds a skill to the character's known skills."""
        # This does not check if they already have it!
        self.known_skills.append(skill)
        if alert is True:
            print(f"{self.name} has learnt the skill {skill.name}!")
            if config['options_game']['announceLearntSkillRead'] == "true":
                if player_confirm(question="Would you like to read about the new skill?") is True:
                    skill.readSkill()
                    input()

    def print_stats(self):
        """Prints the character's statistics."""
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
