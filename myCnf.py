import ReadFile
import OutputFile
import time


class Cordinate():
    def __init__(self, x, y, m, n):
        self.top = max(x - 1, 0)
        self.bottom = min(x + 1, m - 1)
        self.left = max(y - 1, 0)
        self.right = min(y + 1, n - 1)


def combinations(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    if r > n: 
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)


def Deepcopy (cnfs):
    new_cnfs = []
    for cnf in cnfs:
        new_cnf = []
        for literal in cnf:
            new_cnf.append(literal)
        new_cnfs.append(new_cnf)
    return new_cnfs
    
def DPLL(symbols, cnfs, model,step,literal_info):
        
    def satisfies(cnfs,last_key ):
        new_cnfs=[]
        for cnf in cnfs:
            new_cnf=[]
            for literal in cnf:
                if literal == last_key:
                    new_cnf=None
                    break
                if literal == -last_key:
                    continue
                new_cnf.append(literal)
            if  new_cnf ==[]:
                return None
            if new_cnf != None:
                new_cnfs.append(new_cnf)
        return new_cnfs
    
    def extend(model, literal, value):
        new_model = model.copy()

        new_model[literal] = value
        if value == True:
            return new_model,literal
        else:
            return new_model,-literal

    def DPLL_algorithm(symbols, cnfs, model,step,last_key, literal_info):
        if cnfs == []:
            return model
        new_cnfs = None
        if step[1] is not None:
            model,last_key = extend(model, symbols[step[0]], step[1])
            new_cnfs = satisfies(cnfs, last_key)
            if new_cnfs ==None:
                return False
        else:
            new_cnfs = Deepcopy(cnfs)

        if   step[1] == None or literal_info[abs(last_key)][1]<literal_info[abs(last_key)][0]:
            result = DPLL_algorithm(symbols,new_cnfs, model,step=[step[0]+1,False],last_key=last_key,literal_info=literal_info) or DPLL_algorithm(symbols, new_cnfs, model,step=[step[0]+1,True],last_key=last_key,literal_info=literal_info)
        else:
            result = DPLL_algorithm(symbols,new_cnfs, model,step=[step[0]+1,True],last_key=last_key,literal_info=literal_info) or DPLL_algorithm(symbols, new_cnfs, model,step=[step[0]+1,False],last_key=last_key,literal_info=literal_info)
        if result is not None:

            return result
        return None

    return DPLL_algorithm(symbols, cnfs, model,step,0,literal_info)


def extract_symbols(cnfs):
    symbols = set()
    for cnf in cnfs:
        for literal in cnf:
            if abs(literal) not in symbols:
                symbols.add(abs(literal))
    return list(symbols)
def U_Function(variables, k):
    results = []
    for comb in combinations(variables, k + 1):
        temp = []
        for x in comb:
            temp.append(-x)
        results.append(temp)
    return results

def L_Function(variables, k):
    results = []
    for comb in combinations(variables, len(variables) - k + 1):
        temp = []
        for x in comb:
            temp.append(x)
        results.append(temp)
    return results
def permutations(lst, n):
    if n == 0:
        yield []
    else:
        for i in range(len(lst)):
            for perm in permutations(lst[:i] + lst[i+1:], n - 1):
                yield [lst[i]] + perm
def simplify_function(cnf):
    new_cnf = []
    unit_clause = []
    for clause1 in cnf:
        keep_clause = True
        for clause2 in cnf:
              if clause1 != clause2 and set(clause1) >= set(clause2):
                keep_clause = False
                break
        if keep_clause:
            new_cnf.append(clause1)
            if len(clause1) == 1:
                unit_clause.append(clause1[0])
    new_cnfs = []
    for clause in cnf:
            new_clause=[]
            for literal in clause:
                if literal in unit_clause :
                    new_clause=None
                    break
                if -literal in unit_clause:
                    continue
                new_clause.append(literal)
            if new_clause != None:
                new_cnfs.append(new_clause)
    return new_cnfs,unit_clause

def generate_cnf(map_data): 
    cnf = []
    row = len(map_data)
    col = len(map_data[0])    
    for i in range(row):
        for j in range(col):
            if map_data[i][j].isdigit():
                no_traps = int(map_data[i][j])
                empty_cells = []
                for x in [-1, 0, 1]:
                    for y in [-1, 0, 1]:
                        if x != 0 or y != 0:
                            x_, y_ = i + x, j + y
                            if 0 <= x_ < row and 0 <= y_ < col:
                                if map_data[x_][y_] == '_':
                                    empty_cells.append(x_*col + y_ + 1)
                
                if (no_traps != len(empty_cells)):
                    U_kn = U_Function(empty_cells, no_traps)
                    L_kn = L_Function(empty_cells, no_traps)
                    for clause in U_kn:
                            cnf.append(clause)
                    for clause in L_kn:
                        if clause not in cnf: 
                            cnf.append(clause)      
                else:
                    for cell in empty_cells:
                        cnf.append([cell])   

              
    return cnf
def simplify_cnfs(cnf):
    cnf,unit_clause = simplify_function(cnf)
    literal_info = {}
    for clause in cnf:
        for literal in clause:

            abs_literal = abs(literal)
            if abs_literal not in literal_info:
                literal_info[abs_literal] = [0, 0]  # [Số lần, Số lần âm, Số lần dương]

            if literal > 0:
                literal_info[abs_literal][1] += 1
            else:
                literal_info[abs_literal][0] += 1
    sorted_literal_info = sorted(literal_info.items(), key=lambda x: x[1][0] + x[1][1], reverse=True)
    sorted_literal_info_dict = {k: v for k, v in sorted_literal_info}
    return cnf, sorted_literal_info_dict,unit_clause
def create_model(unit_clause):
    model = {}
    for clause in unit_clause:
        if clause > 0:
            model[clause] = True
        else:
            model[-clause] = False
    return model
def solve(map_data, cnfs, n):
    cnfs,literal_info,unit_clause= simplify_cnfs(cnfs)
    model = create_model(unit_clause)
    symbols = extract_symbols(cnfs)
    solution = DPLL(symbols, cnfs, model,[-1,None],literal_info)
    if solution is not None:
        for i in range(len(map_data)):
            for j in range(len(map_data[0])):
               if map_data[i][j] == '_':
                    if  i*n + j + 1 in solution:
                        if  solution[ i*n + j + 1] == True:
                            map_data[i][j] = 'T'
                        else:
                            map_data[i][j] = 'G'
                    else:
                        map_data[i][j] = '_'
    else:
        print("No solution")
PATH = 'testcases\\20x20.txt'
def main():
    
    map_data = ReadFile.read_map(PATH)
    start1 = time.time()
    cnfs = generate_cnf(map_data)
    end1 = time.time()
    time1 = end1 - start1
    start2 = time.time()
   
    n = len(map_data[0])
    solve(map_data, cnfs, n)
    end2 = time.time()
    time2 = end2 - start2
    
    print(f'Solution:')
    for row in map_data:
        print(row)
            
    print("Generating CNFs time: " + str(time1) + " s")
    print("Solving time: " + str(time2) + " s")
    print("Total time: " + str(time2 + time1) + " s")
    
    OutputFile.output_file(map_data, PATH)
if __name__ == '__main__':
    main()

    
