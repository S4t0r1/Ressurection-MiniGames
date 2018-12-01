
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
            diag_vert = [matrix[(size-1)-n-i][n] for n in range(size) if (size-1)-n-i>=0]
            if i > 0:
                diag_horz = [matrix[(size-1)-n][n+i] for n in range(size) if n+i<=(size-1)]
            for lst in (diag_vert, diag_horz):
                if len(lst) >= 4:
                    diags.append(lst)
        return diags
    return ([matrix[(size-1)-n][n] for n in range(size)],)


def getCoordinates(matrix, max_arraynum, arrayindx, arraylen, movingindx):
    size = len(matrix)
    if (0 <= arrayindx <= size-1):
        r, c = arrayindx, movingindx
    elif (size <= arrayindx <= (size*2)-1):
        r, c = movingindx, arrayindx - size
    else:
        fulldiag1_indx = size*2
        fulldiag2_indx = int(fulldiag1_indx + (((max_arraynum+1)-fulldiag1_indx)/2))
        diffr = size - arraylen
        if (fulldiag1_indx <= arrayindx < fulldiag2_indx):
            if arrayindx == fulldiag1_indx:
                r, c = movingindx, movingindx 
            else:
                r = movingindx + (diffr if arrayindx%2!=0 else 0)
                c = movingindx + (diffr if arrayindx%2==0 else 0)
        else:
            if arrayindx == fulldiag2_indx:
                r, c = (size-1)-movingindx, movingindx
            else:
                r = ((size-1)-movingindx) - (diffr if arrayindx%2==0 else 0)
                c = movingindx + (diffr if arrayindx%2!=0 else 0)
    return r, c


def getAllArrays(grid_, gen_arrays_coords=False):
    arrayslst = [subarray for array in (getRow(grid_, all_=True), getCol(grid_, all_=True), 
                                getDiags1(grid_), getDiags2(grid_)) for subarray in array]
    if gen_arrays_coords:
        arrays_coords = {}
        for indx, array in enumerate(arrayslst):
            coords_per_array = []
            for i, cell in enumerate(array):
                r, c = getCoordinates(grid_, len(arrayslst)-1, indx, len(array), i)
                coords_per_array.append((r, c))
            arrays_coords[indx] = coords_per_array
        return arrays_coords
    return arrayslst


def getLinearNeighbors(array, *args):
    neighbors = []
    for i in args:
        for cell in [array[i+1]] if i==0 else [array[i-1]] if i==len(array)-1 else [array[i+1], array[i-1]]:
            neighbors.append(cell)
    return neighbors


def getArraysValues(arrays, symbol):
    arrays_values = {}
    candidate = None
    for indx, array in enumerate(arrays):
        valuecount, maxvalue = 0, 0
        values_ = {}
        opn, connect = False, False
        start = None
        for i, e in enumerate(array):
            neighbors = getLinearNeighbors(array, i)
            if e == '.':
                if i < len(array)-1 and array[i-1]=='.':
                    valuecount = 0
                opn = True if any(x==symbol for x in neighbors) else False
                if any(x==symbol for x in neighbors):
                    valuecount += 1
            elif e == symbol:
                connect = True
                valuecount += 1
            else:
                opn, connect = False, False
                valuecount = 0
            if opn and connect:
                values_[i] = valuecount
        if len(values_.values()) > 0:
            maxvalue = max(values_.values())
            for key in values_.keys():
                if values_[key] == maxvalue:
                    arrays_values[indx if symbol!='o' else str(indx)] = array[key+1-maxvalue:key+1]
    return arrays_values


def getIndx_frSubarray(prim_data, secon_data):
    str_, substr = ''.join(e for e in prim_data), ''.join(e for e in secon_data)
    sindx = str_.index(substr)
    eindx = sindx+(len(substr)-1)
    return (sindx, eindx)


def getMaxDistance(array, array_coordlst, enemy_symb, spot_coord):
    start = 0
    spotted, end = None, None
    for i, cell, coord in zip(range(len(array)), array, array_coordlst):
        if coord == spot_coord:
            spotted = True
        if cell == enemy_symb:
            if spotted:
                end = i
                break
            start = i
    if not end:
        end = i
    return end-start
            

