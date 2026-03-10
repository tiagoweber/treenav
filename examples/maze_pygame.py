import pampa-search as ps
import copy
import pampa-search.problems as problems
import pygame

record_gif = True

#strategy = "depth-first"
#strategy = "breadth-first"
strategy = "a-star"
maze_name = "maze_20_20"   # ./maps/maze_20_20.txt"
record_name = strategy+"-"+maze_name   
game = problems.maze("./maps/"+maze_name+".txt",use_pygame=True,record_gif=True,record_name=record_name+".gif")

game.print_board()

test_tree = ps.tree(game,cross_revisit_allowed=False,strategy=strategy)

# decision
next_node = test_tree.root_node
visited_nodes = 0
while not(game.check()):
    test_tree.current_node = next_node
    test_tree.populate_actions_and_children()

    next_node = test_tree.navigate_node(test_tree.current_node)    # also removes current node from nodes_to_visit
    visited_nodes += 1
    game.print_board_from_node(test_tree,next_node)    

    print("Visited nodes: %d \t Nodes to visit: %d"%(visited_nodes,len(test_tree.nodes_to_visit)))
    

game.print_board_from_node(test_tree,test_tree.current_node,final=True)
