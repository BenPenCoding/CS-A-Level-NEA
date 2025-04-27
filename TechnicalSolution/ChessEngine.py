#Libraries
from random import *

#Functions
def createGame(name):		#A method that creates a Game object, game, to be accessed by Piece objects
	global game				#Sets the game variable as a global variable
	game = Game(name)		#Instantiates the Game object, game
	game.initializeBoard()	#Initializes board, places the Piece objects in the right places
	return game				

#Classes
class Game():	#A class that represents a chess game with attributes such as board, containing Piece objects
		
		def __init__(self,name):	#Constructor for the Game class. Declares the:
			self.board = [[],[],[],[],[],[],[],[]]	#Array that will contain Piece objects 
			self.blackPieces = []					#Array that will contain Piece objects with colour "Black"
			self.whitePieces = []					#Array that will contain Piece objects with colour "White"
			self.name = name						#Name of the Game object
			self.numMoves = 0						#The number of moves 
			self.turn = "White"						#Whose turn is next
			
		def initializeBoard(self):		#Initializes board, places the Piece objects in the right places			
			
				for i in range(8): 		#These nested for loops make every square on the board an empty square.
					for j in range(8):
						self.board[i].append(Piece("Empty", None, i, j))
				
				#All black Piece objects created 
				self.board[0][0] = Rook("Rook",  "Black",  0, 0)	
				self.board[0][1] = Knight("Knight", "Black", 0, 1)
				self.board[0][2] = Bishop("Bishop", "Black", 0, 2)
				self.board[0][3] = Queen("Queen", "Black", 0, 3)
				self.board[0][4] = King("King", "Black", 0, 4)
				self.board[0][5] = Bishop("Bishop", "Black", 0, 5)
				self.board[0][6] = Knight("Knight", "Black", 0, 6)
				self.board[0][7] = Rook("Rook",  "Black",  0, 7)
				
				for i in range(8):		#This for loop adds all the pieces above to the blackPieces array
					self.blackPieces.append(self.board[0][i])
				
				#This for loop creates all the black Pawn objects and adds them to the blackPieces array
				for i in range(8): 		
					self.board[1][i] = Pawn("Pawn", "Black", 1, i)
					self.blackPieces.append(self.board[1][i])                
				 
				#All white Piece objects created  
				self.board[7][0] = Rook("Rook",  "White",  7, 0)	
				self.board[7][1] = Knight("Knight", "White", 7, 1)
				self.board[7][2] = Bishop("Bishop", "White", 7, 2)
				self.board[7][3] = Queen("Queen", "White", 7, 3)
				self.board[7][4] = King("King", "White", 7, 4)
				self.board[7][5] = Bishop("Bishop", "White", 7, 5)
				self.board[7][6] = Knight("Knight", "White", 7, 6)
				self.board[7][7] = Rook("Rook",  "White",  7, 7)
				
				for i in range(8):		#This for loop adds all the pieces above to the whitePieces array
					self.whitePieces.append(self.board[7][i])
				
				#This for loop creates all the white Pawn objects and adds them to the white Pieces array
				for i in range(8):		
					self.board[6][i] = Pawn("Pawn", "White", 6, i)
					self.whitePieces.append(self.board[6][i])
		
		#Displays the board attribute in a readable way to the user. Purely for testing
		def displayBoard(self):
			for row in self.board:
				array = []
				for piece in row:
					array.append(piece.getPieceType())
				print(array)
				print("")
			print("")
		
		#A method that returns a Piece object at a given rank and File of the board
		def getPieceAtLocation(self, rank, file):			
			return self.board[rank][file]
		
		#A method that sets a Piece object at a given rank and File of the board
		def setPieceAtLocation(self, rank, file, piece):		
			self.board[rank][file] = piece

		#A method that returns the total score of a given colour
		def getColourScore(self, colour):
			pieceScoreDict={"King": 900,	#Dictionary that is used to assign a score to a piece
							"Queen": 90,
							"Rook": 50,
							"Bishop": 30,
							"Knight": 30,
							"Pawn": 10}

			score = 0			#Initial score is 0

			pieces = self.getPieces(colour)		#Gets all the pieces of a given colour

			for piece in pieces:		#Iterates through all pieces 
				score += pieceScoreDict[piece.getPieceType()] 	#Adds piece score to total score

			return score	#Returns total score

		#A method that returns a colour's score subtract the other colour's score
		def evaluateBoard(self, colour):		
			oppositeColour = "White" if colour == "Black" else "Black"		#Reverses colour
			return self.getColourScore(colour) - self.getColourScore(oppositeColour)	

		#A method that returns the best move a given colour can make
		def getBestMove(self, depth, playerMove, colour):	 
			
			#Depth determines how many sets of moves ahead are checked
			if depth == 0:		#Recursive base case
				return None, self.evaluateBoard(colour)

			moves = []	#Array for all possible moves to be stored in

			#Adds every possible move to the moves array
			for piece in self.getPieces(colour):
				for moveLocation in piece.getPossibleMoveLocations(game):
					moves.append([piece, moveLocation])

			#Best move is set as a random move in the list in case no move is better than any other
			bestMove = choice(moves)

			#If colour is the same as player colour we want to get the move that maximises the colour's score
			if playerMove == colour:         
				maxScore = -9999 #Sets the initial max score as unrealistically low so any score will be larger
				
				#Iterating through every move in moves
				for move in moves:

					piece = move[0]
					
					pieceRank, pieceFile = piece.getBoardCoords()	#Stores the original location of the piece

					takenPiece = self.getPieceAtLocation(move[1][0], move[1][1])

					#Moves the piece to take the takenPiece, basically a barebones implementation of game.move
					self.setPieceAtLocation(piece.getRank(), piece.getFile(), 
						Piece("Empty", None, piece.getRank(), piece.getFile()))
					self.setPieceAtLocation(move[1][0], move[1][1], piece)
					piece.setBoardCoords(move[1][0], move[1][1])

					#Removes the takenPiece from its holding array, if it's not an empty piece
					if colour == "White": 
						if takenPiece.getPieceType() != "Empty":
							self.blackPieces.remove(takenPiece)
					else: 
						if takenPiece.getPieceType() != "Empty":
							self.whitePieces.remove(takenPiece)

					oppositeColour = "White" if colour == "Black" else "Black"	#Reverses the colour

					#Finds the current score on the board by recursively calling the getBestMove method
					currentScore = self.getBestMove(depth-1, playerMove, oppositeColour)[1]
					
					#Places the moved pieces back in their original location as if nothing happened					
					self.setPieceAtLocation(pieceRank, pieceFile, piece)
					self.setPieceAtLocation(move[1][0], move[1][1], takenPiece)
					piece.setBoardCoords(pieceRank, pieceFile)
					
					#Adds the taken piece back to its holding array
					if colour == "White": 
						if takenPiece.getPieceType() != "Empty":
							self.blackPieces.append(takenPiece)
					else: 
						if takenPiece.getPieceType() != "Empty":
							self.whitePieces.append(takenPiece)
					
					#If current score is larger than max score then store this move as the best move so far			
					if currentScore > maxScore:
						maxScore = max(currentScore, maxScore)
						bestMove = move

				#When iteration is finished, return the best move and its score 
				return bestMove, maxScore

			#If colour is not the same as player colour we want to get the move that minimises the colour's score
			else:			
				minScore = 9999	#Sets the initial max score as unrealistically high so any score will be lower

				#Iterating through every move in moves
				for move in moves:
					
					piece = move[0]
					
					pieceRank, pieceFile = piece.getBoardCoords() 	#Stores the original location of the piece

					takenPiece = self.getPieceAtLocation(move[1][0], move[1][1])

					#Moves the piece to take the takenPiece, basically a barebones implementation of game.move
					self.setPieceAtLocation(piece.getRank(), piece.getFile(), 
						Piece("Empty", None, piece.getRank(), piece.getFile()))
					self.setPieceAtLocation(move[1][0], move[1][1], piece)
					piece.setBoardCoords(move[1][0], move[1][1])

					#Removes the takenPiece from its holding array, if it's not an empty piece
					if colour == "White": 
						if takenPiece.getPieceType() != "Empty":
							self.blackPieces.remove(takenPiece)
					else: 
						if takenPiece.getPieceType() != "Empty":
							self.whitePieces.remove(takenPiece)
					
					oppositeColour = "White" if colour == "Black" else "Black"
							
					#Finds the current score on the board by recursively calling the getBestMove method				
					currentScore = self.getBestMove(depth-1, playerMove, oppositeColour)[1]

					#Places the moved pieces back in their original location as if nothing happened					
					self.setPieceAtLocation(pieceRank, pieceFile, piece)
					self.setPieceAtLocation(move[1][0], move[1][1], takenPiece)
					piece.setBoardCoords(pieceRank, pieceFile)

					#Adds the taken piece back to its holding array
					if colour == "White": 
						if takenPiece.getPieceType() != "Empty":
							self.blackPieces.append(takenPiece)
					else: 
						if takenPiece.getPieceType() != "Empty":
							self.whitePieces.append(takenPiece)

					#If current score is lower than min score then store this move as the best move so far			
					if currentScore < minScore:
							minScore = min(currentScore, minScore)
							bestMove = move
				
				#When iteration is finished, return the best move and its score 
				return bestMove, minScore

		#A method that returns whose move is next
		def getTurn(self):	
			return self.turn

		#A method that sets whose turn is next
		def setTurn(self, newTurn):
			self.turn = newTurn

		#A method that sets the name of the Game object
		def setName(self, newName):
			self.name = newName

		#A method that returns the number of moves made in the Game object
		def getNumMoves(self):
			return self.numMoves
		
		#A method that sets the number of moves made in the Game object
		def setNumMoves(self, newNumMoves):
			self.numMoves = newNumMoves

		#A method that returns the King object of a given colour
		def getKing(self,colour):
			pieces = self.getPieces(colour)
			for piece in pieces:
				if piece.getPieceType() == "King":
					return piece
		
		#A method that returns the algebraic notation of a given move
		def getNotation(self, startPiece, endPiece):

			#The dictionary that the program uses to determine the algebraic notation of a piece type
			pieceTypeDict = {	"Knight":"N",	
			"Queen": "Q",				
			"King": "K",				
			"Bishop": "B",				
			"Pawn":"",				
			"Empty":"",				
			"Rook":"R"}				

			#The dictionary that the program uses to get the alphabetical representation of a coordinate
			locationTypeDict =  {0: 'a',					
			1: 'b',
			2: 'c',
			3: 'd',
			4: 'e',
			5: 'f',
			6: 'g',
			7: 'h'}

			#Checks if the opposite king is in check following this move
			#With algebraic move notation, if the oppositions king is in check, a '+' is added to the end.
			#Assuming it's not in check, check is set to nothing
			check = ""			
			colour = "White" if startPiece.getPieceColour() == "Black" else "Black"		#Reverses colour

			if self.getKing(colour).isPieceInCheck():	

				if self.getKing(colour).isPieceInCheckmate(game):	
					check = "#"		#If the oppositions king is in checkmate, add a '#' to the end.

				else:
					check = "+"		#If the oppositions king is in check, add a '+' to the end.
			
			#With algebraic move notation, if the move takes another piece,
			#an 'x' is added to the end. Assuming it's not, taking is set to nothing
			taking = ""	
			if endPiece.getPieceType() != "Empty":		#If not moving to an empty square
				taking = "x"				#Set taking to 'x'

			#Returns the final algebraic notation
			return (pieceTypeDict[startPiece.getPieceType()] + taking + 
				locationTypeDict[endPiece.getFile()] + str(8-endPiece.getRank()) + check)
		
		#A method that returns the board attribute
		def getBoard(self):
			return self.board
	
		#A method that sets the board attribute 
		def setBoard(self, newBoard):
			self.board = newBoard
	
		#A method that moves a piece to another piece
		def move(self, startPiece, endPiece):
			
			#Stores the location of both pieces
			startRank, startFile = startPiece.getBoardCoords()
			endRank, endFile = endPiece.getBoardCoords()
			
			#Creates an empty piece at the location of the start piece
			self.setPieceAtLocation(startRank, startFile, Piece("Empty",None, startRank, startFile))	
			
			#If taken piece colour is white, remove it from the list of white pieces
			if endPiece.getPieceColour() == "White":
				self.whitePieces.remove(endPiece)

			#If taken piece colour is black, remove it from the list of black pieces
			elif endPiece.getPieceColour() == "Black":
				self.blackPieces.remove(endPiece)	

			else:
				pass
			#Sets the taken square to the taking piece
			self.setPieceAtLocation(endRank, endFile, startPiece)

			#Sets the Piece object's coordinates to the new location
			startPiece.setBoardCoords(endRank, endFile)					
			
			#Reverses whose turn it is 
			self.turn = "White" if self.turn == "Black" else "Black"
			
			#Increments how many times the piece has been moved
			startPiece.increaseTimesMoved()
			
			#Increments how many times the piece has been moved
			self.numMoves += 1
			
		#A method that returns all pieces of a given colour
		def getPieces(self, colour):
			if colour == "Black":
				return self.blackPieces 
			else:
				return self.whitePieces

		#A method that sets all pieces of a given colour
		def setPieces(self, colour, pieces):
			if colour == "Black":
				self.blackPieces = pieces

			else:
				self.whitePieces = pieces

		#A method that adds a piece to a given colour's holding array
		def addPiece(self, colour, piece):
			if colour == "Black":
				self.blackPieces.append(piece)

			else:
				self.whitePieces.append(piece)

