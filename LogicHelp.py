""" 
Custom Exceptions and Helper Functions for Checkers Game. 
 """

# Functions
def _checkType(typeParam, *vals):
    """ Raises Type Error"""
    for idx, val in enumerate(vals):
        if not isinstance(val, typeParam):
            raise TypeError(f"[{idx}] {val} is not type {typeParam}")
        
def _checkIndex(minParam: int, maxParam: int, *vals):
    """ Raises Type Error and Index Error"""
    _checkType(int, minParam, maxParam)
    for idx, val in enumerate(vals):
        if (val < minParam or val > maxParam):
            raise IndexError(f"[{idx}] {val} Out of range.")
        
def _stringToInt(val: str) -> int:
    """ Raises Value Error"""
    try:
        val = val.strip()
        return int(val)
    except ValueError as e:
        raise ValueError(f"Cannot Convert {val} to integer")

def inputHandle(func):
    """Error Handling for Row, Col input."""
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except IndexError:
                print("Out of Range, Try again")
                continue  
            except ValueError:
                print("Non-integer entered. Try again")
                continue
            except Exception as e:
                print(f"Unexpected error: {e}")
                break
    return wrapper

@inputHandle
def chooseCordinate():
    row = _stringToInt(input("Row: "))
    Col = _stringToInt(input("Col: "))
    _checkType(int, row, Col)
    _checkIndex(0, 7, row, Col)
    return (row, Col)

# Exceptions 
class CheckersEvent(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class InvalidSelection(CheckersEvent):
    """ Illogical Selection. """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class BlackLost(CheckersEvent):
    """ Black has lost the game. """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
class WhiteLost(CheckersEvent):
    """ White has lost the game. """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

