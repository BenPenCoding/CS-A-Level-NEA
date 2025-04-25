import sqlite3
import os
import hashlib
import pickle

path = os.path.dirname(__file__)

salt = "ParanoidNokiaPigstepStrangers"

def createTables():

    connection = sqlite3.connect(os.path.join(path,'userDB.db'))
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL)''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS userData (
            username TEXT NOT NULL,
            gameName TEXT NOT NULL,
            FOREIGN KEY(username) REFERENCES users(username),
            FOREIGN KEY(gameName) REFERENCES gameData(gameName),
            PRIMARY KEY(username, gameName))''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gameData (
            gameName TEXT PRIMARY KEY,
            board BLOB NOT NULL,
            turn TEXT,
            numMoves TEXT)''')

    connection.commit()
    connection.close()

def emptyTable(tableName):

    connection = sqlite3.connect(os.path.join(path,'userDB.db'))
    cursor = connection.cursor()

    try:
        cursor.execute(f"DELETE FROM {tableName}")
    
    except:
        print("Invalid table name")

    finally:
        connection.commit()
        connection.close()

def addUser(username, password):
    
    connection = sqlite3.connect(os.path.join(path,'userDB.db'))
    cursor = connection.cursor()

    password = hashlib.md5(f"{password}{salt}".encode('utf-8'))
    
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password.digest()))
        connection.commit()
        print("User added successfully!")

    except sqlite3.IntegrityError:
        print("Username is taken.")

    finally:
        connection.close()

def loginUser(username, password):

    connection = sqlite3.connect(os.path.join(path,'userDB.db'))
    cursor = connection.cursor()

    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))

    result = cursor.fetchone()

    connection.close()

    if result and result[0] == hashlib.md5(f"{password}{salt}".encode('utf-8')).digest():
        print("Login success.")
        return True

    else:
        print("Invalid username or password")
        return False


def saveGame(username, gameName, board, turn, numMoves):

    connection = sqlite3.connect(os.path.join(path,'userDB.db'))
    cursor = connection.cursor()

    boardBlob = pickle.dumps(board)

    try:
        cursor.execute(
            "INSERT INTO gameData (gameName, board, turn, numMoves) VALUES (?, ?, ?, ?)", (gameName, boardBlob, turn, numMoves))

    except sqlite3.IntegrityError:
        print("Game name already exists")

    cursor.execute(
        "INSERT INTO userData (username, gameName) VALUES (?, ?)",(username, gameName))

    connection.commit()
    connection.close()

def getAvailableSaves(username):

    connection = sqlite3.connect(os.path.join(path,'userDB.db'))
    cursor = connection.cursor()

    cursor.execute("SELECT gameName from userData WHERE username = ?", (username,))

    data = cursor.fetchall()
    
    if not data:

        print("No games found")
        connection.close()
        return None

    else:

        gameNames = [Tuple[0] for Tuple in data]
        connection.close()
        return gameNames 

def getDataFromSave(gameName):

    connection = sqlite3.connect(os.path.join(path,'userDB.db'))
    cursor = connection.cursor()

    cursor.execute("SELECT board, turn, numMoves FROM gameData WHERE gameName = ?", (gameName,))

    data = cursor.fetchone()

    if not data:
        print("No game found by that name.")
        return None

    else:
        board = pickle.loads(data[0])
        turn = data[1]
        numMoves = data[2]
        return board, turn, numMoves

