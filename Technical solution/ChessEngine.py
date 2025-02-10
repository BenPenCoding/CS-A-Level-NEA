#Libraries
import pygame as pg

#Classes
class Piece():
	def __init__(self, pieceType, file, column):	#Constructor for the Piece class. Declares the:  
		self.pieceType = pieceType              #type of piece (pawn, rook, etc)
		self.file = file                        #file (row) in the board
		self.column = column                 	#column in the board

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

class Move():
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
	
	
		
