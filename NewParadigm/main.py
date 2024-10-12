"""
Capstone Project. 
"""


import os
from BoardGame import Game
from LogicHelp import (chooseCordinate, InvalidSelection, WhiteLost, BlackLost)

def qClear():
    os.system("cls")

if __name__ == "__main__":
    myGame = Game()
    for row in myGame.board:
        print(row)