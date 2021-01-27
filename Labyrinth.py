class CreateMaze:
    maze_array = []
    file_name = ""
    def __init__(self, file):
        self.file_name = file
    #create mazes and append to maze_array
    def create_maze_array(self):
        datei = open(self.file_name, "r")
        while(1):
            maze = Maze()
            temp = []
            firstline = datei.readline()[:-1].split(" ")
            if(len(firstline) == 1):
                firstline = datei.readline()[:-1].split(" ")
            maze.length.l = int(firstline[0])
            maze.length.r = int(firstline[1])
            maze.length.c = int(firstline[2])

            if(maze.length.l == 0):
                break

            for level in range(maze.length.l):
                temp.append([])
                for row in range(maze.length.r):
                    z_inhalt = datei.readline()[:-1]
                    if(z_inhalt != ""):
                        temp[level].append(z_inhalt)
                    else:
                        temp[level].append(datei.readline()[:-1])
            maze.matrix = temp
            maze.create_visited()
            maze.create_start_coords()
            self.maze_array.append(maze)
        return self.maze_array

class Maze:
    length = None
    start_coords = None
    matrix = []
    visitet = []

    def __init__(self):
        self.length = Coordinates()
        self.start_coords = Coordinates()
        self.matrix = []
        self.visitet = []
        
    def __str__(self):
        return "Matrix: " + str(self.matrix) \
        + "\nVisited: " + str(self.visitet) \
        + "\nStart " + str(self.start_coords) \
        + "\nlength: " + str(self.length)
        + "\n"

    def create_visited(self):
        if(len(self.matrix) == 0):
            return -1
        else:
            for level in self.matrix:
                temp_1 = []
                for rows in level:
                    temp_2 = []
                    for column in rows:
                        temp_2.append(False)
                    temp_1.append(temp_2)
                self.visitet.append(temp_1)
    def create_start_coords(self):
        for level in range(self.length.l):
            for row in range(self.length.r):
                for column in range(self.length.c):
                    if(self.matrix[level][row][column] == "S"):
                        self.start_coords.l = level
                        self.start_coords.r = row
                        self.start_coords.c = column  

                    
class MazeRunner:
    maze = None
    queues = None
    dir_coords = None

    move_counter = 0
    nodes_left_in_layer = 1
    nodes_in_next_layer = 0
    reached_end = False

    def __init__(self, maze):
        self.maze = maze
        self.queues = MazeQueues()
        self.dir_coords = Coordinates()
        self.dir_coords.l = [0, 0, 0, 0, +1, -1] #direction cords for level
        self.dir_coords.r = [0, 0, +1, -1, 0, 0] #direction cords of row
        self.dir_coords.c = [-1, +1, 0, 0, 0, 0] #direction cords for column
        self.move_counter = 0
        self.nodes_left_in_layer = 1
        self.nodes_in_next_layer = 0
        self.reached_end = False
    
    def solve(self):
        self.queues.l_queue.append(self.maze.start_coords.l) #add start coordinates of levels to lvl queue
        self.queues.r_queue.append(self.maze.start_coords.r) #add start coordinates of rows to row queue
        self.queues.c_queue.append(self.maze.start_coords.c) #add start coordinates of columns to column queue
        #set start coordianates on true
        self.maze.visitet[self.maze.start_coords.l][self.maze.start_coords.r][self.maze.start_coords.c] = True 
        while(len(self.queues.l_queue) > 0):
            level = self.queues.l_queue.pop()
            row = self.queues.r_queue.pop()
            column = self.queues.c_queue.pop()
            if(self.reached_end):
                return "Entkommen in " + str(self.move_counter) + " Minute(n)!"
            self.exploreNeighbors(level, row, column)
            self.nodes_left_in_layer -= 1
            if(self.nodes_left_in_layer == 0):
                self.nodes_left_in_layer = self.nodes_in_next_layer
                self.nodes_in_next_layer = 0
                self.move_counter += 1
        return "Gefangen :-("

    def exploreNeighbors(self, level, row, column):
        for nr in range(6): 
            
            #add direction cords to check north, east, south, west, up and down
            new_level = level + self.dir_coords.l[nr]
            new_row = row + self.dir_coords.r[nr]
            new_column = column + self.dir_coords.c[nr]
            
            #skip neighbor when sth is wrong
            if(new_level < 0 or new_row < 0 or new_column < 0): 
                continue
            if(new_level >= self.maze.length.l or new_row >= self.maze.length.r or new_column >= self.maze.length.c):
                continue
            if(self.maze.visitet[new_level][new_row][new_column]): 
                continue
            if(self.maze.matrix[new_level][new_row][new_column] == "#"):
                continue
            #check if neighbor is end
            if(self.maze.matrix[new_level][new_row][new_column] == "E"): 
                self.reached_end = True
            
            #add neighbor to queue
            self.queues.l_queue.append(new_level) 
            self.queues.r_queue.append(new_row) 
            self.queues.c_queue.append(new_column) 
            self.maze.visitet[new_level][new_row][new_column] = True 

            self.nodes_in_next_layer += 1

class Coordinates:
    l = 0
    r = 0
    c = 0

    def __init__(self):
        self.l = 0
        self.r = 0
        self.c = 0

    def __str__(self):
        return "Koordinaten: (" + str(self.l) +", " + str(self.r) + ", " + str(self.c) + ")"

class MazeQueues:
    l_queue = [] 
    r_queue = [] 
    c_queue = [] 
    
    def __init__(self):
        self.l_queue = [] 
        self.r_queue = [] 
        self.c_queue = [] 

########################## Main Programm #########################################
#just change filename
filename = "Eingabe.txt"
maze_file = CreateMaze(filename)
maze_array = maze_file.create_maze_array()
for entries in maze_array:
    runner = MazeRunner(entries)
    print(runner.solve())





        

    
        
    

