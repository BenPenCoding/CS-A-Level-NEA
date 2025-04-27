#Libraries
import tkinter 
import tkinter.font 
import asyncio
from websockets.asyncio.client import connect
import pickle
from GUI import *

#Functions

#The client function that handles communication with the server
async def client(request):

    username = globalUsername
    password = globalPassword

    #Connects to the server
    async with connect("ws://192.168.1.122:8765") as websocket:
        loginData = pickle.dumps((username, password))
        await websocket.send(loginData)

        #Retrieves response
        response = await websocket.recv()
        if response == "Invalid username or password":
            return response

        #Send data save/data retrieve request
        await websocket.send(pickle.dumps(request))
        reply = await websocket.recv()
        return reply

#Subroutine that starts a new game, whether that be tutorial mode, singleplayer, etc
def beginNewGame(type, menuWindow):
    
    #If game request is multiplayer mode start the game with specified mode
    if type == "multiplayer":
        menuWindow.destroy()
        result = beginOfflineMultiplayer(None,None,None)

    #If game request is multiplayer mode start the game with specified mode
    elif type == "singleplayer":
        menuWindow.destroy()
        result = beginOfflineBot(None,None,None)

    #If game request is multiplayer mode start the game with specified mode
    elif type == "tutorial":
        menuWindow.destroy()
        result = beginTutorial(None,None,None)

    #If game request is to start from a previous save, do so
    else:
        menuWindow.destroy()
        
        message = ""

        #Initiates a loop to authenticate the user, the loop is broken when the user is authenticated
        while True:

            #Display the login screen
            showLogin(message)

            #Recieves the requested data from the server
            message = asyncio.run(client(globalGameName))
            message = pickle.loads(message)

            #If the retrieved message is not an error message, break the loop
            if message != "No game found by that name." and message != "Invalid username or password":
                break
        
        #Starts a multiplayer mode game with the retrieved save
        result = beginOfflineMultiplayer(pickle.loads(message[0]), message[1], int(message[2]))

    #If user request is to exit to menu, do so
    if result == "Exit to menu":
        showMenu()

    #If user request is to save their current game, do so
    else:
        board, turn, numMoves = result
        message = ""

        #Initiates a loop to authenticate the user, the loop is broken when the user is authenticated
        while True:

            #Displays the login screen
            showLogin(message)

            #Retrieve the message from the server
            message = asyncio.run(client((globalGameName, board, turn, numMoves)))

            #If the message is not an error message, break the loop
            if message != "Save unsuccessful, game name already exists" and message != "Invalid username or password":
                break
    
    #Display the menu screen
    showMenu()

#Subroutine that displays the menu screen
def showMenu():

    #Defines the window
    menuWindow = tkinter.Tk()
    menuWindow.geometry("800x600")
    menuWindow.title("Build Your Chess - Menu")

    #Define used fonts
    titleFont = tkinter.font.Font(family="Arial", size=60)
    subtitleFont = tkinter.font.Font(family="Arial", size=30)
    buttonFont = tkinter.font.Font(family="Arial", size = 20)

    #Defines and displays the title
    title = tkinter.Label(menuWindow, text="Build Your Chess", font= titleFont)
    title.pack()

    #Defines and displays the subtitle
    subtitle = tkinter.Label(menuWindow, text="Welcome beginners!", font= subtitleFont)
    subtitle.pack()

    #Defines and displays the start multiplayer game button
    multiplayerButton = tkinter.Button(menuWindow, text="Start multiplayer mode", font = buttonFont,
        command= lambda: beginNewGame("multiplayer", menuWindow))
    multiplayerButton.pack()

    #Defines and displays the start singleplayer game button
    singleplayerButton = tkinter.Button(menuWindow, text="Start singleplayer mode", font = buttonFont, 
        command= lambda: beginNewGame("singleplayer", menuWindow))
    singleplayerButton.pack()

    #Defines and displays the start tutorial game button
    tutorialButton = tkinter.Button(menuWindow, text="Start tutorial mode", font = buttonFont,
        command= lambda: beginNewGame("tutorial", menuWindow))
    tutorialButton.pack()

    #Defines and displays the start game from save button
    fromsaveButton = tkinter.Button(menuWindow, text="Start from a save", font = buttonFont, 
        command= lambda: beginNewGame("fromSave", menuWindow))
    fromsaveButton.pack()

    #Defines and displays the quit button
    quitButton = tkinter.Button(menuWindow, text="Exit", font = buttonFont, 
        command= lambda: menuWindow.destroy())
    quitButton.pack()

    #Begins Tkinter's mainloop
    menuWindow.mainloop()

#Subroutine that displays the login screen
def showLogin(message):

    #Defines the window
    loginWindow = tkinter.Tk()
    loginWindow.geometry("600x450")
    loginWindow.title("Build Your Chess - Login")

    #Defines used fonts
    buttonFont = tkinter.font.Font(family="Arial", size = 15)
    entryFont = tkinter.font.Font(family="Arial", size = 15)
    subtitleFont = tkinter.font.Font(family="Arial", size=30)
    messageFont = tkinter.font.Font(family="Arial", size=15)

    #Defines the entry box data
    username = tkinter.StringVar()
    password = tkinter.StringVar()
    gameName = tkinter.StringVar()

    #Defines and displays the username title
    usernameTitle = tkinter.Label(loginWindow, text="Username:", font= subtitleFont)
    usernameTitle.pack()

    #Defines and displays the username entry
    usernameEntry = tkinter.Entry(loginWindow, font = entryFont, textvariable= username)
    usernameEntry.pack()

    #Defines and displays the password title
    passwordTitle = tkinter.Label(loginWindow, text="Password:", font= subtitleFont)
    passwordTitle.pack()

    #Defines and displays the password entry
    passwordEntry = tkinter.Entry(loginWindow, font= entryFont, textvariable= password)
    passwordEntry.pack()

    #Defines and displays the game name title
    gameNameTitle = tkinter.Label(loginWindow, text="Game name:", font= subtitleFont)
    gameNameTitle.pack()

    #Defines and displays the game name entry
    gameNameEntry = tkinter.Entry(loginWindow, font= entryFont, textvariable= gameName)
    gameNameEntry.pack()

    #Subroutine that converts the entry variables to global variables so they 
    #can be used to authenticate the user
    def getValues():
        global globalUsername, globalPassword, globalGameName

        globalUsername = usernameEntry.get()
        globalPassword = passwordEntry.get()
        globalGameName = gameNameEntry.get()    

        #Destroys the login window
        loginWindow.destroy()

    #Defines and displays the button that calls the getValues subroutine
    loginButton = tkinter.Button(loginWindow, text="Login/Sign up", font = buttonFont, command= lambda: getValues())
    loginButton.pack()  

    #Defines and displays the message (error message from server)
    message = tkinter.Label(loginWindow, text=message, font= messageFont, fg= "red")
    message.pack()

    #Begins Tkinter's mainloop
    loginWindow.mainloop()

#Entry point for the file
if __name__ == "__main__":
    showMenu()




