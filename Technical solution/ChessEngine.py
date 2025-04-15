#Libraries

#Classes
class Game():	#A class that represents a chess game with attributes that will be saved if the user decided to continue a game at a later time, and also contains data about the board itself
	def __init__(self,name):	#Constructor for the Game class. Declares the:
		self.board = []		#array that will contain Piece objects 
		self.blackPieces = []
		self.whitePieces = []
		
	def getPieceAtLocation(self, file, column):	#A function that returns the Piece object at a given file and column of the board
		return self.board[file][column]
		
	def getPieces(self, colour):
		if colour == "Black":
			return self.blackPieces 
		else: return self.whitePieces
	
class Piece():		#A class that represents a chess piece with attributes such as piece type and piece location on the board
	def __init__(self, pieceType, pieceColour, file, column):	#Constructor for the Piece class. Declares the:  
		self.pieceType = pieceType              #type of piece (pawn, rook, etc)
		self.pieceColour = pieceColour
		self.timesMoved = 0
		self.file = file                        #file (row) in the board
		self.column = column                 	#column in the board

	#Functions
	def getPossibleMoveLocations(self):	#An empty function that will be overridden in the piece subclasses, returns all locations that a piece can move to
		None
	
	#Setters
	def setFile(self, file):	#'Setter' for the file attribute, called when a piece is instantiated or moved
		self.file = file

	def setColumn(self, column):	#'Setter' for the column attribute, called when a piece is instantiated or moved
		self.column = column

	def setBoardCoords(self, file, column):	     #Subroutine that abstracts the individual 'setter' subroutines for board position from the user for simplicity
		self.setFile(file)
		self.setColumn(column)
		
	def setPieceType(self, pieceType):	#'Setter' for the pieceType attribute, called when a piece is instantiated or a pawn reaches the other side of the board and can change into another piece
		self.pieceType = pieceType

	def setPieceColour(Self, pieceColour):	#'Setter' for the pieceColour attribute, called when a piece is instantiated 
		self.pieceColour = pieceColour

	def increaseTimesMoved(self):
		self.timesMoved += 1
	
	#Getters
	def getFile(self):	#'Getter' for the file attribute, returns said attribute when called
		return self.file
	
	def getColumn(self):	#'Getter' for the column attribute, returns said attribute when called
		return self.column

	def getBoardCoords(self):	#Subroutine that abstracts the individual 'getter' subroutines for board position from the user for simplicity
		return getFile, getColumn

	def getPieceType(self): 	#'Getter' for the pieceType attribute, returns said attribute when called
		return self.pieceType

	def getPieceColour(self):	#'Getter' for the pieceColour attribute, returns said attribute when called
		return self.pieceType

	def getTimesMoved(self):
		return self.timesMoved
	
	#Checkers
	def isPieceEmpty(self):		#'Checker' which returns the bool True if the value of the attribute pieceType is "Empty", meaning that the location that piece takes up is free for another piece to move to
		if self.pieceType == "Empty":
			return True

	def isPieceInCheck(self):	#An empty function that will be overridden in the King subclass
		None
		
