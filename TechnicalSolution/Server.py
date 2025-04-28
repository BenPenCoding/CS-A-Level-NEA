import sqlite3
import os
import hashlib
import pickle
import asyncio
import websockets
from websockets.asyncio.server import serve
import asyncio

#Database

#Relative path
path = os.path.dirname(__file__)

#Salt for the salting function
salt = "ParanoidNokiaPigstepStrangers"

#Subroutine to create the tables required
def createTables():

    #Create connection to the database
    connection = sqlite3.connect(os.path.join(path,'userDB.db'))
    cursor = connection.cursor()

    #Creates the users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL)''')

    #Creates the userData table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS userData (
            username TEXT NOT NULL,
            gameName TEXT NOT NULL,
            FOREIGN KEY(username) REFERENCES users(username),
            FOREIGN KEY(gameName) REFERENCES gameData(gameName),
            PRIMARY KEY(username, gameName))''')

    #Creates the gameData table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gameData (
            gameName TEXT PRIMARY KEY,
            board BLOB NOT NULL,
            turn TEXT,
            numMoves TEXT)''')

    #End the connection
    connection.commit()
    connection.close()

#Subroutine to truncate (empty) a given table
def emptyTable(tableName):

    #Create connection to the database
    connection = sqlite3.connect(os.path.join(path,'userDB.db'))
    cursor = connection.cursor()

    #Try to execute the SQL command
    try:
        cursor.execute(f"DELETE FROM {tableName}")
    
    except:
        print("Invalid table name")

    finally:

        #End the connection and commit the changes
        connection.commit()
        connection.close()

#Function to check if a given username exists
def doesUserExist(username):

    #Create connection to the database
    connection = sqlite3.connect(os.path.join(path,'userDB.db'))
    cursor = connection.cursor()

    #Execute the SQL command
    cursor.execute("SELECT username FROM users WHERE username = ?", (username,))

    #Fetches result from the executed command
    result = cursor.fetchone()

    #If result is not empty (username exists) return True
    if result:
        return True

    #If result is empty (username does not exist) return False
    else:
        return False

#Function that adds a username and hashed password to the users table 
def addUser(username, password):
    
    #Create connection to the database
    connection = sqlite3.connect(os.path.join(path,'userDB.db'))
    cursor = connection.cursor()

    #Encodes the password with the MD5 hash function
    password = hashlib.md5(f"{password}{salt}".encode('utf-8'))
    
    #Try to execute the SQL command
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password.digest()))
        connection.commit()

        #Return specific save success message
        return "User added successfully!"

    #If an error occurs where the SQL command tries to impose a new row with the same username as another
    except sqlite3.IntegrityError:

        #Return specific error message
        return "Username is taken."

    finally:

        #End the connection
        connection.close()

#Authentication function that checks if the given username matches up with the given password in the database
def loginUser(username, password):

    #Create connection to the database
    connection = sqlite3.connect(os.path.join(path,'userDB.db'))
    cursor = connection.cursor()

    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))

    #Fetches result from the executed command
    result = cursor.fetchone()

    #End the connection
    connection.close()

    if result and result[0] == hashlib.md5(f"{password}{salt}".encode('utf-8')).digest():
        #Return specific successful authentication message
        msg = "Login success."
        return True, msg

    else:
        #Return specific error message
        msg = "Invalid username or password"
        return False, msg

#Function that saves given data to the userData and gameData tables
def saveGame(username, gameName, board, turn, numMoves):

    #Create connection to the database
    connection = sqlite3.connect(os.path.join(path,'userDB.db'))
    cursor = connection.cursor()

    #A blob is a data type that can store binary data, hence its use here
    boardBlob = pickle.dumps(board)

    #Try to execute the SQL command
    try:
        
        cursor.execute("INSERT INTO gameData (gameName, board, turn, numMoves) VALUES (?, ?, ?, ?)", 
            (gameName, boardBlob, turn, numMoves))
        
        cursor.execute("INSERT INTO userData (username, gameName) VALUES (?, ?)",(username, gameName))

        #End the connection and commit the changes
        connection.commit()
        connection.close()
        return True, "Save successful"

    #If an error occurs where the SQL command tries to impose a new row with the same gameName as another
    except sqlite3.IntegrityError:

        #End the connection and commit the changes
        connection.commit()
        connection.close()
        return False, "Save unsuccessful, game name already exists"

