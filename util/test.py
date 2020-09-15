from Menu import Menu
from Input import Input

Input.genAliveThread()
menu = Menu("DevTops", "Malware", "Ramaa", header="Pick your favorite person!")
result, index = menu.prompt()

print(f"you picked {result} at index {index}")