class Rook(Piece): 			#A class that represents the rook chess piece, which inherits from the Piece class
	def __init__(self):		#The constructor for the Rook class
		Super().__init__()	#Calls the super constructor from the parent class (Piece class)
	
	def getPossibleMoveLocations(self):		#A function that returns all locations that a piece can move to
		possibleMoveLocations = []		#Declaring the array to add possible move locations to
		pieceFile, pieceColumn = self.getBoardCoords()	#Gets the file and column of the piece to move by using the getBoardCoords function 
		
		fileIncrement, columnIncrement = 0, 0  	#Declares two variables which will be used to change the direction of the board search by switching between -1 and 1 to reverse direction.
		
		for i in range(4):		#The four cardinal directions

			tempFile, tempColumn = pieceFile, pieceColumn	#Initializes two variables that are set to the location of the piece to move
			
			while True:		#A while loop so that all possible move locations in a row are found 
				match i:	#Python's equivalent of a switch/case statement
					case 0:		#If the increment variable has a value of 0, test all possible move locations to the right of the piece
						fileIncrement, columnIncrement = 1, 0
					case 1:		#If the increment variable has a value of 1, test all possible move locations above the piece
						fileIncrement, columnIncrement = 0, -1
					case 2:		#If the increment variable has a value of 2, test all possible move locations to the left of the piece
						fileIncrement, columnIncrement = -1, 0
					case 3:		#If the increment variable has a value of 3, test all possible move locations below the piece
						fileIncrement, columnIncrement = 0, 1
					case _:		#DEBUG - If the increment variable has a value not inside 0 <= i <= 3 then print the nature of the error
						print("Fatal error, Rook class switch/case statement experienced a larger increment value than expected.")
						sleep(5)	#DEBUG - Pauses the program for five seconds to allow the tester to interpret the error message 
						quit()		#DEBUG - Quits the program entirely

				if (tempFile > 7 or tempFile < 0) or (tempColumn > 7 or tempColumn < 0):	#Checks if the file and column of the next piece to check are actually not on the board and therefore if a "IndexError: list index out of range" error will occur                  
					break									#If this is the case, exit the while loop and begin checking in another direction						

				tempFile += fileIncrement		#Increments the file of the next piece to search by the designated direction-dependent increment
				tempColumn += columnIncrement		#Increments the column of the next piece to search by the designated direction-dependent increment
				
				pieceToCheck = game.getPieceAtLocation(tempFile, tempColumn)	#Gets the piece object to check 

				if self.isPieceEmpty(pieceToCheck) == "Empty":			#Checks if the piece object is empty
					possibleMoveLocations.append([tempFile, tempColumn]) 	#If it is, add the location to the list of possible move locations
					continue						#Moves on to checking the next piece
					
				elif (pieceToCheck.getPieceColour() != self.getPieceColour()) and pieceToCheck.getPieceType != "King":	#If the location contains an oppositely coloured piece which can be taken (all except the king)
					possibleMoveLocations.append([tempFile, tempColumn])	#Adds the location to the list of possible move locations
					break							#Stops checking the next piece and exits the while loop
				
				else:		#Otherwise the piece to check is the same colour as the piece to move, or it's the opposition's king piece (which can't be taken)
					break	#Stops checking the next piece and exits the while loop

		return possibleMoveLocations	#Returns the list of possible move locations to wherever the function was called 


class Bishop(Piece):			#A class that represents the bishop chess piece, which inherits from the Piece class
	def __init__(self):		#The constructor for the Bishop class
		Super().__init__()	#Calls the super constructor from the parent class (Piece class)

	def getPossibleMoveLocations(self):
		possibleMoveLocations = []		#Declaring the array to add possible move locations to
		pieceFile, pieceColumn = self.getBoardCoords()	#Gets the file and column of the piece to move by using the getBoardCoords function 

		fileIncrement, columnIncrement = 0, 0  	#Declares two variables which will be used to change the direction of the board search by switching between -1 and 1 to change direction.
		
		for i in range(4):		#The four diagonal directions

			tempFile, tempColumn = pieceFile, pieceColumn	#Initializes two variables that are set to the location of the piece to move
			
			while True:		#A while loop so that all possible move locations in a diagonal line are found 
				match i:	#Python's equivalent of a switch/case statement
					case 0:		#If the increment variable has a value of 0, test all possible move locations to the up and right of the piece
						fileIncrement, columnIncrement = -1, 1
					case 1:		#If the increment variable has a value of 1, test all possible move locations up and left of the piece
						fileIncrement, columnIncrement = -1, -1
					case 2:		#If the increment variable has a value of 2, test all possible move locations to the down and left of the piece
						fileIncrement, columnIncrement = 1, -1
					case 3:		#If the increment variable has a value of 3, test all possible move locations down and right of the piece
						fileIncrement, columnIncrement = 1, 1
					case _:		#DEBUG - If the increment variable has a value not inside 0 <= i <= 3 then print the nature of the error
						print("Fatal error, Bishop class switch/case statement experienced a larger increment value than expected.")
						sleep(5)	#DEBUG - Pauses the program for five seconds to allow the tester to interpret the error message 
						quit()		#DEBUG - Quits the program entirely

				if (tempFile > 7 or tempFile < 0) or (tempColumn > 7 or tempColumn < 0):	#Checks if the file and column of the next piece to check are actually not on the board and therefore if a "IndexError: list index out of range" error will occur                  
					break									#If this is the case, exit the while loop and begin checking in another direction							

				tempFile += fileIncrement		#Increments the file of the next piece to search by the designated direction-dependent increment
				tempColumn += columnIncrement		#Increments the column of the next piece to search by the designated direction-dependent increment
				
				
				pieceToCheck = game.getPieceAtLocation(tempFile, tempColumn)	#Gets the piece object to check 
				
				if self.isPieceEmpty(pieceToCheck) == "Empty":			#Checks if the piece object is empty
					possibleMoveLocations.append([tempFile, tempColumn]) 	#If it is, add the location to the list of possible move locations
					continue
					
				elif (pieceToCheck.getPieceColour() != self.getPieceColour()) and pieceToCheck.getPieceType != "King":	#If the location contains an oppositely coloured piece which can be taken (all except the king)
					possibleMoveLocations.append([tempFile, tempColumn])		#Adds the location to the list of possible move locations
					break
				
				else:		#Otherwise the piece to check is the same colour as the piece to move, or it's the opposition's king piece (which can't be taken)
					break	#Exits the while loop
		
		return possibleMoveLocations	#Returns the list of possible move locations to wherever the function was called 

