class Piece:

    def __init__(self, name, value, color):
        self.name = name
        self.value = value
        self.color = color

class King(Piece):

    def __init__(self, color):
        self.name = 'king'
        self.value = 0
        self.color = color

class Queen(Piece):

    def __init__(self, color):
        self.name = 'queen'
        self.value = 9
        self.color = color

class Rook(Piece):

    def __init__(self, color):
        self.name = 'rook'
        self.value = 5
        self.color = color

class Bishop(Piece):

    def __init__(self, color):
        self.name = 'bishop'
        self.value = 3
        self.color = color

class Knight(Piece):

    def __init__(self, color):
        self.name = 'knight'
        self.value = 3
        self.color = color

class Pawn(Piece):

    def __init__(self, color):
        self.name = 'pawn'
        self.value = 1
        self.color = color

def spilt_squarename(squareName):
    col = ord(squareName[0])-96
    return (col, int(squareName[1]))

def make_squarename(col, row):
    squareChar = chr(96+col)
    return squareChar+str(row)

class Game:
    #Generates class objects
    #places pieces on board in starting position
    #Generates starting piece map
    def __init__(self):
        self.whitesTurn = True
        self.board = {}
        self.moves = []
        self.pieceMap = {}
        for col in range(1,9):
            for row in range(1,9):
                squareName = make_squarename(col,row)
                self.board[squareName] = 0
                #place Rooks
                if col == 1 or col == 8:
                    if row == 1:
                        self.board[squareName] = Rook('white')
                    if row == 8:
                        self.board[squareName] = Rook('black')
                #place knights
                if col == 2 or col == 7:
                    if row == 1:
                        self.board[squareName] = Knight('white')
                    if row == 8:
                        self.board[squareName] = Knight('black')
                #place bishops
                if col == 3 or col == 6:
                    if row == 1:
                        self.board[squareName] = Bishop('white')
                    if row == 8:
                        self.board[squareName] = Bishop('black')
                #place queens
                if col == 4:
                    if row == 1:
                        self.board[squareName] = Queen('white')
                    if row == 8:
                        self.board[squareName] = Queen('black')
                #place kings
                if col == 5:
                    if row == 1:
                        self.board[squareName] = King('white')
                    if row == 8:
                        self.board[squareName] = King('black')
                #place pawns
                if row == 2:
                    self.board[squareName] = Pawn('white')
                if row == 7:
                    self.board[squareName] = Pawn('black')
        self.generate_piece_map()

    #Prints a more or less readable chess map to the console
    def print_board(self):
        for row in range(8,0,-1):
            for col in range(1,9):
                if self.board[make_squarename(col,row)] == 0:
                    print(make_squarename(col,row) + ':' + '0', end='              ')
                else:
                    pieceName = self.board[make_squarename(col,row)].color + ' ' + self.board[make_squarename(col,row)].name
                    length = len(pieceName)
                    spacesToAdd = 15 - length
                    spaceStr = ''
                    for x in range(0,spacesToAdd):
                        spaceStr += ' '
                    print(make_squarename(col,row) + ':' + pieceName, end=spaceStr)
            print('\n')

    #Piece map values:
	# 1 -> Can not move to this square, but square is protected
	# 2 -> Can move to this avaliable square
	# 3 -> Can move to this square and capture piece
	# 4 -> Can capture on this square, but not move to it (En Passant)
	# 5 -> Check (attacking odd colored king)

    #Retuns a map for a pawn
    def map_pawn(self, square):
        resultMap = {}
        piece = self.board[square]
        tuple = spilt_squarename(square)
        inverter = 1
        if self.board[square].color == 'black':
            inverter = -1
        #if from start pos. Can move two steps ahead if squares are not occupied
        if (inverter == 1 and tuple[1] == 2) or (inverter == -1 and tuple[1] == 7):
            if self.board[make_squarename(tuple[0], tuple[1]+2 * inverter)] == 0 and self.board[make_squarename(tuple[0], tuple[1]+1 * inverter)] == 0:
                resultMap[make_squarename(tuple[0], tuple[1]+2 * inverter)] = 2
        #can alway move one step ahead if square is on board and not occupied
        if 1 <= tuple[1]+1 * inverter <= 8:
            if self.board[make_squarename(tuple[0], tuple[1]+1 * inverter)] == 0:
                resultMap[make_squarename(tuple[0], tuple[1]+1 * inverter)] = 2
            #Protects or can attack sideways if square is occupied by enemy
            for j in range(1,3):
                add = j
                if add == 2:
                    add = -1
                if 1 <= tuple[0]+add <= 8 and 1 <= tuple[1]+inverter <= 8:
                    #if there is a piece sideways
                    if self.board[make_squarename(tuple[0]+add,tuple[1]+inverter)] != 0:
                        # if the piece is different colored
                        if self.board[make_squarename(tuple[0]+add,tuple[1]+inverter)].color != piece.color:
                            #if piece is a king
                            if self.board[make_squarename(tuple[0]+add,tuple[1]+inverter)].name == 'king':
                                resultMap[make_squarename(tuple[0]+add,tuple[1]+inverter)] = 5
                            else:
                                #Can capture the piece
                                resultMap[make_squarename(tuple[0]+add,tuple[1]+inverter)] = 3
                         # if there is not an enemy piece, piece is same color 
                        else:
                            resultMap[make_squarename(tuple[0]+add,tuple[1]+inverter)] = 1
                    else:
                        resultMap[make_squarename(tuple[0]+add,tuple[1]+inverter)] = 1

		#If there is an odd-colored pawn to the side that moved two steps in last move, En passant is possible
        if len(self.moves) > 1:
            for j in range(1,3):
                add = j
                if add == 2:
                    add = -1 
                if 1 <= tuple[0] + add <= 8:
                    #if there is a piece
                    if self.board[make_squarename(tuple[0] + add, tuple[1])] != 0:
                        #if its an odd colored pawn
                        if self.board[make_squarename(tuple[0] + add, tuple[1])].color != self.board[square]:
                            if self.board[make_squarename(tuple[0] + add, tuple[1])].name == 'pawn':
                                lastMove = self.moves[-1]
                                #if the last move was to this square
                                if lastMove[1] == make_squarename(tuple[0] + add, tuple[1]):
                                    steps = abs(spilt_squarename(lastMove[0])[1] - spilt_squarename(lastMove[1])[1])
                                    if steps == 2:
                                        resultMap[make_squarename(tuple[0] + add, tuple[1]+inverter)] = 2
                                        resultMap[make_squarename(tuple[0] + add, tuple[1])] = 4
        return resultMap
    #Retuns a map for a knight
    def map_knight(self, square):
        resultMap = {}
        piece = self.board[square]
        tuple = spilt_squarename(square)
        #can either move 1 horisontal and 2 vertical or 2 horisontal and 1 vertical
        #max four possible moves
        for j in range(1, 3):
            if j == 1:
                addCol = 1
                addRow = 2
            elif j == 2:
                addCol = 2
                addRow = 1
            for i in range(1,5):
                if i == 2:
                    addCol = -addCol
                elif i == 3:
                    addCol = abs(addCol)
                    addRow = -addRow
                elif i == 4:
                    addRow = -abs(addRow)
                    addCol = -abs(addCol)
                #if square is on board
                if 1 <= tuple[0] + addCol <= 8 and 1 <= tuple[1] + addRow <= 8:
                    squareToCheck = make_squarename(tuple[0] + addCol, tuple[1] + addRow)
                    #if square is free
                    if self.board[squareToCheck] == 0:
                        resultMap[squareToCheck] = 2
                    #if same colored piece in square
                    elif self.board[squareToCheck].color == piece.color:
                        resultMap[squareToCheck] = 1
                    #if king in sqauare (odd colored)
                    elif  self.board[squareToCheck].name == 'king':
                        resultMap[squareToCheck] = 5
                    #else there has to be odd colored piece (can capture)
                    else:
                        resultMap[squareToCheck] = 3
        return resultMap
    #Retuns a map for a bishop
    def map_bishop(self, square):
        return self.diagonal_mapping(square)
    #Retuns a map for a diagonal moving piece
    def diagonal_mapping(self, square):
        resultMap = {}
        piece = self.board[square]
        tuple = spilt_squarename(square)
        #check 4 axis
        for i in range(1,5):
            if i == 1:
                colInverter = 1
                rowInverter = 1
                steps = 8-tuple[0]
                if 8-tuple[1] < steps:
                    steps = 8-tuple[1]
            elif i == 2:
                colInverter = -1
                rowInverter = 1
                steps = tuple[0]-1
                if 8-tuple[1] < steps:
                    steps = 8-tuple[1]
            elif i == 3:
                colInverter = 1
                rowInverter = -1
                steps = 8-tuple[0]
                if tuple[1]-1 < steps:
                    steps = tuple[1]-1
            elif i == 4:
                colInverter = -1
                rowInverter = -1
                steps = tuple[0]-1
                if tuple[1]-1 < steps:
                    steps = tuple[1]-1

            #search along axis until we hit something
            for step in range(1, steps+1):
                squareToCheck = make_squarename(tuple[0]+step*colInverter, tuple[1]+step*rowInverter)
                # if square is free
                if self.board[squareToCheck] == 0:
                    resultMap[squareToCheck] = 2
                #if same colored piece
                elif self.board[squareToCheck].color == piece.color:
                    resultMap[squareToCheck] = 1
                    break
                #if king (has to be odd colored)
                elif self.board[squareToCheck].name == 'king':
                    resultMap[squareToCheck] = 5
                    break
                #has to be odd colored piece (not king)
                else:
                    resultMap[squareToCheck] = 3
                    break
        return resultMap
    #Retuns a map for a rook
    def map_rook(self, square):
        return self.linear_mapping(square)
    #Retuns a map for a linear moving piece
    def linear_mapping(self, square):
        resultMap = {}
        piece = self.board[square]
        tuple = spilt_squarename(square)
        #search i 4 axis
        for i in range(1,5):
            #to the right
            if i == 1:
                colInverter = 1
                rowInverter = 0
                steps = 8-tuple[0]
            #to the left
            elif i == 2:
                colInverter = -1
                rowInverter = 0
                steps = tuple[0]-1
            #up
            elif i == 3:
                colInverter = 0
                rowInverter = 1
                steps = 8-tuple[1]
            #down
            elif i == 4:
                colInverter = 0
                rowInverter = -1
                steps = tuple[1]-1

            #search along axis until we hit something
            for step in range(1, steps+1):
                squareToCheck = make_squarename(tuple[0]+step*colInverter, tuple[1]+step*rowInverter)
                # if square is free
                if self.board[squareToCheck] == 0:
                    resultMap[squareToCheck] = 2
                #if same colored piece
                elif self.board[squareToCheck].color == piece.color:
                    resultMap[squareToCheck] = 1
                    break
                #if king (has to be odd colored)
                elif self.board[squareToCheck].name == 'king':
                    resultMap[squareToCheck] = 5
                    break
                #has to be odd colored piece that can be captured
                else:
                    resultMap[squareToCheck] = 3
                    break
        return resultMap
    #Retuns a map for a queen
    def map_queen(self, square):
        combinedList = {**self.linear_mapping(square), **self.diagonal_mapping(square)}
        return combinedList
    #Returns a map for a king
    def map_king(self, square):
        resultMap = {}
        piece = self.board[square]
        tuple = spilt_squarename(square)
        for hor in range(-1,2):
            for vert in range(-1,2):
                #every possible move around king square except for king square
                if not(vert == 0 and hor == 0):
                    #if within board
                    if 1 <= tuple[0]+hor <= 8 and 1 <= tuple[1]+vert <= 8:
                        checkSquare  = make_squarename(tuple[0]+hor, tuple[1]+vert)
                        #If there is a piece
                        if self.board[checkSquare] != 0:
                            #if odd colored it can attack (attempts that leads to self check will be filtered away)
                            if self.board[checkSquare].color != piece.color:
                                #if odd colored piece is a king, mark as check (actually ilegal move, but will be filtered away)
                                if self.board[checkSquare].name == 'king':
                                    resultMap[checkSquare] = 5
                                #any other odd colored piece
                                else:
                                    resultMap[checkSquare] = 3
                            #if piece of same color
                            elif self.board[checkSquare].color == piece.color:
                                resultMap[checkSquare] = 1
                        #If square is avaliable
                        else:
                            resultMap[checkSquare] = 2
        return resultMap

    #Generates rough map for all pieces using map classes above
    #Includes moves that can potentially put itself in check
    #Does not contain castling moves
    def generate_piece_map(self):
        self.pieceMap = {}
        for square in self.board:
            if self.board[square] != 0:
                if self.board[square].name == 'pawn':
                    self.pieceMap[square] = self.map_pawn(square)
                elif self.board[square].name == 'knight':
                    self.pieceMap[square] = self.map_knight(square)
                elif self.board[square].name == 'bishop':
                    self.pieceMap[square] = self.map_bishop(square)
                elif self.board[square].name == 'rook':
                    self.pieceMap[square] = self.map_rook(square)
                elif self.board[square].name == 'queen':
                    self.pieceMap[square] = self.map_queen(square)
                elif self.board[square].name == 'king':
                    self.pieceMap[square] = self.map_king(square)

    #Removes moves where it puts itself in check
    def remove_self_checks(self):
        testGame = Game()
        inCheck = False
        removeResult = []
        lastMoveColor = self.board[self.moves[-1][1]].color
        #for every piece with same color as last move
        for square, map in self.pieceMap.items():
            if self.board[square].color != lastMoveColor:
                #For every currently legal move
                for toSquare, result in map.items():
                    if 2 <= result <= 3:
                        testGame.board = self.board.copy()
                        testGame.pieceMap = self.pieceMap.copy()
                        #do the move in the testGame
                        testGame.execute_move(square, toSquare)
                        #Generate a new PieceMap
                        testGame.generate_piece_map()
                        #now, check if the other color has check
                        for testSquare, testMap in testGame.pieceMap.items():
                            if testGame.board[testSquare].color == lastMoveColor:
                                for testToSquare, testResult in testMap.items():
                                    if testResult == 5:
                                        removeResult.append((square,toSquare))

        for tuple in list(set(removeResult)):
            del self.pieceMap[tuple[0]][tuple[1]]

    #Adds Castling moves to pieceMap
    def add_castling(self):
        if self.whitesTurn:
            kingRow = '1'
        else:
            kingRow = '8'

        kingSideCanCastle = True
        queenSideCanCastle = True
        kingHasMoved = False
        aRookHasMoved = False
        hRookHasMoved = False

        for tuples in self.moves:
            if tuples[0] == 'e' + kingRow:
                kingHasMoved = True
            if tuples[0] == 'a' + kingRow:
                aRookHasMoved = True
            if tuples[0] == 'h' + kingRow:
                hRookHasMoved = True

        #if king has moved
        if kingHasMoved:
            kingSideCanCastle = False
            queenSideCanCastle = False
        else:
            #Check if kingside castling is possible
            if hRookHasMoved:
                kingSideCanCastle = False
            #Check if f and g is free of pieces
            elif self.board['f' + kingRow] != 0 or self.board['g' + kingRow] != 0:
                kingSideCanCastle = False
            else:
                #check if e, f or g exists in piecemap for the opposite pieces
                for fromSquare, toSquareMap in self.pieceMap.items():
                    if self.board[fromSquare].color != self.board['e'+kingRow].color:
                        for toSquare, result in toSquareMap.items():
                            if toSquare == 'e' + kingRow or toSquare == 'f' + kingRow or toSquare == 'g' + kingRow:
                                kingSideCanCastle = False
                                break
            #Check if queenside castling is possible
            if aRookHasMoved:
                queenSideCanCastle = False
            #Check if b, c and d is free of pieces
            elif self.board['b' + kingRow] != 0 or self.board['c' + kingRow] != 0 or self.board['d' + kingRow] != 0:
                queenSideCanCastle = False
            else:
                #check if c, d or e exists in piecemap for the black pieces
                for fromSquare, toSquareMap in self.pieceMap.items():
                    if self.board[fromSquare].color != self.board['e'+kingRow].color:
                        for toSquare, result in toSquareMap.items():
                            if toSquare == 'c' + kingRow or toSquare == 'd' + kingRow or toSquare == 'e' + kingRow:
                                queenSideCanCastle = False
                                break
        if kingSideCanCastle:
            self.pieceMap['e' + kingRow]['g' + kingRow] = 2
        if queenSideCanCastle:
            self.pieceMap['e' + kingRow]['c' + kingRow] = 2
    
    #Generates the final piece map
    def mapPieces(self):
        self.generate_piece_map()
        self.remove_self_checks()
        self.add_castling()

    #Checks if the current position is a checkmate or stalemate
    def check_for_mate(self, justMovedColor):
        inCheck = False
        for square, map in self.pieceMap.items():
            if self.board[square].color != justMovedColor:
                for toSquare, result in map.items():
                    if 2 <= result <= 3:
                        return False
            else:
                for toSquare, result in map.items():
                    if result == 5:
                        inCheck = True
                        break
        if inCheck:
            return "Checkmate"
        else:
            return "Stalemate"

    #Executes the moves on the board. The the moves has to be prechecked for legality
    def execute_move(self, fromSquare, toSquare):
        #Execute move
        currentPieceMap = self.pieceMap[fromSquare]
        piece = self.board[fromSquare]
        capture = False
        #If move to empty square. Can be regular move, castling or En Passant
        if currentPieceMap[toSquare] == 2:
            #Check if the move is En Passant (if pawn move sideways(we know target square is empty)(and there can only be one En Passant)
            if piece.name == 'pawn' and spilt_squarename(fromSquare)[0] != spilt_squarename(toSquare)[0]:
                for square, result in currentPieceMap.items():
                    if result == 4:
                        capturedPawnSquare = square
                capturedPiece = self.board[capturedPawnSquare]
                self.board[capturedPawnSquare] = 0
                self.board[toSquare] = self.board[fromSquare]
                self.board[fromSquare] = 0
                capture = True
            #Check if the move is castling. If the king moves more than one column
            elif piece.name == 'king' and abs(spilt_squarename(fromSquare)[0] - spilt_squarename(toSquare)[0]) > 1:
                #If queenside castling
                if toSquare[0] == 'c':
                    self.board[toSquare] = self.board[fromSquare]
                    self.board[fromSquare] = 0
                    self.board['d' + fromSquare[1]] = self.board['a' + fromSquare[1]]
                    self.board['a' + fromSquare[1]] = 0
                #Has to be kingside castling
                else:
                    self.board[toSquare] = self.board[fromSquare]
                    self.board[fromSquare] = 0
                    self.board['f' + fromSquare[1]] = self.board['h' + fromSquare[1]]
                    self.board['h' + fromSquare[1]] = 0
            #If not castling or En Passant, its a regular move
            else:
                self.board[toSquare] = self.board[fromSquare]
                self.board[fromSquare] = 0
        #If move is legal with capture
        elif currentPieceMap[toSquare] == 3:
            capturedPiece = self.board[toSquare]
            self.board[toSquare] = self.board[fromSquare]
            self.board[fromSquare] = 0
            capture = True

        if capture:
            return capturedPiece
        else:
           return False

    #Main method for playing games. 
    #Checks the move and executes if legal.
    #Promotes pawns
    #Returns human language strings
    def move(self, fromSquare, toSquare):
        #If there is not a piece in fromSquare
        if self.board[fromSquare] == 0:
            return 'No piece in that square to move'
        #If the squares are the same
        if fromSquare == toSquare:
            return "The piece has to be moved"

        piece = self.board[fromSquare]
        #Check if piece is wrong color
        if (piece.color == 'white' and not(self.whitesTurn)) or (piece.color == 'black' and self.whitesTurn):
            return "Wrong colored piece to move"

        #Get the current piece map
        currentPieceMap = self.pieceMap[fromSquare]
        legal = False
        #Check if toSquare exists in the current piece map
        for square, result in currentPieceMap.items():
            if square == toSquare and 2<= result <= 3:
                legal = True
                break
        #If move is not legal
        if not(legal):
            return 'move is not legal'
        
        #Execute the move
        executeResult = self.execute_move(fromSquare, toSquare)

        #Promote pawn
        if piece.name == 'pawn' and (toSquare[1] == '1' or toSquare[1] == '8'):
            promotionNotSelected = True
            while promotionNotSelected:
                promoteNum = input('Choose piece to promote pawn. \n 1: Queen \n 2: Rook \n 3: Knight \n 4: Bishop \n Enter number:')
                if promoteNum == '1':
                    self.board[toSquare] = Queen(piece.color)
                    promotionNotSelected = False
                elif promoteNum == '2':
                    self.board[toSquare] = Rook(piece.color)
                    promotionNotSelected = False
                elif promoteNum == '3':
                    self.board[toSquare] = Knight(piece.color)
                    promotionNotSelected = False
                elif promoteNum == '4':
                    self.board[toSquare] = Bishop(piece.color)
                    promotionNotSelected = False

        if not(executeResult):
            capture = False
        else:
            capture = True
            capturedPiece = executeResult

        self.whitesTurn = not(self.whitesTurn)
        self.moves.append((fromSquare, toSquare))
        self.mapPieces()
        #Check for checkmate or stalemate (if no legal moves for any odd colored pieces)
        mateRes = self.check_for_mate(piece.color)
        if mateRes == 'Checkmate':
            return piece.color + " won with checkmate"
        elif mateRes == 'Stalemate':
            return piece.color + " lost with stalemate"

        if capture:
            return piece.color + " " + piece.name + " moved from " + fromSquare + " to " + toSquare + " and captured a " + capturedPiece.color + " " + capturedPiece.name + '\n'
        else:
            return piece.color + " " + piece.name + " moved from " + fromSquare + " to " + toSquare + '\n'

