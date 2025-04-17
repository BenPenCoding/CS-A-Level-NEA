#Libraries

#Classes
class Game():	#A class that represents a chess game with attributes that will be saved if the user decided to continue a game at a later time, and also contains data about the board itself
        def __init__(self,name):	#Constructor for the Game class. Declares the:
            self.board = [[],[],[],[],[],[],[],[]]		#array that will contain Piece objects 
            self.blackPieces = []
            self.whitePieces = []
            self.name = name
            self.numMoves = 0
            
        def initializeBoard(self):
            
                for i in range(8): #These nested for loops make every square on the board an empty square. Like a base template
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
                
                for i in range(8): 		#This for loop creates all the black Pawn objects and adds them to the blackPieces array
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
                    self.blackPieces.append(self.board[0][i])
                
                for i in range(8):		#This for loop creates all the white Pawn objects and adds them to the white Pieces array
                    self.board[6][i] = Pawn("Pawn", "White", 6, i)
                    self.whitePieces.append(self.board[7][i])
                
        def getPieceAtLocation(self, rank, column):	#A function that returns the Piece object at a given rank and column of the board
            return self.board[rank][column]
		
        def setPieceAtLocation(self, rank, column, piece):
             self.board[rank][column] = piece

        def getNotation(startPiece, endPiece):

            pieceTypeDict = {	"Knight":"N",				#The dictionary that the program uses to determine the algebraic notation of a piece type
            "Queen": "Q",				#
            "King": "K",				#
            "Bishop": "B",				#
            "Pawn":"",				#
            "Empty":"",				#
            "Rook":"R"}				#

            locationTypeDict =  {0: 'a',					#The dictionary that the program uses to determine the alphabetical representation of a coordinate
            1: 'b',
            2: 'c',
            3: 'd',
            4: 'e',
            5: 'f',
            6: 'g',
            7: 'h'}

            #Checks if the opposite king is in check following this move
            check = ""			#With algebraic move notation, if the oppositions king is in check, a '+' is added to the end. Assuming it's not in check, check is set to nothing
            colour = "White" if startPiece.getPieceColour() == "Black" else white
            piecesToCheck = game.getPieces(colour)
            for i in piecesToCheck:
                if i.getPieceType() == "King" and i.isPieceInCheck():
                    check = "+"	#If the oppositions king is in check, add a '+' to the end.

            #Checks if the taken piece is empty
            taking = ""		#With algebraic move notation, if the move takes another piece, an 'x' is added to the end. Assuming it's not, taking is set to nothing
            if endPiece.getPieceType() != "Empty":		#If not moving to an empty square
                taking = "x"				#Set taking to 'x'

            return pieceTypeDict[startPiece] + taking + locationTypeDict[endPiece.getFile()] + str(8-endPiece.getRank()) + check

		
				
	
	
        def Move(self, startRank, startColumn, endRank, endColumn):
            
            
                                
            startPiece = self.getPieceAtLocation(startRank, startColumn)
            endPiece = self.getPieceAtLocation(endRank, endColumn)
            
            self.setPieceAtLocation(startRank, startColumn, Piece("Empty",None, startRank, startColumn))	#Make the square that the piece is moving from empty
            
            if endPiece.getPieceColour() == "White":	#If taken piece colour is white, remove it from the list of white pieces
                self.whitePieces.remove(endPiece)
            else:
                self.blackPieces.remove(endPiece)		#If taken piece colour is black, remove it from the list of black pieces
            
            self.setPieceAtLocation(endRank, endColumn, startPiece)		#Sets the taken square to the taking piece
            startPiece.setBoardCoords(endRank, endColumn)
            #notation = f" {self.numMoves}. {self.getNotation(startPiece, endPiece)}" 		#Returns the algebraic notation of the move 
            
            self.numMoves += 1
            
            
	#TESTING - REMOVE BEFORE SUBMISSION
        def displayBoard(self):
            for i in self.board:
                array = []
                for j in i:
                    array.append(j.getPieceType())
                print(array)
	#TESTING - REMOVE BEFORE SUBMISSION
        
        def getPieces(self, colour):
            if colour == "Black":
                return self.blackPieces 
            else:
                return self.whitePieces
	
