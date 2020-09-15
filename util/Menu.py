"""
    
    Created by: DevTops
    Purpose: A easy handler to prompt a user from a list of content.

"""

from Clear import clearScreen
from BoxedText import generateBoxedText
from Input import Input
from time import sleep

class Menu(object):
    """

        Object to prompt the user to select something from a list of content
        
        *selections
        strings that the user can select from when prompted

        **options
        options.header | printed at the top of a refreshed screen.

    """
    def __init__(self, *selections, **options):
        self.selections = selections
        self.header = options.get("header")
        self.input = Input()
        self.index = 0
        self.input.start()

    def refreshScreen(self):
        self.fixIndex()
        clearScreen()
        if self.header:
            print(generateBoxedText(self.header))
        body = "\n"
        index = 0
        for selection in self.selections:
            line = ""
            if index == self.index: line += "█"
            line += selection
            body += f"{line}\n"
            index+=1
        
        body = generateBoxedText(body)
        print(body)
        

    def addSelection(self, *selections):
        """
            Adds some selections to the menu
        """
        self.selections += selections
        self.refreshScreen()

    def removeSelection(self, *selections):
        """
            Removes the given things from the selections
        """
        for selection in selections:
            try:
                del self.selections[self.selections.index(selection)]
            except:
                pass
        self.refreshScreen()  

    def fixIndex(self):
        """
            Gets self.index fixed if it's out-of-whack

            if self.index is 3 but the max index is 2 then it will set it to 0, if it's below 0 it will set it back to 0

        """ 
        if self.index < 0:
            self.index = 0
        elif self.index > len(self.selections) - 1:
            self.index = 0
    
    def indexUp(self):
        """
            moves the index up *down in number terms*, if it is 0 then it will wrap around to len(self.selections) - 1, if not it will just subtract one
        """
        if self.index <= 0:
            self.index = len(self.selections) - 1
        else:
            self.index -= 1
        self.fixIndex()
        self.refreshScreen()
    
    def indexDown(self):
        """
            moves the index down *up in number terms*, if it is = to len(self.selections) - 1 it will get set to 0, else it will just add one
        """
        if self.index >= len(self.selections):
            self.index = 0
        else:
            self.index += 1
        self.fixIndex()
        self.refreshScreen()
            
    def prompt(self, **options):
        """
        
            Makes the user enter in which selection they'd like to select

            return the string they selected and the index they selected

            **options
            startIndex | the index the prompt the user to start at, defaults to 0
            clearBuffer | wether or not the input buffer should be cleared, defaults to True
            doneCheckTime | how long to wait inbetween done checks, default is 0.5
            
            I recommend to not turn off clear buffer as it protects the prompt from getting skipped.
            done check time shouldn't be too low, if it's too low it maybe lag, if it's too high the user may have issues
        """
        startIndex = options.get("startIndex") or 0
        clearBuffer = options.get("clearBuffer") or True
        if clearBuffer == True: self.input.flushInput()
        self.index = startIndex

        self.refreshScreen()

        done = False
        result = False
        index = False

        @self.input.hookKeyEventDecorator('up')
        def event(up):
            if not up: return
            self.indexUp()

        @self.input.hookKeyEventDecorator('down')
        def event(up):
            if not up: return
            self.indexDown()
        
        @self.input.hookKeyEventDecorator('enter')
        def event(up):
            if not up: return
            self.input.unhookAll()
            nonlocal done
            nonlocal result
            nonlocal index
            result = self.selections[self.index]
            index = self.index
            done = True

        while not done:
            sleep(0.5)

        self.input.flushInput()

        return result, index