#Function that returns the name of saved games a user has created 
def getAvailableSaves(username):

    #Create connection to the database
    connection = sqlite3.connect(os.path.join(path,'userDB.db'))
    cursor = connection.cursor()

    #Executes the SQL command
    cursor.execute("SELECT gameName from userData WHERE username = ?", (username,))

    #Fetches result from the executed command
    data = cursor.fetchall()
    
    #If there is not any data
    if not data:

        #End the connection
        connection.close()
        return None

    #If there is any data
    else:

        gameNames = [Tuple[0] for Tuple in data]

        #End the connection
        connection.close()
        return gameNames 

#A function that retrieves data from a given save name
def getDataFromSave(gameName):

    #Create connection to the database
    connection = sqlite3.connect(os.path.join(path,'userDB.db'))
    cursor = connection.cursor()

    #Executes the SQL command
    cursor.execute("SELECT board, turn, numMoves FROM gameData WHERE gameName = ?", (gameName,))

    #Fetches result from the executed command
    data = cursor.fetchone()

    #If there is not any data
    if not data:
        return "No game found by that name."

    #If there is any data
    else:
        board = data[0]
        turn = data[1]
        numMoves = data[2]
        return (board, turn, numMoves)  #Return the retrieved data

#Server

#Dict of connected clients
connectedClients = {}

#Asynchronous function that handles server to client communication
async def handler(websocket):
    try:
        # First message from the client (main.py) is a tuple like this: ("username", "password")
        firstMessage = await websocket.recv()

        #Try to evaluate the message into a username and password value
        try:
            firstMessageTuple = pickle.loads(firstMessage)  
            username, password = firstMessageTuple
 
        #If the message evaluation fails due to invalid format inform the client
        except Exception:
            await websocket.send("Invalid format. Expecting a tuple like this: (username,password)")
            return

        #If given username exists, attempt to authenticate them
        if doesUserExist(username):
            loginAttempt = loginUser(username, password)

            if not loginAttempt[0]:
                await websocket.send(loginAttempt[1])
                return
        
        #If username does not exist, treat this as a sign up attempt
        else:
            addUser(username, password)

        #Add the connected client to the dict of currently connected clients
        connectedClients[username] = websocket
        await websocket.send(f"Welcome, {username}!")

        #Informs me that a user is connected
        print(f"{username} connected.")

        #Expecting message to be a tuple of (gameName, board, turn, numMoves), or just a gameName string
        async for message in websocket: 
            
            #This error handling determines the request type between requesting a save and saving data
            #If the recieved data is game data save it to the database
            try:  
                gameName, board, turn, numMoves = pickle.loads(message)
                msg = saveGame(username, gameName, board, turn, numMoves)[1]
                await websocket.send(msg)
            
            #If the recieved data is a request for game data send it to the user
            except:

                #Evaluates the message from binary to a string
                gameName = pickle.loads(message)

                #Retrieves game data
                data = getDataFromSave(gameName)

                #If the requested game data does not exist return an error message to the client
                if data == "No game found by that name.":
                    await websocket.send(pickle.dumps("No game found by that name."))

                #If the requested game data does exist, send it to the client
                else:
                    data = pickle.dumps(data)
                    await websocket.send(data)

    #This informs me if a user disconnects
    except websockets.ConnectionClosed:
        print(f"{username} disconnected.")

    #Remove the user from the dict of connected clients
    finally:
        if 'username' in locals():
            connectedClients.pop(username, None)        

#Subroutine that activates the server and displays a message to tell me it has been activated
async def runServer():
    print("Server running...")
    async with serve(handler, "192.168.1.122", 8765) as server:
        await server.serve_forever()

#Activates the server listening on port 8765 until the program is stopped
asyncio.run(runServer())