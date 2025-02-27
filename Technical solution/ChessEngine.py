#Libraries
import pygame as pg

#Classes
class Game():

	def __init__(self,name):
		self.name = name
		self.board = []

	def getPieceAtLocation(self, file, column):
		return self.board[file][column]

class Piece():		#A class that represents a chess piece with attributes such as piece type and piece location on the board
	def __init__(self, pieceType, pieceColour, file, column):	#Constructor for the Piece class. Declares the:  
		self.pieceType = pieceType              #type of piece (pawn, rook, etc)
		self.pieceColour = pieceColour
		self.file = file                        #file (row) in the board
		self.column = column                 	#column in the board

	#Functions
	def findPossibleMoveLocations(self):	#An empty function that will be overridden in the piece subclasses, returns all locations that a piece can move to
		None
	
	#Setters
	def setFile(self, file):	#'Setter' for the file attribute, called when a piece is instantiated or moved
		self.file = file

	def setColumn(self, column):	#'Setter' for the column attribute, called when a piece is instantiated or moved
		self.column = column

	def setBoardCoords(self, file, column):	     #Subroutine that abstracts the individual 'setter' subroutines for board position from the user for simplicity
		setFile(file)
		setColumn(column)
		
	def setPieceType(self, pieceType):	#'Setter' for the pieceType attribute, called when a piece is instantiated or a pawn reaches the other side of the board and can change into another piece
		self.pieceType = pieceType

	#Getters
	def getFile(self):	#'Getter' for the file attribute, returns said attribute when called
		return self.file
	
	def getColumn(self):	#'Getter' for the column attribute, returns said attribute when called
		return self.column

	def getBoardCoords(self):	#Subroutine that abstracts the individual 'getter' subroutines for board position from the user for simplicity
		return getFile, getColumn

	def getPieceType(self): 	#'Getter' for the pieceType attribute, returns said attribute when called
		return self.pieceType

class Rook(Piece): 			#A class that represents the rook chess piece, which inherits from the Piece class
	def __init__(self):		#The constructor for the Rook class
		Super().__init__()	#Calls the super constructor from the parent class (Piece class)
	
	def findPossibleMoveLocations(self):		#A function that returns all locations that a piece can move to
		possibleMoveLocations = []		#Declaring the array to add possible move locations to
		file, column = self.getBoardCoords()	#Gets the file and column of the piece to move by using the getBoardCoords function 
		fileIncrement, columnIncrement = 0, 0  	#Declares two variables which will be used to change the direction of the board search by switching between -1 and 1 to reverse direction.
		tempFile, tempColumn = 0, 0		#Declares two variables that will be used to store the temporary file and column of possible locations to move to
		
		for i in range(4):	#The four cardinal directions
			while True:	#A while loop so that all possible move locations in a row are found 

				'''Add recoding to fileIncrement and columnIncrement to change direction each iteration'''
				
				pieceToCheck = game.getPieceAtLocation(tempFile, tempColumn)	#Gets the piece object to check 
				if pieceToCheck.getPieceType() == "Empty":			#Checks if the piece object is empty
					possibleMoveLocations.append([tempFile, tempColumn]) 	#If it is, add the location to the list of possible move locations
				else:		#Otherwise the piece to check is not empty 
					break	#Exits the while loop



class Move():	#A class that represents a chess move with attributes including the piece to move, and the piece for it to replace
	def __init__(self, startPiece, endPiece):				#Constructor for the Move class, declares the:
		pieceTypeDict = {"Knight":"N",					#dictionary that the program uses to determine the algebraic notation of a piece type
				"Queen": "Q",					#
				"King": "K",					#
				"Bishop": "B",					#
				"Pawn":"",					#
				"Empty":"",					#
				"Rook":"R"}					#
		self.startPiece = startPiece					#piece to move
		self.endPiece = endPiece					#piece to replace with startPiece (could be a piece or an empty grid)
		self.startPieceNotation = pieceTypeDict[self.startPiece]	#algebraic notation for piece to move
		self.endPieceNotation = pieceTypeDict[self.endPiece]		#algebraic notation for piece to replace with startPiece

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