import pygame
pygame.init()
BLACK = (26, 16, 41)
WHITE = (111, 100, 124)

pygame.display.set_caption("pyChess")

dot = pygame.image.load('dot.png')
redDot = pygame.image.load('red_dot.png')
piece_sprite = pygame.image.load('Chess_Pieces_Sprite.png')
hihghlight = pygame.image.load('highlight.png')

class pyGame:
    def __init__(self):
        self.selectedPiece = ''
        self.winSize = (800, 800)
        self.win = pygame.display.set_mode(self.winSize)


    def draw_board(self):
        self.win.fill(BLACK)
        for x in range(1, 9):
            for y in range(1, 9):
                if (x + y) % 2 != 1:
                    self.win.fill(WHITE, (x*100-100, y*100-100, 100 ,100))

    def draw_pieces(self, exceptPiece):
        for square in game.board:
            if game.board[square] != 0:
                piece = game.board[square]
                if exceptPiece != piece:
                    xPos = (spilt_squarename(square)[0]-1)*100
                    yPos = (8-spilt_squarename(square)[1])*100
                    colorAdder = 0
                    if piece.color == 'black':
                        colorAdder = 100
                    if piece.name == 'king':
                        self.win.blit(piece_sprite, (xPos,yPos),((0,colorAdder),(100,100)))
                    elif piece.name == 'queen':                                           
                        self.win.blit(piece_sprite, (xPos,yPos),((100,colorAdder),(100,100)))
                    elif piece.name == 'bishop':                                          
                        self.win.blit(piece_sprite, (xPos,yPos),((200,colorAdder),(100,100)))
                    elif piece.name == 'knight':                                          
                        self.win.blit(piece_sprite, (xPos,yPos),((300,colorAdder),(100,100)))
                    elif piece.name == 'rook':                                            
                        self.win.blit(piece_sprite, (xPos,yPos),((400,colorAdder),(100,100)))
                    elif piece.name == 'pawn':                                            
                        self.win.blit(piece_sprite, (xPos,yPos),((500,colorAdder),(100,100)))

    def drag_piece(self, dragPiece, pos):
        for square in game.board:
            if game.board[square] != 0:
                piece = game.board[square]
                xPos = (spilt_squarename(square)[0]-1)*100
                yPos = (8-spilt_squarename(square)[1])*100
                if dragPiece == piece:
                    xPos = pos[0]
                    yPos = pos[1]
                    colorAdder = 0
                    if piece.color == 'black':
                        colorAdder = 100
                    if piece.name == 'king':
                        self.win.blit(piece_sprite, (xPos,yPos),((0,colorAdder),(100,100)))
                    elif piece.name == 'queen':                                           
                        self.win.blit(piece_sprite, (xPos,yPos),((100,colorAdder),(100,100)))
                    elif piece.name == 'bishop':                                          
                        self.win.blit(piece_sprite, (xPos,yPos),((200,colorAdder),(100,100)))
                    elif piece.name == 'knight':                                          
                        self.win.blit(piece_sprite, (xPos,yPos),((300,colorAdder),(100,100)))
                    elif piece.name == 'rook':                                            
                        self.win.blit(piece_sprite, (xPos,yPos),((400,colorAdder),(100,100)))
                    elif piece.name == 'pawn':                                            
                        self.win.blit(piece_sprite, (xPos,yPos),((500,colorAdder),(100,100)))
                    break

