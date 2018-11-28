
#tst = ['.', 'o', '.', '.', 'x', '.', 'x', '.' ,'x', 'x', '.', 'x', 'x', 'x', '.']
tst1 = ['.', 'o', 'x', 'x', 'x']
tst2 = ['.', '.', 'x', 'x', '.']
tst3 = ['.', 'o', 'x', 'x', '.']
tst4 = ['.', '.', 'x', '.', '.']
tst5 = ['x', '.', 'x', '.', 'o', '.', '.', 'x']
tst6 = ['x', '.', 'x', '.', '.', 'o', '.', '.', 'x']
tst7  = ['o', '.', 'x', 'x', '.']
tst8 = ['.', 'x', 'x', '.', 'x', 'o', '.', '.', 'x']
tst9 = ['.', 'x', 'x', '.', '.', 'x', '.', '.', 'x']

def getLinearNeighbors(array, *args):
    neighbors = []
    for i in args:
        for cell in [array[i+1]] if i==0 else [array[i-1]] if i==len(array)-1 else [array[i+1], array[i-1]]:
            neighbors.append(cell)
    return neighbors

def getIndx_frSubarray(prim_data, secon_data):
    str_, substr = ''.join(e for e in prim_data), ''.join(e for e in secon_data)
    sindx = str_.index(substr)
    eindx = sindx+(len(substr)-1)
    return (sindx, eindx)

def getArraysValues(arrays, symbol):
    arrays_values = {}
    candidate = None
    for indx, array in enumerate(arrays):
        valuecount, maxvalue = 0, 0
        values_ = {}
        opn, connect = False, False
        start = None
        for i, e in enumerate(array):
            neighbors = getLinearNeighbors(array, i)
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
                    arrays_values[indx if symbol!='o' else str(indx)] = array[key+1-maxvalue:key+1]
    return arrays_values

def getBestArrays(arrays, arrays_values, symbol):
    maxlen = max(len(v) for v in arrays_values.values())
    for k, v in arrays_values.items():
        indx = int(k)
        vstring = "".join(e for e in v)
        vlen = len(v) + (0.5 if (vstring.startswith('.') and vstring.endswith('.')) else 0)
        if type(vlen)==float:
            sindx, eindx = getIndx_frSubarray(arrays[indx], arrays_values[k])
            if any(x==('.'or symbol) for x in getLinearNeighbors(arrays[indx], sindx, eindx)):
                vlen = vlen + 1
        if vstring.count(symbol)==3:
            if (type(vlen)==int and vstring.count('.')>=1) or (type(vlen)==float and vstring.count('.')%2!=0):
                vlen = 10
        maxlen = vlen if maxlen < vlen else maxlen
        arrays_values[k] = vstring, vlen
    if type(maxlen)==int:
        for k, v in arrays_values.items():
            indx = int(k)
            vstring, vlen = v
            if vlen==maxlen:
                sindx, eindx = getIndx_frSubarray(arrays[indx], arrays_values[k][0])
                if any(x==('.' or symbol) for x in (arrays[indx][sindx-1] if sindx>0 else '', 
                                    arrays[k][eindx+1] if eindx<len(arrays[k])+1 else '')):
                    maxlen = vlen + 1
                    arrays_values[k] = vstring, maxlen
    arrays_values = {k: v for k,v in arrays_values.items() if v[1]==maxlen}
    return arrays_values, maxlen

all_arrays = tst1, tst2, tst3, tst4, tst5, tst6, tst7, tst8, tst9

def bestArray(arrayslst, symb1='', symb2=''):
    arraysdict_s1 = getArraysValues(all_arrays, symb1)
    arraysdict_s2 = getArraysValues(all_arrays, symb2)
    best_array_s1, maxval1 = getBestArrays(all_arrays, arraysdict_s1, symb1)
    best_array_s2, maxval2 = getBestArrays(all_arrays, arraysdict_s2, symb2)
    maxval = maxval1 if maxval1 > maxval2 else maxval2
    best_array = {k: v[1] for k,v in {**best_array_s1, **best_array_s2}.items() if v[1]==maxval}
    candidate = None
    if len(best_array.keys()) > 1:
        for k in best_array.keys():
            if best_array[k]==10:
                if type(k)==str:
                    candidate = all_arrays[int(k)]
                    break
                candidate = all_arrays[k]
                break
            else:
                if type(k)==int:
                    candidate = all_arrays[k]
                    break
                candidate = all_arrays[int(k)]
                break
    else:
        candidate = all_arrays[int(list(best_array.keys())[0])]
    return candidate


print(bestArray(all_arrays, 'x', 'o'))
