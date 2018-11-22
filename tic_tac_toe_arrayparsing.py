tst = ['.', 'o', '.', '.', 'x', '.', 'x', '.' ,'x', 'x', '.', 'x', 'x', 'x', '.']

def editIndex(array, index, symbol=''):
    newindex, counts, count = index, {}, 0
    for i,e in enumerate(array):
        if i < (len(array)-1):
            if e == symbol:
                count += 1
                if array[i+1] != symbol:
                    counts[i] = count
                    count = 0
            if array[i+1] == '.':
                newindex = i+1
            if array[i+1] == symbol and e == '.':
                newindex = i
            if i > 0:
                if array[i-1] == symbol and array[i+1] == symbol and e == '.':
                    counts[i] = "1"
        else:
            if array[i-1] == symbol:
                if e == '.':
                    newindex = i
            if e == symbol:
                counts[i] = count + 1
   
    compare = {}
    sorted_keys = sorted([k for k in counts.keys()])
    for i,indx in enumerate(sorted_keys):
        if type(counts[indx]) == str:
            compare[indx] = counts[sorted_keys[i-1]] + 1 + counts[sorted_keys[i+1]]
    if len(compare.keys()) > 0:
        compare = {v: k for k,v in compare.items()}
        newindex = max([v for v in compare.values()])
    return newindex
                
print(editIndex(tst, 0, 'x'))
