"""Wrapper for my shotty game logic"""
from LogicHelp import (WhiteLost, BlackLost)
from BoardGame import Game



"""

Step needs to return 
    next game state, rewards, done flag, info





"""


class Environment(Game):
    """
    Game contains
        reset method

    
    """

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

    def human_step(self):
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

    def step(self, action):
        """ step for computer 
        
        next game state, rewards, done flag, info
        """
        possibleMoves = self.allMoves()
        doneFlag = self.gameOver


        return doneFlag


    def reward(self):...

    def getGameState(self):
        return self.board

        



if __name__ == "__main__":
    myEnv = Environment()
    while (1):
        try:
            myEnv.reset()
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