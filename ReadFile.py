def read_map(path: str) -> list:
    map_data = []
    with open(path, 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            
            row = line.strip('\n').split(', ')
            map_data.append(row)
        
    return map_data

def read_map2(path: str):
    map_data = []
    empty_pos = []
    with open(path, 'r') as file:
        for row_index, line in enumerate(file):
            row = line.strip('\n').split(', ')
            map_data.append(row)
            for col_index, cell in enumerate(row):
                if cell == '_':
                    empty_pos.append((row_index, col_index))
    return map_data, empty_pos