class Knight(Piece):			#A class that represents the knight chess piece, which inherits from the Piece class
	def __init__(self):		#The constructor for the Knight class
		Super().__init__()	#Calls the super constructor from the parent class (Piece class)

	def getPossibleMoveLocations(self):
		possibleMoveLocations = []		#Declaring the array to add possible move locations to
		pieceFile, pieceColumn = self.getBoardCoords()	#Gets the file and column of the piece to move by using the getBoardCoords function 
		possibleIncrementList = [[-2, 1], [-2, -1], [-1, 2], [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2]]	#Although not obvious, this list contains the increments that must be added to a knight's current location to check the squares it could possibly move to
		
		for coordinates in possibleIncrementList:

			tempFile, tempColumn = pieceFile +coordinates[0], pieceColumn + coordinates[1]	#Declaring and initializing two variables that store the location of the piece to check, they're instantiated as the current increment values added to the knight's position 

			if (tempFile < 0 or tempFile > 7) or (tempColumn < 0 or tempColumn > 7): 	#Checks if the file and column of the next piece to check are actually not on the board and therefore if a "IndexError: list index out of range" error will occur
				continue
				
			pieceToCheck = 	game.getPieceAtLocation(tempFile, tempColumn)

			if self.isPieceEmpty(pieceToCheck) == "Empty":			#Checks if the piece object is empty
				possibleMoveLocations.append([tempFile, tempColumn]) 	#If it is, add the location to the list of possible move locations
				continue		#Skips the rest of the for loop as we have found the state of the piece and returns to the top of the loop
					
			elif (pieceToCheck.getPieceColour() != self.getPieceColour()) and pieceToCheck.getPieceType != "King":	#If the location contains an oppositely coloured piece which can be taken (all except the king)
				possibleMoveLocations.append([tempFile, tempColumn])		#Adds the location to the list of possible move locations
				continue		#Skips the rest of the for loop as we have found the state of the piece and returns to the top of the loop
				
			else:		#Otherwise the piece to check is the same colour as the piece to move, or it's the opposition's king piece (which can't be taken)
				pass	#Nothing happens here, the program returns to the for loop		
		
		return possibleMoveLocations	#Returns the list of possible move locations to wherever the function was called 
		


