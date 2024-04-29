import ReadFile
import time

def checker(map_data, pos):
    count = 0
    empty_count = 0
    top = max(0, pos[0]-1)
    bot = min(len(map_data)-1, pos[0]+1)
    left = max(0, pos[1]-1)
    right = min(len(map_data[0])-1, pos[1]+1)

    n = int(map_data[pos[0]][pos[1]])
    for i in range(top, bot+1):
        for j in range(left, right+1):
            if map_data[i][j] == 'T':
                count = count+1
                if (count > n):
                    return False
            if map_data[i][j] == '_':
                empty_count = empty_count+1
    if empty_count == 0 and count < n:
        return False

    return True


def multiCheck(map_data, pos):
    top = max(0, pos[0]-1)
    bot = min(len(map_data)-1, pos[0]+1)
    left = max(0, pos[1]-1)
    right = min(len(map_data[0])-1, pos[1]+1)
    for i in range(top, bot+1):
        for j in range(left, right+1):
            check_pos = (i, j)
            if map_data[i][j].isdigit():
                if (checker(map_data, check_pos) == False):
                    return False
    return True


def backTracking(map_data, empty_pos, step=0):
    if step == len(empty_pos):
        return True

    i, j = empty_pos[step]
    for symbol in ('T', 'G'):
        map_data[i][j] = symbol
        if multiCheck(map_data, (i, j)):
            if backTracking(map_data, empty_pos, step + 1):
                return True

    map_data[i][j] = '_'
    return False


def bruteForce(map_data, empty_pos, step=0):
    if step == len(empty_pos):
        if all(multiCheck(map_data, pos) for pos in empty_pos):
            return True
        return False

    i, j = empty_pos[step]
    for symbol in ('T', 'G'):
        map_data[i][j] = symbol
        if bruteForce(map_data, empty_pos, step+1):
            return True

    map_data[i][j] = '_'
    return False

def timer(func, map_data, empty_pos):
    start = time.time()
    solvable = func(map_data, empty_pos)
    end = time.time()
    return solvable, end - start

def main():
    path = 'testcases\\input1.txt'
    map_data, empty_pos = ReadFile.read_map2(path)

    for row in map_data:
        print(row)
    print(' ')

    solvable, exe_time = timer(backTracking, map_data, empty_pos)
    print(f"Execution time: {exe_time}")
    if solvable:
        print("Back Tracking")
        for row in map_data:
            print(row)
        print(' ')    
    else:
        print("Cannot solve")

    solvable, exe_time = timer(bruteForce, map_data, empty_pos)
    print(f"Execution time: {exe_time}")
    if solvable:
        print("Brute Force")
        for row in map_data:
            print(row)
        print(' ')
    else:
        print("Cannot solve")


if __name__ == '__main__':
    main()