#A class that represents a chess piece with attributes such as piece type and piece location on the board
class Piece():		
	def __init__(self, pieceType, pieceColour, rank, File):	#Constructor for the Piece class. Declares the:  
		self.pieceType = pieceType              #type of piece (pawn, rook, etc)
		self.pieceColour = pieceColour
		self.timesMoved = 0
		self.rank = rank                        #rank (row) in the board
		self.File = File                 	#File in the board

	#Methods
	#An empty method that will be overridden in the piece subclasses, returns all locations that a piece can move to
	def getPossibleMoveLocations(self):	
		None
	
	#Setters
	def setRank(self, rank):	#'Setter' for the rank attribute, called when a piece is instantiated or moved
		self.rank = rank

	def setFile(self, File):	#'Setter' for the File attribute, called when a piece is instantiated or moved
		self.File = File

	#Subroutine that abstracts the individual 'setter' subroutines for board position from the user for simplicity
	def setBoardCoords(self, rank, File):	     
		self.setRank(rank)
		self.setFile(File)
		
	def setPieceType(self, pieceType):	#'Setter' for the pieceType attribute, called when a piece is instantiated
		self.pieceType = pieceType

	def setPieceColour(self, newPieceColour):	#'Setter' for the pieceColour attribute, called when a piece is instantiated 
		self.pieceColour = newPieceColour

	def increaseTimesMoved(self):	#A method that increments how many times a piece moves
		self.timesMoved += 1
	
	#Getters
	def getRank(self):	#'Getter' for the rank attribute, returns said attribute when called
		return self.rank
	
	def getFile(self):	#'Getter' for the File attribute, returns said attribute when called
		return self.File

	def getBoardCoords(self):	#Subroutine that abstracts the individual 'getter' subroutines 
		return self.getRank(), self.getFile()

	def getPieceType(self): 	#'Getter' for the pieceType attribute, returns said attribute when called
		return self.pieceType

	def getPieceColour(self):	#'Getter' for the pieceColour attribute, returns said attribute when called
		return self.pieceColour

	def getTimesMoved(self):	#'Getter' for the timesMoved attribute, returns said attribute when called
		return self.timesMoved
	
	#Checkers
	def isPieceEmpty(self):		#'Checker' which returns True if the value of the attribute pieceType is "Empty"
		return True if self.pieceType == "Empty" else False
			

	def isPieceInCheck(self):	#An empty method that will be overridden in the King subclass
		None
		
