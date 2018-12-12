
def file_inpt(filename, optype, encoding, frtype=''):
    if frtype == "copypaste":
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
    else:
        if type(frtype)==str:
            return ''.join(frtype)

    
def print_data(datastr, filename=None, end=False):
    datastr = '\n'.join(''.join(str(e) for e in datastr[k-9:k]) for k in range(9, len(datastr)+1, 9))
    print("{} ({})\n\n{}\n{}".format("START" if not end else "END", filename if filename else 'str', datastr, '*'*13))

def getIndxsData(datastr):
    return [i for i in range(len(datastr))]


def getAllArraysDict(datastr, ilst):
    
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
    
    return {**getIntRows(datastr, ilst), **getIntCols(datastr, ilst), **getIntSquares(datastr, ilst)}


def getCellSetDict(datastr, ilst):
    
    def getSetforArray(array):
        return {e for e in "123456789" if e not in set(array)}

    def getEmptCells(datastr):
        return [i for i in range(len(datastr)) if datastr[i]=='0']

    all_arrays_dict = getAllArraysDict(datastr, ilst)
    empt_cells = getEmptCells(datastr)
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


def checkLegal(datastr, ilst):
    all_arrays = getAllArraysDict(datastr, ilst).values()
    for array in all_arrays:
        if any(array.count(x) > 1 for x in array if x!='0'):
            return False
    return True


def makeDataChanges(datastr, celldict):
    changed = None
    for indx in celldict.keys():
        if len(celldict[indx]) == 1:
            changed = True
            datastr[indx] = ''.join(celldict[indx])
    if not changed:
        return changed
    return datastr


def getNxtLenSet(celldict, restricted=[]):
    for k, v in celldict.items():
        if len(v) == 2 and k not in restricted:
            return (k, v)
        

def getNumfrSet(prevpicks_lst, findindx, set_):
    
    def getTakenNum(prevpicks_lst, findindx):
        if len(prevpicks_lst) == 0:
            return ['']
        matches = []
        for item in prevpicks_lst:
            indx, num = item
            if indx == findindx:
                matches.append(num)
            if len(matches) == 2:
                break
        return [''] if len(matches) == 0 else matches
        
    taken = getTakenNum(prevpicks_lst, findindx)
    for num in set_:
        if num not in taken:
            return num
    return len(taken)


def getNxtCelldict(datastr, ilst, item=None):
    temp_data = datastr[:]
    if item:
        indx, picknum = item
        temp_data[indx] = picknum
    while True:
        celldict = getCellSetDict(temp_data, ilst)
        if not celldict:
            return False if (type(celldict) == bool or not checkLegal(temp_data, ilst)) else ''.join(temp_data)
        changes = makeDataChanges(temp_data, celldict)
        if not changes:
            return (temp_data, celldict)
        temp_data = changes


def backTrack(datastr, ilst, celldict):
    temp_data = datastr[:]
    prev_picks, prev_sets, restricted = [], {}, []
    prev_data = [(datastr, celldict)]
    indx, set_ = getNxtLenSet(celldict, restricted)
    restricted.append(indx)
    while True:
        picknum = getNumfrSet(prev_picks, indx, set_)
        if type(picknum) == int:
            prev_data = prev_data[:-1]
            temp_data, new_celldict = prev_data[-1]
            prev_picks = prev_picks[:-2]
            indx = prev_picks[-1][0]
            set_ = prev_sets[indx]
            continue
        prev_picks.append((indx, picknum))
        prev_sets[indx] = set_
        new_data = getNxtCelldict(temp_data, ilst, prev_picks[-1])
        if not new_data:
            continue
        if type(new_data) == str:
            return new_data
        temp_data, new_celldict = new_data
        prev_data.append((temp_data, new_celldict))
        indx, set_ = getNxtLenSet(new_celldict)


def processData(datastr, filename=None):
    ilst = getIndxsData(datastr)
    print_data(datastr, filename)
    while datastr.count('0') > 0:
        celldict = getCellSetDict(datastr, ilst)
        changes = makeDataChanges(datastr, celldict)
        if not changes:
            datastr = backTrack(datastr, ilst, celldict)
        else:
            datastr = changes
    print_data(datastr, filename, end=True)


def solveAll(filenames):
    for filename in filenames:
        data_str = file_inpt(filename, 'r', encoding='utf8', frtype="copypaste")
        processData(list(data_str), filename)

# example file lst, it can be anything like sys.argv[1:] for example...
filenames_lst = ["tst1.py", "tst2.py", "tst3.py", "tst4.py", "tst5.py", "tst6.py"]
solveAll(filenames_lst)
