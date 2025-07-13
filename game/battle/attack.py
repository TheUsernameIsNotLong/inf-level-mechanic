""" 
Modules imported:
- random: For random target selection.
- copy: For deep copying status effects.
- configparser: For reading configuration settings from a file.
- game.character.status: Contains status effects like Poison and Burn.
- game.core.mechanics: Contains the player_choice function for user input.
"""

import random
import copy
import configparser
from game.character.status import *
from game.core.mechanics import player_choice

# Prepare config file
config = configparser.ConfigParser()
config.read('config.ini')

class TargetSelector:
    """Class to handle target selection in battles."""
    def __init__(self, battle, user):
        self.battle = battle
        self.user = user

    def choose_target(self, group, num=1):
        """Choose a target from a group of characters."""
        if len(group) > 1:
            if (group == self.battle.enemies) and (config['options_battle']['autoTargeting'] == "true"):
                return [random.choice(self.battle.enemies)]
            else:
                target_group = []
                for i in range(num, 0, -1):
                    if num > 1:
                        print(f"{i} more target(s)")
                    print("Available targets:")
                    choice = player_choice([member.name for member in group], entry="Which member: ")
                    target_group.append(group[choice])
                return target_group
        else:
            return [group[0]]

    def get_targets(self, target_type):
        """Get targets based on the specified target type."""
        enemies_alive = [enemy for enemy in self.battle.enemies if enemy.stats.hp > 0]
        party_alive = [member for member in self.battle.party if member.stats.hp > 0]
        try:
            match target_type:
                case "enemy1":
                    return self.choose_target(enemies_alive)
                case "enemy2":
                    return self.choose_target(enemies_alive, num=2)
                case "enemyA":
                    return enemies_alive
                case "enemy1Rand":
                    return [random.choice(enemies_alive)]
                case "enemy2Rand":
                    return random.choices(enemies_alive, k=2)
                case "ally1":
                    return self.choose_target(party_alive)
                case "ally2":
                    return self.choose_target(party_alive, num=2)
                case "allyO":
                    return [member for member in party_alive if member != self.user]
                case "allyA":
                    return party_alive
                case "user":
                    return [self.user]
                case "all":
                    return party_alive + enemies_alive
                case _:
                    print("Invalid target type")
                    return None
        except (IndexError, KeyError): # Not sure if this is the right error to catch lol
            return [] # Default to user if something goes wrong - only seen happening so far when random.choices checks an empty list

class Skill:
    """Class representing a skill that can be used in battle."""
    def __init__(self, name:str, desc:str, mp_cost:int, segments:list):
        self.name = name
        self.desc = desc
        self.mp_cost = mp_cost
        self.segments = segments

    def check_valid(self, user):
        """Check if the skill can be used by the user."""
        if self.mp_cost <= user.stats.mp:
            user.battle.pending_action = False
            return True
        else:
            print(f"{user.name} does not have the required MP!")
            input()
        return False

    def read_skill(self):
        """Display skill information."""
        print(f"~ ~ {self.name.upper()} ~ ~")
        print(f"POWER: ? --- HITS: ? --- MP COST: {self.mp_cost}")
        print(self.desc)

    def do(self, user):
        """Execute the skill if valid."""
        if self.check_valid(user):
            user.stats.mp -= self.mp_cost
            battle = user.battle
            if battle is not None:
                scr_turn(battle.turn_num, battle.party, battle.enemies)
            print(f"{user.name} used {self.name}!")
            input()
            for segment in self.segments:
                segment.do(user, battle)


# The skill_segment class links damage/heals and status inflictions to certain target groups, meaning several different groups can now be affected by a single skill

