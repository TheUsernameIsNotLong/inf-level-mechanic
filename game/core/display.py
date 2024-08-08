import configparser
import os
import math

# Prepare config file
config = configparser.ConfigParser()
config.read('config.ini')

hp_Bars = 20
mp_Bars = 20

def statBar(char, stat_Bars:int):
    stat_Remaining = round(stat_Bars*char.stats.hp/char.stats.maxhp)
    stat_Lost = stat_Bars-stat_Remaining
    stat_all = "|" + "█" * stat_Remaining + "_" * stat_Lost + "|"
    return stat_all

def healthBar(char):
    return statBar(char, hp_Bars)

def manaBar(char):
    return statBar(char, mp_Bars)

def numAbbrev(num:float):
    suffix = ["", "K", "M", "B", "T", "Qd", "Qi", "Sx", "Sp", "Oc", "No", "Dc"]
    if num < 1000:
        return num
    size = int(math.log10(num) // 3)
    newNum = num / (10 ** (3 * size))
    newNum = f"{newNum:.4g}"
    return f"{newNum}{suffix[size]}"

def scr_playerStatLabel(member, current, max):
    numCurrent = str(numAbbrev(current))
    numMax = str(numAbbrev(max))
    paddingAmount = (hp_Bars+2) - (len(numCurrent)+len(numMax)+3) # +3 for " / "
    spaces = " " * paddingAmount
    return f"{spaces}{numCurrent} / {numMax}"

def scr_playerHpLabel(member):
    return scr_playerStatLabel(member, member.stats.hp, member.stats.maxhp)

def scr_playerMpLabel(member):
    return scr_playerStatLabel(member, member.stats.mp, member.stats.maxmp)

def scr_memberName(member):
    maxNameLen = (hp_Bars+3) - 11 # +2 for each end of the HP bar, +1 for allowing at least 1 space between name and lvl, -10 for maximum abbreviated lvl length
    nameLabel = member.name[:maxNameLen]
    lvlLabel = f"LV. {numAbbrev(member.stats.lvl)}"
    paddingAmount = (hp_Bars+2) - (len(nameLabel)+len(lvlLabel))
    spaces = " " * paddingAmount
    return f"{lvlLabel}{spaces}{nameLabel}"

def scr_turn(turnNum:int, party:list, enemies:list):
    if config["options"]["keepPrint"] == "false":
        os.system("cls")
    print(f"~~~~~~~~~~ {len(party)} VS {len(enemies)} ~~~~~~~~~~")
    print("~~~~~~~~~~ BATTLE ~~~~~~~~~~")
    print()
    print(f"Turn {turnNum}...")
    print()
    for member in party:
        print(f"      {scr_memberName(member)}")
        print(f"      {healthBar(member)}")
        print(f"   {scr_playerHpLabel(member)} HP")
        print(f"   {scr_playerMpLabel(member)} MP")
        print()
    for member in enemies:
        print(f"{scr_memberName(member)}")
        print(f"{healthBar(member)}")
        print(f"{numAbbrev(member.stats.hp)} / {numAbbrev(member.stats.maxhp)} HP")
        print()
    print("----------------------------")