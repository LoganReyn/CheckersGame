""" Database for Checkers the Fun Game. """

import sqlite3
from typing import Literal

class CheckersDB:
    """
    Database Configured for Checkers the Fun Game. 

    `Information`
    - `ID:` Integer, Primary Key, Auto-incremented
    - `name:` Text, Name of the game
    - `winner:` Text, Either 'White' or 'Black'
    - `date:` Timestamp, Default is the current timestamp
    """

    TABLE_NAME = "Information"

    def __init__(self,
                 filePath: str
                 ) -> None:
        
        self.filePath = filePath
        self.connection = self._connect()
        self.connection.cursor().execute(
            f"""
                CREATE TABLE IF NOT EXISTS {CheckersDB.TABLE_NAME} (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    winner TEXT NOT NULL,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
        )

    def __del__(self):
        if self.connection:
            self.connection.commit()
            self.connection.close()

    @property
    def filePath(self):
        return self.__filePath
    
    @filePath.setter
    def filePath(self, path: str):
        self.__filePath = path
    
    @property
    def connection(self):
        return self.__connection
    
    @connection.setter
    def connection(self, cx: sqlite3.Connection):
        self.__connection = cx

    @connection.deleter
    def connection(self):
        self.connection.commit()
        self.connection.close()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.filePath)
    
    def addRecord(self,
                  name: str,
                  winner: Literal["White", "Black", "No Winner"]):
        
        self.connection.cursor().execute(
            f"""
                INSERT INTO {CheckersDB.TABLE_NAME} (name, winner)
                    VALUES (?, ?)
            """,
            (name, winner)
        )
    
    def queryAll(self):
        cur = self.connection.cursor()
        cur.execute(f"SELECT * FROM {CheckersDB.TABLE_NAME}")
        rows = cur.fetchall()
        return rows
    

if __name__ == "__main__":
    db = CheckersDB("test_checkers_data.db")
    db.addRecord("Logan",
                "Black")
    print(db.queryAll())