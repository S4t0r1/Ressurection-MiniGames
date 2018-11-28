
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
