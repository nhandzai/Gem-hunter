import ReadFile


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


def backTracking(map_data, empty_pos, step):
    end = False
    pos = empty_pos[step]

    map_data[pos[0]][pos[1]] = 'T'
    if multiCheck(map_data, pos):
        if step == len(empty_pos) - 1:
            return map_data, True
        map_data, end = backTracking(map_data, empty_pos, step=step + 1)
        if end:
            return map_data, True
    map_data[pos[0]][pos[1]] = 'G'
    if multiCheck(map_data, pos):
        if step == len(empty_pos) - 1:
            return map_data, True
        map_data, end = backTracking(map_data, empty_pos, step=step + 1)
        if end:
            return map_data, True
    map_data[pos[0]][pos[1]] = '_'
    return map_data, False





def main():
    path = 'testcases\\input3.txt'
    map_data, empty_pos = ReadFile.read_map2(path)

    for row in map_data:
        print(row)
    print(' ')

    map_data, temp = backTracking(map_data, empty_pos, 0)

    for row in map_data:
        print(row)


if __name__ == '__main__':
    main()
