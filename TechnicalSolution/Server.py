import sqlite3
import os
import hashlib
import pickle
import websockets
import asyncio

#Database
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

def doesUserExist(username):

    connection = sqlite3.connect(os.path.join(path,'userDB.db'))
    cursor = connection.cursor()

    cursor.execute("SELECT username FROM users WHERE username = ?", (username,))

    result = cursor.fetchone()

    if result:
        return True
    else:
        return False

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
        msg = "Login success."
        return True, msg

    else:
        msg = "Invalid username or password"
        return False, msg


def saveGame(username, gameName, board, turn, numMoves):

    connection = sqlite3.connect(os.path.join(path,'userDB.db'))
    cursor = connection.cursor()

    boardBlob = pickle.dumps(board)

    try:
        cursor.execute("INSERT INTO gameData (gameName, board, turn, numMoves) VALUES (?, ?, ?, ?)", (gameName, boardBlob, turn, numMoves))
        cursor.execute("INSERT INTO userData (username, gameName) VALUES (?, ?)",(username, gameName))
        connection.commit()
        connection.close()
        return True, "Save successful"
    except sqlite3.IntegrityError:
        print("Game name already exists")
        connection.commit()
        connection.close()
        return False, "Save unsuccessful, game name already exists"

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
        return "No game found by that name."

    else:
        board = data[0]
        turn = data[1]
        numMoves = data[2]
        return (board, turn, numMoves)

#Server
connectedClients = {}

async def handler(websocket, path):
    try:
        # First message from the client (main.py) is a tuple like this: ("username", "password")
        firstMessage = await websocket.recv()

        try:
            username, password = eval(firstMessage)  

        except Exception:
            await websocket.send("Invalid format. Expecting a tuple like this: (username,password)")
            return

        if doesUserExist(username):
            loginAttempt = loginUser(username, password)

            if not loginAttempt[0]:
                await websocket.send(loginAttempt[1])
                return
        else:
            addUser(username, password)

        connectedClients[username] = websocket
        await websocket.send(f"Welcome, {username}!")
        print(f"{username} connected.")

        #Expecting message to be a tuple of (gameName, board, turn, numMoves), or just a gameName string
        async for message in websocket: 
            try:            
                gameName, board, turn, numMoves = eval(message)
                msg = saveGame(username, gameName, board, turn, numMoves)[1]
                await websocket.send(msg)
            
            except ValueError:
                gameName = eval(message)
                data = getDataFromSave(gameName)

                if data == "No game found by that name.":
                    await websocket.send("No game found by that name.")

                else:
                    data = pickle.dumps(data)
                    await websocket.send(data)

    except websockets.ConnectionClosed:
        print(f"{username} disconnected.")

    finally:
        connectedClients.pop(username)

startServer = websockets.serve(handler, "0.0.0.0", 8765)
print("Server running...")
asyncio.get_event_loop().run_until_complete(startServer)
asyncio.get_event_loop().run_forever()