class Rook(Piece): 			#A class that represents the rook chess piece, which inherits from the Piece class
	def __init__(self,pieceType, pieceColour, rank, File):		#The constructor for the Rook class
		super().__init__(pieceType, pieceColour, rank, File)	#Calls the constructor from the parent class 

	#A method that returns an array of coordinates that a Piece object can legally move to
	def getPossibleMoveLocations(self, game):		#A method that returns all locations a piece can move to
		possibleMoveLocations = []		#Declaring the array to add possible move locations to
		pieceRank, pieceFile = self.getBoardCoords()	#Gets the rank and File of the piece to move
		
		#Declares two variables which will be used to change the direction of the board search by
	 	#switching between -1 and 1 to reverse direction.
		rankIncrement, FileIncrement = 0, 0  	
		
		for i in range(4):		#The four cardinal directions

			tempRank, tempFile = pieceRank, pieceFile	#Initializes two variables that are set to the location of the piece to move
			
			while True:		#A while loop so that all possible move locations in a row are found 
				match i:	#Python's equivalent of a switch/case statement
					case 0:	#If the increment variable has a value of 0, test all possible move locations to the right of the piece
						rankIncrement, FileIncrement = 1, 0
					case 1:	#If the increment variable has a value of 1, test all possible move locations above the piece
						rankIncrement, FileIncrement = 0, -1
					case 2:	#If the increment variable has a value of 2, test all possible move locations to the left of the piece
						rankIncrement, FileIncrement = -1, 0
					case 3:	#If the increment variable has a value of 3, test all possible move locations below the piece
						rankIncrement, FileIncrement = 0, 1
					case _:	#DEBUG - If the increment variable has a value not inside 0 <= i <= 3 then print the nature of the error
						print("Fatal error, Rook class switch/case statement experienced a larger increment value than expected.")
						quit()	#DEBUG - Quits the program entirely

				tempRank += rankIncrement	#Increments the rank of the next piece to search by the designated increment
				tempFile += FileIncrement	#Increments the File of the next piece to search by the designated increment
				
				#Checks if the rank and File of the next piece to check are actually not on the board                
				if tempRank > 7 or tempRank < 0 or tempFile > 7 or tempFile < 0:	
					break		#If this is the case, exit the while loop and begin checking in another direction						
				
				pieceToCheck = game.getPieceAtLocation(tempRank, tempFile)	#Gets the piece object to check 

				if pieceToCheck.isPieceEmpty():			#Checks if the piece object is empty
					possibleMoveLocations.append([tempRank, tempFile]) 	#If it is, add the location to the list of possible move locations
					continue						#Moves on to checking the next piece
				else:

					#If the location contains an oppositely coloured piece which can be taken 
					if (pieceToCheck.getPieceColour() != self.getPieceColour()) :	
						possibleMoveLocations.append([tempRank, tempFile])	#Adds the location to the list of possible move locations
						break							#Stops checking the next piece and exits the while loop
					
					else:		#Otherwise the piece to check is the same colour as the piece to move
						break	#Stops checking the next piece and exits the while loop

		return possibleMoveLocations	#Returns the list of possible move locations to wherever the method was called 


