

#tst = ['.', 'o', '.', '.', 'x', '.', 'x', '.' ,'x', 'x', '.', 'x', 'x', 'x', '.']
tst1 = ['.', 'o', 'x', 'x', 'x']
tst2 = ['.', '.', 'x', 'x', '.']
tst3 = ['.', 'o', 'x', 'x', '.']
tst4 = ['.', '.', 'x', '.', '.']
tst5 = ['x', '.', 'x', '.', 'o', '.', '.', 'x']
tst6 = ['x', '.', 'x', '.', '.', 'o', '.', '.', 'x']
tst7 = ['.', 'x', 'x', '.', 'x', 'o', '.', '.', 'x']
tst8 = ['.', 'x', 'x', '.', '.', 'x', '.', '.', 'x']

def getArrayValues(*arrays, symbol=''):
    arrays_values = {}
    for indx, array in enumerate(arrays):
        valuecount = 0
        values = []
        opn, connect = False, False
        for i, e in enumerate(array):
            neighbors = [array[i+1]] if i==0 else [array[i-1]] if i==len(array)-1 else [array[i+1], array[i-1]]
            if opn and connect:
                values.append(valuecount)
            if e == '.':
                if i < len(array)-1 and array[i-1]=='.':
                    valuecount = 0
                opn = True if any(x==symbol for x in neighbors) else False
                valuecount += 0 if all(x!=symbol for x in neighbors) else 1
            elif e == symbol:
                connect = True
                valuecount += 1
            else:
                if opn and connect:
                    values.append(valuecount)
                opn, connect = False, False
                valuecount = 0
        if opn and connect:
            values.append(valuecount)
        if len(values) > 0:
            valuecount = max(values)
            print("array {array} num {indx}: count = {valuecount} | {values}".format(**locals()))
        else:
            print("...not eligible")


getArrayValues(tst1, tst2, tst3, tst4, tst5, tst6, tst7, tst8, symbol='x')
