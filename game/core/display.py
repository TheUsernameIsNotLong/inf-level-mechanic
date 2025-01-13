import configparser
import os
import math

# Prepare config file
config = configparser.ConfigParser()
config.read('config.ini')

# Foreground colors
BLK = "\033[30m"
RED = "\033[31m"
GRN = "\033[32m"
YEL = "\033[33m"
BLU = "\033[34m"
MAG = "\033[35m"
CYN = "\033[36m"
WHT = "\033[37m"

BR_BLK = "\033[90m"
BR_RED = "\033[91m"
BR_GRN = "\033[92m"
BR_YEL = "\033[93m"
BR_BLU = "\033[94m"
BR_MAG = "\033[95m"
BR_CYN = "\033[96m"
BR_WHT = "\033[97m"

# Styles
BOLD = "\033[1m"
ULINE = "\033[4m"
RESET = "\033[0m"  # Reset to default color and style

def colourText(text:str, colour:str):
    return f"{colour}{text}{RESET}"

# Stat bar display

hp_Bars = 20
mp_Bars = 20

def statBar(char, stat_Bars:int):
    stat_Remaining = round(stat_Bars*char.stats.hp/char.stats.maxhp)
    stat_Change = round(stat_Bars*abs(char.changeInHealth)/char.stats.maxhp)
    if char.changeInHealth > 0:
        change = colourText("█",GRN) * stat_Change
        stat_Remaining -= stat_Change
    elif char.changeInHealth < 0:
        change = colourText("█",YEL) * stat_Change
    else:
        change = ""
    stat_Lost = stat_Bars-(stat_Remaining+stat_Change)
    stat_all = "|" + "█" * stat_Remaining + change + "_" * stat_Lost + "|"
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
    if size <= len(suffix):
        newNum = num / (10 ** (3 * size))
        newNum = f"{newNum:.3g}"
        return f"{newNum}{suffix[size]}"
    else:
        newNum = f"{num / (10 ** math.log10(num)):.1f}"
        return f"{newNum}e{round(math.log10(num))}"

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

def scr_memberState(member):
    if member.activeStates:
        state = member.activeStates[0]
        return f"  {state.tag} "
    else:
        return f"      "
        

def scr_turn(turnNum:int, party:list, enemies:list):
    if config["options"]["keepPrint"] == "false":
        os.system("cls")
    print(f"~~~~~~~~~~ {len(party)} VS {len(enemies)} ~~~~~~~~~~")
    print("~~~~~~~~~~ BATTLE ~~~~~~~~~~")
    print()
    print(f"Turn {turnNum}...")
    print()
    for member in party:
        print(f"{scr_memberState(member)}{scr_memberName(member)}")
        print(f"      {healthBar(member)}")
        print(f"   {scr_playerHpLabel(member)} HP")
        print(f"   {scr_playerMpLabel(member)} MP")
        print()
    for member in enemies:
        print(f"{scr_memberName(member)}{scr_memberState(member)}")
        print(f"{healthBar(member)}")
        print(f"{numAbbrev(member.stats.hp)} / {numAbbrev(member.stats.maxhp)} HP")
        print()
    print("----------------------------")