class Bishop(Piece):			#A class that represents the bishop chess piece, which inherits from the Piece class
	def __init__(self,pieceType, pieceColour, rank, File):		#The constructor for the Bishop class
		super().__init__(pieceType, pieceColour, rank, File)	#Calls the super constructor from the parent class (Piece class)

	#A method that returns an array of coordinates that a Piece object can legally move to
	def getPossibleMoveLocations(self,game):
		possibleMoveLocations = []		#Declaring the array to add possible move locations to
		pieceRank, pieceFile = self.getBoardCoords()	#Gets the rank and File of the piece to move by using the getBoardCoords method 

		#Declares two variables which will be used to change the direction of the board search by switching between -1 and 1 to change direction.
		rankIncrement, FileIncrement = 0, 0  	
		
		for i in range(4):		#The four diagonal directions

			tempRank, tempFile = pieceRank, pieceFile	#Initializes two variables that are set to the location of the piece to move
			
			while True:		#A while loop so that all possible move locations in a diagonal line are found 
				match i:	#Python's equivalent of a switch/case statement
					case 0:		#If the increment variable has a value of 0, test all possible move locations to the up and right of the piece
						rankIncrement, FileIncrement = -1, 1
					case 1:		#If the increment variable has a value of 1, test all possible move locations up and left of the piece
						rankIncrement, FileIncrement = -1, -1
					case 2:		#If the increment variable has a value of 2, test all possible move locations to the down and left of the piece
						rankIncrement, FileIncrement = 1, -1
					case 3:		#If the increment variable has a value of 3, test all possible move locations down and right of the piece
						rankIncrement, FileIncrement = 1, 1
					case _:		#DEBUG - If the increment variable has a value not inside 0 <= i <= 3 then print the nature of the error
						print("Fatal error, Bishop class switch/case statement experienced a larger increment value than expected.")
						quit()		#DEBUG - Quits the program entirely

				tempRank += rankIncrement		#Increments the rank of the next piece to search by the designated direction-dependent increment
				tempFile += FileIncrement		#Increments the File of the next piece to search by the designated direction-dependent increment
				
				#Checks if the rank and File of the next piece to check are actually not on the board                
				if tempRank > 7 or tempRank < 0 or tempFile > 7 or tempFile < 0:	
					break									#If this is the case, exit the while loop and begin checking in another direction							

				pieceToCheck = game.getPieceAtLocation(tempRank, tempFile)	#Gets the piece object to check 
				
				if pieceToCheck.isPieceEmpty():			#Checks if the piece object is empty
					possibleMoveLocations.append([tempRank, tempFile]) 	#If it is, add the location to the list of possible move locations
					continue
				else:	

					#If the location contains an oppositely coloured piece which can be taken 
					if pieceToCheck.getPieceColour() != self.getPieceColour():	
						possibleMoveLocations.append([tempRank, tempFile]) #Adds the location to the list of possible move locations	
						break
					
					else:		#Otherwise the piece to check is the same colour as the piece to move
						break	#Exits the while loop
		
		return possibleMoveLocations	#Returns the list of possible move locations to wherever the method was called 

