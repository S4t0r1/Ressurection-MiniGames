

def getCoordinates(matrix, max_arrayindx, arrayindx, movingindx):
    size = len(matrix)
    rowindx, colindx = 0, 0
    if (0 <= arrayindx <= size-1):
        rowindx, colindx = arrayindx, movingindx
    elif (size <= arrayindx <= (size*2)-1):
        rowindx, colindx = movingindx, arrayindx
    else:
        fulldiag1_indx = size*2
        fulldiag2_indx = fulldiag1_indx + (((max_arrayindx+1)-fulldiag1_indx)/2)
        if (fulldiag1_indx <= arrayindx < fulldiag2_indx):
            if arrayindx == fulldiag1_indx:
                rowindx, colindx = movingindx, movingindx 
            else:
                diffr = arrayindx-fulldiag1_indx
                rowindx = movingindx + (diffr if arrayindx%2!=0 else 0)
                colindx = movingindx + (diffr in arrayindx%2==0 else 0)
        elif arrayindx == fulldiag2_indx:
            rowindx, colindx = (size-1)-movindx, movindx
        else:
            if arrayindx == fulldiag2_indx:
                rowindx, colindx = (size-1)-movingindx, movingindx
            else:
                diffr = arrayindx-fulldiag2_indx
                rowindx = ((size-1)-movingindx) - (diffr if arrayindx%2==0 else 0)
                colindx = movingindx + (diffr if arrayindx%2!=0 else 0)
    return rowindx, colindx


'''
def checkNeighbors(matrix, arrayindx):
    count = 0
    for cell in (matrix[index1][index2+1], matrix[index1][index2-1],
                 matrix[index1-1][index2+1], matrix[index1-1][index2-1],
                 matrix[index1+1][index2+1], matrix[index1+1], matrix[index2-1]):
        if cell != '.':
            count += 1
    return count
'''


def checkNeighbors(matrix, rowindx, colindx):
    count = 0
    
