class Piece:

    def __init__(self, name, value, color):
        self.name = name
        self.value = value
        self.color = color

class King(Piece):

    def __init__(self, color):
        self.name = 'King'
        self.value = 1000
        self.color = color

class Queen(Piece):

    def __init__(self, color):
        self.name = 'Queen'
        self.value = 9
        self.color = color

class Rook(Piece):

    def __init__(self, color):
        self.name = 'Rook'
        self.value = 5
        self.color = color

class Bishop(Piece):

    def __init__(self, color):
        self.name = 'Bishop'
        self.value = 3
        self.color = color

class Knight(Piece):

    def __init__(self, color):
        self.name = 'Knight'
        self.value = 3
        self.color = color

class Pawn(Piece):

    def __init__(self, color):
        self.name = 'Pawn'
        self.value = 1
        self.color = color

class Game:

    def __init__(self):
        self.whitesTurn = True
        self.board = {}
        self.moves = []
        self.possibleEnPassant = ''
        for x in range(1,9):
            for y in range(1,9):
                squareChar = chr(96+x)
                squareName = squareChar+str(y)
                self.board[squareName] = 0
                #place Rooks
                if squareChar == 'a' or squareChar == 'h':
                    if y == 1:
                        self.board[squareName] = Rook('white')
                    if y == 8:
                        self.board[squareName] = Rook('black')
                #place knights
                if squareChar == 'b' or squareChar == 'g':
                    if y == 1:
                        self.board[squareName] = Knight('white')
                    if y == 8:
                        self.board[squareName] = Knight('black')
                #place bishops
                if squareChar == 'c' or squareChar == 'f':
                    if y == 1:
                        self.board[squareName] = Bishop('white')
                    if y == 8:
                        self.board[squareName] = Bishop('black')
                #place queens
                if squareChar == 'd':
                    if y == 1:
                        self.board[squareName] = Queen('white')
                    if y == 8:
                        self.board[squareName] = Queen('black')
                #place kings
                if squareChar == 'e':
                    if y == 1:
                        self.board[squareName] = King('white')
                    if y == 8:
                        self.board[squareName] = King('black')
                #place pawns
                if y == 2:
                    self.board[squareName] = Pawn('white')
                if y == 7:
                    self.board[squareName] = Pawn('black')

    def printBoard(self):
        for row in range(8,0,-1):
            for col in range(1,9):
                squareChar = chr(96+col)
                if self.board[squareChar+str(row)] == 0:
                    print(0, end='              ')
                else:
                    pieceName = self.board[squareChar+str(row)].color + ' ' + self.board[squareChar+str(row)].name
                    length = len(pieceName)
                    spacesToAdd = 15 - length
                    spaceStr = ''
                    for x in range(0,spacesToAdd):
                        spaceStr += ' '
                    print(pieceName, end=spaceStr)
            print('\n')

    def move(self, begin, to):
        fromTuple = parseSquareName(begin)
        toTuple = parseSquareName(to)
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

        #Create inverter for row calculations
        inverter = 1
        if not(self.whitesTurn):
            inverter = -1
        #if moving wrong colored piece
        if ((movePiece.color == 'white' and not(self.whitesTurn)) or (movePiece.color == 'black' and self.whitesTurn)):
            return "Wrong color of piece to move"
        #King move logic
        if movePiece.name == 'King':
            something = 1
        #Queen move logic
        elif movePiece.name == 'Queen':
            something = 1
        #Rook move logic
        elif movePiece.name == 'Rook':
            something = 1
        #Bishop move logic
        elif movePiece.name == 'Bishop':
            something = 1
        #Knight move logic
        elif movePiece.name == 'Knight':
            something = 1
 
        #Pawn move logic
        elif movePiece.name == 'Pawn':
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
                    if self.board[to].color != movePiece.color:
                        return self.executeMove(movePiece, begin, to, to)
                #En passant possible?
                elif self.possibleEnPassant != '':
                    enPassantTuple = parseSquareName(self.possibleEnPassant)
                    if toTuple[0] == enPassantTuple[0] and toTuple[1] - enPassantTuple[1] == inverter:
                        return self.executeMove(movePiece, begin, to, self.possibleEnPassant)
                else:
                    return "axial pawn move not regular or En Passant"
            else:
                return "Pawn move, neither legal linear or axial"


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


def parseSquareName(squareName):
    col = ord(squareName[0])-96
    return (col, int(squareName[1]))

game = Game()

game.printBoard()

print(game.move('d2','d4'))
game.printBoard() 

print(game.move('e7','e5'))
game.printBoard()

print(game.move('d4','e5'))
game.printBoard()

print(game.move('d7','d5'))
game.printBoard()

print(game.move('h2','h3'))
game.printBoard()

print(game.move('h7','h6'))
game.printBoard()

print(game.move('e5','d6'))
game.printBoard()
