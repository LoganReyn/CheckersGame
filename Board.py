import os
from PieceSquare import (Piece, Square)
from LogicHelp import (InvalidSelection, WhiteLost, BlackLost, _checkType)

        
class Board:
    """ Controller For Checkers Game. """

    def __init__(self, pieceId1, pieceId2) -> None:
        self.setTurn(False) # False = white, True = black
        self.setGameState([[Square() for col in range(8)] for row in range(8)])
        self.setMoves(None)
        self.setSelection(None)
        self.__populateBoard(pieceId1, pieceId2)
        
    def __repr__(self) -> str:
        return str(self.getGameState())
    
    def __str__(self) -> str:
        return self.__repr__()

    def __checkBounds(self, *boardParam: int):
        for param in boardParam:
            if (param > 7 or param < 0):
                raise InvalidSelection
    
    ######### GETS, SETS ###########################
    def getGameState(self) -> list[list]:
        return self.__gameState
    
    def getSelection(self) -> tuple[int, int] | None:
        return self.__selection
    
    def getTurn(self):
        return self.__turn
    
    def getMoves(self) -> dict[str, tuple[int, int]] | None:
        return self.__moves
    
    def setGameState(self, val: list[list]) -> None:
        self.__gameState = val

    def setSelection(self, rowCol=None):
        if rowCol is None:
            self.__selection = None
            return None
        try:
            myPiece = self.getPiece((rowCol[0], rowCol[1]))
            if myPiece == None:
                raise AttributeError
            if ((myPiece.getTeam() == "w" and self.getTurn()) or (myPiece.getTeam() == "b" and not self.getTurn())):
                raise InvalidSelection("Improper Team Selection")
            else:
                self.__selection = rowCol
        except AttributeError:
            raise InvalidSelection("No Piece Selected")
            
    def setTurn(self, val: bool):
        self.__turn = val
    
    def setMoves(self, moves=None):
        self.__moves = moves

    ######### OTHER GETS ###########################
    # These gets are used for logic

    def getSquare(self, rowCol: tuple[int, int]) -> Square:
        return self.getGameState()[rowCol[0]][rowCol[1]]
    
    def getPiece(self, rowCol: tuple[int, int]) -> Piece:
        try:
            return self.getSquare(rowCol).getOccupant()
        except Exception:
            raise InvalidSelection("No Piece Selected.")
        
    ######### BOARD POPULATION ######################
    def __populateBoard(self, clsOne, clsTwo):
        """ Put checkers pieces in starting squares """
        self.__sequenceOne(0, clsOne) # White Pieces
        self.__sequenceTwo(1, clsOne)
        self.__sequenceOne(2, clsOne)
        self.__sequenceTwo(5, clsTwo) # Black Pieces
        self.__sequenceOne(6, clsTwo)
        self.__sequenceTwo(7, clsTwo)

    def __sequenceOne(self, row, pieceId):
        """ Populate every other square in row starting at 0. """
        for idx, square in enumerate(self.getGameState()[row]):
            if idx % 2 == 0:
                square.setOccupant(Piece(pieceId))

    def __sequenceTwo(self, row, pieceId):
        """ Populate every other square in row starting at 1. """
        for idx, square in enumerate(self.getGameState()[row]):
            if idx % 2 != 0:
                square.setOccupant(Piece(pieceId))
    
    ############# DISPALY #############
    def displayBoard(self):
        print("~~~~~~~~~~~~~")
        for (row) in self.getGameState():
            print(row)

    def displayTurn(self):
        print("BLACK" if self.__turn else "WHITE" + "'s Turn.")
    
    def displayClear(self):
        os.system("cls")
    
    def displayMoves(self):
        print(self.getMoves())

    ########### MOVES ###############

    def __cleanUpMoves(self, toRemove:list):
        for move in toRemove:
            self.getMoves().pop(move)

    def __addMoves(self, toAdd:dict[str, tuple[int, int]]):
        self.getMoves().update(toAdd)

    def __gridMoves(self) -> None:
        myPiece: Piece = self.getPiece(self.getSelection())
        self.setMoves(myPiece.cardinalMoves(self.getSelection())) 

    def __removeSameTeamMoves(self) -> None:
        myPiece = self.getPiece(self.getSelection())
        moves = self.getMoves()
        if moves:
            toRemove = list()
            toAdd = dict()
            for key, move in moves.items():
                try:
                    otherPiece: Piece = self.getSquare(move).getOccupant()
                    if otherPiece is None: raise Exception
                except Exception as e:
                    continue
                if (myPiece.getTeam() == otherPiece.getTeam()):
                    toRemove.append(key)
                else:
                    addIt, removeIt = self.__jumpLogic(moves, key, move)
                    toAdd.update(addIt)
                    toRemove.append(removeIt)

            self.__cleanUpMoves(toRemove)
            self.__addMoves(toAdd)

    # (2.5) update dict with new square for jump
    def __jumpLogic (self, moves:dict[str, tuple[int, int]], currentKey: str, currentMove:tuple) -> tuple[dict, str]:
        """ Figure out if square after enemy piece unnocupied. Use in for loop"""
        # current square is occupied by enemy
        toAdd = {}    # for cross square empty
        row, Col = currentMove
        direction: str = currentKey.split(".")[-1]
        try:
            match direction:
                case "leftUp":
                    row -= 1
                    Col -= 1
                    self.__checkBounds(row, Col)
                    crossSquare: Square = self.getSquare((row, Col))
                    if not crossSquare.isOccupied():
                        toAdd.update({f"J.{currentKey}": (row, Col)})
                    
                case "rightUp":
                    row -= 1
                    Col += 1
                    self.__checkBounds(row, Col)
                    crossSquare: Square = self.getSquare((row, Col))
                    if not crossSquare.isOccupied():
                        toAdd.update({f"J.{currentKey}": (row, Col)})

                case "leftDown":
                    row += 1
                    Col -= 1
                    self.__checkBounds(row, Col)
                    crossSquare: Square = self.getSquare((row, Col))
                    if not crossSquare.isOccupied():
                        toAdd.update({f"J.{currentKey}": (row, Col)})

                case "rightDown":
                    row += 1
                    Col += 1
                    self.__checkBounds(row, Col)
                    crossSquare: Square = self.getSquare((row, Col))
                    if not crossSquare.isOccupied():
                        toAdd.update({f"J.{currentKey}": (row, Col)})
                case _:
                    raise KeyError
            return (toAdd, currentKey)
        except InvalidSelection: # logic if jump is out of bounds
            return (toAdd, currentKey)
        
    
    def thinkMove(self, onlyJumps=False) -> str:
        self.__gridMoves()
        self.__removeSameTeamMoves()
        if not self.getMoves(): # is None
            print("No moves available for piece")        
        
        if onlyJumps: # for recursion 
            jumpMoves = {k: v for k, v in self.getMoves().items() if k.startswith('J')}
            self.setMoves(jumpMoves)
            if not self.getMoves():
                return None
            
        self.displayMoves()
        userChoice = input("Type Key of Moves Presented: ")
        return userChoice
    
    def move(self, multiJump=False):
        
        userChoice = self.thinkMove(multiJump)

        if userChoice is None: # should only happen after recursion 
            print("No more jumps available")
            self.setTurn(not self.getTurn())
            self.__checkWinner()
            return None
        
        if userChoice not in self.getMoves().keys():
            print("No Move selected")
            return None
        
        myMove = self.getMoves()[userChoice]
        currentLocation = self.getSelection()
        pieceInTransit: Piece = self.getPiece(currentLocation)

        self.__removePiece(currentLocation)
        self.__addPiece(pieceInTransit, myMove)
        self.__checkPromotion(pieceInTransit, myMove[0])
        if self.__capturePieceMaybe(currentLocation, myMove):
            # Recursion 
            self.setSelection(myMove)
            self.move(multiJump=True)
        else:
            self.__checkWinner()
            self.__swapTurn()

    def __swapTurn(self):
        self.setMoves(None)
        self.setTurn(not self.getTurn())

    def __capturePieceMaybe(self, currentLocation, newLocation) -> bool:
        """ Delete piece on square if jumped. """
        if (abs(currentLocation[0] - newLocation[0]) > 1):
            midRow = (currentLocation[0] + newLocation[0]) // 2
            midCol = (currentLocation[1] + newLocation[1]) // 2
            self.__removePiece((midRow, midCol))
            return True
        else: return False


    ################ Some Checks #######################
    def __removePiece(self, rowCol: tuple[int, int]) -> None:
        square: Square = self.getSquare(rowCol)
        square.setOccupant(None)
    
    def __addPiece(self, cls: Piece, rowCol: tuple[int, int]) -> None:
        square = self.getSquare(rowCol)
        square.setOccupant(cls)

    def __checkPromotion(self, cls: Piece, row: int) -> None:
            if isinstance(cls, Piece):
                if not cls.isKing():
                    pieceId = cls.getId()
                    if (pieceId == "w" and row == 7) or (pieceId == "b" and row == 0):
                        cls.setId(pieceId.upper())
                        print(f" {'White' if pieceId == "w" else "Black"} Promoted to King")



