tst = ['.', 'o', '.', '.', 'x', '.', 'x', '.' ,'x', 'x', '.', 'x', 'x', 'x', '.']
tst2 = ['.', '.', 'x', 'x', '.']

def checkNeighbors(matrix, index1=0, index2=0):
    count = 0
    for cell in (matrix[index1][index2+1], matrix[index1][index2-1]):
        if cell != '.':
            count += 1
    return str(count)

def editIndex(array, index1, index2, symbol=''):
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
                
print(editIndex(tst, 0, 'x'))
print(editIndex(tst2, 0, 'x'))