class Piece():		#A class that represents a chess piece with attributes such as piece type and piece location on the board
	def __init__(self, pieceType, pieceColour, rank, column):	#Constructor for the Piece class. Declares the:  
		self.pieceType = pieceType              #type of piece (pawn, rook, etc)
		self.pieceColour = pieceColour
		self.timesMoved = 0
		self.rank = rank                        #rank (row) in the board
		self.column = column                 	#column in the board

	#Functions
	def getPossibleMoveLocations(self):	#An empty function that will be overridden in the piece subclasses, returns all locations that a piece can move to
		None
	
	#Setters
	def setRank(self, rank):	#'Setter' for the rank attribute, called when a piece is instantiated or moved
		self.rank = rank

	def setColumn(self, column):	#'Setter' for the column attribute, called when a piece is instantiated or moved
		self.column = column

	def setBoardCoords(self, rank, column):	     #Subroutine that abstracts the individual 'setter' subroutines for board position from the user for simplicity
		self.setRank(rank)
		self.setColumn(column)
		
	def setPieceType(self, pieceType):	#'Setter' for the pieceType attribute, called when a piece is instantiated or a pawn reaches the other side of the board and can change into another piece
		self.pieceType = pieceType

	def setPieceColour(Self, pieceColour):	#'Setter' for the pieceColour attribute, called when a piece is instantiated 
		self.pieceColour = pieceColour

	def increaseTimesMoved(self):
		self.timesMoved += 1
	
	#Getters
	def getRank(self):	#'Getter' for the rank attribute, returns said attribute when called
		return self.rank
	
	def getColumn(self):	#'Getter' for the column attribute, returns said attribute when called
		return self.column

	def getBoardCoords(self):	#Subroutine that abstracts the individual 'getter' subroutines for board position from the user for simplicity
		return self.getRank(), self.getColumn()

	def getPieceType(self): 	#'Getter' for the pieceType attribute, returns said attribute when called
		return self.pieceType

	def getPieceColour(self):	#'Getter' for the pieceColour attribute, returns said attribute when called
		return self.pieceColour

	def getTimesMoved(self):
		return self.timesMoved
	
	#Checkers
	def isPieceEmpty(self):		#'Checker' which returns the bool True if the value of the attribute pieceType is "Empty", meaning that the location that piece takes up is free for another piece to move to
		return True if self.pieceType == "Empty" else False
			

	def isPieceInCheck(self):	#An empty function that will be overridden in the King subclass
		None
		
class Rook(Piece): 			#A class that represents the rook chess piece, which inherits from the Piece class
	def __init__(self,pieceType, pieceColour, rank, column):		#The constructor for the Rook class
		super().__init__(pieceType, pieceColour, rank, column)	#Calls the super constructor from the parent class (Piece class)
	
	def getPossibleMoveLocations(self):		#A function that returns all locations that a piece can move to
		possibleMoveLocations = []		#Declaring the array to add possible move locations to
		pieceRank, pieceColumn = self.getBoardCoords()	#Gets the rank and column of the piece to move by using the getBoardCoords function 
		
		rankIncrement, columnIncrement = 0, 0  	#Declares two variables which will be used to change the direction of the board search by switching between -1 and 1 to reverse direction.
		
		for i in range(4):		#The four cardinal directions

			tempRank, tempColumn = pieceRank, pieceColumn	#Initializes two variables that are set to the location of the piece to move
			
			while True:		#A while loop so that all possible move locations in a row are found 
				match i:	#Python's equivalent of a switch/case statement
					case 0:		#If the increment variable has a value of 0, test all possible move locations to the right of the piece
						rankIncrement, columnIncrement = 1, 0
					case 1:		#If the increment variable has a value of 1, test all possible move locations above the piece
						rankIncrement, columnIncrement = 0, -1
					case 2:		#If the increment variable has a value of 2, test all possible move locations to the left of the piece
						rankIncrement, columnIncrement = -1, 0
					case 3:		#If the increment variable has a value of 3, test all possible move locations below the piece
						rankIncrement, columnIncrement = 0, 1
					case _:		#DEBUG - If the increment variable has a value not inside 0 <= i <= 3 then print the nature of the error
						print("Fatal error, Rook class switch/case statement experienced a larger increment value than expected.")
						sleep(5)	#DEBUG - Pauses the program for five seconds to allow the tester to interpret the error message 
						quit()		#DEBUG - Quits the program entirely

				tempRank += rankIncrement		#Increments the rank of the next piece to search by the designated direction-dependent increment
				tempColumn += columnIncrement		#Increments the column of the next piece to search by the designated direction-dependent increment
				
				if (tempRank > 7 or tempRank < 0) or (tempColumn > 7 or tempColumn < 0):	#Checks if the rank and column of the next piece to check are actually not on the board and therefore if a "IndexError: list index out of range" error will occur                  
					break									#If this is the case, exit the while loop and begin checking in another direction						
				
				pieceToCheck = game.getPieceAtLocation(tempRank, tempColumn)	#Gets the piece object to check 

				if pieceToCheck.isPieceEmpty():			#Checks if the piece object is empty
					possibleMoveLocations.append([tempRank, tempColumn]) 	#If it is, add the location to the list of possible move locations
					continue						#Moves on to checking the next piece
				else:
                                        if (pieceToCheck.getPieceColour() != self.getPieceColour()) and pieceToCheck.getPieceType != "King" :	#If the location contains an oppositely coloured piece which can be taken (all except the king)
                                            possibleMoveLocations.append([tempRank, tempColumn])	#Adds the location to the list of possible move locations
                                            break							#Stops checking the next piece and exits the while loop
                                        
                                        else:		#Otherwise the piece to check is the same colour as the piece to move, or it's the opposition's king piece (which can't be taken)
                                            break	#Stops checking the next piece and exits the while loop

		return possibleMoveLocations	#Returns the list of possible move locations to wherever the function was called 


