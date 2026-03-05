import treenav
import copy
import treenav.problems


game = treenav.problems.maze()
#game = maze("./maps/maze_50_50.txt")

game.print_board()

test_tree = treenav.tree(game,cross_revisit_allowed=False)

# decision
next_node = test_tree.root_node
visited_nodes = 0
while not(game.check()):
    test_tree.current_node = next_node
    test_tree.populate_actions_and_children()

    next_node = test_tree.navigate_node_astar(test_tree.current_node)    # also removes current node from nodes_to_visit
    visited_nodes += 1    
    #test_tree.print_board_from_node(next_node)    
    print("Visited nodes: %d \t Nodes to visit: %d"%(visited_nodes,len(test_tree.nodes_to_visit)))


game.print_board_from_node(test_tree,test_tree.current_node)
