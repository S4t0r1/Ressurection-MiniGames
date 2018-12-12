

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
    else:
        if type(frtype)==str:
            return ''.join(frtype)

    

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



def checkLegal(datastr, ilst):
    all_arrays = getAllArraysDict(datastr, ilst).values()
    for array in all_arrays:
        if any(array.count(x)>1 for x in array if x!='0'):
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
        if len(v)==2 and k not in restricted:
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


def getNxtCelldict(datastr, ilst, item):
    indx, picknum = item
    temp_data = datastr[:]
    temp_data[indx] = picknum
    while True:
        celldict = getCellSetDict(temp_data, ilst)
        if not celldict:
            return False if (type(celldict) == bool or not checkLegal(temp_data, ilst)) else ''.join(temp_data)
        changes = makeDataChanges(temp_data, celldict)
        if not changes:
            #print(celldict, '\n')
            return (temp_data, celldict)
        temp_data = changes


def backTrack(datastr, ilst, celldict):
    temp_data = datastr[:]
    prev_picks, prev_sets, restricted = [], {}, []
    prev_data = [(datastr, celldict)]
    indx, set_ = getNxtLenSet(celldict, restricted)
    restricted.append(indx)
    new_celldict = None
    while temp_data.count('0') > 0:
        '''
        temp_data = temp_data[:]
        new_celldict = dict(celldict) if not new_celldict else dict(new_celldict)
        '''
        picknum = getNumfrSet(prev_picks, indx, set_)
        print(prev_picks)
        if type(picknum) == int:
            prev_data = prev_data[:-1]
            
            '''
            if len(prev_data) == 0:
                indx = prev_picks[0][0]
                set_ = prev_sets[indx]
                temp_data, new_celldict = datastr[:], celldict
                continue
            '''
            
            '''
            if len(prev_data) == 0:
                indx, set_ = getNxtLenSet(celldict, restricted)
                restricted.append(indx)
                prev_picks, prev_sets, prev_data = [], {}, []
                temp_data, new_celldict = datastr[:], celldict
                print(restricted)
                continue
            '''
            
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
        #print(''.join(temp_data))



'''
# [(3, '9'), (5, '8'), (2, '4'), (0, '3'), (10, '1'), (10, '5'), (26, '9')]

# [(40, '9'), (1, '8'), (2, '9'), (3, '6'), (3, '7')]
# OR 
# [(8, '3'), (1, '8'), (3, '7'), (22, '2'), (21, '8'), (24, '4'), (24, '6')]
def bckTrck(datastr, ilst, celldict, changes=None, new_celldict=None):
    temp_data = datastr[:]
    prev_data, prev_picks, prev_sets = [], [], {}
    restricted = []
    indx, set_ = getNxtLenSet(celldict)
    restricted.append(indx)
    while True:
        if not changes or not new_celldict:
            picknum = getNumfrSet(prev_picks, indx, set_)
            if type(picknum) == tuple:
                cutlen = picknum[0]
                prev_picks = prev_picks[:-cutlen]
                if len(prev_picks) == 0:
                    indx, set_ = getNxtLenSet(celldict, restricted)
                    restricted.append(indx)
                    prev_data, prev_picks, prev_sets = [], [], {}
                    temp_data = datastr
                    continue
                indx = prev_picks[-1][0]
                set_ = prev_sets[indx]
                continue
                
            temp_data = temp_data[:]
            temp_data[indx] = picknum
            prev_data.append(temp_data)
            prev_picks.append((indx, picknum))
            prev_sets[indx] = set_
        
        print(prev_picks)
        #print('\n'.join(''.join(e for e in temp_data) for temp_data in prev_data))
        new_celldict = getCellSetDict(temp_data, ilst)
        if not new_celldict:
            if type(new_celldict) == bool or not checkLegal(temp_data, ilst):
                prev_data.pop()
                temp_data = prev_data[-1]
                continue 
            else:
                return temp_data
        
        changes = makeDataChanges(temp_data, new_celldict)
        if not changes:
            indx, set_ = getNxtLenSet(new_celldict)
            continue
        temp_data = changes


def tryBckTrcks(datastr, ilst, celldict):
    datastr = datastr[:]
    celldict = dict(celldict)
    while True:
        try:
            temp_data = bckTrck(datastr, ilst, celldict)
        except TypeError:
            continue
        else:
            return ''.join(temp_data)
'''