class Bishop(Piece):			#A class that represents the bishop chess piece, which inherits from the Piece class
	def __init__(self,pieceType, pieceColour, rank, column):		#The constructor for the Bishop class
		super().__init__(pieceType, pieceColour, rank, column)	#Calls the super constructor from the parent class (Piece class)

	def getPossibleMoveLocations(self):
		possibleMoveLocations = []		#Declaring the array to add possible move locations to
		pieceRank, pieceColumn = self.getBoardCoords()	#Gets the rank and column of the piece to move by using the getBoardCoords function 

		rankIncrement, columnIncrement = 0, 0  	#Declares two variables which will be used to change the direction of the board search by switching between -1 and 1 to change direction.
		
		for i in range(4):		#The four diagonal directions

			tempRank, tempColumn = pieceRank, pieceColumn	#Initializes two variables that are set to the location of the piece to move
			
			while True:		#A while loop so that all possible move locations in a diagonal line are found 
				match i:	#Python's equivalent of a switch/case statement
					case 0:		#If the increment variable has a value of 0, test all possible move locations to the up and right of the piece
						rankIncrement, columnIncrement = -1, 1
					case 1:		#If the increment variable has a value of 1, test all possible move locations up and left of the piece
						rankIncrement, columnIncrement = -1, -1
					case 2:		#If the increment variable has a value of 2, test all possible move locations to the down and left of the piece
						rankIncrement, columnIncrement = 1, -1
					case 3:		#If the increment variable has a value of 3, test all possible move locations down and right of the piece
						rankIncrement, columnIncrement = 1, 1
					case _:		#DEBUG - If the increment variable has a value not inside 0 <= i <= 3 then print the nature of the error
						print("Fatal error, Bishop class switch/case statement experienced a larger increment value than expected.")
						sleep(5)	#DEBUG - Pauses the program for five seconds to allow the tester to interpret the error message 
						quit()		#DEBUG - Quits the program entirely

				tempRank += rankIncrement		#Increments the rank of the next piece to search by the designated direction-dependent increment
				tempColumn += columnIncrement		#Increments the column of the next piece to search by the designated direction-dependent increment
				
				if (tempRank > 7 or tempRank < 0) or (tempColumn > 7 or tempColumn < 0):	#Checks if the rank and column of the next piece to check are actually not on the board and therefore if a "IndexError: list index out of range" error will occur                  
					break									#If this is the case, exit the while loop and begin checking in another direction							

				pieceToCheck = game.getPieceAtLocation(tempRank, tempColumn)	#Gets the piece object to check 
				
				if pieceToCheck.isPieceEmpty():			#Checks if the piece object is empty
					possibleMoveLocations.append([tempRank, tempColumn]) 	#If it is, add the location to the list of possible move locations
					continue
				else:	
                                        if pieceToCheck.getPieceColour() != self.getPieceColour() and pieceToCheck.getPieceType() != "King" :	#If the location contains an oppositely coloured piece which can be taken (all except the king)
                                            possibleMoveLocations.append([tempRank, tempColumn])		#Adds the location to the list of possible move locations
                                            break
                                        
                                        else:		#Otherwise the piece to check is the same colour as the piece to move, or it's the opposition's king piece (which can't be taken)
                                            break	#Exits the while loop
		
		return possibleMoveLocations	#Returns the list of possible move locations to wherever the function was called 

