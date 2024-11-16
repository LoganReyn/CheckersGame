"""
Contains _Board and Game class. 

This is one of the most important modules 
in the checkers game. 
"""

import random

from GameLogic.PieceSquare import (Piece, 
                                   Square)

from GameLogic.LogicHelp import (InvalidSelection,
                                WhiteLost, 
                                BlackLost, 
                                _checkType, 
                                _rowColGen,
                                _checkIndex)

class _Board:

    def __init__(self, pieceStringOne, pieceStringTwo) -> None:
        self.setBoard([[Square() for col in range(8)] for row in range(8)])
        self.populateBoard(pieceStringOne, pieceStringTwo)

    def getBoard(self):
        return self.__board

    def setBoard(self, board:list[list]):
        self.__board = board

    def populateBoard(self, pieceStringOne, pieceStringTwo):
        """ Combines sequences to populate starting checkers board """
        self.__sequenceOne(0, pieceStringOne) # White Pieces
        self.__sequenceTwo(1, pieceStringOne)
        self.__sequenceOne(2, pieceStringOne)
        self.__sequenceTwo(5, pieceStringTwo) # Black Pieces
        self.__sequenceOne(6, pieceStringTwo)
        self.__sequenceTwo(7, pieceStringTwo)

    def __sequenceOne(self, row, pieceId):
        """ Populate every other square in row starting at 0. """
        for idx, square in enumerate(self.getBoard()[row]):
            if idx % 2 == 0:
                square.setOccupant(Piece(pieceId))

    def __sequenceTwo(self, row, pieceId):
        """ Populate every other square in row starting at 1. """
        for idx, square in enumerate(self.getBoard()[row]):
            if idx % 2 != 0:
                square.setOccupant(Piece(pieceId))

