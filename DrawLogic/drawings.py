""" 
This module contains all screens in checkers game. 

There are 4 possible screens. 
    - start
    - information
    - game 
    - end
"""

import pygame
import sys
from datetime import date

from GameLogic import (Environment as E, 
                       LogicHelp as L)

from DrawLogic import (drawBasics as VDB, # Visual Draw Basics
                       visualInput as VI,
                       visualButton as VB)

from Misc import (startMusic as SM,
                  constants as C)


def startScreen(window):
    """ Uses constants, Button, visualInput, & pygame """

    # music
    SM.startMusic(".\Misc\Laughing_Love.mp3")

    # animation
    animationY = 100
    direction = 1
    speed = 2
    
    welcomeMessage = VDB.createText(C.TITLE, 50)
    todaysDay = VDB.createText(date.today().strftime("%A %h %d"), 30, (C.LIGHT_BROWN))
    startButton = VB.Button("CONTINUE", 300, 100, (50, 200))
    clock = pygame.time.Clock()

    while True:

        window.fill(C.PINKISH)
        clock.tick(C.FPS)
        mousePos = VI.mousePosition()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if startButton.clicked(event):
                return None # end loop
            
        # animation update
        animationY += direction * speed
        if animationY > 150 or animationY < 10:  # Limits for bouncing
            direction *= -1
        
        startButton.hovering(mousePos)
        startButton.draw(window)
        window.blits([(welcomeMessage, (0, animationY)),
                      (todaysDay, (10, C.HEIGHT - 50))])

        pygame.display.flip()

def informationScreen(window):

    clock = pygame.time.Clock()
    textBox = VB.InputBox(10, 250, 380, 50)
    userText = None


    TEXT_SIZE = 20
    STRT = (20, 40) # (x, y)


    header = VDB.createText("Info & Name Entry", TEXT_SIZE * 2)
    line1 = VDB.createText(C.GAME_INFORMATION_1, TEXT_SIZE)
    line2 = VDB.createText(C.GAME_INFORMATION_2, TEXT_SIZE)
    line3 = VDB.createText(C.GAME_INFORMATION_3, TEXT_SIZE)
    line4 = VDB.createText(C.GAME_INFORMATION_4, TEXT_SIZE)
    line5 = VDB.createText(C.GAME_INFORMATION_5, TEXT_SIZE)

    while True:

        window.fill(C.PINKISH)
        clock.tick(C.FPS)
        mousePos = VI.mousePosition()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            result = textBox.entry(event)
            if result is not None:
                pygame.mixer.stop()
                userText = result
                return userText

        window.blits([(header, (10, 5)), 
                      (line1, STRT), 
                      (line2, (STRT[0], STRT[1] * 2)),
                      (line3, (STRT[0], STRT[1] * 3)),
                      (line4, (STRT[0], STRT[1] * 4)),
                      (line5, (STRT[0], STRT[1] * 5))
                      ]) 
        
        textBox.draw(window)
        pygame.display.flip()

def gameScreen(game: E.Environment, window):

    pygame.mixer_music.stop()

    selected_piece: tuple[int, int] | None = None
    end: bool = False
    end_message: str = ""
    resetButton = VB.Button("RESET", 100, 50, (C.WIDTH-100, C.HEIGHT-50))
    clock = pygame.time.Clock()


    while True:

        clock.tick(C.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if resetButton.clicked(event):
                return "Reset"

            if event.type == pygame.MOUSEBUTTONDOWN:
                    squareCords = VI.getCords()

                    # first click, select piece
                    if selected_piece is None:
                        try:
                            game.visual_select(squareCords)
                            selected_piece = squareCords
                        except L.InvalidSelection as e:
                            continue
                        except IndexError as e:
                            continue
                    
                    # second click, select square
                    else:
                        try: # move to valid spot
                            game.visual_move(squareCords)
                            selected_piece = None
                            game.checkLoss(game.allMoves())
                            game._changeTeam()
                            game.computer_step()
                            game._changeTeam()
                        except L.InvalidSelection:
                            selected_piece = None
                            continue
                        except L.BlackLost:
                            end_message = "White Won"
                            end = True
                        except L.WhiteLost:
                            end_message = "Black Won"
                            end = True

            if not end:
                # logic updates
                theBoard = VDB.createBoard(game.board)
                turnMessage = VDB.createText(f"{"Black" if game.turn else "White"}'s Turn", 30)

                # Render of Game Screen  
                window.blit(VDB.createSquare(C.WHITE, C.WIDTH, C.HEIGHT), (0,0))
                window.blits([(theBoard, (0,0)), (turnMessage, (50, 360))])
            else:
                # Render of Final Screen
                window.blit(VDB.createSquare(C.WHITE, C.WIDTH, C.HEIGHT), (0,0))
                window.blits([(theBoard, (0,0)), (VDB.createText(end_message, 50), (0,0))])
                return end_message

            resetButton.hovering(VI.mousePosition())
            resetButton.draw(window)
            pygame.display.flip()
        
def endScreen(game: E.Environment, window, endMessage: str):

    msg = VDB.createText(endMessage, 60, C.PURPLE)
    againButton = VB.Button("Play Again", 200, 50, (C.WIDTH-200, C.HEIGHT-50))
    clock = pygame.time.Clock()


    while True:

        clock.tick(C.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if againButton.clicked(event):
                return True
            
            theBoard = VDB.createBoard(game.board)
            background = VDB.createSquare(C.WHITE, C.WIDTH, C.HEIGHT)
            window.blits([
                    (background, (0,0)),
                    (theBoard, (0,0)),
                    (msg, (0, 0))
                           ])
            
            againButton.hovering(VI.mousePosition())
            againButton.draw(window)
            pygame.display.flip()


if __name__ == "__main__":
    #####################################################
    # initilization of board 
    pygame.init()
    WINDOW = pygame.display.set_mode((C.WIDTH, C.HEIGHT))
    pygame.display.set_caption(C.TITLE)
    pygame.display.set_icon(VDB.createSquare(C.GRAY, 20, 20))
    ######################################################
    
    run = True

    while run:

        myGame = E.Environment()

        startScreen(WINDOW)
        
        informationScreen(WINDOW)

        if gameScreen(myGame, WINDOW):
            continue