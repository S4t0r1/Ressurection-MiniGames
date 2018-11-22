
tst = ['.', 'o', 'x', '.', 'x', '.' ,'x', 'x', '.', 'o']

def checkArrayPot(array, symbol1='', symbol2=''):
    start, end = 0, len(array)
    if array.count(symbol1)+array.count('.') >= 4:
        for index, e in enumerate(array):
            if e == symbol2:
                if index < (len(array)-1):
                    start = index+1
                else:
                    end = index
        return array[start:end]
    return False

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
                    counts[str(i)] = 1
        else:
            if array[i-1] == symbol and e == '.':
                newindex = i
    
    for key in counts.keys():
        if type(key) == str:
            newindex = int(key)
    print(counts)
    return newindex
                
     
tst2 = checkArrayPot(tst, 'x', 'o')
print(tst2)
print(editIndex(tst2, 0, 'x'))