def evalAreaArrays(matrix, arrays_coord_dict, arrays, best_arrays):
    max_pot_scores = {}
    prev_coords_data = {}
    for k, v in best_arrays.items():
        indx = int(k)
        vstring = v[0]
        pot_distances_per_array = 0
        for i, e in enumerate(vstring):
            if e=='.':
                coord_tuple = getCoordinates(matrix, len(arrays)-1, indx, len(arrays[indx]), i)
                if coord_tuple not in prev_coords_data.keys():
                    affected_arrays = {i: (arrays[i], coordlst) for i, coordlst in arrays_coord_dict.items() if coord_tuple in coordlst}
                else:
                    affected_arrays = prev_coords_data[coord_tuple]
                pot_distances_per_pos = 0
                for key, v in affected_arrays.items():
                    array, coordlst = v
                    if getMaxDistance(array, coordlst, 'x', coord_tuple) >= 4:
                        pot_distances_per_pos += 1
                pot_distances_per_array += pot_distances_per_pos
        max_pot_scores[k] = pot_distances_per_array
    maxscore = max(max_pot_scores.values())
    best_array_key = list(k for k, v in max_pot_scores.items() if v==maxscore)[0]
    return best_array_key                  
                

def getBestArrays(arrays, arrays_coord_dict, arrays_values, symbol):
    maxlen = max(len(v) for v in arrays_values.values())
    for k, v in arrays_values.items():
        indx = int(k)
        vstring = "".join(e for e in v)
        vlen = len(v) + (0.5 if (vstring.startswith('.') and vstring.endswith('.')) else 0)
        if type(vlen)==float:
            sindx, eindx = getIndx_frSubarray(arrays[indx], arrays_values[k])
            if any(x==('.'or symbol) for x in getLinearNeighbors(arrays[indx], sindx, eindx)):
                vlen = vlen + 1
        if vstring.count(symbol)==3:
            if (type(vlen)==int and vstring.count('.')>=1) or (type(vlen)==float and (vstring.count('.')%2!=0 or vstring.count('.')==2)):
                vlen = 10
        if vstring.count('o')==2:
            if type(vlen)==int:
                sindx, eindx = getIndx_frSubarray(arrays[indx], arrays_values[k])
                i = sindx if arrays[indx][sindx]=='.' else eindx
                if getMaxDistance(arrays[indx], arrays_coord_dict[indx], 'x', arrays_coord_dict[indx][i]) >= 4:
                    vlen = 7
            else:
                vlen = 7
        maxlen = vlen if maxlen < vlen else maxlen
        arrays_values[k] = vstring, vlen
    if type(maxlen)==int:
        for k, v in arrays_values.items():
            indx = int(k)
            vstring, vlen = v
            if vlen==maxlen:
                sindx, eindx = getIndx_frSubarray(arrays[indx], arrays_values[k][0])
                if any(x==('.' or symbol) for x in (arrays[indx][sindx-1] if sindx>0 else '', 
                                    arrays[indx][eindx+1] if eindx<len(arrays[indx])-1 else '')):
                    maxlen = vlen + 1
                    arrays_values[k] = vstring, maxlen
    arrays_values = {k: v for k,v in arrays_values.items() if v[1]==maxlen}
    return arrays_values, maxlen


def bestArray(matrix, all_arrays, arrays_coord_dict, symb1='', symb2=''):
    arraysdict_s1 = getArraysValues(all_arrays, symb1)
    arraysdict_s2 = getArraysValues(all_arrays, symb2)
    best_array_s1, maxval1 = getBestArrays(all_arrays, arrays_coord_dict, arraysdict_s1, symb1)
    best_array_s2, maxval2 = getBestArrays(all_arrays, arrays_coord_dict, arraysdict_s2, symb2)
    maxval = maxval1 if maxval1 > maxval2 else maxval2
    best_arrays = {k: v for k,v in {**best_array_s1, **best_array_s2}.items() if v[1]==maxval}
    candidate_data = None
    if len(best_arrays.keys()) > 1:
        for k in best_arrays.keys():
            if best_arrays[k]==10:
                if type(k)==str:
                    candidate_data = (all_arrays[int(k)], int(k), symb2)
                    break
                candidate_data = (all_arrays[k], k, symb1)
            else:
                k = evalAreaArrays(matrix, arrays_coord_dict, all_arrays, best_arrays)
                if type(k)==str:
                    candidate_data = (all_arrays[int(k)], int(k), symb2)
                    break
                candidate_data = (all_arrays[int(k)], int(k), symb1)
    else:
        candidate_data = list(best_arrays.keys())[0]
        candidate_data = (all_arrays[int(candidate_data)], int(candidate_data), symb1 if type(candidate_data)==int else symb2)
    return candidate_data