class Knight(Piece):			#A class that represents the knight chess piece, which inherits from the Piece class
	def __init__(self,pieceType, pieceColour, rank, File):		#The constructor for the Knight class
		super().__init__(pieceType, pieceColour, rank, File)	#Calls the super constructor from the parent class 

	#A method that returns an array of coordinates that a Piece object can legally move to
	def getPossibleMoveLocations(self, game):
		possibleMoveLocations = []		#Declaring the array to add possible move locations to
		pieceRank, pieceFile = self.getBoardCoords()	#Gets the rank and File of the piece to move
		possibleIncrementList = [[-2, 1], [-2, -1], [-1, 2], [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2]]	
		
		for coordinates in possibleIncrementList:
			#Declaring and initializing two variables that store the location of the piece to check
			tempRank, tempFile = pieceRank +coordinates[0], pieceFile + coordinates[1]	

			#Checks if the rank and File of the next piece to check are actually not on the board
			if (tempRank < 0 or tempRank > 7) or (tempFile < 0 or tempFile > 7): 	
				continue
				
			pieceToCheck = game.getPieceAtLocation(tempRank, tempFile)

			if pieceToCheck.isPieceEmpty():		#Checks if the piece object is empty
				possibleMoveLocations.append([tempRank, tempFile]) 	#If it is, add the location to the list of possible move locations
				continue		#Skips the rest of the for loop as we have found the state of the piece and returns to the top of the loop
			else:	
				#If the location contains an oppositely coloured piece which can be taken
				if (pieceToCheck.getPieceColour() != self.getPieceColour()):	
					possibleMoveLocations.append([tempRank, tempFile])		#Adds the location to the list of possible move locations
					continue		#Skips the rest of the for loop as we have found the state of the piece and returns to the top of the loop
		
				else:	#Otherwise the piece to check is the same colour as the piece to move
					pass	#Nothing happens here, the program returns to the for loop		
		
		return possibleMoveLocations	#Returns the list of possible move locations to wherever the method was called 
		