class Queen(Piece):			#A class that represents the queen chess piece, which inherits from the Piece class
	def __init__(self):		#The constructor for the Queen class
		Super().__init__()	#Calls the super constructor from the parent class (Piece class)

	def getPossibleMoveLocations(self):
		possibleMoveLocations = []		#Declaring the array to add possible move locations to
		pieceFile, pieceColumn = self.getBoardCoords()	#Gets the file and column of the piece to move by using the getBoardCoords function 
		fileIncrement, columnIncrement = 0, 0  	#Declares two variables which will be used to change the direction of the board search by switching between -1 and 1 to reverse direction.

		#The queen piece can move like a rook and a bishop at the same time, to check for possible move locations I used the same code from both the Bishop class and the Rook class
		#The code from the Rook class:
		for i in range(4):		#The four cardinal directions

			tempFile, tempColumn = pieceFile, pieceColumn	#Initializes two variables that are set to the location of the piece to move
			
			while True:		#A while loop so that all possible move locations in a row are found 
				match i:	#Python's equivalent of a switch/case statement
					case 0:		#If the increment variable has a value of 0, test all possible move locations to the right of the piece
						fileIncrement, columnIncrement = 1, 0
					case 1:		#If the increment variable has a value of 1, test all possible move locations above the piece
						fileIncrement, columnIncrement = 0, -1
					case 2:		#If the increment variable has a value of 2, test all possible move locations to the left of the piece
						fileIncrement, columnIncrement = -1, 0
					case 3:		#If the increment variable has a value of 3, test all possible move locations below the piece
						fileIncrement, columnIncrement = 0, 1
					case _:		#DEBUG - If the increment variable has a value not inside 0 <= i <= 3 then print the nature of the error
						print("Fatal error, Rook class switch/case statement experienced a larger increment value than expected.")
						sleep(5)	#DEBUG - Pauses the program for five seconds to allow the tester to interpret the error message 
						quit()		#DEBUG - Quits the program entirely

				if (tempFile > 7 or tempFile < 0) or (tempColumn > 7 or tempColumn < 0):	#Checks if the file and column of the next piece to check are actually not on the board and therefore if a "IndexError: list index out of range" error will occur                  
					break									#If this is the case, exit the while loop and begin checking in another direction						

				tempFile += fileIncrement		#Increments the file of the next piece to search by the designated direction-dependent increment
				tempColumn += columnIncrement		#Increments the column of the next piece to search by the designated direction-dependent increment
				
				pieceToCheck = game.getPieceAtLocation(tempFile, tempColumn)	#Gets the piece object to check 

				if self.isPieceEmpty(pieceToCheck) == "Empty":			#Checks if the piece object is empty
					possibleMoveLocations.append([tempFile, tempColumn]) 	#If it is, add the location to the list of possible move locations
					continue						#Moves on to checking the next piece
					
				elif (pieceToCheck.getPieceColour() != self.getPieceColour()) and pieceToCheck.getPieceType != "King":	#If the location contains an oppositely coloured piece which can be taken (all except the king)
					possibleMoveLocations.append([tempFile, tempColumn])	#Adds the location to the list of possible move locations
					break							#Stops checking the next piece and exits the while loop
				
				else:		#Otherwise the piece to check is the same colour as the piece to move, or it's the opposition's king piece (which can't be taken)
					break	#Stops checking the next piece and exits the while loop

		#The code from the Bishop class:
		for i in range(4):		#The four diagonal directions

			tempFile, tempColumn = pieceFile, pieceColumn	#Initializes two variables that are set to the location of the piece to move
			
			while True:		#A while loop so that all possible move locations in a diagonal line are found 
				match i:	#Python's equivalent of a switch/case statement
					case 0:		#If the increment variable has a value of 0, test all possible move locations to the up and right of the piece
						fileIncrement, columnIncrement = -1, 1
					case 1:		#If the increment variable has a value of 1, test all possible move locations up and left of the piece
						fileIncrement, columnIncrement = -1, -1
					case 2:		#If the increment variable has a value of 2, test all possible move locations to the down and left of the piece
						fileIncrement, columnIncrement = 1, -1
					case 3:		#If the increment variable has a value of 3, test all possible move locations down and right of the piece
						fileIncrement, columnIncrement = 1, 1
					case _:		#DEBUG - If the increment variable has a value not inside 0 <= i <= 3 then print the nature of the error
						print("Fatal error, Bishop class switch/case statement experienced a larger increment value than expected.")
						sleep(5)	#DEBUG - Pauses the program for five seconds to allow the tester to interpret the error message 
						quit()		#DEBUG - Quits the program entirely

				if (tempFile > 7 or tempFile < 0) or (tempColumn > 7 or tempColumn < 0):	#Checks if the file and column of the next piece to check are actually not on the board and therefore if a "IndexError: list index out of range" error will occur                  
					break									#If this is the case, exit the while loop and begin checking in another direction							

				tempFile += fileIncrement		#Increments the file of the next piece to search by the designated direction-dependent increment
				tempColumn += columnIncrement		#Increments the column of the next piece to search by the designated direction-dependent increment
				
				
				pieceToCheck = game.getPieceAtLocation(tempFile, tempColumn)	#Gets the piece object to check 
				
				if self.isPieceEmpty(pieceToCheck) == "Empty":			#Checks if the piece object is empty
					possibleMoveLocations.append([tempFile, tempColumn]) 	#If it is, add the location to the list of possible move locations
					continue
					
				elif (pieceToCheck.getPieceColour() != self.getPieceColour()) and pieceToCheck.getPieceType != "King":	#If the location contains an oppositely coloured piece which can be taken (all except the king)
					possibleMoveLocations.append([tempFile, tempColumn])		#Adds the location to the list of possible move locations
					break
				
				else:		#Otherwise the piece to check is the same colour as the piece to move, or it's the opposition's king piece (which can't be taken)
					break	#Exits the while loop
		
		return possibleMoveLocations	#Returns the list of possible move locations to wherever the function was called 
	


