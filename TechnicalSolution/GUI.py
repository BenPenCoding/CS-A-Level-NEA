import pygame
import os
from ChessEngine import *
import time 

pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width,height))

class DisplayPiece(pygame.sprite.Sprite):
	
	def __init__(self, top, left, piece):
		self.piece = piece
		self.path = os.path.dirname(__file__)
		self.image = pygame.image.load(os.path.join(self.path,f"Images/{piece.getPieceColour()}{piece.getPieceType()}.jpg")).convert_alpha() if piece.getPieceType() != "Empty" else pygame.image.load(os.path.join(self.path,"Images/square.jpg")).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.top, self.rect.left = top, left
		self.selected = False
		self.highlighted = False

	def getPiece(self):
		return self.piece

	def setLocation(self, top, left):
		self.rect.top, self.rect.left = top, left
	
	def clicked(self):
		self.selected = not self.selected
		
	def isSelected(self):
		return self.selected
	
	def highlight(self):
		self.image = pygame.image.load(os.path.join(self.path,f"Images/{self.piece.getPieceColour()}{self.piece.getPieceType()}H.jpg")).convert_alpha() if self.piece.getPieceType() != "Empty" else pygame.image.load(os.path.join(self.path, "Images/squareH.jpg")).convert_alpha()
		self.highlighted = True
		
	def unhighlight(self):
		self.image = pygame.image.load(os.path.join(self.path, f"Images/{self.piece.getPieceColour()}{self.piece.getPieceType()}.jpg")).convert_alpha() if self.piece.getPieceType() != "Empty" else pygame.image.load(os.path.join(self.path, "Images/square.jpg")).convert_alpha()
		self.highlighted = False
	
	def isHighlighted(self):
		return self.highlighted

def deselectAll(pieces):
	for row in pieces:
		for piece in row:
			if piece.isSelected():
				piece.clicked()

def unhighlightAll(pieces):
	for row in pieces:
		for piece in row:
			piece.unhighlight()

def returnSelected(pieces):
	for row in pieces:
		for piece in row:
			if piece.isSelected():
				return piece
	return None