class Knight(Piece):			#A class that represents the knight chess piece, which inherits from the Piece class
	def __init__(self,pieceType, pieceColour, rank, column):		#The constructor for the Knight class
		super().__init__(pieceType, pieceColour, rank, column)	#Calls the super constructor from the parent class (Piece class)

	def getPossibleMoveLocations(self):
		possibleMoveLocations = []		#Declaring the array to add possible move locations to
		pieceRank, pieceColumn = self.getBoardCoords()	#Gets the rank and column of the piece to move by using the getBoardCoords function 
		possibleIncrementList = [[-2, 1], [-2, -1], [-1, 2], [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2]]	#Although not obvious, this list contains the increments that must be added to a knight's current location to check the squares it could possibly move to
		
		for coordinates in possibleIncrementList:

			tempRank, tempColumn = pieceRank +coordinates[0], pieceColumn + coordinates[1]	#Declaring and initializing two variables that store the location of the piece to check, they're instantiated as the current increment values added to the knight's position 

			if (tempRank < 0 or tempRank > 7) or (tempColumn < 0 or tempColumn > 7): 	#Checks if the rank and column of the next piece to check are actually not on the board and therefore if a "IndexError: list index out of range" error will occur
				continue
				
			pieceToCheck = game.getPieceAtLocation(tempRank, tempColumn)

			if pieceToCheck.isPieceEmpty():			#Checks if the piece object is empty
				possibleMoveLocations.append([tempRank, tempColumn]) 	#If it is, add the location to the list of possible move locations
				continue		#Skips the rest of the for loop as we have found the state of the piece and returns to the top of the loop
			else:	
                                    if (pieceToCheck.getPieceColour() != self.getPieceColour()) and pieceToCheck.getPieceType != "King":	#If the location contains an oppositely coloured piece which can be taken (all except the king)
                                        possibleMoveLocations.append([tempRank, tempColumn])		#Adds the location to the list of possible move locations
                                        continue		#Skips the rest of the for loop as we have found the state of the piece and returns to the top of the loop
                            
                                    else:		#Otherwise the piece to check is the same colour as the piece to move, or it's the opposition's king piece (which can't be taken)
                                        pass	#Nothing happens here, the program returns to the for loop		
		
		return possibleMoveLocations	#Returns the list of possible move locations to wherever the function was called 
		


