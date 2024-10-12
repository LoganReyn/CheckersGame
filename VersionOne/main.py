"""
Capstone Project. 
"""
# TODO:
#       Implement AI Bot
#       Make Game Look good via Pygame 


import os
from Board import Board
from LogicHelp import (chooseCordinate, InvalidSelection, WhiteLost, BlackLost)

def qClear():
    os.system("cls")

if __name__ == "__main__":

    os.system("cls")

    myB = Board("w", "b")

    run = True
    """
    setup the jump here
    """
    # myB.setSelection((2, 0))
    # myB.move()
    # myB.setSelection((5, 1))
    # myB.move()
    # myB.setSelection((2,2))
    # myB.move()

    while (1):

        qClear()
        myB.displayBoard()
        myB.displayTurn()

        row, Col = chooseCordinate() # exception handling accounted for 

        # MAY NEED TO ADD MORE EXCEPTION HANDLING!
        try:
            myB.setSelection((row, Col))
        except InvalidSelection as e:
            print(e)
            continue

        if myB.getSelection() is None: 
            continue
        
        # movement stuff 
        try:
            myB.move()
        except WhiteLost:
            print("Black wins! Game over")
            exit()
        except BlackLost:
            print("White wins! Game over")
            exit()
