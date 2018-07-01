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

class Game:

    def __init__(self):
        self.whitesTurn = True
        self.board = {}
        self.moves = []
        self.possibleEnPassant = ''
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
                    print(0, end='              ')
                else:
                    pieceName = self.board[parseSquareName(col,row)].color + ' ' + self.board[parseSquareName(col,row)].name
                    length = len(pieceName)
                    spacesToAdd = 15 - length
                    spaceStr = ''
                    for x in range(0,spacesToAdd):
                        spaceStr += ' '
                    print(pieceName, end=spaceStr)
            print('\n')

    def move(self, begin, to):
        fromTuple = unParseSquareName(begin)
        toTuple = unParseSquareName(to)
        #Check that moving from square is within board
        if not (1 <= fromTuple[0] <= 8 and 1 <= fromTuple[1] <= 8):
            return "From square does not exist"
        #Check that moving to square is within board
        if not (1 <= toTuple[0] <= 8 and 1 <= toTuple[1] <= 8):
            return "To square does not exist"
        #Copy possible piece object to var
        movePiece = self.board[begin]
        #Check if move piece does not exist
        if movePiece == 0:
            return "No piece in that square"
        #Check that the move is not from and to the same square
        if begin == to:
            return "Can not move to and from same square"
        #Check if square to move to is occupied by piece of same color
        if self.board[to] != 0:
            if self.board[to].color == movePiece.color:
                return "Square occupied by piece of same color"
        #Create inverter for row calculations
        inverter = 1
        if not(self.whitesTurn):
            inverter = -1
        #if moving wrong colored piece
        if ((movePiece.color == 'white' and not(self.whitesTurn)) or (movePiece.color == 'black' and self.whitesTurn)):
            return "Wrong color of piece to move"

        #Create steps variables
        stepsHorisontal = toTuple[0] - fromTuple[0]
        stepsVertical = toTuple[1] - fromTuple[1]
        #create negative/positive multiplicators
        if stepsHorisontal < 0:
            horisontalNegative = -1
        else:
            horisontalNegative = 1
        if stepsVertical < 0:
            verticalNegative = -1
        else:
            verticalNegative = 1
 
        #King move logic
        if movePiece.name == 'king':
            something = 1

        #Queen move logic
        elif movePiece.name == 'queen':
            #Check if move is neither linear or axial
            if not(abs(stepsHorisontal) == abs(stepsVertical) or fromTuple[0] == toTuple[0] or fromTuple[1] == toTuple[1]):
                return "illegal queen move"

            if fromTuple[0] == toTuple[0] or fromTuple[1] == toTuple[1]:
                #Check if pieces in the way linear move
                for steps in range(1, stepsHorisontal + 1):
                    squareToCheck = parseSquareName(fromTuple[0] + steps*horisontalNegative,fromTuple[1])
                    #if same colored piece in the way
                    if self.board[squareToCheck] != 0:
                        if self.board[squareToCheck].color == movePiece.color:
                            return "Same colored piece in the way for queen" 
                        elif squareToCheck != to:
                            return "Enemy piece in the way for queen"
                for steps in range(1, stepsVertical + 1):
                    squareToCheck = parseSquareName(fromTuple[0], fromTuple[1] + steps*verticalNegative)
                    #if same colored piece in the way
                    if self.board[squareToCheck] != 0:
                        if self.board[squareToCheck].color == movePiece.color:
                            return "Same colored piece in the way for queen"
                        elif squareToCheck != to:
                            return "Enemy piece in the way for queen"
            if abs(stepsHorisontal) == abs(stepsVertical):
                #Check if pieces in the way axial move
                queenSteps = abs(fromTuple[0] - toTuple[0])
                for steps in range(1,queenSteps+1):
                    squareToCheck = parseSquareName(fromTuple[0] + steps*horisontalNegative,fromTuple[1] + steps*verticalNegative)
                    if self.board[squareToCheck] != 0:
                        if self.board[squareToCheck].color == movePiece.color:
                            return "Same colored piece in the way for queen"
                        elif squareToCheck != to:
                            return "Enemy piece in the way for queen"
            #if square to move to is free
            if self.board[to] == 0:
                return self.executeMove(movePiece, begin, to, False)
            else:
                return self.executeMove(movePiece, begin, to, to)

        #Rook move logic
        elif movePiece.name == 'rook':
            #Check if move in more than one axis
            if not(fromTuple[0] == toTuple[0] or fromTuple[1] == toTuple[1]):
                return "Not linear move for Rook"
            #Check if pieces in the way
            for steps in range(1, stepsHorisontal + 1):
                squareToCheck = parseSquareName(fromTuple[0] + steps*horisontalNegative,fromTuple[1])
                #if same colored piece in the way
                if self.board[squareToCheck] != 0:
                    if self.board[squareToCheck].color == movePiece.color:
                        return "Same colored piece in the way for rook" 
                    elif squareToCheck != to:
                        return "Enemy piece in the way for rook"
            for steps in range(1, stepsVertical + 1):
                squareToCheck = parseSquareName(fromTuple[0], fromTuple[1] + steps*verticalNegative)
                #if same colored piece in the way
                if self.board[squareToCheck] != 0:
                    if self.board[squareToCheck].color == movePiece.color:
                        return "Same colored piece in the way for rook"
                    elif squareToCheck != to:
                        return "Enemy piece in the way for rook"
            #if square to move to is free
            if self.board[to] == 0:
                return self.executeMove(movePiece, begin, to, False)
            else:
                return self.executeMove(movePiece, begin, to, to)

        #Bishop move logic
        elif movePiece.name == 'bishop':
            #vertical and horisontal steps has to be equal
            if abs(stepsHorisontal) != abs(stepsVertical):
                return "Not a valid bishop move (horisontal steps does not match vertical)"

            bishopSteps = abs(fromTuple[0] - toTuple[0])
            for steps in range(1,bishopSteps+1):
                squareToCheck = parseSquareName(fromTuple[0] + steps*horisontalNegative,fromTuple[1] + steps*verticalNegative)
                if self.board[squareToCheck] != 0:
                    if self.board[squareToCheck].color == movePiece.color:
                        return "Same colored piece in the way for bishop"
                    elif squareToCheck != to:
                        return "Enemy piece in the way for bishop"
            if self.board[to] == 0:
                return self.executeMove(movePiece, begin, to, False)
            else:
                return self.executeMove(movePiece, begin, to, to)

        #Knight move logic
        elif movePiece.name == 'knight':
            #can either move 1 horisontal and 2 vertical or 2 horisontal and 1 vertical
            if ( abs(fromTuple[0] - toTuple[0]) == 1 and abs(fromTuple[1] - toTuple[1]) == 2) or ( abs(fromTuple[0] - toTuple[0]) == 2 and abs(fromTuple[1] - toTuple[1]) == 1):
                if self.board[to] == 0:
                    return self.executeMove(movePiece, begin, to, False)
                else:
                    return self.executeMove(movePiece, begin, to, to)
            else:
                return "Not a valid Knight move"
 
        #Pawn move logic
        elif movePiece.name == 'pawn':
            #linear moves
            if fromTuple[0] == toTuple[0]:
                #can not capture at linear moves, so to square has to be avaliable
                if not(self.board[to] == 0):
                    return "can not move pawn linear to occupied square"

                pawnSteps = (toTuple[1] - fromTuple[1])*inverter
                #if from start row move one or two squares possible
                if pawnSteps == 2:
                    if (movePiece.color == 'white' and fromTuple[1] == 2) or (movePiece.color == 'black' and fromTuple[1] == 7):
                        #mark possible En Passant Square
                        self.possibleEnPassant = to
                        return self.executeMove(movePiece, begin, to, False)
                    else:
                        return "Double pawn step only possible from start row"
                elif pawnSteps == 1:
                    return self.executeMove(movePiece, begin, to, False)
                else:
                    return "Invalid linear pawn move"
            #axial pawn move, has to capture, either En Passant or regular axial move
            elif (fromTuple[0] == toTuple[0]-1 or fromTuple[0] == toTuple[0]+1) and fromTuple[1]+inverter == toTuple[1]:
                #Regualar axial move?
                if self.board[to] != 0:
                    return self.executeMove(movePiece, begin, to, to)
                #En passant possible?
                elif self.possibleEnPassant != '':
                    enPassantTuple = unParseSquareName(self.possibleEnPassant)
                    if toTuple[0] == enPassantTuple[0] and toTuple[1] - enPassantTuple[1] == inverter:
                        return self.executeMove(movePiece, begin, to, self.possibleEnPassant)
                else:
                    return "axial pawn move not regular or En Passant"
            else:
                return "Pawn move, neither legal linear or axial"

    def mapPawn(self, square):
        resultMap = {}
        piece = self.board[square]
        tuple = unParseSquareName(square)
        #if from start pos. Can move two steps ahead if square is not occupied
        if tuple[1] == 2:
            if self.board[parseSquareName(tuple[0], tuple[1]+2)] == 0:
                resultMap[parseSquareName(tuple[0], tuple[1]+2)] = 2
        #can alway move one step ahead if square is not occupied
        if self.board[parseSquareName(tuple[0], tuple[1]+1)] == 0:
            resultMap[parseSquareName(tuple[0], tuple[1]+1)] = 2
        #Protects or can attack sideways if square is occupied by enemy
        for j in range(1,3):
            add = j
            if add == 2:
                add = -1
            if 1 <= tuple[0]+add <= 8 and 1 <= tuple[1]+1 <= 8:
                #if there is a piece sideways
                if self.board[parseSquareName(tuple[0]+add,tuple[1]+1)] != 0:
                    # if the piece is different colored
                    if self.board[parseSquareName(tuple[0]+add,tuple[1]+1)].color != piece.color:
                        #Can capture the piece
                        resultMap[parseSquareName(tuple[0]+add,tuple[1]+1)] = 3
                     # if there is not an enemy piece, piece is same color 
                    else:
                        resultMap[parseSquareName(tuple[0]+add,tuple[1]+1)] = 1
                else:
                    resultMap[parseSquareName(tuple[0]+add,tuple[1]+1)] = 1

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
                                steps = unParseSquareName(lastMove[0])[1] - unParseSquareName(lastMove[1])[1]
                                if steps == 2:
                                    resultMap[parseSquareName(tuple[0] + add, tuple[1]+1)] = 2
                                    resultMap[parseSquareName(tuple[0] + add, tuple[1])] = 4
        return resultMap

    def mapKnight(self, square):
        resultMap = {}
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
                    #else there has to be odd colored piece (can capture)
                    else:
                        resultMap[squareToCheck] = 3
        return resultMap

    def mapBishop(self, square):
        return self.axialMapping(square)

    def axialMapping(self, square):
        resultMap = {}
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
                elif self.board[squareToCheck].color != piece.color:
                    resultMap[squareToCheck] = 3
                    break
        return resultMap

    def mapRook(self, square):
        return self.linearMapping(square)

    def linearMapping(self, square):
        resultMap = {}
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
                elif self.board[squareToCheck].color != piece.color:
                    resultMap[squareToCheck] = 3
                    break
        return resultMap

    def mapQueen(self, square):
        combinedList = { **self.linearMapping(square), **self.axialMapping(square) }
        return combinedList

    def executeMove(self, piece, begin, to, captureSquare):
        #reset possible En Passant (if not this is the move where possible En Passant was created)
        if self.possibleEnPassant !='':
            if not(piece == self.board[begin] and to == self.possibleEnPassant):
                self.possibleEnPassant = ''

        if captureSquare:
            capturedPiece = self.board[captureSquare]
            self.board[captureSquare] = 0
        self.board[to] = self.board[begin]
        self.board[begin] = 0

        self.whitesTurn = not(self.whitesTurn)
        self.moves.append((begin, to))
        if captureSquare:
            return piece.color + " " + piece.name + " moved from " + begin + " to " + to + " and captured a " + capturedPiece.color + " " + capturedPiece.name + '\n'
        else:
            return piece.color + " " + piece.name + " moved from " + begin + " to " + to + '\n'

game = Game()

print(game.mapPawn('a2'))

game.printBoard()

print(game.move('d2','d4'))
game.printBoard() 

print(game.move('h7','h6'))
game.printBoard()

print(game.move('d4','d5'))
game.printBoard()

print(game.move('c7','c5'))
game.printBoard()

print(game.move('g1','f3'))
game.printBoard()

print(game.move('a7','a5'))
game.printBoard()

print(game.mapQueen('d1'))
print(game.mapQueen('d8'))


#print(game.moves)

