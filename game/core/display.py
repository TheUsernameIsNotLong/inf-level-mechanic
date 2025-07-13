""" 
Modules imported:
- configparser: For configuration file handling.
- os: For operating system dependent functionality.
- math: For mathematical operations.
"""

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

def colour_text(text:str, colour:str):
    """Returns the text wrapped in ANSI escape codes for colouring."""
    return f"{colour}{text}{RESET}"

# Stat bar display

HP_BARS = 20
MP_BARS = 20

def stat_bar(char, stat_bars:int):
    """Generates a health or mana bar for the character."""
    stat_remaining = round(stat_bars*char.stats.hp/char.stats.maxhp)
    stat_change = round(stat_bars*abs(char.change_in_health)/char.stats.maxhp)
    if char.change_in_health > 0:
        change = colour_text("█",GRN) * stat_change
        stat_remaining -= stat_change
    elif char.change_in_health < 0:
        change = colour_text("█",YEL) * stat_change
    else:
        change = ""
    stat_lost = stat_bars-(stat_remaining+stat_change)
    stat_all = "|" + "█" * stat_remaining + change + "_" * stat_lost + "|"
    return stat_all

def health_bar(char):
    """Generates a health bar for the character."""
    return stat_bar(char, HP_BARS)

def mana_bar(char):
    """Generates a mana bar for the character."""
    return stat_bar(char, MP_BARS)

def num_abbrev(num:float):
    """Abbreviates large numbers for display."""
    suffix = ["", "K", "M", "B", "T", "Qd", "Qi", "Sx", "Sp", "Oc", "No", "Dc"]
    if num < 1000:
        return num
    size = int(math.log10(num) // 3)
    if size <= len(suffix):
        new_num = num / (10 ** (3 * size))
        new_num = f"{new_num:.3g}"
        return f"{new_num}{suffix[size]}"
    else:
        new_num = f"{num / (10 ** math.log10(num)):.1f}"
        return f"{new_num}e{round(math.log10(num))}"

def scr_player_stat_label(current, max_length):
    """Generates a label for player stats with current and max values."""
    num_current = str(num_abbrev(current))
    num_max = str(num_abbrev(max_length))
    padding_amount = (HP_BARS+2) - (len(num_current)+len(num_max)+3) # +3 for " / "
    spaces = " " * padding_amount
    return f"{spaces}{num_current} / {num_max}"

def scr_player_hp_label(member):
    """Generates a label for player HP."""
    return scr_player_stat_label(member.stats.hp, member.stats.maxhp)

def scr_player_mp_label(member):
    """Generates a label for player MP."""
    return scr_player_stat_label(member.stats.mp, member.stats.maxmp)

def scr_member_name(member):
    """Generates a label for the member's name and level."""
    max_name_len = (HP_BARS+3) - 11 # +2 for each end of the HP bar, +1 for allowing at least 1 space between name and lvl, -10 for maximum abbreviated lvl length
    name_label = member.name[:max_name_len]
    lvl_label = f"LV. {num_abbrev(member.stats.lvl)}"
    padding_amount = (HP_BARS+2) - (len(name_label)+len(lvl_label))
    spaces = " " * padding_amount
    return f"{lvl_label}{spaces}{name_label}"

def scr_member_state(member):
    """Generates a label for the member's current status state."""
    if member.active_states:
        state = member.active_states[0]
        return f"  {state.tag} "
    else:
        return "      "


def scr_turn(turn_num:int, party:list, enemies:list):
    """Displays the current turn information and character states."""
    if config["options"]["keepPrint"] == "false":
        os.system("cls")
    print(f"~~~~~~~~~~ {len(party)} VS {len(enemies)} ~~~~~~~~~~")
    print("~~~~~~~~~~ BATTLE ~~~~~~~~~~")
    print()
    print(f"Turn {turn_num}...")
    print()
    for member in party:
        print(f"{scr_member_state(member)}{scr_member_name(member)}")
        print(f"      {health_bar(member)}")
        print(f"   {scr_player_hp_label(member)} HP")
        print(f"   {scr_player_mp_label(member)} MP")
        print()
    for member in enemies:
        print(f"{scr_member_name(member)}{scr_member_state(member)}")
        print(f"{health_bar(member)}")
        print(f"{num_abbrev(member.stats.hp)} / {num_abbrev(member.stats.maxhp)} HP")
        print()
    print("----------------------------")
