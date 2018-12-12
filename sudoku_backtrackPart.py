
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
            return (temp_data, celldict)
        temp_data = changes


def backTrack(datastr, ilst, celldict):
    temp_data = datastr[:]
    prev_picks, restricted = [], []
    indx, set_ = getNxtLenSet(celldict, restricted)
    while temp_data.count('0') > 0:
        picknum = getNumfrSet(prev_picks, indx, set_)
        if type(picknum) == int:
            prev_picks = prev_picks[:-2]
            indx, set_ = getNxtLenSet(celldict, restricted)
            continue
        prev_picks.append((indx, picknum))
        new_data = getNxtCelldict(temp_data, ilst, prev_picks[-1])
        if not new_data:
            continue  
        temp_data, celldict = new_data
    return ''.join(temp_data)
