def playerChoice(options:list, entry:str="Option: ", defaultOption:int=None):
    for i, choice in enumerate(options):
        print(f"{i+1}. {options[i]}")
    while True:
        try:
            choice = input(entry)
            if (defaultOption is not None) and (choice == ""):
                return defaultOption
            choice = int(choice)
            if (choice >= 1) and (choice <= len(options)):
                return choice-1
        except:
            print("You can't do that!")
            
def playerConfirm(question:str=""):
    print(question)
    if playerChoice(["Yes", "No"], defaultOption=1) == 0:
        return True
    else:
        return False