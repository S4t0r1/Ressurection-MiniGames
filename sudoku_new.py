
def file_inpt(filename, optype, encoding):
    with open(filename, optype, encoding=encoding) as fi:
        lines = fi.readlines()
        all_data = [(l.strip() if l!='\n' else '0') for l in lines[2:]]
        parsed_data = []
        spotted = None
        for i, e in enumerate(all_data):
            if e == '0':
                if not spotted and not any(i==x for x in (0, len(all_data)-1)):
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
    return {getIndxsKey(newilst[k-9:k]): [datastr[i] for i in newilst[k-9:k]] for k in range(9, len(datastr)+1, 9)}

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
            print(celldict[indx])
    if changed:
        return datastr

def getAllArraysSetsDict(all_arrays_dict, celldict):
    return {idxs: [celldict[int(idx)] for i, idx in enumerate(idxs.split(';')) if all_arrays_dict[idxs][i]=='0'] for idxs in all_arrays_dict.keys()}

def getArrayNakedSets(setslst):
    print(setslst)
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
    newsetslst = setslst
    if len(checkwith) > 0:
        for check_set in checkwith:
            for i, st in enumerate(setslst):
                if st not in checkwith:
                    changesets[i] = {num for num in st if num not in check_set}
                    newsetslst[i] = {num for num in st if num not in check_set}
        print(newsetslst)
        return changesets
    else:
        return

def applyAllNakedSets(all_arrays_dict, celldict, all_arrays_sets_dict=None):
    if not all_arrays_sets_dict:
        all_arrays_sets_dict = getAllArraysSetsDict(all_arrays_dict, celldict)
    found_naked = None
    for indxs_key in all_arrays_sets_dict.keys():
        changes = getArrayNakedSets(all_arrays_sets_dict[indxs_key])
        if changes:
            found_naked = True
            for change_indx, newset in changes.items():
                celldict[change_indx] = newset
                all_arrays_sets_dict[indxs_key][change_indx] = newset
    if found_naked:
        return (celldict, all_arrays_sets_dict)
        

def processChangeAndUpdate(datastr, ilst, cell_dict=None, all_arrays_sets_dict=None):
    print("processing")
    rows, cols, squares = getIntRows(datastr, ilst), getIntCols(datastr, ilst), getIntSquares(datastr, ilst)
    all_arrays_dict = {**rows, **cols, **squares}
    if not cell_dict and not all_arrays_sets_dict:
        emptcells_lst = getEmptCells(data_str)
        if len(emptcells_lst) == 0:
            return data_str
        cell_dict = cellsSetDict(getEmptCells(data_str), all_arrays_dict)
        if not cell_dict:
            return print("ERROR")
    changed_datastr = makeDataChanges(datastr, cell_dict)
    if changed_datastr:
        datastr = changed_datastr
        print_data(datastr)
        print('*'*15)
        return processChangeAndUpdate(datastr, ilst)
    dicts_changes = applyAllNakedSets(all_arrays_dict, cell_dict, all_arrays_sets_dict if all_arrays_sets_dict else None)
    if dicts_changes:
        print("dicts changes")
        cell_dict, all_arrays_sets_dict = dicts_changes
        return processChangeAndUpdate(datastr, ilst, cell_dict, all_arrays_sets_dict)
    else:
        return data_str
        

data_str = file_inpt("tst3.py", 'r', encoding='utf8')
print_data(data_str)
print('*'*15)


ilst = getIndxsData(data_str)
while data_str.count('0') > 0:
    data_str = list(data_str)
    data_str = processChangeAndUpdate(data_str, ilst)
    print_data(data_str)
    print('*'*15)
