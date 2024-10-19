import json
from game.character.character import *
from game.battle.attack import *

party = []

selectedFile = "saves/file1.json"

def getMemberData(member):
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

def getSkillData(skill):
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
    
def setMemberData(member):
    return Character(member["name"],
                     Stats(member["lvl"],
                           setProficiencyData(member["proficiency"])),
                     True)

def setProficiencyData(prof):
    return Proficiency("custom",
                       prof["hp"],
                       prof["mp"],
                       prof["atk"],
                       prof["dfc"],
                       prof["mAtk"],
                       prof["mDfc"],
                       prof["spd"])

def setSkillData(skill):
    statusClass = availableStates.get(skill["status"])
    statusInstance = statusClass() if statusClass else None
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
    data = {"party":[]}
    for member in party:
        memberData = getMemberData(member)
        data["party"].append(memberData)
        for skill in member.knownSkills:
            skillData = getSkillData(skill)
            if isinstance(skill, Attack_Magical):
                skillData["type"] = 1
            memberData["knownSkills"].append(skillData)
    with open(selectedFile, "w") as f:
        json.dump(data, f, indent=4)

def load():
    with open(selectedFile, "r") as f:
        data = json.load(f)
    print(data)
    party.clear()
    for member in data["party"]:
        memberInstance = setMemberData(member)
        for skill in member["knownSkills"]:
            skillInstance = setSkillData(skill)
            memberInstance.knownSkills.append(skillInstance)
        party.append(memberInstance)