def beginOfflineBot():		#Begins a chess game against a bot
	
	game = createGame("Game")	#Creates a Game piece, game

	#Creates and fills the list that will contain all display pieces (frontend)
	displayPieceList = [[],[],[],[],[],[],[],[]]	
	for rowOfPieces in game.getBoard():
		for piece in rowOfPieces:
			#The pieces are 50x50 so the pixel coordinates are simply the array coordinates multiplied by 50
			top = piece.getRank() * 50	
			left = piece.getFile() * 50
			displayPieceList[game.getBoard().index(rowOfPieces)].append(DisplayPiece(top, left, piece))

	#These store the algebraic notation of each move made
	whiteNotation = []
	blackNotation = []

	#Begins the chess game's mainloop
	running = True
	while running:
		
		for event in pygame.event.get(): 	#Loops through all current events that pygame has detected
			
			#If game turn is white's, then it's the user's turn
			if game.getTurn() == "White":	
				if event.type == pygame.MOUSEBUTTONUP:
					left, top = pygame.mouse.get_pos()
					if left > 399 or top > 399:
						pass
					else:
						
						clickedPiece = displayPieceList[int(top/50)][int(left/50)]	#Finds individual piece that is clicked on
						
						if returnSelected(displayPieceList) == None:				#If no other pieces are selected
							
							if clickedPiece.piece.getPieceColour() != game.turn:			#If selected piece is not the colour of the current turn
								continue										#Skip it 
							
							clickedPiece.clicked()										#Select this piece
							if clickedPiece.piece.getPieceType() != "Empty":					#If piece is not empty
								possibleMoveLocations = clickedPiece.piece.getPossibleMoveLocations(game)	#Find possible move locations
								
								if game.getKing(game.getTurn()).isPieceInCheck():	#If the same coloured king is in check we can only move pieces that would prevent this
									pieceRank, pieceFile = clickedPiece.piece.getBoardCoords()			#Saves a copy of the clicked piece's locationfor later reference
									for moveLocation in possibleMoveLocations:						#Repeats through all possible move locations
										takenPiece = game.getPieceAtLocation(moveLocation[0], moveLocation[1])
										#Fake move, where the piece is moved, the program checks if the king piece is in check, then highlights the move if not
										game.setPieceAtLocation(clickedPiece.piece.getRank(), clickedPiece.piece.getFile(), Piece("Empty", None, clickedPiece.piece.getRank(), clickedPiece.piece.getFile))						
										game.setPieceAtLocation(moveLocation[0], moveLocation[1], clickedPiece.piece)																	
										clickedPiece.piece.setBoardCoords(moveLocation[0], moveLocation[1])
										
										#If this move would not cause the king to be in check, highlight the move
										if not game.getKing(game.getTurn()).isPieceInCheck():
											displayPieceList[moveLocation[0]][moveLocation[1]].highlight()
											
										#Resets the moved piece and its attributes, hence the name 'fake' move
										game.setPieceAtLocation(pieceRank, pieceFile, clickedPiece.piece)
										clickedPiece.piece.setBoardCoords(pieceRank, pieceFile)
										game.setPieceAtLocation(moveLocation[0], moveLocation[1], takenPiece)
										
								else:		#If the same coloured king is not in check we can highlight all possible moves
									for moveLocation in possibleMoveLocations:
										displayPieceList[moveLocation[0]][moveLocation[1]].highlight()		#Highlights all possible moves
										
						else:		#If a piece is already selected
							firstClickedPiece = returnSelected(displayPieceList)	#Finds the already selected piece, as this will be the piece that's moving
							secondClickedPiece = clickedPiece						#This is the most recently clicked piece, the piece to be taken
							
							if firstClickedPiece == secondClickedPiece or not secondClickedPiece.isHighlighted():	#If both pieces are the same (same piece clicked twice) or the second piece hasn't been highlighted (not a valid move)
								deselectAll(displayPieceList)		#Then deselect and unhighlight all pieces
								unhighlightAll(displayPieceList)
							
							else:		#If both pieces are valid and not equal
								
								#The coordinates of the first piece are stored
								firstRank = firstClickedPiece.piece.getRank()	
								firstFile = firstClickedPiece.piece.getFile()
								
								#The coordinates of the second piece are stored
								secondRank = secondClickedPiece.piece.getRank()
								secondFile = secondClickedPiece.piece.getFile()

								#Makes the move on the game array (backend)
								game.move(firstClickedPiece.piece, secondClickedPiece.piece)
								
								#Finds the algebraic notation of the move
								notation = f"{game.getNumMoves()}. {game.getNotation(displayPieceList[firstRank][firstFile].piece, displayPieceList[secondRank][secondFile].piece)}"
								
								#Stores the algebraic notation in its respective array
								whiteNotation.append(notation)

								#Makes the move on the display array (frontend)
								displayPieceList[firstRank][firstFile] = DisplayPiece(firstRank*50, firstFile*50,  game.getPieceAtLocation(firstRank, firstFile))
								displayPieceList[secondRank][secondFile] = DisplayPiece(secondRank*50, secondFile*50,  game.getPieceAtLocation(secondRank, secondFile))
								
								#Deselects and unhighlights all pieces
								deselectAll(displayPieceList)
								unhighlightAll(displayPieceList)
								
								oppositionColour = "White" if game.getTurn() == "Black" else "Black"	#Finds the opposite colour to the one stored currently

								if game.getKing(game.getTurn()).isPieceInCheckmate(game):	#If a player places their oppositions king in checkmate, end game
									print(f"{oppositionColour} wins the game by checkmate!")
									running = False

			else:	#If it's the bot's move
				time.sleep(2)
				move = game.getBestMove(2,"Black", "Black")		#Find the best move
				
				piece1 = move[0][0]		#Assigns the piece used in the best move to piece1 

				#Finds the display piece (frontend) that piece1 is an attribute of
				for displayPieceRow in displayPieceList:
					for displayPiece in displayPieceRow:
						if displayPiece.getPiece() == piece1:
							firstPiece = displayPiece

				#Finds the coordinates of the moving piece
				firstRank = firstPiece.piece.getRank()
				firstFile = firstPiece.piece.getFile()
				
				piece2 = game.getPieceAtLocation(move[0][1][0], move[0][1][1])		#Finds the piece at the location specified by the best move found earlier

				#Finds the display piece (frontend) that piece2 is an attribute of
				for displayPieceRow in displayPieceList:
					for displayPiece in displayPieceRow:
						if displayPiece.piece == piece2:
							secondPiece = displayPiece

				#Finds the coordinates of the piece to be taken
				secondRank = secondPiece.piece.getRank()
				secondFile = secondPiece.piece.getFile()

				#Makes the move on the game array (backend)
				game.move(firstPiece.piece, secondPiece.piece)
				
				#Finds the algebraic notation of the move	
				notation = f"{game.getNumMoves()}. {game.getNotation(displayPieceList[firstRank][firstFile].piece, displayPieceList[secondRank][secondFile].piece)}"
				blackNotation.append(notation)				

				#Makes the move on the display array (frontend)
				displayPieceList[firstRank][firstFile] = DisplayPiece(firstRank*50, firstFile*50,  game.getPieceAtLocation(firstRank, firstFile))
				displayPieceList[secondRank][secondFile] = DisplayPiece(secondRank*50, secondFile*50,  game.getPieceAtLocation(secondRank, secondFile))
			
			#If the user closes the program, end the game		
			if event.type == pygame.QUIT:
				running = False
		
		screen.fill((255, 255, 255))	#Every frame, fill the screen white
		
		#For each display piece in displayPieceList, draw it to the screen every frame
		for rowOfPieces in displayPieceList:
			for piece in rowOfPieces:
				screen.blit(piece.image,piece.rect)
		
		#Updates the screen every frame	
		pygame.display.update()
		
	  

