
tst = ['.', 'o', '.', '.', 'x', '.', 'x', '.' ,'x', 'x', '.', 'x', 'x', 'x', '.']
tst2 = ['.', '.', 'x', 'x', '.']

def checkNeighbors(matrix, max_arrayindx, arrayindx, arraylen, movingindx, indexonly=False):
    size = len(matrix)
    count = 0
    if (0 <= arrayindx <= size-1):
        r, c = arrayindx, movingindx
        neighbors = "matrix[r+1][c-1];matrix[r+1][c];matrix[r+1][c+1];"  \
                    "matrix[r-1][c-1];matrix[r-1][c];matrix[r-1][c+1]"
    elif (size <= arrayindx <= (size*2)-1):
        r, c = movingindx, arrayindx - size
        neighbors = "matrix[r-1][c-1];matrix[r-1][c+1];"  \
                    "matrix[r][c-1];matrix[r][c+1];"      \
                    "matrix[r+1][c-1];matrix[r+1][c+1]"
    else:
        fulldiag1_indx = size*2
        fulldiag2_indx = int(fulldiag1_indx + (((max_arrayindx+1)-fulldiag1_indx)/2))
        diffr = size - arraylen
        if (fulldiag1_indx <= arrayindx < fulldiag2_indx):
            if arrayindx == fulldiag1_indx:
                r, c = movingindx, movingindx 
            else:
                r = movingindx + (diffr if arrayindx%2!=0 else 0)
                c = movingindx + (diffr if arrayindx%2==0 else 0)
            neighbors = "matrix[r-1][c];matrix[r-1][c+1];matrix[r][c+1];"  \
                        "matrix[r][c-1];matrix[r+1][c-1];matrix[r+1][c]"
        else:
            if arrayindx == fulldiag2_indx:
                r, c = (size-1)-movingindx, movingindx
            else:
                r = ((size-1)-movingindx) - (diffr if arrayindx%2==0 else 0)
                c = movingindx + (diffr if arrayindx%2!=0 else 0)
            neighbors = "matrix[r][c-1];matrix[r-1][c-1];matrix[r-1][c];"  \
                        "matrix[r+1][c];matrix[r+1][c+1];matrix[r][c+1]"
    if indexonly:
        return r, c
    for cell in neighbors.strip().split(';'):
        try:
            indxs = [indx_str[:-1] for indx_str in cell.split('[') if ']' in indx_str]
            for indx in indxs:
                if eval(indx) < 0 or eval(indx) >= (size-1):
                    raise IndexError()
            if eval(cell) != '.':
                count += 1
        except IndexError:
            continue
        else:
            print("{} | {} : filled count = {}".format(r, c, count))
    return count

def evalIndexes(matrix, arrays, arrayindx, symbol=''):
    array = arrays[arrayindx]
    newindex = 0
    counts, empt_counts = {}, {}
    count, emptcount = 0, 0
    coordinates = {}
    for i, e in enumerate(array):
        coordinates[i] = checkNeighbors(matrix, len(arrays)-1, arrayindx, len(array), i, indexonly=True)
        if i < (len(array)-1):
            if e == symbol:
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
                    empt_counts[i] = emptcount
                    emptcount = 0
        else:
            if e == '.':
                if array[i-1] == symbol:
                    counts[i] = str(checkNeighbors(matrix, len(arrays)-1, arrayindx, len(array), i))
                    newindex = i
                empt_counts[i] = emptcount + 1
            elif e == symbol:
                counts[i] = count + 1
    return counts, empt_counts, coordinates

def pickCoordinates(counts_coordinates_tuple):
    counts, empt_counts, coordinates = counts_coordinates_tuple
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
