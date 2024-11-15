from GameLogic.LogicHelp import (WhiteLost, BlackLost, InvalidSelection, _checkIndex)
from GameLogic.BoardGame import Game
from ComputerPlayer.randbot import bot_moveSelect, bot_pieceSelect



class Environment(Game):
    """ 2nd part of Game class. """

    def __init__(self) -> None:
        super().__init__()

    def showBoard(self):
        for row in self.board:
            print(row)
            
    def showMoves(self, dictParam):
        for key, move in dictParam.items():
            print(key, move)
        
    def showTurn(self):
        print("Black" if self.turn else "White")

    def terminal_step(self):
        """ This is the human entry varient. """
        # (1) check if team lost
        # (2) choose piece from all pieces that can move
        # (3) choose move from piece selected 
        possibleMoves = self.allMoves()
        self.checkLoss(possibleMoves)
        self.showMoves(possibleMoves)
        self.choosePiece(possibleMoves, int(input("choose piece int: ")))
        self.showMoves(self._pieceMove(self.selection))
        self.turnLogic(input("Movement Selection: "))

    def computer_step(self):
        possiblePieces = self.allMoves()
        self.checkLoss(possiblePieces)
        self.choosePiece(possiblePieces, bot_pieceSelect(possiblePieces))
        possibleDirections = self._pieceMove(self.selection)
        self.computerTurnLogic(bot_moveSelect(possibleDirections))

    ###################################33





    def visual_select(self, cordsOfSelection: tuple[int, int]):
        """
        Let user select piece that can move and in accordance to proper team

        raises Invalid Selection if requirments not met
        raises Index Error if selection off the board
        """

        try:
            mySqure = self.getSquare(cordsOfSelection)
            if mySqure.isOccupied():
                myPiece = self.getPiece(cordsOfSelection)
                if len(self._pieceMove(cordsOfSelection)) > 0:
                    tmpTeam = myPiece.getTeam()
                    if (tmpTeam == "b" and self.turn) or (tmpTeam == "w" and not self.turn):
                        self.selection = cordsOfSelection
                    else:
                        raise InvalidSelection
                else:
                    raise InvalidSelection
            else:
                raise InvalidSelection("No Piece Selected")
        except IndexError:
            raise IndexError("No Square Selected")
        except InvalidSelection:
            raise InvalidSelection("Wrong Team")
            

    # Currently Working on 
    def visual_move(self, cordsOfSelection):
        # SHOULD BE: selection is set to cordinates of piece
        possibleMoves = self._pieceMove(self.selection)
        print(f"Moves for Selected piece {possibleMoves}")

        selection: tuple[int, int]
        for validMove in possibleMoves.values():
            if cordsOfSelection == validMove:
                # valid move selected so move logic needs to take place
                self.visualTurnLogic(cordsOfSelection)
                return
        else:
            raise InvalidSelection("Can't move there")



    def _visualSingleMove(self, cordsOfMove, jmpsOnly=False):
        
        myPiece = self.getPiece(self.selection)
        
        if jmpsOnly: pieceMoves = self._pieceMove(self.selection, True)
        else:        pieceMoves = self._pieceMove(self.selection)

        self._removePiece(self.selection)
        self._addPiece(cordsOfMove, myPiece)
        self.checkPromotion()

        if self._jumpedPiece(self.selection, cordsOfMove):
            self.selection = cordsOfMove
            return True
        else:
            return False

    def visualTurnLogic(self, cordsOfMove, keepOnlyJumps=False):

        if self._visualSingleMove(cordsOfMove, keepOnlyJumps):
            validMoves = self._pieceMove(self.selection, True)
            if validMoves is not None:
                if len(validMoves) > 0:
                    print("double Jump opportunity")
                    self.visualTurnLogic(list(validMoves.values())[0], True)

        self.selection = None
        # self._changeTeam()

            

    #############################################

    def choosePiece(self, allTheMoves, playChoice) -> None:
        """ Select `Piece` from moveable pieces. """
        if self._checkDictionaryKeys(allTheMoves, playChoice):
            piecePos: tuple = [key for key in allTheMoves.keys()][playChoice][1]
            self.selection = piecePos
            return None
        raise InvalidSelection(f"From moveable pieces, none selected -> {playChoice}")  


    def getGameState(self):
        return self.board

        



if __name__ == "__main__":
    myEnv = Environment()
    while (1):
        try:
            myEnv.showBoard()
            myEnv.showTurn()
            myEnv.human_step()

        except WhiteLost:
            print("White Lost")
            break
        except BlackLost:
            print("Black Lost")
            break

        except Exception as e:
            print(f"{str(e.__traceback__)}")