from util.Input import Input

def prompt():
    Input.flushInput()
    return input("Yes: ")

def run(inputString):
    return f"*{inputString}*"