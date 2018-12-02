from math import sqrt


def file_inpt(filename, optype, encoding):
    with open(filename, optype, encoding=encoding) as fi:
        lines = fi.readlines()
        all_data = [(l.strip() if l!='\n' else '0') for l in lines[2:]]
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
    print('\n'.join(datastr[k-9:k] for k in range(9, len(datastr)+1, 9)))

def getIndxsData(datastr):
    return [i for i in range(len(datastr))]

def getIndxsKey(ilst):
    return ';'.join(str(i) for i in ilst)

def getRows(datastr):
    return [datastr[k-9:k] for k in range(9, len(datastr)+1, 9)]

def getCols(datastr):
    return [datastr[k:len(datastr):9] for k in range(9)]

def getSquares(datastr):
    templst = [datastr[k-3:k] for k in range(3, len(datastr)+1, 3)]
    templst = ''.join([''.join(templst[k:len(templst):3]) for k in range(len(templst)//9)])
    print(templst)
    return [templst[k-9:k] for k in range(9, len(templst)+1, 9)]

def getArraysDict(arrays, datastr, issquare=False):
    if issquare:
        ilst = [num for num in range(len(arrays))]
        ilst = [e for sblst in [ilst[k:len(ilst):int(sqrt(len(ilst)))] for k in range(int(sqrt(len(ilst))))] for e in sblst]
        return {k: v for k, v in sorted(list({i: square for i, square in zip(ilst, arrays)}.items()))}
    return {i: ar for i, ar in enumerate(arrays)}

def getArraysSetsDict(arrays):
    sets_dict = {}
    for i, array in enumerate(arrays):
        sets_dict[i] = {e for e in "123456789" if e not in set(array)}
    return sets_dict

data_str = file_inpt("sudoku_data.py", 'r', encoding='utf8')
print_data(data_str)
print(getRows(data_str))
print(getCols(data_str))
print(getSquares(data_str))
