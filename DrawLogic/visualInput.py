""" Functions to help understand user motives on GUI. """

from pygame.mouse import get_pos
from Misc import constants as C
from GameLogic import Environment as E

def mousePosition():
    return get_pos()

def getCords():
    x, y = mousePosition()
    x = x // C.SQUARE_SIZE
    y = y // C.SQUARE_SIZE
    return (y, x)

def getSquare(env: E):
    col, row = getCords()
    env.getSquare(col, row)

if __name__ == "__main__":
    ...