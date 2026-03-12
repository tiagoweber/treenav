# PAMPA-SEARCH: A minimalist graph navigation library to solve path-finding optimization problems

PAMPA-SEARCH provides basic state-space-search in graphs (graph navigation) for path-finding optimization problems. It has configurable features that allows the user to adapt it to the problem at hand. Its first use was to solve maze problems (see examples).

The library works both for manually created graphs or for problems in which the graph is created dinamically through iterations/movements in the problem. For that purpose, the user can create a class to describe its problems.


## Functionalities

- works for manually created graphs and for dinamically created graphs (when the state-space is implicit);
- to solve specific path-finding problems, it interacts with specific problems through a user-defined class which require a minimal number of methods;
- implements Depth-first, Breadth-first and A* (A star) algorithms

# Problem and Examples

There is a Maze solver example already implemented inside the library.

Depth-first strategy on a 20x20 maze

![Depth-first strategy on a 20x20 maze](https://raw.githubusercontent.com/tiagoweber/pampa-search/main/examples/depth-first-maze_20_20.gif)

Breadth-first strategy on a 20x20 maze

![Breadth-first strategy on a 20x20 maze](https://raw.githubusercontent.com/tiagoweber/pampa-search/main/examples/breadth-first-maze_20_20.gif)

A* strategy on a 20x20 maze

![A* strategy on a 20x20 maze](https://raw.githubusercontent.com/tiagoweber/pampa-search/main/examples/a-star-maze_20_20.gif)

# About the author and license

- Copyright 2026 Tiago Oliveira Weber
- License: MIT License
- Repository: https://github.com/tiagoweber/pampa-search
- Author professional website: www.tiagoweber.com.br
- Contact: tiago.oliveira.weber@gmail.com