'''
def backTrack(datastr, ilst, prev_data=[], prev_picks=[], prev_sets={}, restricted=[], count=0):
    #print("\n".join(''.join(e for e in lst) for lst in prev_data))
    #print(prev_picks)
    if count > 200:
        return 
    temp_data = datastr[:]
    if temp_data.count('0') == 0:
        if checkLegal(temp_data, ilst):
            return temp_data 
        prev_data.pop()
        temp_data = prev_data[-1]
        return backTrack(temp_data, ilst, prev_data, prev_picks, prev_sets, restricted, count=count+1)
    else:
        while True:
            celldict = getCellSetDict(temp_data, ilst)
            if not celldict:
                if type(celldict) == bool or not checkLegal(temp_data, ilst):
                    prev_data.pop()
                    temp_data = prev_data[-1]
                    return backTrack(temp_data, ilst, prev_data, prev_picks, prev_sets, restricted, count=count+1)
                return temp_data
            changes = makeDataChanges(temp_data, celldict)
            if not changes:
                break
            temp_data = changes
        
        print("restricted", restricted)
        indx, set_ = getNxtLenSet(celldict, restricted)
        prev_sets[indx] = set_
        if len(prev_data) == 1:
            restricted.append(indx)
        cnt = 0
        print("fresh", prev_picks)
        while True:
            picknum = getNumfrSet(prev_picks, indx, set_)
            if cnt > 0:
                print("check", indx, set_)
            if type(picknum) == str:
                print("won", indx, picknum)
                if cnt > 0:
                    print("wooon")
                break 
            cutlen = picknum[0]
            prev_picks = prev_picks[:-cutlen]
            if len(prev_picks) == 0:
                indx, set_ = getNxtLenSet(celldict, restricted)
                picknum = getNumfrSet(prev_picks, indx, set_)
                break
            else:
                indx = prev_picks[-1][0]
                set_ = prev_sets[indx]
                prev_data.pop()
            cnt += 1
            if cnt > 0:
                print("edited", prev_picks)
        
        temp_data[indx] = picknum
        prev_data.append(temp_data)
        prev_picks.append((indx, picknum))
        if cnt > 0:
            print("out of while", indx, picknum)
            print("new", prev_picks)
        return backTrack(temp_data, ilst, prev_data, prev_picks, prev_sets, restricted, count=count+1)
'''


        
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

def getLenNSetsDict(celldict, nlen=2):
    return {k: v for k, v in celldict.items() if len(v)==nlen}

def runTests(datastr, ilst, celldict):
    tstdict = getLenNSetsDict(celldict)
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
    for temp in reliant:
        temp_data, new_legit_celldict = temp
        new_temp = runTests(temp_data, ilst, new_legit_celldict)
        if new_temp:
            return new_temp
'''



def processData(datastr):
    ilst = getIndxsData(datastr)
    while datastr.count('0') > 0:
        celldict = getCellSetDict(datastr, ilst)
        changes = makeDataChanges(datastr, celldict)
        if not changes:
            datastr = backTrack(datastr, ilst, celldict)
            #datastr = tryBckTrcks(datastr, ilst, celldict)
            #datastr = backTrack(datastr, ilst, prev_data=[datastr])
            #datastr = runTests(datastr, ilst, celldict)
        else:
            datastr = changes
        print_data(datastr)
        print('*'*15)


              
data_str = file_inpt("tst3.py", 'r', encoding='utf8', frtype="copypaste")
data_str2 = "000000000010620090002009310004006080008702100030800500069100400080073050000000000"
print_data(data_str)
print('*'*15)
processData(list(data_str))
