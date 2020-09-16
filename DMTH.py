"""

    Contains some cool things were you can input text and it returns edited text

    Created By: DevTops

    Discord Message Tricks Hub
    Version: 0.1

    Usage:
        - run DMTH.py
        - select a trick, use the up-down arrows to navigate, most of them will give a short description of what they do, if they do not it will warn you.
        - the trick will prompt you to enter in some text, after this hit enter and it will spit back your output
        - you will then be prompted to either return to the main menu or do that same trick again
        
"""

from importlib import import_module
from os import listdir
from util.Input import Input
from util.Menu import Menu
from util.BoxedText import generateBoxedText
from util.Clear import clearScreen

disallowedTrickNames = [
    #This trick names will not load because they are used by the system as built in "tricks"
    "__pycache__",
    "Tricks.__pycache__",
    "Reload"
]

mainHeader = """Welcome to Discord Message Tricks Hub
- use the up key to move the selection up
- use the down key to move the selection down
- enter to select that trick
==Special Options=====================
- reload reloads from the tricks folder"""

def doesTrickHavePrompt(trick):
    try:
        if trick.prompt == None: pass
        return True
    except:
        return False

def doesTrickHaveInfo(trick):
    try:
        if trick.information == None: pass
        return True
    except:
        return False

def getNameOfTrick(trick):
    #Returns the name of a trick
    if not doesTrickHaveInfo(trick):
        return trick.__name__.split(".")[1]
    else:
        return trick.information.get("Name")

def getTrickPage(trick, box=False):
    #Makes a page out of a trick
    page = ""
    if not doesTrickHaveInfo(trick):
        page = "Name: {}\nThis trick does not contain additional information.".format(getNameOfTrick(trick))
    else:
        def getThing(thing): return (trick.information.get(thing) if trick.information.get(thing) else f"{thing} was not found")
        page = "Name: {}\nDescription: {}\nAuthor: {}\nCustom Prompt?: {}".format(getNameOfTrick(trick), getThing("Description"), getThing("Author"), ("Yes" if doesTrickHavePrompt(trick) else "No"))

    return (generateBoxedText(page) if box == True else page)

def loadTricks():
    #Returns a list of the tricks loaded
    returnTable = {}
    for trick in listdir('Tricks'):
        try:
            print(trick)
            loaded = import_module('.{}'.format(trick.split(".")[0]), 'Tricks')
            name = getNameOfTrick(loaded)
            if name in disallowedTrickNames:
                continue
            returnTable[name] = loaded
        except:
            pass

    return returnTable

def main():
    Input.genAliveThread()
    tricks = loadTricks()
    tricksMenu = Menu("Reload", header=mainHeader)
    for trick in tricks:
        tricksMenu.addSelection(getNameOfTrick(tricks[trick]))
    
    def selectionMenu():
        selected, Nil = tricksMenu.prompt()

        #edge cases
        if selected == "Reload":
            clearScreen()
            Input.flushInput()
            main()

        selectedTrick = tricks.get(selected)
        clearScreen()
        if not selectedTrick:
            clearScreen()
            print("A error ocurred, press ENTER to try again")
            print(selected)
            Input.flushInput()
            input()
            clearScreen()
            selectionMenu()
        pickMenu = Menu("Yes", "No", header="{}\nWould you like to use this trick.".format(getTrickPage(selectedTrick)))
        clearScreen()
        ready = pickMenu.prompt()[0] == "Yes"
        if ready:
            inpt = None
            if doesTrickHavePrompt(selectedTrick):
                inpt = selectedTrick.prompt()
            else:
                Input.flushInput()
                inpt = input("Input:\n")
            print("output:\n{}".format(selectedTrick.run(inpt)))
            Input.flushInput()
            input("Press enter to continue")
            selectionMenu()
        else:
            clearScreen()
            selectionMenu()
    
    selectionMenu()

main()