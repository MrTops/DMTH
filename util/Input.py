"""

    Used to handle key inputs
    Imported from: https://github.com/MrTops/Spelunkr/blob/master/Input.py
    Created by: DevTops

"""

import keyboard
import threading
import time
import msvcrt

class Input(object):
    @staticmethod
    def flushInput():
        """
            flushes input stream/buffer
        """
        while msvcrt.kbhit():
            msvcrt.getch()

    @staticmethod
    def genAliveThread():
        """
            creates then runs a thread to keep the process from exiting
            then returns it
        """
        def func(): time.sleep(999999)

        aliveThread = threading.Timer(9999, func)
        aliveThread.start()
        return aliveThread

    def __init__(self):
        self.KeysDown = []
        self.KeyHooks = {}
    
    def hookKeyEventDecorator(self, keyname):
        """
            hooks a key using a decorator
            @Input.hookKeyEventDecorator(keyname)
        """
        def wrapper(function):
            if not keyname in self.KeyHooks: self.KeyHooks[keyname] = []
            self.KeyHooks[keyname].append(function)
        return wrapper
    
    def hookKeyEvent(self, function, keyname):
        """
            hooks a predefined function to a key, it's recommended to use decorators
        """
        if not keyname in self.KeyHooks: self.KeyHooks[keyname] = []
        self.KeyHooks[keyname].append(function)
    
    def unhookKey(self, keyname):
        """
            unhooks a key event then returns the function if exists
        """
        if keyname in self.KeyHooks:
            save = self.KeyHooks[keyname]
            del self.KeyHooks[keyname]
            return save
        else:
            return None
    
    def unhookAll(self):
        """
            unhooks ALL key events
        """
        self.KeyHooks = {}
        self.KeysDown = []

    def start(self):
        """
            starts listening to key presses and keyhooks
        """

        def keypress(e):
            down = keyboard.is_pressed(e.name)

            if down:
                if e.name in self.KeysDown: return
                self.KeysDown.append(e.name)
                if e.name in self.KeyHooks:
                    for hook in self.KeyHooks[e.name]: hook(down)
            elif not down:
                if e.name in self.KeysDown: self.KeysDown.remove(e.name)
                if e.name in self.KeyHooks:
                    for hook in self.KeyHooks[e.name]: hook(down)
        
        keyboard.hook(keypress)
