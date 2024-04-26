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