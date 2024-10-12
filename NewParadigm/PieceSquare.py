""" Square and Piece Class """

from LogicHelp import (_checkType, _checkIndex)

def cardinalHandle(func):
    """ Catches Index Error and will Return None if so. """
    def wrapper(*args, **kwargs):
        try: 
            return func(*args, **kwargs)
        except IndexError as e:
            return None 
    return wrapper


class Piece:
    """ 
    w - white Man 
    W - white King 
    b - black Man   
    B - black King   
    """

    def __init__(self, id:str) -> None:
        self.setId(id)
    
    def __str__(self):
        return f"{self.getId()}"
    
    def __repr__(self) -> str:
        return f"{self.getId()}"

    def getId(self):
        return self.__id
    
    def getTeam(self):
        return (self.__id).lower()
    
    def setId(self, id: str):
        _checkType(str, id)
        self.__id = id

    def promote(self) -> None:
        self.setId(self.__id.upper())
    
    def isKing(self) -> bool:
        return self.__id.isupper()

    # Movement 
    @cardinalHandle
    def moveLeUp(self, row, col) -> tuple[int, int]: #
        row -= 1 
        col -= 1
        _checkIndex(0, 7, row, col)
        return (row, col)

    @cardinalHandle
    def moveLeDn (self, row, col) -> tuple[int, int]:
        row += 1
        col -= 1
        _checkIndex(0, 7, row, col)
        return (row, col)

    @cardinalHandle
    def moveRiUp (self, row, col) -> tuple[int, int]:
        row -= 1
        col += 1
        _checkIndex(0, 7, row, col)
        return (row, col)

    @cardinalHandle    
    def moveRiDn(self, row, col) -> tuple[int, int]:
        row += 1
        col += 1 
        _checkIndex(0, 7, row, col)
        return (row, col)
    
    # Other Private Functions 
    def __kingFilter(self, moves:dict) -> None:
        """ Reduce 4 moves to 2 if not king. Based on team."""
        if self.isKing():
            return None
        if self.getId() == "w":
            del moves["rightUp"]
            del moves["leftUp"]
        elif self.getId() == "b":
            del moves["rightDown"]
            del moves["leftDown"]
        else:
            raise ValueError("Invalide Piece Id")       
        
    def __boundryFilter(self, moves:dict) -> None:
        """ Remove move from dictionary if None. """
        toRemove = [key for key, value in moves.items() if value is None]
        for key in toRemove:
            del moves[key]
        return None
            

    def cardinalMoves(self, rowCol:tuple[int, int]) -> dict[str, tuple]:
        """ 
        King & Boundry filter applied.      \n
        
        e.g.                                \n
            Input: rowCol = (2, 0)          \n
            Output: {'rightDown': (3, 1)}   
        """

        moves = {
            "leftDown" : self.moveLeDn(rowCol[0], rowCol[1]),
            "rightDown": self.moveRiDn(rowCol[0], rowCol[1]),
            "leftUp"   : self.moveLeUp(rowCol[0], rowCol[1]),
            "rightUp"  : self.moveRiUp(rowCol[0], rowCol[1]),
        }
        
        self.__kingFilter(moves)
        self.__boundryFilter(moves)
        return moves
        

class Square:
    
    def __init__(self, cls=None) -> None:
        self.setOccupant(cls)

    def __repr__(self) -> str:
        return f"{self.getOccupant().getId() if self.isOccupied() else '-'}" 

    def getOccupant(self) -> Piece:
        return self.__occupant
    
    def setOccupant(self, cls:Piece | None):
        self.__occupant = cls
    
    def isOccupied(self):
        return self.getOccupant() is not None


if __name__ == "__main__":

    print("Normal")
    myP = Piece("b")
    print(myP.cardinalMoves((2, 0)))
    myP.promote()
    print("King")
    print(myP.cardinalMoves((2,0)))

    myS = Square()
    myS.setOccupant(myP)
    print(myS)