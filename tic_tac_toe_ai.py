
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

def getRow(matrix, r=0, all_=False):
    if all_:
        rows = []
        for i in range(len(matrix)):
            rows.append([matrix[i][n] for n in range(len(matrix))])
        return rows
    return ([matrix[r][n] for n in range(len(matrix))],)

def getCol(matrix, c=0, all_=False):
    if all_:
        cols = []
        for i in range(len(matrix)):
            cols.append([matrix[n][i] for n in range(len(matrix))])
        return cols
    return ([matrix[n][c] for n in range(len(matrix))],)

def getDiags1(matrix):
    size = len(matrix)
    if size > 3:
        diags, diag_horz = [], []
        for i in range(size):
            diag_vert = [matrix[n+i][n] for n in range(size) if n+i<=(size-1)]
            if i > 0:
                diag_horz = [matrix[n][n+i] for n in range(size) if n+i<=(size-1)]
            for lst in (diag_vert, diag_horz):
                if len(lst) >= 4:
                    diags.append(lst)
        return diags
    return ([matrix[n][n] for n in range(size)],)

def getDiags2(matrix):
    size = len(matrix)
    if size > 3:
        diags, diag_horz = [], []
        for i in range(size):
            diag_vert = [matrix[(size-1)-n+i][n] for n in range(size) if (size-1)-n+i<=(size-1)]
            if i > 0:
                diag_horz = [matrix[(size-1)-n][n+i] for n in range(size) if n+i<=(size-1)]
            for lst in (diag_vert, diag_horz):
                if len(lst) >= 4:
                    diags.append(lst)
        return diags
    return ([matrix[(size-1)-n][n] for n in range(size)],)

def winCheck(matrix, r, c, size, player):
    printGrid(matrix)
    row = getRow(matrix, r)
    col = getCol(matrix, c)
    diags1 = getDiags1(matrix)
    diags2 = getDiags2(matrix)
    for array in (*row, *col, *diags1, *diags2):
        count = 0
        for i in range(len(array)):
            count += 1
            if array[i] != player:
                count = 0
            if count == (4 if size > 3 else 3):
                print("{} wins!".format(player.upper()))
                return True
    return False

def checkNeighbors(matrix, index1=0, index2=0):
    count = 0
    for cell in (matrix[index1][index2+1], matrix[index1][index2-1]):
        if cell != '.':
            count += 1
    return str(count)

def pickIndex(matrix, array, index1, index2, symbol=''):
    newindex = index1
    counts, count = {}, 0
    empt_counts, emptcount = {}, 0
    for i,e in enumerate(array):
        if i < (len(array)-1):
            if e == symbol:
                count += 1
                if array[i+1] != symbol:
                    counts[i] = count
                    count = 0
            if e == '.':
                if array[i+1] == symbol or array[i-1] == symbol:
                    counts[i] = checkNeighbors(matrix, i, index2)
                    newindex = i
                emptcount += 1
                if array[i+1] != '.':
                    empt_counts[i] = emptcount
                    emptcount = 0
        else:
            if e == '.':
                if array[i-1] == symbol:
                    counts[i] = checkNeighbors(matrix, i, index2)
                    newindex = i
                empt_counts[i] = emptcount + 1
            elif e == symbol:
                counts[i] = count + 1
    compare = {}
    sorted_keys = sorted([k for k in counts.keys()])
    for i,indx in enumerate(sorted_keys):
        nxt, prev = 0, 0
        if type(counts[indx]) == str:
            if i > 0:
                prev = counts[sorted_keys[i-1]]
                prev = prev if type(prev)==int else 0
            if i < len(sorted_keys)-1:
                nxt = counts[sorted_keys[i+1]]
                nxt = nxt if type(nxt)==int else 0    
            compare[indx] = prev + (int(counts[indx])+1) + nxt
    if len(compare.keys()) > 0:
        compare = {str(k)+str(v): k for k,v in compare.items() if v==max(compare.values())}
        if len(compare.keys()) == 1:
            newindex = list(compare.values())[0]
        else:
            empt_counts = {str(k)+str(v): k for k,v in empt_counts.items() if v==max(empt_counts.values())}
            newindex = list(empt_counts.values())[0]
    return newindex

def checkArraysAI(matrix, symbol1='', symbol2='', countlimit=0):
    size = len(matrix)
    print(countlimit)
    for symbol in (symbol1, symbol2):
        print(symbol)
        for r in range(size):
            print("row", matrix[r])
            if matrix[r].count(symbol)==countlimit and '.' in matrix[r]:
                c = matrix[r].index('.')
                return r, pickIndex(matrix, matrix[r], c, r, symbol)
    
        for c in range(size):
            col = [matrix[r][c] for r in range(size)]
            print("col", col)
            if col.count(symbol)==countlimit and '.' in col:
                r = col.index('.')
                return pickIndex(matrix, col, r, c, symbol), c
    
        diag1 = [matrix[n][n] for n in range(size)]
        print("diag1", diag1)
        if diag1.count(symbol)==countlimit and '.' in diag1:
            r, c = diag1.index('.'), diag1.index('.')
            return pickIndex(matrix, diag1, r, c, symbol), pickIndex(matrix, diag1, c, r, symbol)
    
        diag2 = [matrix[(size-1)-n][n] for n in range(size)]
        print("diag2", diag2)
        if diag2.count(symbol)==countlimit and '.' in diag2:
            r, c = (size-1)-diag2.index('.'), diag2.index('.')
            return pickIndex(matrix, diag2, r, c, symbol), pickIndex(matrix, diag2, c, r, symbol)

def ai_move(matrix, emptycount, r, c):
    movescount = (len(matrix)**2)-emptycount
    if movescount == 1:
        return (random.choice((r+1,r-1)), random.choice((c+1,c-1))) if (r == 1 and c == 1) else (1, 1)
    else:
        countlimit = 3 if len(matrix) > 3 else 2
        try:
            r, c = checkArraysAI(matrix, 'x', 'o', countlimit)
        except (ValueError, TypeError):
            countlimit -= 1
            r, c = checkArraysAI(matrix, 'x', 'o', countlimit)
        return r, c    

def game_set(ai=False, p1='x', p2='o'):
    matrix, size = grid()
    empty_count = size**2
    printGrid(matrix)
    while True:
        if empty_count == size**2:
            player_now = p1
        r, c =  ai_move(matrix, empty_count, r, c) if (ai and player_now==p2) else makeTurns(matrix, size, player_now)
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
