from pysat.formula import *
from pysat.solvers import *
import ReadFile
import time

class Cordinate():
    def __init__(self, x, y, m, n):
        self.top = max(x - 1, 0)
        self.bottom = min(x + 1, m - 1)
        self.left = max(y - 1, 0)
        self.right = min(y + 1, n - 1)   

def generate_cnfs(map_data: list):
    m = len(map_data)
    n = len(map_data[0])
    formula = None
    cnfs = []
    
    for i in range(0, m):
        for j in range(0, n):
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
                
                if len(empty_cells) == 0:
                    continue
                
                f = None
                atoms = []
                clause = None
                
                # generate cnfs
                if no_traps == 0:
                    for cell in empty_cells:
                        # all empty cells are gems
                        atoms.append(Neg(Atom('x_{}_{}'.format(cell[0], cell[1]))))
                        
                    clause = And(atoms[0])
                    
                    if atoms[0] not in cnfs:
                        cnfs.append(atoms[0])
                        
                    for _ in range(1, len(atoms)):
                        clause = clause & atoms[_]   
                        if atoms[_] not in cnfs:
                            cnfs.append(atoms[_])
                    
                    if formula is None:
                        formula = clause
                    else:
                        formula = formula & clause
                        
                else:
                    # at most k of empty_cells contain a trap
                    number = no_traps + 1
                    for comb in itertools.combinations(empty_cells, number):
                        cells = list(comb)
                        atoms = []
                        
                        for cell in cells:
                            atoms.append(Neg(Atom('x_{}_{}'.format(cell[0], cell[1]))))
                            
                        clause = Or(atoms[0])
                        for _ in range(1, len(atoms)):
                            clause = clause | atoms[_]
                    
                        if formula is None:
                            formula = clause
                        else:
                            formula = formula & clause
                            
                        cnfs.append(clause)
                            
                    # at least k of emtpy_cells contains a trap
                    number = len(empty_cells) - no_traps + 1
                    for comb in itertools.combinations(empty_cells, number):
                        cells = list(comb)
                        atoms = []
                        
                        for cell in cells:
                            atoms.append(Atom('x_{}_{}'.format(cell[0], cell[1])))
                            
                        clause = Or(atoms[0])
                        for _ in range(1, len(atoms)):
                            clause = clause | atoms[_]
                            
                        if formula is None:
                            formula = clause
                        else:
                            formula = formula & clause
                            
                        cnfs.append(clause)

    return formula, cnfs

def solve(map_data: list, formula):
    start = time.time()
    solver = Solver(bootstrap_with=formula)
    solvable = solver.solve()
    end = time.time()
    if solvable == False:
        print("cant solve")
        quit()
    
    id_name = formula.export_vpool().id2obj
    model = solver.get_model()
    for i in model:
        if (i in id_name) or (-i in id_name):
            key = i if i in id_name else -i
            string = id_name[key].__str__()
            if ('&' in string) or ('|') in string:
                continue      
            
            li = string.split('_')
            x, y = int(li[1]), int(li[2])
            if map_data[x][y] == '_':
                if string[0] == '~':
                    map_data[x][y] = 'G' if key == i else 'T'
                else:
                    map_data[x][y] = 'T' if key == i else 'G'
                    
    return end - start

PATH = 'testcases\\20x20.txt'

def main():
    map_data = ReadFile.read_map(PATH)
    start1 = time.time()
    formula, cnfs = generate_cnfs(map_data)
    formula.clausify()
    end1 = time.time()
    time1 = end1 - start1

    for i, cnf in enumerate(cnfs):
        print(f"{i + 1}: {cnf}")
        print()
    print()
    
    time2 = solve(map_data, formula)
    
    print(f'Solution:')
    for row in map_data:
        print(row)
        
    print(time1)
    print(time2)
    print(time2 + time1)
    
if __name__ == '__main__':
    main()