def checkNeighbors(matrix, max_arrayindx, arrayindx, arraylen, movingindx, indexonly=False):
    r, c = getCoordinates(matrix, max_arrayindx, arrayindx, arraylen, movingindx)
    size = len(matrix)
    fulldiag1_indx = size*2
    fulldiag2_indx = int(fulldiag1_indx + (((max_arrayindx+1)-fulldiag1_indx)/2))
    if (0 <= arrayindx <= size-1):
        neighbors = "matrix[r+1][c-1];matrix[r+1][c];matrix[r+1][c+1];"  \
                    "matrix[r-1][c-1];matrix[r-1][c];matrix[r-1][c+1];"   \
                    "matrix[r][c-1];matrix[r][c+1]"
    elif (size <= arrayindx <= (size*2)-1):
        neighbors = "matrix[r-1][c-1];matrix[r-1][c+1];"  \
                    "matrix[r][c-1];matrix[r][c+1];"      \
                    "matrix[r+1][c-1];matrix[r+1][c+1];"  \
                    "matrix[r-1][c];matrix[r+1][c]"
    else:
        if (fulldiag1_indx <= arrayindx < fulldiag2_indx):
            neighbors = "matrix[r-1][c];matrix[r-1][c+1];matrix[r][c+1];"  \
                        "matrix[r][c-1];matrix[r+1][c-1];matrix[r+1][c];"   \
                        "matrix[r-1][c-1];matrix[r+1][c+1]"
        else:
            neighbors = "matrix[r][c-1];matrix[r-1][c-1];matrix[r-1][c];"  \
                        "matrix[r+1][c];matrix[r+1][c+1];matrix[r][c+1];"   \
                        "matrix[r+1][c-1];matrix[r-1][c+1]"
    count = 0
    for cell in neighbors.strip().split(';'):
        try:
            indxs = [indx_str[:-1] for indx_str in cell.split('[') if ']' in indx_str]
            for indx in indxs:
                if eval(indx) < 0 or eval(indx) >= (size-1):
                    raise IndexError()
            if eval(cell) != '.':
                count += (2+(1 if neighbors.count('x')>=3 else 0) if eval(cell)=='x' else 1)
        except IndexError:
            continue
    return count


def evalIndexes(matrix, arrays, arrayindx, symbol=''):
    array = arrays[arrayindx]
    newindex = 0
    counts, empt_counts = {}, {}
    count, emptcount = 0, 0
    coordinates = {}
    spotted = None
    for i, e in enumerate(array):
        coordinates[i] = getCoordinates(matrix, len(arrays)-1, arrayindx, len(array), i)
        if i < (len(array)-1):
            if e == symbol:
                spotted = i
                count += 1
                if array[i+1] != symbol:
                    counts[i] = count
                    count = 0
            if e == '.':
                if array[i+1] == symbol or array[i-1] == symbol:
                    counts[i] = str(checkNeighbors(matrix, len(arrays)-1, arrayindx, len(array), i))
                    newindex = i
                emptcount += 1
                if array[i+1] != '.':
                    empt_counts[i if not spotted else spotted+1] = emptcount
                    emptcount = 0
        else:
            if e == '.':
                if array[i-1] == symbol:
                    counts[i] = str(checkNeighbors(matrix, len(arrays)-1, arrayindx, len(array), i))
                    newindex = i
                empt_counts[i-emptcount] = emptcount + 1
            elif e == symbol:
                counts[i] = count + 1
    return counts, empt_counts, coordinates


def pickCoordinates(counts_coords_tuple):
    counts, empt_counts, coordinates = counts_coords_tuple
    newindex = 0
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
    return coordinates[newindex]


