#Libraries
import tkinter 
import tkinter.font 
import asyncio
from websockets.asyncio.client import connect
import pickle
from GUI import *

async def client(request):

    username = globalUsername
    password = globalPassword

    async with connect("ws://192.168.1.122:8765") as websocket:
        loginData = pickle.dumps((username, password))
        await websocket.send(loginData)

        response = await websocket.recv()
        if response == "Invalid username or password":
            return response

        await websocket.send(pickle.dumps(request))
        reply = await websocket.recv()
        return reply

def saveGame(username, password, loginWindow):
    loginWindow.destroy()

def getSave(username, password, loginWindow):
    loginWindow.destroy()

def beginNewGame(type, menuWindow):
    
    if type == "multiplayer":
        menuWindow.destroy()
        result = beginOfflineMultiplayer(None,None,None)

    elif type == "singleplayer":
        menuWindow.destroy()
        result = beginOfflineBot(None,None,None)

    elif type == "tutorial":
        menuWindow.destroy()
        result = beginTutorial(None,None,None)

    else:
        menuWindow.destroy()
        message = ""
        while True:
            showLogin(message)
            message = asyncio.run(client(globalGameName))
            message = pickle.loads(message)
            if message != "No game found by that name." and message != "Invalid username or password":
                break
        
        result = beginOfflineMultiplayer(pickle.loads(message[0]), message[1], int(message[2]))

    if result == "Exit to menu":
        showMenu()

    else:
        board, turn, numMoves = result
        message = ""
        while True:
            showLogin(message)
            message = asyncio.run(client((globalGameName, board, turn, numMoves)))
            if message != "Save unsuccessful, game name already exists" and message != "Invalid username or password":
                break
        showMenu()

def showMenu():
    menuWindow = tkinter.Tk()
    menuWindow.geometry("800x600")
    menuWindow.title("Build Your Chess - Menu")

    titleFont = tkinter.font.Font(family="Arial", size=60)
    subtitleFont = tkinter.font.Font(family="Arial", size=30)
    buttonFont = tkinter.font.Font(family="Arial", size = 20)

    title = tkinter.Label(menuWindow, text="Build Your Chess", font= titleFont)
    title.pack()

    subtitle = tkinter.Label(menuWindow, text="Welcome beginners!", font= subtitleFont)
    subtitle.pack()

    multiplayerButton = tkinter.Button(menuWindow, text="Start multiplayer mode", font = buttonFont, command= lambda: beginNewGame("multiplayer", menuWindow))
    multiplayerButton.pack()

    singleplayerButton = tkinter.Button(menuWindow, text="Start singleplayer mode", font = buttonFont, command= lambda: beginNewGame("singleplayer", menuWindow))
    singleplayerButton.pack()

    tutorialButton = tkinter.Button(menuWindow, text="Start tutorial mode", font = buttonFont, command= lambda: beginNewGame("tutorial", menuWindow))
    tutorialButton.pack()

    fromsaveButton = tkinter.Button(menuWindow, text="Start from a save", font = buttonFont, command= lambda: beginNewGame("fromSave", menuWindow))
    fromsaveButton.pack()

    quitButton = tkinter.Button(menuWindow, text="Exit", font = buttonFont, command= lambda: menuWindow.destroy())
    quitButton.pack()

    menuWindow.mainloop()

def showLogin(message):
    loginWindow = tkinter.Tk()
    loginWindow.geometry("600x450")
    loginWindow.title("Build Your Chess - Login")

    buttonFont = tkinter.font.Font(family="Arial", size = 15)
    entryFont = tkinter.font.Font(family="Arial", size = 15)
    subtitleFont = tkinter.font.Font(family="Arial", size=30)
    messageFont = tkinter.font.Font(family="Arial", size=15)

    username = tkinter.StringVar()
    password = tkinter.StringVar()
    gameName = tkinter.StringVar()

    usernameTitle = tkinter.Label(loginWindow, text="Username:", font= subtitleFont)
    usernameTitle.pack()

    usernameEntry = tkinter.Entry(loginWindow, font = entryFont, textvariable= username)
    usernameEntry.pack()

    passwordTitle = tkinter.Label(loginWindow, text="Password:", font= subtitleFont)
    passwordTitle.pack()

    passwordEntry = tkinter.Entry(loginWindow, font= entryFont, textvariable= password)
    passwordEntry.pack()

    gameNameTitle = tkinter.Label(loginWindow, text="Game name:", font= subtitleFont)
    gameNameTitle.pack()

    gameNameEntry = tkinter.Entry(loginWindow, font= entryFont, textvariable= gameName)
    gameNameEntry.pack()

    def getValues():
        global globalUsername, globalPassword, globalGameName

        globalUsername = usernameEntry.get()
        globalPassword = passwordEntry.get()
        globalGameName = gameNameEntry.get()    

        loginWindow.destroy()

    loginButton = tkinter.Button(loginWindow, text="Login/Sign up", font = buttonFont, command= lambda: getValues())
    loginButton.pack()  

    message = tkinter.Label(loginWindow, text=message, font= messageFont, fg= "red")
    message.pack()

    loginWindow.mainloop()

showMenu()