class Queen(Piece):			#A class that represents the queen chess piece, which inherits from the Piece class
	def __init__(self,pieceType, pieceColour, rank, column):		#The constructor for the Queen class
		super().__init__(pieceType, pieceColour, rank, column)	#Calls the super constructor from the parent class (Piece class)

	def getPossibleMoveLocations(self):
		possibleMoveLocations = []		#Declaring the array to add possible move locations to
		pieceRank, pieceColumn = self.getBoardCoords()	#Gets the rank and column of the piece to move by using the getBoardCoords function 
		rankIncrement, columnIncrement = 0, 0  	#Declares two variables which will be used to change the direction of the board search by switching between -1 and 1 to reverse direction.

		#The queen piece can move like a rook and a bishop at the same time, to check for possible move locations I used the same code from both the Bishop class and the Rook class
		#The code from the Rook class:
		for i in range(4):		#The four cardinal directions

			tempRank, tempColumn = pieceRank, pieceColumn	#Initializes two variables that are set to the location of the piece to move
			
			while True:		#A while loop so that all possible move locations in a row are found 
				match i:	#Python's equivalent of a switch/case statement
					case 0:		#If the increment variable has a value of 0, test all possible move locations to the right of the piece
						rankIncrement, columnIncrement = 1, 0
					case 1:		#If the increment variable has a value of 1, test all possible move locations above the piece
						rankIncrement, columnIncrement = 0, -1
					case 2:		#If the increment variable has a value of 2, test all possible move locations to the left of the piece
						rankIncrement, columnIncrement = -1, 0
					case 3:		#If the increment variable has a value of 3, test all possible move locations below the piece
						rankIncrement, columnIncrement = 0, 1
					case _:		#DEBUG - If the increment variable has a value not inside 0 <= i <= 3 then print the nature of the error
						print("Fatal error, Rook class switch/case statement experienced a larger increment value than expected.")
						sleep(5)	#DEBUG - Pauses the program for five seconds to allow the tester to interpret the error message 
						quit()		#DEBUG - Quits the program entirely

												#If this is the case, exit the while loop and begin checking in another direction						
				tempRank += rankIncrement		#Increments the rank of the next piece to search by the designated direction-dependent increment
				tempColumn += columnIncrement		#Increments the column of the next piece to search by the designated direction-dependent increment
				
				if (tempRank > 7 or tempRank < 0) or (tempColumn > 7 or tempColumn < 0):	#Checks if the rank and column of the next piece to check are actually not on the board and therefore if a "IndexError: list index out of range" error will occur                  
					break	
				
				pieceToCheck = game.getPieceAtLocation(tempRank, tempColumn)	#Gets the piece object to check 

				if pieceToCheck.isPieceEmpty():			#Checks if the piece object is empty
					possibleMoveLocations.append([tempRank, tempColumn]) 	#If it is, add the location to the list of possible move locations
					continue						#Moves on to checking the next piece
				else:
                                        if (pieceToCheck.getPieceColour() != self.getPieceColour()) and pieceToCheck.getPieceType != "King":	#If the location contains an oppositely coloured piece which can be taken (all except the king)
                                            possibleMoveLocations.append([tempRank, tempColumn])	#Adds the location to the list of possible move locations
                                            break							#Stops checking the next piece and exits the while loop
                                        
                                        else:		#Otherwise the piece to check is the same colour as the piece to move, or it's the opposition's king piece (which can't be taken)
                                            break	#Stops checking the next piece and exits the while loop

		#The code from the Bishop class:
		for i in range(4):		#The four diagonal directions

			tempRank, tempColumn = pieceRank, pieceColumn	#Initializes two variables that are set to the location of the piece to move
			
			while True:		#A while loop so that all possible move locations in a diagonal line are found 
				match i:	#Python's equivalent of a switch/case statement
					case 0:		#If the increment variable has a value of 0, test all possible move locations to the up and right of the piece
						rankIncrement, columnIncrement = -1, 1
					case 1:		#If the increment variable has a value of 1, test all possible move locations up and left of the piece
						rankIncrement, columnIncrement = -1, -1
					case 2:		#If the increment variable has a value of 2, test all possible move locations to the down and left of the piece
						rankIncrement, columnIncrement = 1, -1
					case 3:		#If the increment variable has a value of 3, test all possible move locations down and right of the piece
						rankIncrement, columnIncrement = 1, 1
					case _:		#DEBUG - If the increment variable has a value not inside 0 <= i <= 3 then print the nature of the error
						print("Fatal error, Bishop class switch/case statement experienced a larger increment value than expected.")
						sleep(5)	#DEBUG - Pauses the program for five seconds to allow the tester to interpret the error message 
						quit()		#DEBUG - Quits the program entirely

				tempRank += rankIncrement		#Increments the rank of the next piece to search by the designated direction-dependent increment
				tempColumn += columnIncrement		#Increments the column of the next piece to search by the designated direction-dependent increment
				
				if (tempRank > 7 or tempRank < 0) or (tempColumn > 7 or tempColumn < 0):	#Checks if the rank and column of the next piece to check are actually not on the board and therefore if a "IndexError: list index out of range" error will occur                  
					break									#If this is the case, exit the while loop and begin checking in another direction							
				
				pieceToCheck = game.getPieceAtLocation(tempRank, tempColumn)	#Gets the piece object to check 
				
				if pieceToCheck.isPieceEmpty():			#Checks if the piece object is empty
					possibleMoveLocations.append([tempRank, tempColumn]) 	#If it is, add the location to the list of possible move locations
					continue
				else:
                                        if (pieceToCheck.getPieceColour() != self.getPieceColour()) and pieceToCheck.getPieceType != "King":	#If the location contains an oppositely coloured piece which can be taken (all except the king)
                                            possibleMoveLocations.append([tempRank, tempColumn])		#Adds the location to the list of possible move locations
                                            break
                                        
                                        else:		#Otherwise the piece to check is the same colour as the piece to move, or it's the opposition's king piece (which can't be taken)
                                            break	#Exits the while loop
		
		return possibleMoveLocations	#Returns the list of possible move locations to wherever the function was called 
	