class SkillSegment:
    """Class representing a segment of a skill that can perform an action."""
    def __init__(self, magic:bool, target_type, instances:int, power:float, hit_chance:float, status, status_chance:float, healing:bool=False):
        self.magic = magic
        self.target_type = target_type
        self.instances = instances # Number of times a skill can hit
        self.power = power # Affects damage/healing output on each hit - 100 is a standard attack when paired up against an opponent of similar stats, or a full heal when healing
        self.hit_chance = hit_chance # Chance of a skill hitting
        self.status = status # Status effect a skill can inflict
        self.status_chance = status_chance # Chance of the status effect inflicting
        self.healing = healing # Determines whether the attack damages or heals the target

    def choose_target(self, group:list, battle, num:int=1):
        """Choose a target from a group of characters."""
        if len(group) > 1:
            if (group == battle.enemies) and (config['options_battle']['autoTargeting'] == "true"): # Only apply auto targetting to enemies
                return [random.choice(battle.enemies)] # Attacking randomly is a horrible strategy
            else:
                target_group = []
                for i in range(num+1, 1, -1):
                    if num > 1:
                        print(f"{i} more target(s)")
                    print("Available targets:")
                    choice = player_choice([member.name for member in group], entry="Which member: ")
                    target_group.append(group[choice])
                return target_group
        else:
            return [group[0]] # Don't offer choice if there is only 1 character in group

    def calc_value(self, user, target):
        """Calculate the value of the attack or heal."""
        total_value = 0
        for _ in range(self.instances):
            if config['options_game']['damageVarianceEnabled'] == "true":
                rand_modifier = 0.75 + (random.random()/2) # Random value between -25% and +25% the actual value
            else:
                rand_modifier = 1
            if self.healing is False:
                if self.magic is False:
                    value = round(self.power*rand_modifier*((2*user.stats.atk) - (target.stats.dfc))/200)
                else:
                    value = round(self.power*rand_modifier*((2*user.stats.m_atk) - (target.stats.m_dfc))/200)
            else:
                value = round((self.power * target.stats.maxhp)/100)
            total_value += value
        return total_value

    def do(self, user, battle):
        """Execute the skill segment."""
        target_selector = TargetSelector(battle, user)
        if user.player is True:
            while True:
                target = target_selector.get_targets(self.target_type)
                if len(target) > 0:
                    user.battle.pending_action = False
                    break
                else:
                    if all(member.stats.hp == 0 for member in battle.party) or all(member.stats.hp == 0 for member in battle.enemies):
                        break
                    else:
                        print("There's no one to target!")
                        input()
        else:
            target = [random.choice(battle.party)] # Change this before giving enemies healing spells! :)

        if self.power > 0:
            for member in target:
                value = self.calc_value(user, member)
                if self.healing is False:
                    member.harm(value)
                    if battle:
                        scr_turn(battle.turn_num, battle.party, battle.enemies)
                    print(f"{user.name} attacked {member.name} for {value} DMG!")
                    input()
                    member.check_dead()
                else:
                    member.heal(value)
                    if battle:
                        scr_turn(battle.turn_num, battle.party, battle.enemies)
                    print(f"{user.name} healed {member.name} for {value} HP!")
                    input()

        if self.status is not None:
            for member in target:
                if (member.inflicted_this_turn is False) and (random.random() <= self.status_chance):
                    new_instance = copy.deepcopy(self.status)
                    member.add_status(new_instance)
                    member.inflicted_this_turn = True # Prevents multiple inflictions on one target




# ~ SKILL SEGMENTS ~ #

singleHit = SkillSegment(False, "enemy1", 1, 100, 1, None, 0)
singleHitPsn = SkillSegment(False, "enemy1", 1, 100, 1, Poison(), 0.5)
singleToxSpore = SkillSegment(True, "enemy1", 1, 0, 1, Poison(1.5), 1)
singleHitBrn = SkillSegment(False, "enemy1", 1, 100, 1, Burn(), 0.5)
flame = SkillSegment(True, "enemy2Rand", 3, 10, 1, Burn(2), 1)

heal = SkillSegment(True, "user", 1, 40, 1, None, 0, True)

# ~ SKILLS ~ #

sklDefault = Skill("Attack", "Perform a weak attack.", 0, [singleHit])
sklPsnSlash = Skill("Poison Slash", "Slash the opponent with a toxic blade. Chance to poison.", 12, [singleHitPsn])
sklToxSpore = Skill("Toxic Spore", "Shoot a toxic spore, inflicting poison. Chance to double poison strength.", 22, [singleToxSpore])
sklBrnBlade = Skill("Burning Blade", "Perform a flaming double-slash upon the opponent. Chance to burn.", 18, [singleHitBrn])
sklFlamethrower = Skill("Flamethrower", "Spur endless flames towards the oppenents!", 32, [flame, flame, flame, flame])
sklHeal = Skill("Heal", "Heals the user by 40% of their HP", 18, [heal])
