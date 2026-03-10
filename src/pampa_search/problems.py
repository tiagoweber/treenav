# Samples problems for PAMPA_SEARCH
# PAMPA_SEARCH provides basic tree navigation for path-finding optimization problems. It has configurable features that allows the user to adapt it to the problem at hand. Its first use was to solve maze and routing problems (see examples).
# The library works both for  manually created trees or for problems in which the tree is created dinamically through iterations/movements in the problem. For that purpose, the user can create a class to describe its problems.
#
# - Copyright 2026 Tiago Oliveira Weber
# - License: MIT License
# - Repository: https://github.com/tiagoweber/pampa_search
# - Author professional website: www.tiagoweber.com.br
# - Contact: tiago.oliveira.weber@gmail.com


import copy
import pygame
import pygame_gifs

#**************************************
#  Sample Problem: Maze
#**************************************
class maze():
    def __init__(self,filename = None,use_pygame=False,record_gif=False,record_name="result.gif"):
        if filename != None:
            self.load_map_from_file(filename)
        else:
            self.board_size =  [10,10]
            self.board_obstacles =        [
                [2, 2],
                [2, 3],
                [2, 4],
            ]
            self.board_goal_position = [4,4]
            self.initial_state = { 
                "board_player_position" : [1,1]
                }        
        self.restart()
        self.use_pygame= use_pygame
        if (self.use_pygame):            
            self.WHITE = [255, 255, 255]
            self.BLACK = [0, 0, 0]
            self.GRAY = [100, 100, 100]
            self.LIGHT_GRAY = [180, 180, 180]
            self.BLUE = [0, 0, 255]
            self.LIGHT_BLUE = [100, 100, 255]
            self.YELLOW = [150, 150, 0]
            SIZE = 400
            nrows = self.board_size[1]
            ncolumns = self.board_size[1]
            max_length = max(nrows,ncolumns)            
            self.pygame_CELL_SIZE = SIZE // max_length
            XSIZE = self.pygame_CELL_SIZE*nrows
            YSIZE = self.pygame_CELL_SIZE*ncolumns

            self.SCREEN = pygame.display.set_mode((XSIZE, YSIZE))

            self.border_width = max(int(SIZE/1000),1)
            pygame.init()
            self.ever_visited_pos = []
            self.record_gif = record_gif

            if self.record_gif:
                self.gf = pygame_gifs.GifRecorder(record_name, XSIZE, YSIZE, threads=8)
                self.gf.start_recording()



            
    def load_map_from_file(self,filename):
        self.board_obstacles = []
        i = 0 # map lines
        with open(filename, 'r') as file:            
            for line in file:
                line = line.rstrip()
                if line == '':
                    pass
                elif line[0] == "|":
                    # real line
                    j = -1
                    for character in line:
                        if (character == "|"):
                            j+=1
                        elif (character == "*"):
                            self.initial_state = {
                                "board_player_position" : [i,j]
                            }
                        elif (character == "O"):
                            self.board_goal_position = [i,j] 
                        elif (character == "#"):
                            self.board_obstacles.append([i,j])
                    i+=1
                        
                self.board_size = [i,j]

                

    def restart(self):
        self.state = copy.deepcopy(self.initial_state)
            
    def estimate_hcost(self,node_state):
        """ calculates an estimate cost for the node. Required for A* search """
        node_player_pos = node_state["board_player_position"]
        goal_pos = self.board_goal_position
        manhattan_distance = abs(node_player_pos[0] - goal_pos[0]) + abs(node_player_pos[1] - goal_pos[1])
        #manhattan_distance = 2*abs(node_player_pos[0] - goal_pos[0]) + abs(node_player_pos[1] - goal_pos[1])
        return 2*manhattan_distance  # was 1.1
        
    def get_available_actions(self):
        
        list_of_actions = ["left","right","up","down"]  # in the future, it will have to test if there is any blockage
        node_player_pos = self.state["board_player_position"]
        x = node_player_pos[0]
        y = node_player_pos[1]

        # #################################
        # check if any next_node is blocked by:
        #  - obstacle OR
        #  - if is in the path navigated so far --> this is going to happen at the tree class
        ####################################

        for obstacle in self.board_obstacles:
            if ((  (x-1) == obstacle[0]) and (y == obstacle[1])):
                list_of_actions.remove("up")
            elif ((  (x+1) == obstacle[0]) and (y == obstacle[1])):
                list_of_actions.remove("down")
            elif ((  x == obstacle[0]) and ( (y-1) == obstacle[1])):
                list_of_actions.remove("left")
            elif ((  x == obstacle[0]) and ( (y+1) == obstacle[1])):
                list_of_actions.remove("right")

        
        return list_of_actions
        
        
    def print_board(self,visited_path=None):

        lines = self.board_size[0]
        columns = self.board_size[1]

        if (self.use_pygame==False):
            print("Current Board Status")
            print("")
            for i in range(0,lines):
                print("\n|",end="") #first |
                for j in range(0,columns):
                    #if ([i,j] == self.state["board_player_position"]):
                    #    print("*",end="")
                    if ([i,j] == self.initial_state["board_player_position"]):
                        print("*",end="")
                    elif ([i,j] == self.board_goal_position):
                        print("O",end="")
                    elif ([i,j] in self.board_obstacles):
                        print("#",end="")                        
                    elif ((visited_path != None) and ([i,j] in visited_path)):
                        if ([i,j] == visited_path[-1]):
                            print("%",end="")
                        else:
                            print("+",end="")
                    else:
                        print(" ",end="")
                    print("|",end="")  # in-line separator |
            print("")
        elif(self.use_pygame):
            self.SCREEN.fill(self.WHITE)
            for i in range(0,lines):
                print("\n|",end="") #first |
                for j in range(0,columns):
                    #if ([i,j] == self.state["board_player_position"]):
                    #    print("*",end="")

                    rect = pygame.Rect(j * self.pygame_CELL_SIZE,
                                       i * self.pygame_CELL_SIZE,
                                       self.pygame_CELL_SIZE,
                                       self.pygame_CELL_SIZE)
                    
                    if ([i,j] == self.initial_state["board_player_position"]):
                        #print("*",end="")
                        color = self.GRAY
                    elif ([i,j] == self.board_goal_position):
                        #print("O",end="")
                        color = self.YELLOW
                    elif ([i,j] in self.board_obstacles):
                        #print("#",end="")
                        color = self.BLACK
                    elif ((visited_path != None) and ([i,j] in visited_path)):
                        if ([i,j] == visited_path[-1]):
                            #print("%",end="")
                            color = self.BLUE
                        else:
                            #print("+",end="")
                            color = self.LIGHT_BLUE
                    elif ([i,j] in self.ever_visited_pos):
                        color = self.LIGHT_GRAY
                    else:
                        #print(" ",end="")
                        color = self.WHITE
                    #print("|",end="")  # in-line separator |

                    pygame.draw.rect(self.SCREEN, color, rect)
                    pygame.draw.rect(self.SCREEN, self.BLACK, rect, self.border_width) # Border

            if self.record_gif:
                self.gf.upload_frame(self.SCREEN) # Upload the current frame to the recorder
                
            pygame.display.flip()
                    
            pygame.time.delay(100)
                    
                    
            #print("")
            
        
    def print_board_from_node(self,tree,next_node,final=False):
            path_to_node = tree.print_and_get_path_to_node(next_node)
            #print("Visited nodes: %d"%(visited_nodes))

            visited_path = []
            for node in path_to_node:
                visited_path.append(node.state["board_player_position"])

            self.print_board(visited_path)
            if ((self.use_pygame) and final):
                pygame.time.delay(2000)
                if self.record_gif:
                    self.gf.stop_recording() # Stop recording and compile the GIF


                                            
    def move(self,direction):
        """Move piece in the board."""
        
        if direction == "right":
            self.state["board_player_position"][1] += 1
        elif direction == "left":
            self.state["board_player_position"][1] -= 1
        elif direction == "down":
            self.state["board_player_position"][0] += 1            
        elif direction == "up":
            self.state["board_player_position"][0] -= 1            

        # check limits
        if self.state["board_player_position"][0] >= self.board_size[0]:
            self.state["board_player_position"][0] = self.board_size[0]-1
                                                           
        if self.state["board_player_position"][1] >= self.board_size[1]:
            self.state["board_player_position"][1] = self.board_size[1]-1

        if self.state["board_player_position"][0] < 0:
            self.state["board_player_position"][0] = 0

        if self.state["board_player_position"][1] < 0:
            self.state["board_player_position"][1] = 0

        if ([self.state["board_player_position"][0],self.state["board_player_position"][1]] not in self.ever_visited_pos):
            self.ever_visited_pos.append([self.state["board_player_position"][0],self.state["board_player_position"][1]])
            
    def check(self):

        # check goal
        if (self.state["board_player_position"] == self.board_goal_position):            
            return 1
        else:
            return 0
