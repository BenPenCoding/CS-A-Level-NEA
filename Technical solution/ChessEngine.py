#Libraries
import pygame as pg

class Game():

	def __init__(self,name):
		self.name = name
		self.board = []

	def getPieceAtLocation(self, file, column):
		return self.board[file][column]
	
	#Classes
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
	
	class Rook(Piece):
		def __init__(self):
			Super().__init__()
		
		def findPossibleMoveLocations(self):	#A function that returns all locations that a piece can move to
			if self.colour == "white": i = -1
			else: i = 1
			while True:	#Down
			///MUST FINISH///
				
	
	
	
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
			
