def player_choice(options:list, entry:str="Option: ", default_option:int=None, return_option:bool=True):
    """Prompts the player to choose an option from a list."""
    if return_option is True:
        options.insert(0,"<-- BACK")
        offset = 0
    else:
        offset = 1
    for i, choice in enumerate(options):
        print(f"{i+offset}. {options[i]}")
    while True:
        try:
            choice = input(entry)
            if (default_option is not None) and (choice == ""):
                return default_option
            choice = int(choice)
            if (choice >= offset) and (choice <= (len(options)+offset-1)):
                return choice-1
            else:
                print("That's not an option!")
        except ValueError:
            print("You can't do that!")

def player_confirm(question:str=""):
    """Asks the player to confirm a question with Yes or No."""
    print(question)
    if player_choice(["Yes", "No"], default_option=1) == 0:
        return True
    else:
        return False
