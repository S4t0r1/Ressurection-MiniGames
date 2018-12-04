
from math import sqrt


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
    templst = [(getIndxsKey(ilst[k-3:k]), datastr[k-3:k]) for k in range(3, len(datastr)+1, 3)]
    ilst, elst = [item[0] for item in templst], [item[1] for item in templst]
    templst = []
    for k in range(len(elst)//9):
        templst.append((getIndxsKey(ilst[k:len(ilst):3]).split(';'), ''.join(elst[k:len(elst):3])))
    ilst = [indx for indxlst in [item[0] for item in templst] for indx in indxlst]
    elst = ''.join(str(e) for e in [item[1] for item in templst])
    return {getIndxsKey(ilst[k-9:k]): elst[k-9:k] for k in range(9, len(elst)+1, 9)}

def getSetforArray(array):
    return {e for e in "123456789" if e not in set(array)}

data_str = file_inpt("test.py", 'r', encoding='utf8')
print_data(data_str)
print('*'*15)


while data_str.count('0') > 0:
    data_str = list(data_str)
    rows = getIntRows(data_str, getIndxsData(data_str))
    cols = getIntCols(data_str, getIndxsData(data_str))
    squares = getIntSquares(''.join(data_str), getIndxsData(data_str))
    all_arrays = {**rows, **cols, **squares}
    for i in range(len(data_str)):
        check_sets = []
        for key in all_arrays.keys():
            if str(i) in key.split(';') and data_str[i]=='0':
                check_sets.append(getSetforArray(all_arrays[key]))
        candidate = {str(e) for e in "123456789"}
        for st in check_sets:
            candidate &= st
        if len(candidate)==1:
            data_str[i] = ''.join(candidate)
    print_data(data_str)
    print('*'*15)