class Pawn(Piece):			#A class that represents the pawn chess piece, which inherits from the Piece class
	def __init__(self):		#The constructor for the Pawn class
		Super().__init__()	#Calls the super constructor from the parent class (Piece class)

	def getPossibleMoveLocations(self):
		possibleMoveLocations = []		#Declaring the array to add possible move locations to
		pieceFile, pieceColumn = self.getBoardCoords()	#Gets the file and column of the piece to move by using the getBoardCoords function 

		if piece.colour = "white":	#This if statement initializes an inrement variable, i, which will alter the direction of the pawns movement depending on its colour
			i = i
		else:
			i= -1
		
		tempFile, tempColumn = pieceFile + (-1 * i), pieceColumn + 0

		if (game.getPieceAtLocation(tempFile, tempColumn).getPieceType() == "Empty":
			possibleMoveLocations.append([tempFile, tempColumn])

		tempFile, tempColumn = pieceFile + (-1 * i), pieceColumn + 1
		
		if (game.getPieceAtLocation(tempFile, tempColumn).getColour() != self.getColour()) and (game.getPieceAtLocation(tempFile, tempColumn).getPieceType() != "King") and (game.getPieceAtLocation(tempFile, tempColumn).getPieceType() != "Empty"):
			possibleMoveLocations.append([tempFile, tempColumn])
		
		tempFile, tempColumn = pieceFile + (-1 * i), pieceColumn + -1

		if (game.getPieceAtLocation(tempFile, tempColumn).getColour() != self.getColour()) and (game.getPieceAtLocation(tempFile, tempColumn).getPieceType() != "King") and (game.getPieceAtLocation(tempFile, tempColumn).getPieceType() != "Empty"):
			possibleMoveLocations.append([tempFile, tempColumn])
			
		#ADD EN PASSANT CASE


class King(Piece):			#A class that represents the king chess piece, which inherits from the Piece class
	def __init__(self):		#The constructor for the King class
		Super().__init__()	#Calls the super constructor from the parent class (Piece class)

	def getPossibleMoveLocations(self):

		possibleMoveLocations = []		#Declaring the array to add possible move locations to
		pieceFile, pieceColumn = self.getBoardCoords()	#Gets the file and column of the piece to move by using the getBoardCoords function 
		possibleIncrementList = [[-1, -1],[-1, 0],[-1, 1], [0,-1],[0, 1],[1, -1],[1, 0],[1, 1]]	This list contains the increments that must be added to a king's current location to check the squares it could possibly move to
		
		for coordinates in possibleIncrementList:

			tempFile, tempColumn = pieceFile +coordinates[0], pieceColumn + coordinates[1]	#Declaring and initializing two variables that store the location of the piece to check, they're instantiated as the current increment values added to the knight's position 

			if (tempFile < 0 or tempFile > 7) or (tempColumn < 0 or tempColumn > 7):	#Checks if the file and column of the next piece to check are actually not on the board and therefore if a "IndexError: list index out of range" error will occur
				continue
				
			pieceToCheck = 	game.getPieceAtLocation(tempFile, tempColumn)

			if self.isPieceEmpty(pieceToCheck) == "Empty":			#Checks if the piece object is empty
				possibleMoveLocations.append([tempFile, tempColumn]) 	#If it is, add the location to the list of possible move locations
				continue		#Skips the rest of the for loop as we have found the state of the piece and returns to the top of the loop
					
			elif (pieceToCheck.getPieceColour() != self.getPieceColour()) and pieceToCheck.getPieceType != "King":	#If the location contains an oppositely coloured piece which can be taken (all except the king)
				possibleMoveLocations.append([tempFile, tempColumn])		#Adds the location to the list of possible move locations
				continue		#Skips the rest of the for loop as we have found the state of the piece and returns to the top of the loop
				
			else:		#Otherwise the piece to check is the same colour as the piece to move, or it's the opposition's king piece (which can't be taken)
				pass	#Nothing happens here, the program returns to the for loop		
		
		return possibleMoveLocations	#Returns the list of possible move locations to wherever the function was called 
		
		

	def isPieceInCheck:	#Function to check if the King object is in check
		pieceFile, pieceColumn = self.getBoardCoords()		#Initializes two variables which will be used to store the file and column of the King piece
		colour = "Black" if self.getPieceColour == "White" else "Black"
		for i in game.getPieces(colour):
			pieceToCheck = i
			possibleMoveLocations = pieceToCheck.getPossibleMoveLocations()					#Then get all possible moves of said piece
			if [pieceFile, pieceColumn] in possibleMoveLocations:						#If the King piece's file and column are present in the list of the other piece's possible moves:
				return True										#Then return true, the King piece is in check
		return False	#If the program reaches here then the King piece is not in check and so return false

	def isPieceInCheckmate:
		#NEED SINGLE CHECKMATE AND DOUBLE CHECKMATE CASES

class Move():	#A class that represents a chess move with attributes including the piece to move, and the piece for it to replace
	def __init__(self, startPiece, endPiece):				#Constructor for the Move class, declares:
		pieceTypeDict = {"Knight":"N",					#the dictionary that the program uses to determine the algebraic notation of a piece type
				"Queen": "Q",					#
				"King": "K",					#
				"Bishop": "B",					#
				"Pawn":"",					#
				"Empty":"",					#
				"Rook":"R"}					#
		self.startPiece = startPiece					#the piece to move
		self.endPiece = endPiece					#the piece to replace with startPiece (could be a piece or an empty grid)
		self.startPieceNotation = pieceTypeDict[self.startPiece]	#the algebraic notation for piece to move
		self.endPieceNotation = pieceTypeDict[self.endPiece]		#the algebraic notation for piece to replace with startPiece

	#Getters
	def getStartPiece(self):	#'Getter' for the startPiece attribute, returns said attribute when called
		return self.startPiece

	def getEndPiece(self):		#'Getter' for the endPiece attribute, returns said attribute when called
		return self.endPiece

	def getStartPieceNotation(self):	#'Getter' for the startPieceNotation attribute, returns said attribute when called
		return self.startPieceNotation

	def getEndPieceNotation(self):		#'Getter' for the endPieceNotation attribute, returns said attribute when called
		return self.endPieceNotation

game = Game()
















