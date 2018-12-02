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
    print('\n'.join(datastr[k-9:k] for k in range(0, len(datastr)+1, 9)))

data_str = file_inpt("sudoku_data.py", 'r', encoding='utf8')
print_data(data_str)

def getRows(datastr):
    return [datastr[k-9:k] for k in range(0, len(datastr)+1, 9)][1:]

print(getRows(data_str))

def getCols(datastr):
    return [datastr[k:len(datastr):9] for k in range(9)]

print(getCols(data_str))

rows = getRows(data_str)

for row in rows:
    