def aiStart_3x3(maxindx, coordtup, arrays_coords):
    coords_flatlst = sorted(list({ct for coordslst in arrays_coords.values() for ct in coordslst}))
    if coordtup == (1, 1):
        return random.choice([ct for ct in coords_flatlst if ct!=(1, 1) and any(sum(ct)==x for x in (0, maxindx, maxindx*2))])
    else:
        return (1, 1)


def aiDecide_3x3(matrix, all_arrays, arrays_coords, prim_symb, sec_symb):
    chosen = None
    maxindx = len(matrix)-1
    for i, array in enumerate(all_arrays):
        if (array.count(prim_symb)==2 or array.count(sec_symb)==2) and array.count('.')==1:
            r, c = arrays_coords[i][array.index('.')]
            chosen = True
            break
    if not chosen:
        for i, array in enumerate(all_arrays):
            if array.count(prim_symb)==1 and array.count('.')==2:
                coords_flatlst = sorted(list({ct for coordslst in arrays_coords.values() for ct in coordslst}))
                enemy_coords = [ct for ct in coords_flatlst if matrix[ct[0]][ct[1]]==sec_symb]
                own_coords = [ct for ct in coords_flatlst if matrix[ct[0]][ct[1]]==prim_symb]
                corner_tups = [ct for ct in coords_flatlst if any(sum(ct)==x for x in (0, maxindx, maxindx*2)) and ct!=(1, 1)]
                if len([ct for ct in enemy_coords if ct in corner_tups]) == 1 and (1, 1) in enemy_coords:
                    r, c = random.choice([ct for ct in corner_tups if all(ct not in x for x in (own_coords, enemy_coords))])
                else:
                    r, c = arrays_coords[i][array.index('.')]
                chosen = True
                break
    if not chosen:
        for i, array in enumerate(all_arrays):
            if array.count('.')>=1:
                r, c = arrays_coords[i][array.index('.')]
                break
    return r, c


def aiStart(matrix, maxindx, coordtup):
    if any(sum(coordtup)==x for x in (0, maxindx, maxindx*2)):
        return tuple(len(matrix)//2 +(1 if maxindx%2==0 else 0) for i in range(2))
    else:
        coords = []
        for coord in coordtup:
            coords.append(coord-1 if coord>= len(matrix)//2 else coord+1)
        return coords


def aiMovesAnalysis(matrix, all_arrays, arrays_coords, symbol1, symbol2):
    best_array, arrayindx, best_symb = bestArray(matrix, all_arrays, arrays_coords, symbol1, symbol2)
    coordinates_tuple = pickCoordinates(evalIndexes(matrix, all_arrays, arrayindx, best_symb))
    return coordinates_tuple


def aiMove(matrix, arrays_coords, emptycount, coordtup, prim_symb, msg="\nAi taking a move.."):
    sec_symb = 'x' if prim_symb=='o' else 'o'
    movescount = (len(matrix)**2)-emptycount
    maxindx = len(matrix)-1
    print(msg)
    if movescount == 1:
        return aiStart_3x3(maxindx, coordtup, arrays_coords) if len(matrix)==3 else aiStart(matrix, maxindx, coordtup)
    else:
        all_arrays = getAllArrays(matrix, gen_arrays_coords=False)
        if len(matrix)==3:
            return aiDecide_3x3(matrix, all_arrays, arrays_coords, prim_symb, sec_symb)
        else: 
            return aiMovesAnalysis(matrix, all_arrays, arrays_coords, sec_symb, prim_symb)


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


def gameSet(ai=False, p1='x', p2='o'):
    matrix, size = grid()
    arrays_coords = getAllArrays(matrix, gen_arrays_coords=True)
    empty_count = size**2
    printGrid(matrix)
    while True:
        if empty_count == size**2:
            player_now = p1
        r, c =  aiMove(matrix, arrays_coords, empty_count, (r, c), player_now) if (ai and player_now==p2) else makeTurns(matrix, size, player_now)
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
        gameset = gameSet(ai=True)
        if gameset:
            player_scores[gameset] += 1
        print("Player1 'X': {x}\nPlayer2 'O': {o}".format(**player_scores))
        if input("\nNew game? (y/Y):\n") not in {'y', 'Y'}:
            return print("Exiting...")

game()