class Pawn(Piece):			#A class that represents the pawn chess piece, which inherits from the Piece class
	def __init__(self,pieceType, pieceColour, rank, column):		#The constructor for the Pawn class
		super().__init__(pieceType, pieceColour, rank, column)	#Calls the super constructor from the parent class (Piece class)

	def getPossibleMoveLocations(self):
		possibleMoveLocations = []		#Declaring the array to add possible move locations to
		pieceRank, pieceColumn = self.getBoardCoords()	#Gets the rank and column of the piece to move by using the getBoardCoords function 

		if piece.colour == "white":	#This if statement initializes an inrement variable, i, which will alter the direction of the pawns movement depending on its colour
			i = 1
		else:
			i= -1
		
		tempRank, tempColumn = pieceRank + (-1 * i), pieceColumn + 0

		if (game.getPieceAtLocation(tempRank, tempColumn).getPieceType())== "Empty":
			possibleMoveLocations.append([tempRank, tempColumn])

		tempRank, tempColumn = pieceRank + (-1 * i), pieceColumn + 1
		
		if (game.getPieceAtLocation(tempRank, tempColumn).getColour() != self.getColour()) and (game.getPieceAtLocation(tempRank, tempColumn).getPieceType() != "King") and (game.getPieceAtLocation(tempRank, tempColumn).getPieceType() != "Empty"):
			possibleMoveLocations.append([tempRank, tempColumn])
		
		tempRank, tempColumn = pieceRank + (-1 * i), pieceColumn + -1

		if (game.getPieceAtLocation(tempRank, tempColumn).getColour() != self.getColour()) and (game.getPieceAtLocation(tempRank, tempColumn).getPieceType() != "King") and (game.getPieceAtLocation(tempRank, tempColumn).getPieceType() != "Empty"):
			possibleMoveLocations.append([tempRank, tempColumn])
			
		#ADD EN PASSANT CASE


class King(Piece):			#A class that represents the king chess piece, which inherits from the Piece class
	def __init__(self,pieceType, pieceColour, rank, column):		#The constructor for the King class
		super().__init__(pieceType, pieceColour, rank, column)	#Calls the super constructor from the parent class (Piece class)

	def getPossibleMoveLocations(self):

		possibleMoveLocations = []		#Declaring the array to add possible move locations to
		pieceRank, pieceColumn = self.getBoardCoords()	#Gets the rank and column of the piece to move by using the getBoardCoords function 
		possibleIncrementList = [[-1, -1],[-1, 0],[-1, 1], [0,-1],[0, 1],[1, -1],[1, 0],[1, 1]]	#This list contains the increments that must be added to a king's current location to check the squares it could possibly move to
		
		for coordinates in possibleIncrementList:

			tempRank, tempColumn = pieceRank +coordinates[0], pieceColumn + coordinates[1]	#Declaring and initializing two variables that store the location of the piece to check, they're instantiated as the current increment values added to the knight's position 

			if (tempRank < 0 or tempRank > 7) or (tempColumn < 0 or tempColumn > 7):	#Checks if the rank and column of the next piece to check are actually not on the board and therefore if a "IndexError: list index out of range" error will occur
				continue
				
			pieceToCheck = 	game.getPieceAtLocation(tempRank, tempColumn)

			if pieceToCheck.isPieceEmpty():			#Checks if the piece object is empty
				possibleMoveLocations.append([tempRank, tempColumn]) 	#If it is, add the location to the list of possible move locations
				continue		#Skips the rest of the for loop as we have found the state of the piece and returns to the top of the loop
					
			elif (pieceToCheck.getPieceColour() != self.getPieceColour()) and pieceToCheck.getPieceType != "King":	#If the location contains an oppositely coloured piece which can be taken (all except the king)
				possibleMoveLocations.append([tempRank, tempColumn])		#Adds the location to the list of possible move locations
				continue		#Skips the rest of the for loop as we have found the state of the piece and returns to the top of the loop
				
			else:		#Otherwise the piece to check is the same colour as the piece to move, or it's the opposition's king piece (which can't be taken)
				pass	#Nothing happens here, the program returns to the for loop		
		
		return possibleMoveLocations	#Returns the list of possible move locations to wherever the function was called 
		
		

	def isPieceInCheck(self):	#Function to check if the King object is in check
		pieceRank, pieceColumn = self.getBoardCoords()		#Initializes two variables which will be used to store the rank and column of the King piece
		colour = "Black" if self.getPieceColour() == "White" else "White"
		for i in game.getPieces(colour):
			pieceToCheck = i
			possibleMoveLocations = pieceToCheck.getPossibleMoveLocations()					#Then get all possible moves of said piece
			if [pieceRank, pieceColumn] in possibleMoveLocations:						#If the King piece's rank and column are present in the list of the other piece's possible moves:
				return True										#Then return true, the King piece is in check
		return False	#If the program reaches here then the King piece is not in check and so return false

	#def isPieceInCheckmate(self):
		#NEED SINGLE CHECKMATE AND DOUBLE CHECKMATE CASES


game = Game("Test")
game.initializeBoard()
