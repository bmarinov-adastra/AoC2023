def read_input(path="input.txt"):
    with open(path, "r") as f:
        grid = [list(line.strip()) for line in f.readlines()]
    
    current_number = 1
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == ".":
                grid[i][j] = (False, 0)
            else:
                grid[i][j] = (True, current_number)
                current_number += 1
    return grid


def find_empty_rows(grid):
    empty_rows = []
    for i, row in enumerate(grid):
        if not any([cell[0] for cell in row]):
            empty_rows.append(i)
    empty_columns = []
    for i, column in enumerate(zip(*grid)):
        if not any([cell[0] for cell in column]):
            empty_columns.append(i)
    return empty_rows, empty_columns


def find_coordinates(grid, number):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell[1] == number:
                return i, j


def find_shortest_path(grid, start, end, empty_rows, empty_columns, expand):
    i, j = find_coordinates(grid, start)
    current_position = (i, j)
    k, l = find_coordinates(grid, end)
    end_position = (k, l)

    empty_rows_in_path = 0
    empty_columns_in_path = 0

    if current_position[0] != end_position[0]:
        for row in empty_rows:
            if current_position[0] < row < end_position[0] or current_position[0] > row > end_position[0]:
                empty_rows_in_path += 1
    if current_position[1] != end_position[1]:
        for column in empty_columns:
            if current_position[1] < column < end_position[1] or current_position[1] > column > end_position[1]:
                empty_columns_in_path += 1
    distance = abs(current_position[0] - end_position[0]) + abs(current_position[1] - end_position[1]) + empty_rows_in_path * expand + empty_columns_in_path * expand
    return distance


def main():
    galaxy_map = read_input("galaxy_map.txt")
    empty_rows, empty_columns = find_empty_rows(galaxy_map)
    list_of_galaxies = [cell[1] for row in galaxy_map for cell in row if cell[0]]
    pairs = []
    for i, galaxy in enumerate(list_of_galaxies):
        for j in range(i + 1, len(list_of_galaxies)):
            pairs.append((galaxy, list_of_galaxies[j]))

    distances = []
    for pair in pairs:
        distances.append(find_shortest_path(galaxy_map, pair[0], pair[1], empty_rows, empty_columns, 999999))

    print("Sum of all distances: {}".format(sum(distances)))


if __name__ == "__main__":
    main()
