""" 
This module still uses the old attack system, using Physical_Attack and Magical_Attack classes,
as opposed to the new Skill_Segment and Skill classes.

Modules imported:
- json: For JSON file handling.
- game.character.character: For character management.
- game.battle.attack: For attack management.
"""

import json
from game.character.character import *
from game.battle.attack import *

party = []

SELECTED_FILE = "saves/file1.json"

def get_member_data(member):
    """Converts a Character object to a dictionary."""
    return {
        "name": member.name,
        "lvl": member.stats.lvl,
        "proficiency": {
            "hp": member.stats.prof.hp,
            "mp": member.stats.prof.mp,
            "atk": member.stats.prof.atk,
            "dfc": member.stats.prof.dfc,
            "mAtk": member.stats.prof.mAtk,
            "mDfc": member.stats.prof.mDfc,
            "spd": member.stats.prof.spd
        },
        "knownSkills": [],
        "inv": []
    }

def get_skill_data(skill):
    """Converts a skill object to a dictionary."""
    return {
        "type": 0,
        "name": skill.name,
        "desc": skill.desc,
        "mpCost": skill.mpCost,
        "instances": skill.instances,
        "power": skill.power,
        "hitChance": skill.hitChance,
        "status": skill.status.tag if skill.status else None,
        "statusChance": skill.statusChance
    }

def set_member_data(member):
    """Converts a member dictionary to a Character object."""
    return Character(member["name"],
                     Stats(member["lvl"],
                           set_proficiency_data(member["proficiency"])),
                     True)

def set_proficiency_data(prof):
    """Converts a proficiency dictionary to a Proficiency object."""
    return Proficiency("custom",
                       prof["hp"],
                       prof["mp"],
                       prof["atk"],
                       prof["dfc"],
                       prof["mAtk"],
                       prof["mDfc"],
                       prof["spd"])

def set_skill_data(skill):
    """Converts a skill dictionary to an Attack object."""
    status_class = availableStates.get(skill["status"])
    status_instance = statusClass() if status_class else None
    if skill["type"] == 0:
        return Attack_Physical(skill["name"],
                               skill["desc"],
                               skill["mpCost"],
                               skill["instances"],
                               skill["power"],
                               skill["hitChance"],
                               statusInstance,
                               skill["statusChance"])
    else:
        return Attack_Magical(skill["name"],
                              skill["desc"],
                              skill["mpCost"],
                              skill["instances"],
                              skill["power"],
                              skill["hitChance"],
                              statusInstance,
                              skill["statusChance"])

def save():
    """Saves the current party data to a JSON file."""
    data = {"party":[]}
    for member in party:
        member_data = get_member_data(member)
        data["party"].append(member_data)
        for skill in member.knownSkills:
            skill_data = get_skill_data(skill)
            if isinstance(skill, Attack_Magical):
                skill_data["type"] = 1
            member_data["knownSkills"].append(skill_data)
    with open(SELECTED_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load():
    """Loads party data from a JSON file."""
    with open(SELECTED_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(data)
    party.clear()
    for member in data["party"]:
        member_instance = set_member_data(member)
        for skill in member["knownSkills"]:
            skill_instance = set_skill_data(skill)
            member_instance.known_skills.append(skill_instance)
        party.append(member_instance)