######### WIN CONDITIONS #################
    def __checkWinner(self):
        self.__outOfPiece()
        if self.__noMovesWhite():
            raise WhiteLost
        if self.__noMovesBlack():
            raise BlackLost
        
    def __noMovesWhite(self):
        """ Check every square and see if a white piece can move"""
        for row, col in self.__rowColGen():
            mySquare = self.getSquare((row, col))
            if mySquare.isOccupied():
                myPiece = mySquare.getOccupant()
                if myPiece.getTeam() == "w":
                    moves = myPiece.cardinalMoves((row, col))
                    if (len(moves) < 1):
                        continue
                    for key, move in moves.items():

                        # empty square
                        if not self.getSquare(move).isOccupied():
                            return False
                        
                        #jumpable piece
                        addIt, _ = self.__jumpLogic(moves, key, move)
                        if (len(addIt) > 1):
                            return False
        return True


    def __noMovesBlack(self) -> bool:
        """ game starts at getTurn() -> False """
        for row, col in self.__rowColGen():
            mySquare = self.getSquare((row, col))
            if mySquare.isOccupied():
                myPiece = mySquare.getOccupant()
                if myPiece.getTeam() == "b":
                    moves = myPiece.cardinalMoves((row, col))
                    if (len(moves) < 1): # no moves for current piece
                        continue
                    for key, move in moves.items():
                        # empty square
                        if not self.getSquare(move).isOccupied():
                            return False
                        
                        #jumpable piece
                        addIt, _ = self.__jumpLogic(moves, key, move)
                        if (len(addIt) > 0):
                            return False
        return True
    
    def __outOfPiece(self):
        blackCount = 0
        whiteCount = 0
        for row, col in self.__rowColGen():
            mySquare = self.getSquare((row, col))
            if mySquare.isOccupied():
                myP = mySquare.getOccupant()
                if myP.getTeam() == "b":
                    blackCount += 1
                else:
                    whiteCount += 1
        if whiteCount < 1:
            raise WhiteLost
        if blackCount < 1:
            raise BlackLost
        return None
    
    def __rowColGen(self):
        for row in range(8):
            for col in range(8):
                yield (row, col)
##################################################

    
if __name__ == "__main__":

    # init
    myB = Board("w", "b")

    myB.displayBoard()
    myB.displayTurn()
    myB.setSelection((2, 0))
    myB.move()
    myB.displayBoard()