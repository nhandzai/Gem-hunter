
import ReadFile
import time




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
        for subcnf in cnf:
            new_subcnf = subcnf.copy()
            new_cnf.append(new_subcnf)
        new_cnfs.append(new_cnf)
    return new_cnfs
    
def DPLL(symbols, cnfs, model,step):
                    
    def satisfies(cnfs, model,len_symbols):
       # print(cnfs)
        if not cnfs:
            return True
   
        for cnf in cnfs:
          #  print("cnf tiep theo",cnf)
            flag_none = False
            clause_satisfied = None
            for subcnf in cnf:
              #  i=0
                for literal in subcnf[:]:
                    #if i==0 and model!= {}:
                    #    i=1
                    #    last_key = list(model.keys())[-1]
                       # print("last key",last_key)
                     #   print("last key",last_key)
                        #print("literal",literal,"last key",last_key)
                    #    if(literal > last_key or -literal > last_key):
                          #  print("1")
                     #       return None

                    if literal in model:
                        if model[literal]:
                            clause_satisfied = True
                       
                            subcnf.remove(literal)
                          

                        else:
                            clause_satisfied = False
                            break
                    elif -literal in model:
                        if model[-literal] == False:
                            clause_satisfied = True
                            subcnf.remove(literal)

 
                           
                        else:
                            clause_satisfied = False
                            break
                    else:
                        flag_none = True


                if clause_satisfied:
                    break
            if clause_satisfied == False and flag_none == False:
                return False
            if clause_satisfied == True and flag_none == False:
                #xoa cnf neu cnf = True
                cnfs.remove(cnf)
           #     print("cnf bi xoa",cnf)
        if len_symbols != len(model):
            return None
        return True
    

    def unit_clauses(symbols, model):
        unit = []
        for symbol in symbols:
            if symbol not in model and -symbol not in model:
                unit.append(symbol)
        return unit

    def extend(model, literal, value):
        new_model = model.copy()
        new_model[literal] = value
        return new_model

    def DPLL_algorithm(symbols, cnfs, model,step):
        satisfied = satisfies(cnfs, model,len(symbols))

        if satisfied== True:

            return model
        if satisfied == False:
            return None
        if step[1] is not None:
            model = extend(model, symbols[step[0]], step[1])
        new_cnfs = Deepcopy(cnfs)
        result = DPLL_algorithm(symbols,new_cnfs, model,step=[step[0]+1,True]) or DPLL_algorithm(symbols, new_cnfs, model,step=[step[0]+1,False])
        if result is not None:
            return result
        return None

    return DPLL_algorithm(symbols, cnfs, model,step)


def extract_symbols(cnfs):
    symbols = set()
    for cnf in cnfs:
        for literals in cnf:
            for literal in literals:
                if abs(literal) not in symbols:
                    symbols.add(abs(literal))
    return list(symbols)
def generate_cnf(map_data):
    cnfs = []

    m = len(map_data)
    n = len(map_data[0])

    for i in range(m):
        for j in range(n):
            if map_data[i][j].isdigit():
                no_traps = int(map_data[i][j])

                if no_traps > 8:
                    raise Exception("Invalid input")

                cordinate = Cordinate(i, j, m, n)

                empty_cells = []

                for a in range(cordinate.top, cordinate.bottom + 1):
                    for b in range(cordinate.left, cordinate.right + 1):
                        if map_data[a][b] == '_':
                            empty_cells.append((a, b))

                if len(empty_cells) < no_traps:
                    print("No solution")
                    quit()

                cnf = []

                if no_traps == 0:
                    subcnf = []
                    for cell in empty_cells:
                        subcnf.append(-cell[0]*n - cell[1] - 1)
                    cnf.append(subcnf)
                else:
                    for comb in combinations(empty_cells, no_traps):
                        traps = list(comb)
                        gems = [cell for cell in empty_cells if cell not in traps]
                        subcnf = []
                        for trap in traps:
                            subcnf.append(trap[0]*n + trap[1] + 1)
                        for gem in gems:
                            subcnf.append(-gem[0]*n - gem[1] - 1)
                        cnf.append(subcnf)

                cnfs.append(cnf)

    return cnfs


def solve(map_data, cnfs, n):
    model = {}
    
    symbols = extract_symbols(cnfs)
    solution = DPLL(symbols, cnfs, model,[-1,None])
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

PATH = 'testcases\\input2.txt'
def main():
    
    map_data = ReadFile.read_map(PATH)
    start = time.time()
    cnfs = generate_cnf(map_data)
    n = len(map_data[0])
    solve(map_data, cnfs, n)
    end = time.time()
    print(end-start)
    


if __name__ == '__main__':
    main()
