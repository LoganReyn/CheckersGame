""" Function's for Drawing Game Board. """

import pygame
from GameLogic.PieceSquare import Square, Piece
import Misc.constants as C

def createSquare(color: tuple[int, int, int], width: int , height: int) -> pygame.Surface:
    mySquare = pygame.Surface((width, height))
    mySquare.fill(color)
    return mySquare

def createCircle(color: tuple[int, int, int], radius: int):
    """ Create transparent surface, draw circle on it. """
    myCircle = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA) # SRCALPHA allows for transparent pixels
    pygame.draw.circle(myCircle, color, (radius, radius), radius)
    return myCircle

def createText(text: str, textSize: int, textColor: tuple=(0,0,0)):
    font = pygame.font.Font(None, textSize)
    myText = font.render(f"{text}", True, textColor)
    return myText

def createBoard(gameState: list[list]) -> pygame.Surface:
    brd: pygame.Surface = createSquare(C.BLACK, 320, 320)
    squareOne: pygame.Surface  = createSquare(C.DARK_BROWN, C.SQUARE_SIZE, C.SQUARE_SIZE)
    squareTwo: pygame.Surface = createSquare(C.LIGHT_BROWN, C.SQUARE_SIZE, C.SQUARE_SIZE)

    # peices 
    whiteMan = createCircle(C.GRAY, C.SQUARE_SIZE // 2)
    blackMan = createCircle(C.BLACK, C.SQUARE_SIZE // 2)
    kingMarker = createCircle(C.GOLD, C.SQUARE_SIZE / 2.5)
    
    for idxRow, row in enumerate(gameState):
        for idxCol, col in enumerate(row):

            x = idxCol * C.SQUARE_SIZE
            y = idxRow * C.SQUARE_SIZE

            # alternate squres 
            if (idxRow + idxCol) % 2 == 0:
                sqr = squareOne
            else:
                sqr = squareTwo

            # draw square 
            brd.blit(sqr, (x, y))

            col: Square
            if col.isOccupied():
                id: str
                id = col.getOccupant().getId()
                match id:
                    case "w":
                        brd.blit(whiteMan, (x, y))
                    case "W":
                        brd.blit(whiteMan, (x, y ))
                        brd.blit(kingMarker, (x, y))
                    case "b":
                        brd.blit(blackMan, (x, y))
                    case "B":
                        brd.blit(blackMan, (x, y))
                        brd.blit(kingMarker, (x, y))
                    case _:
                        ...
    return brd