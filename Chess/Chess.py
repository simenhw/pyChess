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

def unParseSquareName(squareName):
    col = ord(squareName[0])-96
    return (col, int(squareName[1]))

def parseSquareName(col, row):
    squareChar = chr(96+col)
    return squareChar+str(row)

def nullMap():
    map = {}
    for col in range(1,9):
        for row in range(1,9):
            squareName = parseSquareName(col,row)
            map[squareName] = 0
    return map

class Game:

    def __init__(self):
        self.whitesTurn = True
        self.board = {}
        self.moves = []
        for col in range(1,9):
            for row in range(1,9):
                squareName = parseSquareName(col,row)
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

    def printBoard(self):
        for row in range(8,0,-1):
            for col in range(1,9):
                if self.board[parseSquareName(col,row)] == 0:
                    print(parseSquareName(col,row) + ':' + '0', end='              ')
                else:
                    pieceName = self.board[parseSquareName(col,row)].color + ' ' + self.board[parseSquareName(col,row)].name
                    length = len(pieceName)
                    spacesToAdd = 15 - length
                    spaceStr = ''
                    for x in range(0,spacesToAdd):
                        spaceStr += ' '
                    print(parseSquareName(col,row) + ':' + pieceName, end=spaceStr)
            print('\n')

    def mapPawn(self, square):
        resultMap = nullMap()
        piece = self.board[square]
        tuple = unParseSquareName(square)
        inverter = 1
        if self.board[square].color == 'black':
            inverter = -1
        #if from start pos. Can move two steps ahead if square is not occupied
        if (inverter == 1 and tuple[1] == 2) or (inverter == -1 and tuple[1] == 7):
            if self.board[parseSquareName(tuple[0], tuple[1]+2 * inverter)] == 0:
                resultMap[parseSquareName(tuple[0], tuple[1]+2 * inverter)] = 2
        #can alway move one step ahead if square is not occupied
        if self.board[parseSquareName(tuple[0], tuple[1]+1 * inverter)] == 0:
            resultMap[parseSquareName(tuple[0], tuple[1]+1 * inverter)] = 2
        #Protects or can attack sideways if square is occupied by enemy
        for j in range(1,3):
            add = j
            if add == 2:
                add = -1
            if 1 <= tuple[0]+add <= 8 and 1 <= tuple[1]+inverter <= 8:
                #if there is a piece sideways
                if self.board[parseSquareName(tuple[0]+add,tuple[1]+inverter)] != 0:
                    # if the piece is different colored
                    if self.board[parseSquareName(tuple[0]+add,tuple[1]+inverter)].color != piece.color:
                        #if piece is a king
                        if self.board[parseSquareName(tuple[0]+add,tuple[1]+inverter)].name == 'king':
                            resultMap[parseSquareName(tuple[0]+add,tuple[1]+inverter)] = 5
                        else:
                            #Can capture the piece
                            resultMap[parseSquareName(tuple[0]+add,tuple[1]+inverter)] = 3
                     # if there is not an enemy piece, piece is same color 
                    else:
                        resultMap[parseSquareName(tuple[0]+add,tuple[1]+inverter)] = 1
                else:
                    resultMap[parseSquareName(tuple[0]+add,tuple[1]+inverter)] = 1

		#If there is an odd-colored pawn to the side that moved two steps in last move, En passant is possible
        if len(self.moves) > 1:
            for j in range(1,3):
                add = j
                if add == 2:
                    add = -1 
                if 1 <= tuple[0] + add <= 8:
                    #if there is a piece
                    if self.board[parseSquareName(tuple[0] + add, tuple[1])] != 0:
                        #if its odd colored
                        if self.board[parseSquareName(tuple[0] + add, tuple[1])].color != self.board[square]:
                            lastMove = self.moves[-1]
                            #if the last move was to this square
                            if lastMove[1] == parseSquareName(tuple[0] + add, tuple[1]):
                                steps = abs(unParseSquareName(lastMove[0])[1] - unParseSquareName(lastMove[1])[1])
                                if steps == 2:
                                    resultMap[parseSquareName(tuple[0] + add, tuple[1]+inverter)] = 2
                                    resultMap[parseSquareName(tuple[0] + add, tuple[1])] = 4
        return resultMap

    def mapKnight(self, square):
        resultMap = nullMap()
        piece = self.board[square]
        tuple = unParseSquareName(square)
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
                    squareToCheck = parseSquareName(tuple[0] + addCol, tuple[1] + addRow)
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

    def mapBishop(self, square):
        return self.axialMapping(square)

    def axialMapping(self, square):
        resultMap = nullMap()
        piece = self.board[square]
        tuple = unParseSquareName(square)
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
                squareToCheck = parseSquareName(tuple[0]+step*colInverter, tuple[1]+step*rowInverter)
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

    def mapRook(self, square):
        return self.linearMapping(square)

    def linearMapping(self, square):
        resultMap = nullMap()
        piece = self.board[square]
        tuple = unParseSquareName(square)
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
                squareToCheck = parseSquareName(tuple[0]+step*colInverter, tuple[1]+step*rowInverter)
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

    def mapQueen(self, square):
        combinedList = {}
        for col in range(1,9):
            for row in range(1,9):
                checkSquare = parseSquareName(col, row)
                if self.linearMapping(square)[checkSquare] != 0:
                    combinedList[checkSquare] = self.linearMapping(square)[checkSquare] 
                elif self.axialMapping(square)[checkSquare] != 0:
                    combinedList[checkSquare] = self.axialMapping(square)[checkSquare] 
                else:
                    combinedList[checkSquare] = 0
        return combinedList

    def mapKing(self, square):
        resultMap = nullMap()
        piece = self.board[square]
        tuple = unParseSquareName(square)
        for hor in range(-1,2):
            for vert in range(-1,2):
                #every possible move around king square except for king square
                if not(vert == 0 and hor == 0):
                    #if within board
                    if 1 <= tuple[0]+hor <= 8 and 1 <= tuple[1]+vert <= 8:
                        checkSquare  = parseSquareName(tuple[0]+hor, tuple[1]+vert)
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

    def checkMove(self, fromSquare, withCheck):
        if self.board[fromSquare].name == 'pawn':
            pieceMap = self.mapPawn(fromSquare,)
        if self.board[fromSquare].name == 'knight':
            pieceMap = self.mapKnight(fromSquare)
        if self.board[fromSquare].name == 'bishop':
            pieceMap = self.mapBishop(fromSquare)
        if self.board[fromSquare].name == 'rook':
            pieceMap = self.mapRook(fromSquare)
        if self.board[fromSquare].name == 'queen':
            pieceMap = self.mapQueen(fromSquare)
        if self.board[fromSquare].name == 'king':
            pieceMap = self.mapKing(fromSquare)
        if withCheck:
            for testSquare in pieceMap:
                if 2 <= pieceMap[testSquare] <= 3:
                    if self.checkForCheck(fromSquare, testSquare):
                        pieceMap[testSquare] = 0
        return pieceMap

    def checkForCheck(self, fromSquare, toSquare):
        testGame = Game()
        testGame.board = self.board.copy()
        inCheck = False
        testGame.executeMove(fromSquare, toSquare)
        for square in testGame.board:
            if testGame.board[square] != 0:
                if testGame.board[square].color != self.board[fromSquare].color:
                    #opposite color inner results..
                    innerRes = testGame.checkMove(square, False)
                    if innerRes:
                        for innerSquare in innerRes:
                            if innerRes[innerSquare] == 5:
                                inCheck = True
        return inCheck

    def executeMove(self, fromSquare, toSquare):
        capture = False
        checkRes = self.checkMove(fromSquare, False)
        piece = self.board[fromSquare]
        capturedPiece = 0
        #If move to empty square. Can be regular move or En Passant
        if checkRes[toSquare] == 2:
            #Check if the move is En Passant (if pawn move sideways(we know target square is empty))
            if piece.name == 'pawn' and unParseSquareName(fromSquare)[0] != unParseSquareName(toSquare)[0]:
                for result in checkRes:
                    if checkRes[result] == 4:
                        capturedPawnSquare = result
                capturedPiece = board[capturedPawnSquare]
                self.board[capturedPawnSquare] = 0
                self.board[toSquare] = board[fromSquare]
                self.board[fromSquare] = 0
                capture = True
            #if not En Passant, its a regular move
            else:
                self.board[toSquare] = self.board[fromSquare]
                self.board[fromSquare] = 0

        #if move is legal with capture
        elif checkRes[toSquare] == 3:
            capturedPiece = self.board[toSquare]
            self.board[toSquare] = self.board[fromSquare]
            self.board[fromSquare] = 0

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

        checkRes = self.checkMove(fromSquare, True)
        #If move is not legal
        if not( 2 <= checkRes[toSquare] <= 3):
            return 'move is not legal'

        #execute move
        capture = False
        #If move to empty square. Can be regular move or En Passant
        if checkRes[toSquare] == 2:
            #Check if the move is En Passant (if pawn move sideways(we know target square is empty))
            if piece.name == 'pawn' and unParseSquareName(fromSquare)[0] != unParseSquareName(toSquare)[0]:
                for result in checkRes:
                    if checkRes[result] == 4:
                        capturedPawnSquare = result
                capturedPiece = self.board[capturedPawnSquare]
                self.board[capturedPawnSquare] = 0
                self.board[toSquare] = self.board[fromSquare]
                self.board[fromSquare] = 0
                capture = True
            #if not En Passant, its a regular move
            else:
                self.board[toSquare] = self.board[fromSquare]
                self.board[fromSquare] = 0

        #if move is legal with capture
        elif checkRes[toSquare] == 3:
            capturedPiece = self.board[toSquare]
            self.board[toSquare] = self.board[fromSquare]
            self.board[fromSquare] = 0
            capture = True

        self.whitesTurn = not(self.whitesTurn)
        self.moves.append((fromSquare, toSquare))
        if capture:
            return piece.color + " " + piece.name + " moved from " + fromSquare + " to " + toSquare + " and captured a " + capturedPiece.color + " " + capturedPiece.name + '\n'
        else:
            return piece.color + " " + piece.name + " moved from " + fromSquare + " to " + toSquare + '\n'

game = Game()

game.printBoard()

gameOn = True
while gameOn:
    fromSquare = input('Move from: ')
    toSquare = input('Move to: ')
    if fromSquare == 'exit' or toSquare == 'exit':
        gameOn = False
    else:
        print(game.move(fromSquare,toSquare))
        game.printBoard()  
