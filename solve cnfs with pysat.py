from pysat.formula import *
from pysat.solvers import *
import ReadFile
import OutputFile
import time

class Cordinate():
    def __init__(self, x, y, m, n):
        self.top = max(x - 1, 0)
        self.bottom = min(x + 1, m - 1)
        self.left = max(y - 1, 0)
        self.right = min(y + 1, n - 1)   

def encode(x, y, z):
    return x * z + y

def decode(value, z):
    return (value // z, value % z)

def generate_cnfs(map_data: list):
    def at_most_k(k, empty_cells, z):
        number = k + 1
        clause = []
        for comb in itertools.combinations(empty_cells, number):
            cells = list(comb)
            clause.append([-encode(cell[0], cell[1], z) for cell in cells])
        return clause
    
    def at_least_k(k, n, empty_cells, z):
        number = n - k + 1
        clause = []
        for comb in itertools.combinations(empty_cells, number):
            cells = list(comb)
            clause.append([encode(cell[0], cell[1], z) for cell in cells])     
        return clause
    
    m = len(map_data)
    n = len(map_data[0])
    z = max(m, n)
    formula = CNF()
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
                
                # generate cnfs
                if no_traps == 0:
                    for cell in empty_cells:
                        clause = [-encode(cell[0], cell[1], z)]
                        formula.append(clause)
                        if clause not in cnfs:
                            cnfs.append([clause])
                        
                else:
                    f1 = at_most_k(no_traps, empty_cells, z)
                    f2 = at_least_k(no_traps, len(empty_cells), empty_cells, z)
                    if len(f1) > 0:
                        formula.extend(f1)
                        if f1 not in cnfs:
                            cnfs.append(f1)
                    if len(f2) > 0:
                        formula.extend(f2)
                        if f2 not in cnfs:
                            cnfs.append(f2)

    return formula, cnfs

def solve(map_data: list, formula: CNF):
    start = time.time()
    solver = Solver(bootstrap_with=formula)
    solvable = solver.solve()
    if solvable == False:
        print("cant solve")
        quit()
    
    m = len(map_data)
    n = len(map_data[0])
    z = max(m, n)
    
    model = solver.get_model()
    for i in model:
        key = abs(i)
        x, y = decode(key, z)
        
        if map_data[x][y] == '_':
            map_data[x][y] = 'G' if i < 0 else 'T'
                    
    end = time.time()
    return end - start

def print_cnfs(cnfs, map_data):
    m = len(map_data)
    n = len(map_data[0])
    z = max(m, n)
    count = 1
    
    for cnf in cnfs:
        for i in range(len(cnf)):
            clause = ""
            clause += '('
            for j in range(len(cnf[i])):
                value = cnf[i][j]
                x, y = decode(abs(value), z)
                if value < 0:
                    clause += f"~x_{x}_{y}"
                else:
                    clause += f"x_{x}_{y}"
                    
                if j != len(cnf[i]) - 1:
                    clause += ' | '
                else:
                    clause += ') '
                    print(f"{count}: {clause}")
                    count += 1

PATH = 'testcases\\5x5.txt'

def main():
    map_data = ReadFile.read_map(PATH)
    start1 = time.time()
    formula, cnfs = generate_cnfs(map_data)
    end1 = time.time()
    time1 = end1 - start1
    
    time2 = solve(map_data, formula)
    
    print_cnfs(cnfs, map_data)
    
    print(f'Solution:')
    for row in map_data:
        print(row)
        
    print("Generating CNFs time: " + str(time1) + " s")
    print("Solving time: " + str(time2) + " s")
    print("Total time: " + str(time2 + time1) + " s")
    
    OutputFile.output_file(map_data, PATH)
    
if __name__ == '__main__':
    main()