class Queen(Piece):			#A class that represents the queen chess piece, which inherits from the Piece class
	def __init__(self,pieceType, pieceColour, rank, File):		#The constructor for the Queen class
		super().__init__(pieceType, pieceColour, rank, File)	#Calls the super constructor from the parent class (Piece class)

	#A method that returns an array of coordinates that a Piece object can legally move to
	def getPossibleMoveLocations(self,game):
		possibleMoveLocations = []		#Declaring the array to add possible move locations to
		pieceRank, pieceFile = self.getBoardCoords()	#Gets the rank and File of the piece to move by using the getBoardCoords method 
		rankIncrement, FileIncrement = 0, 0  	#Declares two variables which will be used to change the direction of the board search

		#The queen piece can move like a rook and a bishop at the same time, 
		#to check for possible move locations I used the same code from both the Bishop class and the Rook class
		#The code from the Rook class:
		for i in range(4):		#The four cardinal directions

			tempRank, tempFile = pieceRank, pieceFile	#Initializes two variables that are set to the location of the piece to move
			
			while True:		#A while loop so that all possible move locations in a row are found 
				match i:	#Python's equivalent of a switch/case statement
					case 0:	#If the increment variable has a value of 0, test all possible move locations to the right of the piece
						rankIncrement, FileIncrement = 1, 0
					case 1:	#If the increment variable has a value of 1, test all possible move locations above the piece
						rankIncrement, FileIncrement = 0, -1
					case 2:	#If the increment variable has a value of 2, test all possible move locations to the left of the piece
						rankIncrement, FileIncrement = -1, 0
					case 3:	#If the increment variable has a value of 3, test all possible move locations below the piece
						rankIncrement, FileIncrement = 0, 1
					case _:	#DEBUG - If the increment variable has a value not inside 0 <= i <= 3 then print the nature of the error
						print("Fatal error, Rook class switch/case statement experienced a larger increment value than expected.")
						quit()	#DEBUG - Quits the program entirely

				tempRank += rankIncrement	#Increments the rank of the next piece to search by the designated direction-dependent increment
				tempFile += FileIncrement	#Increments the File of the next piece to search by the designated direction-dependent increment
				
				#Checks if the rank and File of the next piece to check are actually not on the board
				if tempRank > 7 or tempRank < 0 or tempFile > 7 or tempFile < 0:	
					break	
				
				pieceToCheck = game.getPieceAtLocation(tempRank, tempFile)	#Gets the piece object to check 

				if pieceToCheck.isPieceEmpty():			#Checks if the piece object is empty
					possibleMoveLocations.append([tempRank, tempFile]) 	#If it is, add the location to the list of possible move locations
					continue						#Moves on to checking the next piece
				else:
					if (pieceToCheck.getPieceColour() != self.getPieceColour()): #If the location contains an oppositely coloured piece 
						possibleMoveLocations.append([tempRank, tempFile])	#Adds the location to the list of possible move locations
						break							#Stops checking the next piece and exits the while loop
					
					else:		#Otherwise the piece to check is the same colour as the piece to move, 
						break	#Stops checking the next piece and exits the while loop

		#The code from the Bishop class:
		for i in range(4):		#The four diagonal directions

			tempRank, tempFile = pieceRank, pieceFile	#Initializes two variables that are set to the location of the piece to move
			
			while True:		#A while loop so that all possible move locations in a diagonal line are found 
				match i:	#Python's equivalent of a switch/case statement
					case 0:	#If the increment variable has a value of 0, test all possible move locations to the up and right of the piece
						rankIncrement, FileIncrement = -1, 1
					case 1:	#If the increment variable has a value of 1, test all possible move locations up and left of the piece
						rankIncrement, FileIncrement = -1, -1
					case 2:	#If the increment variable has a value of 2, test all possible move locations to the down and left of the piece
						rankIncrement, FileIncrement = 1, -1
					case 3:	#If the increment variable has a value of 3, test all possible move locations down and right of the piece
						rankIncrement, FileIncrement = 1, 1
					case _:	#DEBUG - If the increment variable has a value not inside 0 <= i <= 3 then print the nature of the error
						print("Fatal error, Bishop class switch/case statement experienced a larger increment value than expected.")
						quit()	#DEBUG - Quits the program entirely

				tempRank += rankIncrement	#Increments the rank of the next piece to search by the designated direction-dependent increment
				tempFile += FileIncrement	#Increments the File of the next piece to search by the designated direction-dependent increment
				
				#Checks if the rank and File of the next piece to check are actually not on the board                 
				if tempRank > 7 or tempRank < 0 or tempFile > 7 or tempFile < 0:	
					break									#If this is the case, exit the while loop and begin checking in another direction							
				
				pieceToCheck = game.getPieceAtLocation(tempRank, tempFile)	#Gets the piece object to check 
				
				if pieceToCheck.isPieceEmpty():			#Checks if the piece object is empty
					possibleMoveLocations.append([tempRank, tempFile]) 	#If it is, add the location to the list of possible move locations
					continue
				else:
					if (pieceToCheck.getPieceColour() != self.getPieceColour()):	#If the location contains an oppositely coloured piece
						possibleMoveLocations.append([tempRank, tempFile])		#Adds the location to the list of possible move locations
						break
					
					else:		#Otherwise the piece to check is the same colour as the piece to move
						break	#Exits the while loop

		return possibleMoveLocations	#Returns the list of possible move locations to wherever the method was called 
	


