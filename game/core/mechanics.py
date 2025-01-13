def playerChoice(options:list, entry:str="Option: ", defaultOption:int=None, returnOption:bool=True):
    if returnOption is True:
        options.insert(0,"<-- BACK")
        offset = 0
    else:
        offset = 1
    for i, choice in enumerate(options):
        print(f"{i+offset}. {options[i]}")
    while True:
        try:
            choice = input(entry)
            if (defaultOption is not None) and (choice == ""):
                return defaultOption
            choice = int(choice)
            if (choice >= offset) and (choice <= (len(options)+offset-1)):
                return choice-1
            else:
                print("That's not an option!")
        except:
            print("You can't do that!")
            
def playerConfirm(question:str=""):
    print(question)
    if playerChoice(["Yes", "No"], defaultOption=1) == 0:
        return True
    else:
        return False