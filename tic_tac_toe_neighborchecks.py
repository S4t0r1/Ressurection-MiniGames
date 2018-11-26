

def checkNeighbors(matrix, max_arrayindx, arrayindx, movingindx):
    count, size = 0, len(matrix)
    rowindx, colindx = 0, 0
    if (0 <= arrayindx <= size-1):
        rowindx, colindx = arrayindx, movingindx
    elif (size <= arrayindx <= (size*2)-1):
        rowindx, colindx = movingindx, arrayindx
    else:
        fulldiag1_indx = size*2
        fulldiag2_indx = fulldiag1_indx + (((max_arrayindx+1)-fulldiag1_indx)/2)
        diffr = 0
        if arrayindx == fulldiag1_indx:
            rowindx, colindx = movingindx, movingindx
        elif (fulldiag1_indx < arrayindx < fulldiag2_indx):
            diffr = arrayindx-fulldiag1_indx
            
        elif arrayindx == fulldiag2_indx:
            rowindx, colindx = (size-1)-movindx, movindx
