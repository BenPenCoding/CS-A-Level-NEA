import pygame as pg

class Piece():
	def __init__(self, pieceType, column, file):
		self.pieceType = pieceType
		self.column = column
		self.file = file
		

class Move():

	def __init__(self, startPiece, endPiece):
		pieceTypeDict ={"Knight":"N", "Queen": "Q", "King": "K", "Bishop": "B", "Pawn":"", "Empty":"", "Rook":"R"}
		self.startPiece = startPiece
		self.endPiece = endPiece
		self.startPieceNotation = pieceTypeDict[self.startPiece]
		self.endPieceNotation = pieceTypeDict[self.endPiece]
	
	
		