def beginOfflineMultiplayer():		#Starts 

	game = createGame("Game")

	displayPieceList = [[],[],[],[],[],[],[],[]]	

	for rowOfPieces in game.getBoard():
		for piece in rowOfPieces:
			top = piece.getRank() * 50
			left = piece.getFile() * 50
			displayPieceList[game.getBoard().index(rowOfPieces)].append(DisplayPiece(top, left, piece))

	#These store the algebraic notation of each move made
	whiteNotation = []
	blackNotation = []

	running = True

	while running:
		
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONUP:
				left, top = pygame.mouse.get_pos()
				if left > 399 or top > 399:
					pass
				else:
					clickedPiece = displayPieceList[int(top/50)][int(left/50)]	#Finds individual piece that is clicked on
					
					if returnSelected(displayPieceList) == None:				#If no other pieces are selected
						
						if clickedPiece.piece.getPieceColour() != game.turn:			#If selected piece is not the colour of the current turn
							continue										#Skip it 
						
						clickedPiece.clicked()										#Select this piece
						if clickedPiece.piece.getPieceType() != "Empty":					#If piece is not empty
							possibleMoveLocations = clickedPiece.piece.getPossibleMoveLocations(game)	#Find possible move locations
							
							if game.getKing(game.getTurn()).isPieceInCheck():	#If the same coloured king is in check we can only move pieces that would prevent this
								pieceRank, pieceFile = clickedPiece.piece.getBoardCoords()			#Saves a copy of the clicked piece's locationfor later reference
								for moveLocation in possibleMoveLocations:						#Repeats through all possible move locations
									takenPiece = game.getPieceAtLocation(moveLocation[0], moveLocation[1])
									#Fake move, where the piece is moved, the program checks if the king piece is in check, then highlights the move if not
									game.setPieceAtLocation(clickedPiece.piece.getRank(), clickedPiece.piece.getFile(), Piece("Empty", None, clickedPiece.piece.getRank(), clickedPiece.piece.getFile))						
									game.setPieceAtLocation(moveLocation[0], moveLocation[1], clickedPiece.piece)																	
									clickedPiece.piece.setBoardCoords(moveLocation[0], moveLocation[1])
									
									if not game.getKing(game.getTurn()).isPieceInCheck():
										displayPieceList[moveLocation[0]][moveLocation[1]].highlight()
										
									#Resets the moved piece and its attributes, hence the name 'fake' move
									game.setPieceAtLocation(pieceRank, pieceFile, clickedPiece.piece)
									clickedPiece.piece.setBoardCoords(pieceRank, pieceFile)
									game.setPieceAtLocation(moveLocation[0], moveLocation[1], takenPiece)
									
							else:	#If the same coloured king is not in check we can highlight all possible moves
								for moveLocation in possibleMoveLocations:
									displayPieceList[moveLocation[0]][moveLocation[1]].highlight()
									
					else:		#If a piece is already selected
						firstClickedPiece = returnSelected(displayPieceList)
						secondClickedPiece = clickedPiece
						
						if firstClickedPiece == secondClickedPiece or not secondClickedPiece.isHighlighted():
							deselectAll(displayPieceList)
							unhighlightAll(displayPieceList)
						
						else:
							
							firstRank = firstClickedPiece.piece.getRank()
							firstFile = firstClickedPiece.piece.getFile()
							
							secondRank = secondClickedPiece.piece.getRank()
							secondFile = secondClickedPiece.piece.getFile()
	
							game.move(firstClickedPiece.piece, secondClickedPiece.piece)
												
							notation = f"{game.getNumMoves()}. {game.getNotation(displayPieceList[firstRank][firstFile].piece, displayPieceList[secondRank][secondFile].piece)}"
							
							#Stores the algebraic notation in its respective array
							if firstClickedPiece.getPieceColour() == "White":
								whiteNotation.append(notation)
							else:
								blackNotation.append(notation)
							
							displayPieceList[firstRank][firstFile] = DisplayPiece(firstRank*50, firstFile*50,  game.getPieceAtLocation(firstRank, firstFile))
							displayPieceList[secondRank][secondFile] = DisplayPiece(secondRank*50, secondFile*50,  game.getPieceAtLocation(secondRank, secondFile))
							
							
							deselectAll(displayPieceList)
							unhighlightAll(displayPieceList)
							
							oppositionColour = "White" if game.getTurn() == "Black" else "Black"
							if game.getKing(game.getTurn()).isPieceInCheckmate(game):
								print(f"{oppositionColour} wins the game by checkmate!")
								running = False
							
							
			elif event.type == pygame.QUIT:
				running = False
		
		screen.fill((255, 255, 255))
		for rowOfPieces in displayPieceList:
			for piece in rowOfPieces:
				screen.blit(piece.image,piece.rect)
				
		pygame.display.update()

beginOfflineBot()		
pygame.quit()



