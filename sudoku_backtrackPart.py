
def getNxtCelldict(datastr, ilst, item):
    indx, picknum = item
    temp_data = datastr[:]
    temp_data[indx] = picknum
    while True:
        celldict = getCellSetDict(temp_data, ilst)
        if not celldict:
            return False
        changes = makeDataChanges(temp_data, celldict)
        if not changes:
            #print(celldict, '\n')
            return (temp_data, celldict)
        temp_data = changes


def backTrack(datastr, ilst, celldict):
    temp_data = datastr[:]
    prev_picks, prev_sets, restricted = [], {}, []
    prev_data = []
    indx, set_ = getNxtLenSet(celldict, restricted)
    restricted.append(indx)
    while temp_data.count('0') > 0:
        picknum = getNumfrSet(prev_picks, indx, set_)
        if type(picknum) == int:
            prev_data = prev_data[:-1]
            if len(prev_data) == 0:
                indx, set_ = getNxtLenSet(celldict, restricted)
                restricted.append(indx)
                prev_picks, prev_sets, prev_data = [], {}, []
                print(restricted)
                continue
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
        else:
            temp_data, new_celldict = new_data
            prev_data.append((temp_data, new_celldict))
            indx, set_ = getNxtLenSet(new_celldict)
    return ''.join(temp_data)
