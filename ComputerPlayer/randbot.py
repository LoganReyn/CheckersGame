""" Computer Player Functions """

import random   

def bot_pieceSelect(dictParam: dict[tuple: str]) -> int:
    """ select random piece from dict of pieces that can move
    
    e.g.
    >>> n = bot_pieceSelect({(0, (2, 0)) : "rightDown"})
    >>> print(n)
    0
    """
    mvs = [key[0] for key in dictParam.keys()]
    jmpMvs = [key[0] for key, val in dictParam.items() if "J" in val]
    myChoice: int = random.choice(mvs)
    return myChoice

def bot_moveSelect(dictParam: dict[str, tuple]) -> str:
    """ 
    select random move from dict of moves
    will choose jump everytime
    
    >>> n = bot_moveSelect({"rightDown": (3,1)}) 
    >>> print(n) 
    rightDown
    """

    possibleMoves = [keyString for keyString in dictParam.keys()]
    for move in possibleMoves:
        if "J" in move:
            return move
    else:
        move = random.choice(possibleMoves)
        return move

if __name__ == "__main__":

    import doctest

    doctest.testmod() # if no problems, outputs nothing to console 