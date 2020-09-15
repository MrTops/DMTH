"""
    
    Created by: DevTops
    Purpose: Has a function to clear the screen

"""

import os

def clearScreen():
    """Clears the output window"""
    os.system('cls' if os.name == 'nt' else 'clear')
