
import ReadFile
import time
import itertools
import cProfile
class Cordinate():
    def __init__(self, x, y, m, n):
        self.top = max(x - 1, 0)
        self.bottom = min(x + 1, m - 1)
        self.left = max(y - 1, 0)
        self.right = min(y + 1, n - 1)


def combinations(iterable, r):
    # Generate combinations of size r from iterable
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
        
    def satisfies(cnfs,model,last_key ):
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
            new_cnfs = satisfies(cnfs,model, last_key)
            if new_cnfs ==None:
                return False
        else:
            new_cnfs = Deepcopy(cnfs)
        if   step[1] == None or literal_info[abs(last_key)][1]<literal_info[abs(last_key)][0]:
            result = DPLL_algorithm(symbols,new_cnfs, model,step=[step[0]+1,False],last_key=last_key,literal_info=literal_info,) or DPLL_algorithm(symbols, new_cnfs, model,step=[step[0]+1,True],last_key=last_key,literal_info=literal_info,)
        else:
            result = DPLL_algorithm(symbols,new_cnfs, model,step=[step[0]+1,True],last_key=last_key,literal_info=literal_info,) or DPLL_algorithm(symbols, new_cnfs, model,step=[step[0]+1,False],last_key=last_key,literal_info=literal_info,)
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
def Most_Digit(variables, k):
    results = []
    for comb in combinations(variables, k + 1):
        temp = []
        for x in comb:
            temp.append(-x)
        results.append(temp)
    return results

def Least_Digit(variables, k):
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

def modified_function(cnf_instance):
    new_cnf = []
    for i, clause1 in enumerate(cnf_instance):
        keep_clause = True
        for j, clause2 in enumerate(cnf_instance):
              if clause1 != clause2 and set(clause1) >= set(clause2):
     #           print("false",clause1,clause2)
                keep_clause = False
                break
    #    print("clause:",clause1,)
        if keep_clause:
   #         print("true",clause1)
            new_cnf.append(clause1)
    return new_cnf

def simplify_cnf(cnf):
    # Loại bỏ các mệnh đề trùng lặp
    cnf = modified_function(cnf)

    return cnf
def generate_cnf(map_data): 
    cnf = []
    literal_info = {}
    row = len(map_data)
    col = len(map_data[0])    
    for i in range(row):
        for j in range(col):
            if map_data[i][j] != '_':
                digit_ = int(map_data[i][j])
                valid_cell = []
                for x in [-1, 0, 1]:
                    for y in [-1, 0, 1]:
                        if x != 0 or y != 0:
                            ix, jy = i + x, j + y
                            if 0 <= ix < row and 0 <= jy < col:
                                if map_data[ix][jy] == '_':
                                    valid_cell.append(ix*col + jy + 1)
                
                if (digit_ == len(valid_cell)):
                    for cell in valid_cell:
                        cnf.append([cell])
                else:
                    U_kn = Most_Digit(valid_cell, digit_)
                    L_kn = Least_Digit(valid_cell, digit_)
                    for clause in U_kn:
                            cnf.append(clause)
                    for clause in L_kn:
                        if clause not in cnf: 
                            cnf.append(clause)    
    print(cnf)
    cnf = simplify_cnf(cnf)
    for clause in cnf:
        for literal in clause:
            abs_literal = abs(literal)
            if abs_literal not in literal_info:
                literal_info[abs_literal] = [0, 0,]  # [Số lần, Số lần âm, Số lần dương]

            if literal > 0:
                literal_info[abs_literal][1] += 1
            else:
                literal_info[abs_literal][0] += 1
    sorted_literal_info = sorted(literal_info.items(), key=lambda x: x[1][0] + x[1][1], reverse=True)
    sorted_literal_info_dict = {k: v for k, v in sorted_literal_info}
   # print(literal_info)
    print (sorted_literal_info)
    return cnf, sorted_literal_info_dict
   

def solve(map_data, cnfs, n,literal_info):
    
    model = {}
    symbols = extract_symbols(cnfs)
    #new_cnfs= simplify_cnf(cnfs)
    solution = DPLL(symbols, cnfs, model,[-1,None],literal_info)
    
    if solution is not None:
        print("Solution:")
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
            print(map_data[i])
    else:
        print("No solution")
PATH = 'testcases\\20x20.txt'
def main():
    
    map_data = ReadFile.read_map(PATH)
    start = time.time()
    cnfs,literal_info = generate_cnf(map_data)
    n = len(map_data[0])
    solve(map_data, cnfs, n, literal_info)
    end = time.time()
    print(end-start)
    #print(cnfs)
#def profile_main():
 #   main()
    


if __name__ == '__main__':
  #  cProfile.run('profile_main()')
    main()

    