import math

def animate_drag_piece(fromPos, pos):
    fromSquare = get_click_square(fromPos)
    piecePos = (math.floor(fromPos[0]/100)*100,math.floor(fromPos[1]/100)*100)
    print(piecePos)
    toPos = (pos[0]-fromPos[0]+piecePos[0],pos[1]-fromPos[1]+piecePos[1])
    piece = game.board[fromSquare]
    print(piece)
    gui.draw_board()
    gui.draw_pieces(piece)
    gui.drag_piece(piece, toPos)


def get_click_square(pos):
    for n in range(0, 8):
        if n*100 <= pos[0] <= n*100+100:
            col = 1+n
        if n*100 <= pos[1] <= n*100+100:
            row = 8-n
    if col >= 0 and row >= 0:
        make_squarename(col, row)
        return make_squarename(col, row)

clickFromSquare = ''
clickToSquare = ''

def show_possible_moves():
    gui.draw_board()
    gui.draw_pieces(False)
    print(game.pieceMap[clickFromSquare])
    res = spilt_squarename(clickFromSquare)
    gui.win.blit(hihghlight, ((res[0]-1)*100, (8-res[1])*100))
    for square, result in game.pieceMap[clickFromSquare].items():
        res = spilt_squarename(square)
        if result == 2:
            gui.win.blit(dot, ((res[0]-1)*100, (8-res[1])*100))
        elif result == 3:
            gui.win.blit(redDot, ((res[0]-1)*100, (8-res[1])*100))
    