class Game:
    """ Class that contains board state and manipulations.  """

    def __init__(self) -> None:
        self.board      = _Board("w", "b").getBoard()
        self.selection  = None
        self.moves      = None
        self.turn       = False 
        self.gameOver   = False

    # helper functions
    def getSquare(self, rowCol:tuple[int, int]) -> Square:
        """ 
        Raises 
            - Index error if elements of tuple not between 0 and 7.
            - Type error if not tuple or if tuple elements not int
        """
        _checkType(tuple, rowCol); 
        _checkType(int, rowCol[0], rowCol[1])
        _checkIndex(0, 7, rowCol[0], rowCol[1])
        return self.board[rowCol[0]][rowCol[1]]
    
    def getPiece(self, rowCol:tuple[int, int]) -> Piece:
        return self.getSquare(rowCol).getOccupant()

    def generateAllSquares(self):
        for row, col in _rowColGen():
            yield self.getSquare((row, col))

    def generateAllPieces(self):
        for square in self.generateAllSquares():
            if square.isOccupied():
                yield square.getOccupant()

    # piece manipulation
    def _removePiece(self, rowCol:tuple[int, int]) -> None:
        self.getSquare(rowCol).setOccupant(None)
    
    def _addPiece(self, rowCol:tuple[int, int], myPiece:Piece) -> None:
        if not isinstance(myPiece, Piece): raise Exception
        self.getSquare(rowCol).setOccupant(myPiece)

    # movement functions
    def _movesJumpLogic(self, currentMove:tuple[int, int], currentKey:str) -> tuple[dict, str]:

        """ Use in a loop to either allow for a jump or remove a move if square is occupied by an enemy. """

        keyToRemove = currentKey.split(".")[-1]
        directions = [("leftUp", -1, -1), 
                      ("rightUp", -1, 1),
                      ("leftDown", 1, -1), 
                      ("rightDown", 1, 1)]
        row, col = currentMove
        addThese = {}

        try:
            for direction in directions:
                if keyToRemove == direction[0]:
                    row = row + direction[1]
                    col = col + direction[2]
                    _checkIndex(0, 7, row, col)
                    crossSquare: Square = self.getSquare((row, col))
                    if not crossSquare.isOccupied():
                        addThese.update({f"J.{keyToRemove}": (row, col)})
        except IndexError:
            ... # out of bounds, do nothing
        return (addThese, keyToRemove)
    
    def _jumpedPiece(self, currentLocation:tuple[int, int], newLocation:tuple[int, int]) -> bool:
        """ Delete piece on square if jumped. """
        if (abs(currentLocation[0] - newLocation[0]) > 1):
            midRow = (currentLocation[0] + newLocation[0]) // 2
            midCol = (currentLocation[1] + newLocation[1]) // 2
            self._removePiece((midRow, midCol))
            return True
        else: return False
    
    def _movesCleanTeam(self, currentRowCol:tuple[int, int], moves:dict):
        """ Remove possible move for Piece if square is occupied by piece of same team. """
        removeThese = []
        addThese    = {}
        myPiece     = self.getPiece(currentRowCol)

        for key, move in moves.items():
            squareInQuestion = self.getSquare(move)
            if squareInQuestion.isOccupied():
                pieceInQuestion = squareInQuestion.getOccupant()
                if myPiece.getTeam() == pieceInQuestion.getTeam():
                    # same team
                    removeThese.append(key)
                else:
                    # different team
                    toAdd, toDel = self._movesJumpLogic(move, key)
                    addThese.update(toAdd)
                    removeThese.append(toDel)
        
        for key in removeThese:
            moves.pop(key)
        moves.update(addThese)

        return moves

    def _pieceMove(self, rowCol, jmpsOnly=False):
        """ Valid moves for individual piece. """
        mvs = self.getSquare(rowCol).getOccupant().cardinalMoves(rowCol)
        mvs = self._movesCleanTeam(rowCol, mvs)
        # sequence for n jumps
        if jmpsOnly:
            mvs = self._jumpsOnlyFilter(mvs)             
        return mvs

    def _checkDictionaryKeys(self, mDict: dict, toCheck):
        """ Check if piece choice is indeed in pieces that can move. """
        tKeys = [key[0] for key in mDict.keys()]
        if toCheck not in tKeys:
            return False
        else:
            return True

    def allMoves(self):
        """ Show all moves for a team. """
        allMoveD = {}
        currentTeam = "w" if self.turn is False else "b"
        for row, col in _rowColGen():
            currentSquare = self.getSquare((row, col))
            if currentSquare.isOccupied():
                currentPiece = self.getPiece((row, col))
                if currentPiece.getTeam() == currentTeam:
                    cDict = self._pieceMove((row, col))
                    if len(cDict) > 0:
                        allMoveD[(len(allMoveD)), (row, col)] = cDict
        return allMoveD

    def choosePiece(self, allTheMoves, playChoice) -> None:
        """ Select `Piece` from moveable pieces. """
        if self._checkDictionaryKeys(allTheMoves, playChoice):
            piecePos: tuple = [key for key in allTheMoves.keys()][playChoice][1]
            self.selection = piecePos
            return None
        raise InvalidSelection(f"From moveable pieces, none selected -> {playChoice}")  

    def _jumpsOnlyFilter(self, movesDict:dict[str, tuple]) -> dict | None:
        tDict = dict()
        for key, val in movesDict.items():
            if key.startswith("J."):
                tDict[key] = val

        if len(tDict) == 0:
            return None
        else:
            return tDict

    def _singleMove(self, playChoice:str, jmpsOnly=False) -> bool:
        """
        :param playChoice: playChoice could be leftUp, J.leftUp, . . .
        :return True: if a piece was jumped in the move
        :return False: if a move was to blank square 
        """
        myPiece = self.getPiece(self.selection)
        if jmpsOnly:
            pieceMoves = self._pieceMove(self.selection, True)
        else:
            pieceMoves = self._pieceMove(self.selection)
            
        newRowCol = pieceMoves.get(playChoice)

        self._removePiece(self.selection)
        self._addPiece(newRowCol, myPiece)

        self.checkPromotion()

        if self._jumpedPiece(self.selection, newRowCol):
            self.selection = newRowCol
            return True
        else:
            return False
        
    def turnLogic(self, playChoice, keepOnlyJumps=False):
        """ Configured for human input at the moment """
        if self._singleMove(playChoice, keepOnlyJumps):
            validMoves = self._pieceMove(self.selection, True)
            if validMoves is None:
                self._changeTeam()
                self.selection = None
                return
            if len(validMoves) > 0: # check if multi jump 
                print(validMoves)
                userChoice = input("Piece Move? (None to stop jump) ")
                if userChoice: #    
                    self.turnLogic(userChoice, True)
        
        self._changeTeam()
        self.selection = None

    def computerTurnLogic(self, playChoice, keepOnlyJumps=False):
        if self._singleMove(playChoice, keepOnlyJumps):
            validMoves = self._pieceMove(self.selection, True)
            if validMoves is None:
                self.selection = None
                return
            if len(validMoves) > 0: # check if multi jump 
                possibleMoves = [keyString for keyString in validMoves.keys()]
                userChoice = random.choice(possibleMoves)
                if userChoice: 
                    self.computerTurnLogic(userChoice, True)
        self.selection = None

    def checkLoss(self, movesDict: dict) -> None:
        """ 
        :raise WhiteLost: if len(movesDict) < 1
        :raise BlackLost: if len(movesDict) < 1
        """
        # WIN CONDITION LOGIC
        # if a team has no moves, then the length of all moves should be 0
        # if a team has no pieces, how can allMoves contain any moves at all? 
        currentTeam = "b" if self.turn else "w"
        if len(movesDict) < 1:
            self.gameOver = True
            if currentTeam == "w":
                raise WhiteLost
            else:
                raise BlackLost
        else:
            return None
    
    def checkPromotion(self):
        """ If `Piece` is on last row opposite of starting side, promote to king. """
        # check white row, check black row
        row = 0
        for _ in range(2):
            for col in range(8):
                mySqure = self.getSquare((row, col))
                if mySqure.isOccupied():
                    myPiece = mySqure.getOccupant()
                    if not myPiece.isKing():
                        if myPiece.getTeam() == "w" and row == 7 or myPiece.getTeam() == "b" and row == 0:
                            myPiece.promote()
            row += 7

    def _changeTeam(self):
        """ White: False, Black: True """
        self.turn = not self.turn