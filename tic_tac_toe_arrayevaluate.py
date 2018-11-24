

#tst = ['.', 'o', '.', '.', 'x', '.', 'x', '.' ,'x', 'x', '.', 'x', 'x', 'x', '.']
tst1 = ['.', 'o', 'x', 'x', 'x']
tst2 = ['.', '.', 'x', 'x', '.']
tst3 = ['.', 'o', 'x', 'x', '.']
tst4 = ['.', '.', 'x', '.', '.']
tst5 = ['x', '.', 'x', '.', 'o', '.', '.', 'x']
tst6 = ['x', '.', 'x', '.', '.', 'o', '.', '.', 'x']
#tst7 = ['.', 'x', 'x', '.', 'x', 'o', '.', '.', 'x']
#tst8 = ['.', 'x', 'x', '.', '.', 'x', '.', '.', 'x']

def getArrayValues(*arrays, symbol=''):
    arrays_values = {}
    candidate = None
    for indx, array in enumerate(arrays):
        valuecount, maxvalue = 0, 0
        values_ = {}
        opn, connect = False, False
        start = None
        for i, e in enumerate(array):
            neighbors = [array[i+1]] if i==0 else [array[i-1]] if i==len(array)-1 else [array[i+1], array[i-1]]
            if e == '.':
                if i < len(array)-1 and array[i-1]=='.':
                    valuecount = 0
                opn = True if any(x==symbol for x in neighbors) else False
                if any(x==symbol for x in neighbors):
                    valuecount += 1
            elif e == symbol:
                connect = True
                valuecount += 1
            else:
                opn, connect = False, False
                valuecount = 0
            if opn and connect:
                values_[i] = valuecount

        if len(values_.values()) > 0:
            maxvalue = max(values_.values())
            for key in values_.keys():
                if values_[key] == maxvalue:
                    arrays_values[indx] = array[key+1-maxvalue:key+1]
            print("array {array} num {indx}: count = {maxvalue} | {values_}".format(**locals()))
        else:
            print("...not eligible")
    print(arrays_values)
    maxlen = max(len(v) for v in arrays_values.values())
    for k, v in arrays_values.items():
        vstring = "".join(e for e in v)
        vlen = len(v) + (0.5 if (vstring.startswith('.') and vstring.endswith('.')) else 0)
        maxlen = vlen if maxlen < vlen else maxlen
        arrays_values[k] = vlen
    candidate = arrays[list(k for k,v in arrays_values.items() if v==maxlen)[0]]
    print(arrays_values)
    print(candidate)


getArrayValues(tst1, tst2, tst3, tst4, tst5, tst6, symbol='x')
