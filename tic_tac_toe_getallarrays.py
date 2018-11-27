
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
getAllArrays(grid_)
