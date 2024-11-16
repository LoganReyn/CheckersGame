""" Functions to help draw. """

import pygame
import sys
import Misc.constants as C
import GameLogic.Environment as E
import DrawLogic.drawBasics as drawBasics
from GameLogic.LogicHelp import (WhiteLost, 
                                 BlackLost)

#####################################################
# initilization of board 
pygame.init()
WINDOW = pygame.display.set_mode((C.WIDTH, C.HEIGHT))
pygame.display.set_caption(C.TITLE)
pygame.display.set_icon(drawBasics.createSquare(C.GRAY, 20, 20))
clock = pygame.time.Clock()
######################################################

myGame = E.Environment()


def main():

    end = False
    end_message = ""

    while 1:
        clock.tick(C.FPS)

        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        try:
            myGame.computer_step()
            myGame._changeTeam()
        except BlackLost:
            end = True
            end_message = "White Won"

        except WhiteLost:
            end = True
            end_message = "Black Won"

                                
        if not end:
            # logic updates
            theBoard = drawBasics.createBoard(myGame.board)
            turnMessage = drawBasics.createText(f"{'Black' if myGame.turn else 'White'}'s Turn", 30)


            # Render        
            WINDOW.blit(drawBasics.createSquare(C.WHITE, C.WIDTH, C.HEIGHT), (0,0))
            WINDOW.blit(theBoard, (0,0))
            WINDOW.blit(turnMessage, (0, 360))
        
        else:
            WINDOW.blit(drawBasics.createSquare(C.WHITE, C.WIDTH, C.HEIGHT), (0,0))
            WINDOW.blit(theBoard, (0,0))
            WINDOW.blit(drawBasics.createText(end_message, 50), (0, 0))

        pygame.display.update()

if __name__ == "__main__":
    main()
    