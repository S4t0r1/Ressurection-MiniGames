

def grid(size=None):
    if not size:
        size = getSize()
    return ([["." for e in range(size)] for l in range(size)], size)

def printGrid(matrix):
    print("\n{}\n".format('\n'.join(' '.join(e for e in l) for l in matrix)))

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


def getAllArrays(grid_):
    arrays = [subarray for array in (getRow(grid_, all_=True), getCol(grid_, all_=True), 
                              getDiags1(grid_), getDiags2(grid_)) for subarray in array]
    for i, a in enumerate(arrays):
        print("{} : {} |{}".format(i, a, len(a)))
    return arrays


grid_ = grid(6)[0]
printGrid(grid_)
all_arrays = getAllArrays(grid_)

def checkNeighbors(matrix, max_arrayindx, arrayindx, arraylen, movingindx):
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

for i in range(len(all_arrays)):
    for n in range(len(all_arrays[i])):
        checkNeighbors(grid_, len(all_arrays)-1, i, len(all_arrays[i]), n)
