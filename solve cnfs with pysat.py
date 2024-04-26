from pysat.formula import *
from pysat.solvers import *
import ReadFile

PATH = 'testcases\\input2.txt'

class Cordinate():
    def __init__(self, x, y, m, n):
        self.top = max(x - 1, 0)
        self.bottom = min(x + 1, m - 1)
        self.left = max(y - 1, 0)
        self.right = min(y + 1, n - 1)   

def generate_whatever_i_have_to(map_data: list):
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
                    f = clause
                        
                else:
                    for comb in itertools.combinations(empty_cells, no_traps):
                        # comb is a possible combination of cells that are traps
                        traps = list(comb)
                        gems = [cell for cell in empty_cells if cell not in traps]
                        atoms = []
                        
                        for trap in traps:
                            atoms.append(Atom('x_{}_{}'.format(trap[0], trap[1])))
                        for gem in gems:
                            atoms.append(Neg(Atom('x_{}_{}'.format(gem[0], gem[1]))))
                            
                        clause = And(atoms[0])
                        for _ in range(1, len(atoms)):
                            clause = clause & atoms[_]
                            
                        if f is None:
                            f = clause
                        else:
                            f = f | clause
                            
                if formula is None:
                    formula = f
                else: 
                    formula = formula & f

                if no_traps != 0:
                    cnfs.append(f)

    return formula, cnfs

def solve(map_data: list, formula):
    solver = Solver(bootstrap_with=formula)
    if solver.solve() == False:
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
           
    print(f'Solution:')
    for row in map_data:
        print(row)

def main():
    map_data = ReadFile.read_map(PATH)
    formula, cnfs = generate_whatever_i_have_to(map_data)
    formula.clausify()

    # temp = formula.export_vpool().id2obj
    # for key, value in temp.items():
    #     print(f"{key}: {value}")
    # print()

    for i, cnf in enumerate(cnfs):
        print(f"{i + 1}: {cnf}")
        print()
    print()

    solve(map_data, formula)
    
if __name__ == '__main__':
    main()