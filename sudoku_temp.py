
def file_inpt(filename, optype, encoding):
    with open(filename, optype, encoding=encoding) as fi:
        lines = fi.readlines()
        all_data = [(l.strip() if l!='\n' else '0') for l in lines[2:]]
        print(all_data)
        parsed_data = []
        spotted = None
        for e in all_data:
            if e == '0':
                if not spotted:
                    spotted = True
                    parsed_data.append('')
                else:
                    parsed_data.append(e)
            else:
                spotted = False
                parsed_data.append(e)
        return ''.join(parsed_data) 


def print_data(datastr):
    print('\n'.join(''.join(str(e) for e in datastr[k-9:k]) for k in range(9, len(datastr)+1, 9)))

def getIndxsData(datastr):
    return [i for i in range(len(datastr))]

def getIndxsKey(ilst):
    return ';'.join(str(i) for i in ilst)

def getIntRows(datastr, ilst):
    return {getIndxsKey(ilst[k-9:k]): datastr[k-9:k] for k in range(9, len(datastr)+1, 9)}

def getIntCols(datastr, ilst):
    return {getIndxsKey(ilst[k:len(datastr):9]): datastr[k:len(datastr):9] for k in range(9)}

def getIntSquares(datastr, ilst):
    itmp = [ilst[k-3:k] for k in range(3, len(datastr)+1, 3)]
    newilst = []
    for j in range(3):
        for tripl in itmp[j:(len(datastr)//3):3]:
            for e in tripl:
                newilst.append(e)
    return {getIndxsKey(newilst[k-9:k]): ''.join(datastr[i] for i in newilst[k-9:k]) for k in range(9, len(datastr)+1, 9)}

def getSetforArray(array):
    return {e for e in "123456789" if e not in set(array)}

def getEmptCells(datastr):
    return [i for i in range(len(datastr)) if datastr[i]=='0']

def cellsSetDict(empt_cells, all_arrays_dict):
    celldict = {}
    for indx in empt_cells:
        check_sets = [getSetforArray(all_arrays_dict[k]) for k in all_arrays_dict if str(indx) in k.split(';')]
        numset = {str(e) for e in "123456789"}
        for st in check_sets:
            numset &= st
        if numset == set():
            return False
        celldict[indx] = numset
    return celldict

def makeDataChanges(datastr, celldict):
    changed = None
    for indx in celldict.keys():
        if len(celldict[indx]) == 1:
            changed = True
            datastr[indx] = ''.join(celldict[indx])
    if not changed:
        return changed
    return datastr

def getArraysSetsDict(all_arrays_dict, celldict):
    return {indxs_key: [st for st in all_arrays_dict[indxs_key]] for indxs_key in all_arrays_dict.keys()}

def getArrayNakedSets(setslst):
    checkwith = []
    for i in range(len(setslst)):
        count = 1
        for j, st in enumerate(setslst):
            if i != j: 
                if setslst[i] == st:
                    count += 1
                    if count == len(setslst[i]) and setslst[j] not in checkwith:
                        checkwith.append(setslst[i])
    changesets = {}
    if len(checkwith) > 0:
        for check_set in checkwith:
            for i, st in enumerate(setslst):
                if st not in checkwith:
                    changesets[i] = {num for num in st if num not in check_set}
    else:
        return False
    return changesets

def applyAllNakedSets(all_arrays_sets_dict, celldict):
    found_naked = None
    for indxs_key in all_arrays_sets_dict.key():
        changes = getArrayNakedSets(all_arrays_sets_dict[indxs_key])
        if changes:
            found_naked = True
            for change_indx, newset in changes.items():
                celldict[change_indx] = newset
                all_arrays_sets_dict[indxs_key][change_indx] = newset
    if found_naked:
        return (all_arrays_sets_dict, celldict)
        
            
data_str = file_inpt("tst.py", 'r', encoding='utf8')
print_data(data_str)
print('*'*15)


while data_str.count('0') > 0:
    data_str = list(data_str)
    ilst = getIndxsData(data_str)
    rows, cols, squares = getIntRows(data_str, ilst), getIntCols(data_str, ilst), getIntSquares(data_str, ilst)
    cell_dict = cellsSetDict(getEmptCells(data_str), {**rows, **cols, **squares})
    data_str = makeDataChanges(data_str, cell_dict)
    print_data(data_str)
    print('*'*15)
