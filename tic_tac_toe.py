
def getSize(warning=None):
    try:
        inpt = int(input("\nChoose TicTacToe grid size (min=3): "))
        if not (3 <= inpt <= 10):
            raise ValueError("ERROR: Pick a whole num that is (3 <= num <= 10)!")
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
        r, c = makeTurns(matrix, size, player, print("You have to write number coordinates!\n"))
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
    return (row, col, diag1, diag2)
            
        
def game_set(ai=False, p1='x', p2='o'):
    matrix, size = grid()
    empty_count = size**2
    printGrid(matrix)
    while True:
        if empty_count == size**2:
            player_now = p1
        r, c = makeTurns(matrix, size, player_now)
        matrix[r][c] = player_now
        empty_count -= 1
        if winCheck(matrix, r, c, size, player_now) == True:
            break
        if empty_count <= 1:
            print("It's a tie!")
            break
        player_now = p2 if player_now == p1 else p1
    return player_now

def game():
    player1, player2 = 0, 0
    player_scores = {"x": player1, "o": player2}
    while True:
        player_scores[game_set()] += 1
        print("Player1 : {x}\nPlayer2 : {o}".format(**player_scores))

game()
