

def file_inpt(filename, optype, encoding, frtype=''):
    if frtype == "copypaste":
        with open(filename, optype, encoding=encoding) as fi:
            lines = fi.readlines()
            all_data = [(l.strip() if l!='\n' else '0') for l in lines[2:]]
            print(all_data)
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
            print(len(parsed_data))
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



def getCellSetDict(datastr, ilst, forchanges=None):

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
    
    '''
    def getAllArraysSetsDict(all_arrays_dict, celldict):
        return {idxs: [celldict[int(idx)] for i, idx in enumerate(idxs.split(';'))
            if all_arrays_dict[idxs][i]=='0'] for idxs in all_arrays_dict.keys()}
    
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
        newsetslst = setslst
        if len(checkwith) > 0:
            for check_set in checkwith:
                for i, st in enumerate(setslst):
                    if st not in checkwith:
                        changesets[i] = {num for num in st if num not in check_set}
            return changesets

    def applyAllNakedSets(all_arrays_sets_dict):
        found_naked = None
        for indxs_key in all_arrays_sets_dict.keys():
            changes = getArrayNakedSets(all_arrays_sets_dict[indxs_key])
            if changes:
                found_naked = True
                for change_indx, newset in changes.items():
                    celldict[change_indx] = newset
                    all_arrays_sets_dict[indxs_key][change_indx] = newset
        if found_naked:
            return celldict
    
    edited_celldict = applyAllNakedSets(getAllArraysSetsDict(all_arrays_dict, celldict))
    celldict = celldict if not edited_celldict else edited_celldict
    '''
    return celldict if not forchanges else {k: v for k, v in celldict.items() if len(v)==1}



def checkLegal(datastr, ilst):
    all_arrays = getAllArraysDict(datastr, ilst).values()
    for array in all_arrays:
        if any(array.count(x)>1 for x in array if x!='0'):
            return False
    return True



def makeDataChanges(datastr, changesdict):
    changed = None
    for indx in changesdict.keys():
        if len(changesdict[indx]) == 1:
            changed = True
            datastr[indx] = ''.join(changesdict[indx])
    if not changed:
        return changed
    return datastr


'''
def getNxtLenSet(celldict, restricted=[]):
    for k, v in celldict.items():
        if len(v)==2 and k not in restricted:
            return (k, v)

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

def getNumfrSet(prevpicks_lst, findindx, set_):
    taken = getTakenNum(prevpicks_lst, findindx)
    for num in set_:
        if num not in taken:
            return num
    return (len(taken), False)



def runTests(datastr, ilst, prev_sets={}, prev_picks=[], prev_data=[], inicialized=None, count=0):
    #print('\n'.join(''.join(e for e in datastr) for datastr in prev_data))
    #print(len(prev_data), len(set(''.join(e for e in datastr) for datastr in prev_data)))
    print(prev_picks)
    temp_data = datastr[:]
    if temp_data.count('0') == 0:
        if not checkLegal(temp_data, ilst):
            prev_data = prev_data[:-1]
            temp_data = prev_data[-1]
            return runTests(temp_data, ilst, prev_sets, prev_picks, prev_data, count=count+1)
        return temp_data
    else:
        if not inicialized:
            while True:
                new_legit_celldict = getCellSetDict(temp_data, ilst)
                if not new_legit_celldict and not checkLegal(temp_data, ilst):
                    prev_data = prev_data[:-1]
                    temp_data = prev_data[-1]
                    return runTests(temp_data, ilst, prev_sets, prev_picks, prev_data, count=count+1)
                changes = makeDataChanges(temp_data, new_legit_celldict)
                if not changes:
                    break
                temp_data = changes
        
        new_legit_celldict = inicialized if inicialized else new_legit_celldict
        indx, set_ = getNxtLenSet(new_legit_celldict)
        prev_sets[indx] = set_
        while True:
            picknum = getNumfrSet(prev_picks, indx, set_)
            if type(picknum) == str:
                #print(picknum)
                break
            if len(prev_data) > 1:
                prev_data = prev_data[:-1]
                temp_data = prev_data[-1]
            prev_picks = prev_picks[:-picknum[0]]
            indx = prev_picks[-1][0]
            set_ = prev_sets[indx]
            #print("setback", indx, prev_picks)
        temp_data[indx] = picknum
        #print(picknum)
        return runTests(temp_data, ilst, prev_sets, prev_picks+[(indx, picknum)], prev_data+[temp_data], count=count+1)   
'''


def getAllCombs(inptlst, combs=['']):
    if len(inptlst) == 0:
        return combs
    else:
        newcombs = []
        for comb in combs:
            for num in inptlst[0]:
                newcombs.append(comb + num)
        return getAllCombs(inptlst[1:], newcombs)

def getLen2SetsDict(celldict):
    return {k: v for k, v in celldict.items() if len(v)==2}


def runTests(datastr, ilst, celldict):
    tstdict = getLen2SetsDict(celldict)
    indxslst, setslst = list(tstdict.keys()), list(tstdict.values())
    all_combs = getAllCombs(setslst)
    print(len(all_combs))
    reliant = []
    for comb in all_combs:
        temp_data = datastr[:]
        for indx, num in zip(indxslst, comb):
            temp_data[indx] = num
        passed_test = True
        while True:
            new_legit_celldict = getCellSetDict(temp_data, ilst)
            if type(new_legit_celldict)==bool:
                passed_test = False
                break
            changes = makeDataChanges(temp_data, new_legit_celldict)
            if not checkLegal(temp_data, ilst):
                passed_test = False
                break
            if not changes:
                break
            temp_data = changes
        if passed_test:
            if temp_data.count('0')==0:
                return temp_data
            reliant.append((temp_data, new_legit_celldict))
    print(len(reliant))
    if any(x.count('0')==0 for x in [tup[0] for tup in reliant]):
        for temp in reliant:
            if temp[0].count('0')==0:
                return temp[0]
    for temp in reliant:
        temp_data, new_legit_celldict = temp
        new_temp = runTests(temp_data, ilst, new_legit_celldict)
        if new_temp:
            return new_temp



def processData(datastr):
    ilst = getIndxsData(datastr)
    while datastr.count('0') > 0:
        celldict = getCellSetDict(datastr, ilst)
        changes = makeDataChanges(datastr, celldict)
        if not changes:
            #datastr = runTests(datastr, ilst, prev_data=[datastr], inicialized=celldict)
            datastr = runTests(datastr, ilst, celldict)
        else:
            datastr = changes
        print_data(datastr)
        print('*'*15)


              
data_str = file_inpt("tst6.py", 'r', encoding='utf8', frtype="copypaste")
print_data(data_str)
print('*'*15)
processData(list(data_str))
