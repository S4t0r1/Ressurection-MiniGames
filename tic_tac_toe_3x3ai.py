import random


def getSize(warning=None):
    try:
        inpt = int(input("\nChoose TicTacToe grid size (min=3): "))
        if not (3 <= inpt <= 10):
            raise ValueError("ERROR: Pick an integer that is (3 <= num <= 10)!")
    except ValueError as err:
        inpt = getSize(print(err))
    return inpt

def grid(size=None):
    if not size:
        size = getSize()
    return ([["." for e in range(size)] for l in range(size)], size)

def printGrid(matrix):
    print("\n{}\n".format('\n'.join(' '.join(e for e in l) for l in matrix)))

def makeTurns(matrix, size, player, warning=None):
    try:
        r, c = [int(num) for num in input("{} make a turn!\n(number1=row)\n(number2=col)\n"
                                              .format(player.upper())) if num.isdecimal()]
        if any(num >= size for num in (r, c)):
            raise IndexError("Coordinate/-s out of bounds!\n")
        if matrix[r][c] != '.':
            raise IndexError("Spot taken!\n")
    except ValueError:
        r, c = makeTurns(matrix, size, player, print("You have to write integer coordinates!\n"))
    except IndexError as err:
        r, c = makeTurns(matrix, size, player, print(err))
    return (r, c)

def winCheck(matrix, r, c, size, player):
    printGrid(matrix)
    row = [matrix[r][n] for n in range(size)]
    col = [matrix[n][c] for n in range(size)]
    diag1 = [matrix[n][n] for n in range(size)]
    diag2 = [matrix[(size-1)-n][n] for n in range(size)]
    for array in (row, col, diag1, diag2):
        count = 0
        for i in range(len(array)):
            count += 1
            if array[i] != player:
                count = 0
            if count == (4 if size > 3 else 3):
                print("{} wins!".format(player.upper()))
                return True
    return False

def checkArraysAI(matrix, symbol1='', symbol2='', countlimit=0):
    size = len(matrix)
    for symbol in (symbol1, symbol2):
        for r in range(size):
            if matrix[r].count(symbol)==countlimit and '.' in matrix[r]:
                return r, matrix[r].index('.')
    
        for c in range(size):
            col = [matrix[r][c] for r in range(size)]
            if col.count(symbol)==countlimit and '.' in col:
                return col.index('.'), c
    
        diag1 = [matrix[n][n] for n in range(size)]
        if diag1.count(symbol)==countlimit and '.' in diag1:
            return diag1.index('.'), diag1.index('.')
    
        diag2 = [matrix[(size-1)-n][n] for n in range(size)]
        if diag2.count(symbol)==countlimit and '.' in diag2:
            return (size-1)-diag2.index('.'), diag2.index('.')

def ai_3x3(matrix, emptycount, r, c):
    movescount = (len(matrix)**2)-emptycount
    if movescount == 1:
        return (random.choice((r+1,r-1)), random.choice((c+1,c-1))) if (r == 1 and c == 1) else (1, 1)
    else:
        countlimit = 3 if len(matrix) > 3 else 2
        try:
            r, c = checkArraysAI(matrix, 'o', 'x', countlimit)
        except (ValueError, TypeError):
            countlimit -= 1
            r, c = checkArraysAI(matrix, 'o', 'x', countlimit)
        return r, c    

def game_set(ai=False, p1='x', p2='o'):
    matrix, size = grid()
    empty_count = size**2
    printGrid(matrix)
    while True:
        if empty_count == size**2:
            player_now = p1
        r, c =  ai_3x3(matrix, empty_count, r, c) if (ai and player_now==p2) else makeTurns(matrix, size, player_now)
        matrix[r][c] = player_now
        empty_count -= 1
        if winCheck(matrix, r, c, size, player_now) == True:
            return player_now
        if empty_count <= 1:
            print("It's a tie!")
            return False
        player_now = p2 if player_now == p1 else p1

def game():
    player1, player2 = 0, 0
    player_scores = {"x": player1, "o": player2}
    while True:
        gameset = game_set(ai=True)
        if gameset:
            player_scores[gameset] += 1
        print("Player1 'X': {x}\nPlayer2 'O': {o}".format(**player_scores))
        if input("\nNew game? (y/Y):\n") not in {'y', 'Y'}:
            return print("Exiting...")

game()
