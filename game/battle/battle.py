""" 
Modules imported:
- game.battle.attack: Contains definitions for various attack actions.
- game.core.display: Provides functions for displaying the battle state on the screen.
- game.core.mechanics: Contains functions for player choices and other mechanics.
"""

from game.battle.attack import *
from game.core.display import scr_turn
from game.core.mechanics import player_choice

class Battle:
    """The Battle class manages the battle between a party of characters and a group of enemies."""
    def __init__(self, party:list, enemies:list):

        self.party = party
        self.enemies = enemies

        self.active = True

        self.pending_action = False

        for member in self.party + self.enemies:
            member.battle = self

        print(f"~ {[member.name for member in party]}  VS. {[member.name for member in enemies]} ~")
        print(f"  LV. {[member.stats.lvl for member in party]}    LV. {[member.stats.lvl for member in enemies]}")

        self.turn_num = 0

        while self.active:
            self.turn()

    def turn(self):
        """Processes a single turn in the battle."""
        self.turn_num += 1
        self.active_members = [member for member in self.party + self.enemies if not member.check_status(KO())]
        for member in self.active_members:
            self.apply_damage_states(member)
            self.decrease_status_duration(member)
        speed_ordered_members = sorted(self.active_members, key=lambda member: member.stats.spd, reverse=True)
        for member in speed_ordered_members:
            if not member.check_status(KO()) and self.active:
                member.change_in_health = 0
                self.action(member)


    def action(self, user):
        """Executes the action for the given character."""
        self.pending_action = True
        while self.pending_action:
            scr_turn(self.turn_num, self.party, self.enemies)
            if user.player:
                choice = player_choice([action.name for action in battle_actions], entry=f"{user.name}'s turn: ", return_option=False)
                battle_actions[choice].do(self, user)
            else:
                user.known_skills[0].do(user)
        self.check_wipeout()

    def apply_damage_states(self, char):
        """Applies damage states to the character."""
        grouped_states = {}

        for status in char.active_states:
            if isinstance(status, StatusDamage):
                if status.stackable:
                    if type(status) not in grouped_states:
                        grouped_states[type(status)] = 0
                    grouped_states[type(status)] += status.lvl
                else:
                    if type(status) not in grouped_states:
                        grouped_states[type(status)] = status.lvl

        for status_type, lvl in grouped_states.items():
            temp_status = status_type(lvl=lvl)
            temp_status.apply(char)
            char.check_dead()

    def decrease_status_duration(self, char):
        """Decreases the duration of active statuses for the character."""
        for status in char.active_states[:]:
            if isinstance(status, StatusDamage) or isinstance(status, StatusState):
                status.duration -= 1
                if status.duration < 1:
                    char.remove_status(status)

    def special_atk_menu(self, user):
        """Displays the special attack menu for the user."""
        special_skills = user.known_skills[1:]
        if len(special_skills) >= 1:
            print("Your skills:")
            skill_list = [f"{skill.name}  [{skill.mp_cost} MP]" for skill in special_skills]
            choice = player_choice(skill_list, entry="Which special move: ")
            if choice >= 0:
                special_skills[choice].do(user)

    def check_wipeout(self):
        """Checks if either the party or the enemies have been wiped out."""
        if all(member.stats.hp == 0 for member in self.party):
            self.end(0)
        elif all(member.stats.hp == 0 for member in self.enemies):
            self.end(2)
        else:
            return None

    def end(self, outcome:int):
        """Ends the battle and processes the outcome."""
        self.active = False
        scr_turn(self.turn_num, self.party, self.enemies)
        if outcome == 0: # Loss
            print("Game over!")
        elif outcome == 1: # Escape
            print("You fled the battle!")
        elif outcome == 2: # Win
            total_battle_exp = 0
            total_battle_gold = 0
            scaling_mult = exp_scaling_modifier(self.party, self.enemies)
            for member in self.enemies:
                battle_exp = calc_battle_exp(member, scaling_mult)
                total_battle_exp += battle_exp
                battle_gold = calc_battle_gold(member)
                total_battle_gold += battle_gold
            print("Battle is over!")
            print("Rewards:")
            print(f"Exp.\t{total_battle_exp}")
            print(f"Gold\t{total_battle_gold}")
            member_battle_exp = (2*total_battle_exp)/len(self.party)
            for member in self.party:
                member.stats.add_exp(member_battle_exp)
            input()
        else:
            print("The battle ended unnaturally...?")
        for member in self.party + self.enemies:
            member.battle = None
            member.active_states.clear()
        return



# vvv  i do NOT think im understanding inheritence as much as i think i am...

class Act:
    """Base class for actions in the battle."""
    def __init__(self, name:str):
        self.name = name

    def do(self, battle, char):
        """Placeholder method for performing the action."""


class ActAttack(Act):
    """Action for performing a basic attack in the battle."""
    def __init__(self):
        super().__init__("Attack")

    def do(self, battle, char):
        """Executes the attack action for the character."""
        char.known_skills[0].do(char)

class ActSpecial(Act):
    """Action for performing a special attack in the battle."""
    def __init__(self):
        super().__init__("Special")

    def do(self, battle, char):
        """Executes the special action for the character."""
        battle.special_atk_menu(char)

class ActEscape(Act):
    """Action for escaping the battle."""
    def __init__(self):
        super().__init__("Escape")

    def do(self, battle, char):
        """Executes the escape action for the character."""
        battle.pending_action = False
        battle.end(1)


battle_actions = [ActAttack(),
                ActSpecial(),
                ActEscape()]

def exp_scaling_modifier(party:list, enemies:list):
    """Calculates the experience scaling modifier based on the levels of the party and enemies."""
    if config['options_game']['experienceScalingEnabled'] == "true":
        enemies_lvl_sum = sum(member.stats.lvl for member in enemies)
        party_lvl_sum = sum(member.stats.lvl for member in party)
        level_ratio = 10*((enemies_lvl_sum*len(party)**0.5)/(party_lvl_sum*len(enemies)**0.5) - 1)
    else:
        level_ratio = 0
    scaling_power = float(config['options_game']['experienceScalingPower'])
    return 2**(level_ratio*scaling_power)

def calc_battle_exp(char, scaling_mult):
    """Calculates the experience gained from defeating a character."""
    return round(scaling_mult*(120*(char.stats.lvl**(2/3)) + (400 * len(char.modifiers))))

def calc_battle_gold(char):
    """Calculates the gold gained from defeating a character."""
    return round(10*(char.stats.lvl**0.5) + (30 * len(char.modifiers)))
