
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


def makeDataChanges(datastr, celldict):
    changed = None
    for indx in celldict.keys():
        if len(celldict[indx]) == 1:
            changed = True
            datastr[indx] = ''.join(celldict[indx])
    if not changed:
        return changed
    return datastr


def pickItem(celldict, takenlst, lenlimit=2):
    for indx in celldict.keys():
        if len(celldict[indx]) == lenlimit and indx not in taken:
            return (indx, celldict[indx])
    return pickItem(celldict, takenlst, lenlimit + 1)


def tryNum(datastr, ilst, celldict, takenlst):
    print("trying")
    indx, set_ = pickItem(celldict, takenlst)
    temp = datastr
    for num in set_:
        temp[indx] = num
        if getCellSetDict(temp, ilst):
            return (temp, indx)


def processData(datastr):
    ilst = getIndxsData(datastr)
    takenlst = []
    while datastr.count('0') > 0:
        celldict = getCellSetDict(datastr, ilst)
        changes = makeDataChanges(datastr, celldict)
        if not changes:
            datastr, taken_new = tryNum(datastr, ilst, celldict, takenlst)
            takenlst.append(taken_new)
        else:
            datastr = changes
        print_data(datastr)
        print('*'*15)
        
              
data_str = file_inpt("tst.py", 'r', encoding='utf8')
print_data(data_str)
print('*'*15)
processData(list(data_str))
