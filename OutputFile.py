import os

def output_file(map_data, PATH):
    base_name = os.path.basename(PATH)
    output_path = f"testcases\\output_{base_name}"
    with open(output_path, 'w') as file:
        for row in map_data:
            for i in range(len(row)):
                file.write(row[i])
                if i != len(row) - 1:
                    file.write(', ')
            file.write('\n')