class Pawn(Piece):			#A class that represents the pawn chess piece, which inherits from the Piece class
	def __init__(self,pieceType, pieceColour, rank, File):		#The constructor for the Pawn class
		super().__init__(pieceType, pieceColour, rank, File)	#Calls the super constructor from the parent class (Piece class)

	#A method that returns an array of coordinates that a Piece object can legally move to
	def getPossibleMoveLocations(self, game):
			possibleMoveLocations = []		#Declaring the array to add possible move locations to
			pieceRank, pieceFile = self.getBoardCoords()	#Gets the rank and File of the piece to move by using the getBoardCoords method 

			if self.pieceColour == "White":	#This if statement initializes an inrement variable, i
				i = 1
			else:
				i= -1
			
			#Checks the Piece object in front of the Pawn, if empty, add it to the possible move locations
			tempRank, tempFile = pieceRank + (-1 * i), pieceFile + 0
			if  not (tempRank > 7 or tempRank < 0 or tempFile > 7 or tempFile < 0):        
				if game.getPieceAtLocation(tempRank, tempFile).getPieceType() == "Empty":
					possibleMoveLocations.append([tempRank, tempFile])
					
			#Checks the Piece object in front of and to the right of the Pawn, if an opposing Piece, add it to the possible move locations
			tempRank, tempFile = pieceRank + (-1 * i), pieceFile + 1
			if  not (tempRank > 7 or tempRank < 0 or tempFile > 7 or tempFile < 0):      
				if ((game.getPieceAtLocation(tempRank, tempFile).getPieceColour() != self.getPieceColour()) and 
				(game.getPieceAtLocation(tempRank, tempFile).getPieceType() != "Empty")):
					possibleMoveLocations.append([tempRank, tempFile])
			
			#Checks the Piece object in front of and to the left of the Pawn, if an opposing Piece, add it to the possible move locations
			tempRank, tempFile = pieceRank + (-1 * i), pieceFile - 1
			if  not (tempRank > 7 or tempRank < 0 or tempFile > 7 or tempFile < 0):      
				if ((game.getPieceAtLocation(tempRank, tempFile).getPieceColour() != self.getPieceColour()) and 
					(game.getPieceAtLocation(tempRank, tempFile).getPieceType() != "Empty")):
					possibleMoveLocations.append([tempRank, tempFile])

			#Checks the Piece object if it has moved more than once. If not, check two spaces in front of the Pawn,
			#if empty, add it to the possible move locations
			if self.timesMoved == 0:
				tempRank, tempFile = pieceRank + (-2 * i), pieceFile + 0
				if  not (tempRank > 7 or tempRank < 0 or tempFile > 7 or tempFile < 0):        
					if game.getPieceAtLocation(tempRank, tempFile).getPieceType() == "Empty":
						possibleMoveLocations.append([tempRank, tempFile])
			
			return possibleMoveLocations	#Returns the list of possible move locations to wherever the method was called 
					
