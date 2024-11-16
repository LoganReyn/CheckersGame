"""
Program Name: Checkers the Fun Game
Author: Logan Reynolds
Date: 11/16/2024
Version: 1.0
Description: 
        Play a game of checkers against a bot. 
        Improve your game! Or don't.
        Created for ARTI 499: A.I. Capstone.
"""

import pygame

from GameLogic import Environment as E
from Misc import constants as C
from Database import checkersData as D
from DrawLogic import (drawBasics as VDB,
                       drawings as SCREENS)

#####################################################
## Initilizations of main Window and Database 

# Pygame Window
pygame.init()
WINDOW = pygame.display.set_mode((C.WIDTH, C.HEIGHT))
pygame.display.set_caption(C.TITLE)
pygame.display.set_icon(VDB.createSquare(C.GRAY, 20, 20))

# Database
db = D.CheckersDB("checkers_data.db")
######################################################

def main():

    print(f"{__doc__} \n Music Credit: {C.SONG_CREDIT}")

    while 1:

        myGame = E.Environment()

        SCREENS.startScreen(WINDOW)

        playerName = SCREENS.informationScreen(WINDOW)
        
        print(f"Name: {playerName}")

        option = SCREENS.gameScreen(myGame, WINDOW)

        db.addRecord(playerName,
                     option)

        match option:
            case "Reset":
                for row in db.queryAll(): print (row)
                continue
            case _:
                for row in db.queryAll(): print (row)
                print(option)
                # didnt click reset button, show end screen 
                if SCREENS.endScreen(myGame, WINDOW, option):
                    continue


if __name__ == "__main__":
    main()