def reg_click():
    print(clickFromSquare)
    print(clickToSquare)
    legalSelect = False
    legalClickMove = False

    if gui.selectedPiece != '' and clickFromSquare == clickToSquare:
        for square, result in game.pieceMap[gui.selectedPiece].items():
            if square == clickToSquare and 2 <= result <= 3:
                print(game.move(gui.selectedPiece,clickToSquare))
                gui.selectedPiece = ''
                game.print_board()
                gui.draw_board()
                gui.draw_pieces(False)
                legalClickMove = True
        if not(legalClickMove):
            gui.selectedPiece = ''
            gui.draw_board()
            gui.draw_pieces(False)

    if not(legalClickMove):
        for square in game.board:
            if square == clickFromSquare:
                if game.board[square] != 0:
                    if (game.board[square].color == 'white' and game.whitesTurn) or (game.board[square].color == 'black' and not(game.whitesTurn)):
                        legalSelect = True
        if legalSelect:
            if clickFromSquare == clickToSquare:
                if gui.selectedPiece == '':
                    show_possible_moves()
                    gui.selectedPiece = clickToSquare

            else:
                gui.selectedPiece = ''
                print(game.move(clickFromSquare,clickToSquare))
                game.print_board()
                gui.draw_board()
                gui.draw_pieces(False)
        else:
            gui.selectedPiece = ''
            gui.draw_board()
            gui.draw_pieces(False)



game = Game()

game.print_board()

gui = pyGame()
gui.draw_board()
gui.draw_pieces(False)
run = True
pressed = False
dragActive = False

#clock = pygame.time.Clock()

#mainloop
while run:
    #clock.tick(10)
    for event in pygame.event.get():
        if pygame.mouse.get_pressed() == (1,0,0):
            if dragActive == False:
                dragFromPos = pygame.mouse.get_pos()
                dragActive = True
            animate_drag_piece(dragFromPos, pygame.mouse.get_pos())
            pygame.display.flip()
            if not(pressed):
                clickFromSquare = get_click_square(pygame.mouse.get_pos())
                pressed = True
        elif pygame.mouse.get_pressed() == (0,0,0) and pressed:
            clickToSquare = get_click_square(pygame.mouse.get_pos())
            reg_click()
            pressed = False
            dragActive = False
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()