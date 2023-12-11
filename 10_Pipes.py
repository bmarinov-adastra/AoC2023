import shapely.geometry as sg
from PIL import Image, ImageDraw


def read_input(path="input.txt"):
    with open(path, "r") as f:
        pipes = [list(line.strip()) for line in f.readlines()]
    return pipes
    
def find_connections(pipes, current_position):
    i, j = current_position
    current_pipe = pipes[i][j]
    connections = []
    coonections_cordinates = []
    
    if i > 0:
        if current_pipe in "|LJS":
            if pipes[i-1][j] in "|F7S":
                connections.append("up")
                coonections_cordinates.append((i-1, j))
    if i < len(pipes)-1:
        if current_pipe in "|F7S":
            if pipes[i+1][j] in "|LJS":
                connections.append("down")
                coonections_cordinates.append((i+1, j))
    if j > 0:
        if current_pipe in "-J7S":
            if pipes[i][j-1] in "-LFS":
                connections.append("left")
                coonections_cordinates.append((i, j-1))
    if j < len(pipes[0])-1:
        if current_pipe in "-LFS":
            if pipes[i][j+1] in "-J7S":
                connections.append("right")
                coonections_cordinates.append((i, j+1))
    
    return connections, coonections_cordinates
    
def find_start(pipes):
    for i, row in enumerate(pipes):
        for j, pipe in enumerate(row):
            if pipe == "S":
                start = (i, j)
                possible_connections = find_connections(pipes, start)
                return start
            

            
def find_main_looop(pipes, start, image):
    current_position = start
    previous_position = None
    main_loop = [start]

    while True:
        possible_connections,surrounding_pipes = find_connections(pipes, current_position)

        draw = ImageDraw.Draw(image)
        if pipes[current_position[0]][current_position[1]] == "S":
            x = current_position[1] * 3
            y = current_position[0] * 3
            draw.rectangle([(x, y), (x + 2, y + 2)], fill="blue")
        elif pipes[current_position[0]][current_position[1]] == "-":
            x = current_position[1] * 3
            y = current_position[0] * 3
            draw.line([(x, y+1), (x + 2, y+1)], fill="red", width=1)
        elif pipes[current_position[0]][current_position[1]] == "|":
            x = current_position[1] * 3
            y = current_position[0] * 3
            draw.line([(x+1, y), (x+1, y + 2)], fill="red", width=1)
        elif pipes[current_position[0]][current_position[1]] == "F":
            x = current_position[1] * 3
            y = current_position[0] * 3
            draw.line([(x+1, y+2), (x+1, y + 1), (x+2, y + 1)], fill="red", width=1)
        elif pipes[current_position[0]][current_position[1]] == "7":
            x = current_position[1] * 3
            y = current_position[0] * 3
            draw.line([(x, y+1), (x+1, y + 1), (x+1, y + 2)], fill="red", width=1)
        elif pipes[current_position[0]][current_position[1]] == "J":
            x = current_position[1] * 3
            y = current_position[0] * 3
            draw.line([(x, y+1), (x+1, y + 1), (x+1, y)], fill="red", width=1)
        elif pipes[current_position[0]][current_position[1]] == "L":
            x = current_position[1] * 3
            y = current_position[0] * 3
            draw.line([(x+1, y), (x+1, y + 1), (x+2, y + 1)], fill="red", width=1)        
        else:
            pass

        if previous_position is not None:
            if previous_position in surrounding_pipes:
                surrounding_pipes.remove(previous_position)
                previous_position = current_position
                current_position = surrounding_pipes[0]
                main_loop.append(current_position)
            else:
                raise ValueError("Previous position not in surrounding pipes.")
        else:
            previous_position = current_position
            current_position = surrounding_pipes[0]
            main_loop.append(current_position)
            continue

        if current_position == start:
            return main_loop, image

def is_enclosed(loop, point):
    polygon = sg.Polygon(loop)
    point = sg.Point(point)
    return polygon.contains(point)
            

def main():
    pipes = read_input(path="pipes.txt")
    start = find_start(pipes)
    image = Image.new("RGB", (len(pipes[0])*3, len(pipes)*3), color="black")

    main_loop, image = find_main_looop(pipes=pipes, start=start, image=image)
    
    
    print("Farthest point:", len(main_loop)//2)

    ground_tiles = []
    for i, row in enumerate(pipes):
        for j, pipe in enumerate(row):
            if pipe == ".":
                ground_tiles.append((i, j))

    draw = ImageDraw.Draw(image)
    for tile in ground_tiles:
        x = tile[1] * 3
        y = tile[0] * 3
        draw.rectangle([(x, y), (x + 2, y + 2)], fill="green")


    enclosed_polygones = []
    for i, row in enumerate(pipes):
        for j, pipe in enumerate(row):
            # if pipe == ".":
            if is_enclosed(loop=main_loop, point=(i, j)):
                enclosed_polygones.append((i, j))
                x = j * 3
                y = i * 3
                draw.rectangle([(x+1, y+1), (x + 1, y + 1)], fill="purple")
    print("Enclosed polygones:", enclosed_polygones)
    print("Number of enclosed polygones:", len(enclosed_polygones))


    

    image.save("pipes.png")
    
if __name__ == "__main__":
    main()