class King(Piece):			#A class that represents the king chess piece, which inherits from the Piece class
	def __init__(self,pieceType, pieceColour, rank, File):		#The constructor for the King class
		super().__init__(pieceType, pieceColour, rank, File)	#Calls the super constructor from the parent class (Piece class)
	
	#A method that returns an array of coordinates that a Piece object can legally move to
	def getPossibleMoveLocations(self, game):

		possibleMoveLocations = []		#Declaring the array to add possible move locations to
		pieceRank, pieceFile = self.getBoardCoords()	#Gets the rank and File of the piece to move
		possibleIncrementList = [[-1, -1],[-1, 0],[-1, 1], [0,-1],[0, 1],[1, -1],[1, 0],[1, 1]]	

		for coordinates in possibleIncrementList:
			pieceRank, pieceFile = self.getBoardCoords()

			#Declaring and initializing two variables that store the location of the piece to check
			tempRank, tempFile = pieceRank +coordinates[0], pieceFile + coordinates[1]	

			#Checks if the rank and File of the next piece to check are actually not on the board 
			if (tempRank < 0 or tempRank > 7 or tempFile < 0 or tempFile > 7):	
				continue
				
			pieceToCheck = game.getPieceAtLocation(tempRank, tempFile)

			if pieceToCheck.isPieceEmpty():			#Checks if the piece object is empty
				possibleMoveLocations.append([tempRank, tempFile]) 	#If it is, add the location to the list of possible move locations
				continue		#Skips the rest of the for loop as we have found the state of the piece and returns to the top of the loop
				
			#If the location contains an oppositely coloured piece which can be taken (all except the king)
			elif (pieceToCheck.getPieceColour() != self.getPieceColour()) and pieceToCheck.getPieceType != "King":	
				possibleMoveLocations.append([tempRank, tempFile])		#Adds the location to the list of possible move locations
				continue		#Skips the rest of the for loop as we have found the state of the piece and returns to the top of the loop
				
			else:		#Otherwise the piece to check is the same colour as the piece to move
				pass	#Nothing happens here, the program returns to the for loop		

		return possibleMoveLocations	#Returns the list of possible move locations to wherever the method was called 
	
	
	# A method to check if the King object is in check
	def isPieceInCheck(self):	

		#Initializes two variables which will be used to store the rank and File of the King piece
		pieceRank, pieceFile = self.getBoardCoords()		
		colour = "Black" if self.getPieceColour() == "White" else "White" 	#Reverses the colour

		#Iterates through all pieces of the opposing colour
		for pieceToCheck in game.getPieces(colour):
			possibleMoveLocations = pieceToCheck.getPossibleMoveLocations(game)		#Then get all possible moves of said piece

			#If the King piece's rank and File are present in the list of the other piece's possible moves:
			if [pieceRank, pieceFile] in possibleMoveLocations:		
				return True			#Then return true, the King piece is in check

		return False	#If the program reaches here then the King piece is not in check and so return false
	
	#a Method to check if the King object is in checkmate
	def isPieceInCheckmate(self,game):
		kingColour = self.getPieceColour()	#Stores the colour of the king

		#If King piece is in check
		if game.getKing(kingColour).isPieceInCheck():

			#Iterate through all pieces of the same colour
			for piece in game.getPieces(kingColour):

						#Stores the piece location and all its possible move locations 
						pieceRank, pieceFile = piece.getBoardCoords()
						possibleMoveLocations = piece.getPossibleMoveLocations(game)

						#Iterates through the list of possible move locations
						for moveLocation in possibleMoveLocations:

							#Gets the Piece object for taken piece
							takenPiece = game.getPieceAtLocation(moveLocation[0], moveLocation[1])

							#Makes a temporary move to check if the King piece is still in check
							game.setPieceAtLocation(piece.getRank(), piece.getFile(), Piece("Empty", None, piece.getRank(), piece.getFile()))
							game.setPieceAtLocation(moveLocation[0], moveLocation[1], piece)
							piece.setBoardCoords(moveLocation[0], moveLocation[1])
							
							#If King piece is not in check following the move
							if not self.isPieceInCheck():

								#Return pieces to their original coordinates
								game.setPieceAtLocation(pieceRank, pieceFile, piece)
								piece.setBoardCoords(pieceRank, pieceFile)
								game.setPieceAtLocation(moveLocation[0], moveLocation[1], takenPiece)
								
								#Return false, as there exists a move to take the King piece out of check
								return False

							else:
								
								#Return pieces to their original coordinates								
								game.setPieceAtLocation(pieceRank, pieceFile, piece)
								piece.setBoardCoords(pieceRank, pieceFile)
								game.setPieceAtLocation(moveLocation[0], moveLocation[1], takenPiece)
				
			#If the end of the iteration is reached and there is no move which would take the King piece out of checkmate, return True				
			return True
		
		else:

			return False	#Returns false, if King piece is not in check it can't be in checkmate


