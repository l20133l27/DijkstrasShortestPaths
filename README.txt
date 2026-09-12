DijkstrasShortestPaths - Robert Wood rwood1@muskingum.edu

Files:
README.txt: This file.
network.txt: Sample input based on the given graph in the project requirements.
DijkstrasShortestPaths.py: Contains all relevant code and implementation. 

Programming Language:
Python 3.10.11

Tested:
Windows 11 PowerShell
Thonny IDE

TO RUN:
py DijkstrasShortestPaths.py network.txt

Description:
This program creates a directed weighted graph that represents a network. The initial graph is built from a text file given as a command-line argument. Each line of the file contains 2 vertex names, and a transmission time (weight). Two directed edges are made pointing from one vertex to the other. 

After the graph is built, the user can enter commands via input. The program prints the graph, finds the shortest possible path between 2 vertices, marking edges and vertices as active or inactive, adding and deleting edges not in the initial file, finding reachable vertices, and exiting the program

Design: 
3 Classes
	1: Edge: Stores destination, the weight assigned, and if the edge is active.

	2: Vertex: Stores the name of the vertex, if the vertex is active, and an adjacency list of outgoing edges.

	3: Graph: Stores vertices in a dictionary. Contains all functions related to the graph, including the initial setup of the graph, adding and deleting edges, flagging if an edge or vertex is active, printing the graph in full, determining the shortest path with Dijkstra's Algorithm, and printing reachable vertices.

Shortest Path:
The shortest path command uses Dijkstra's algorithm. It uses a min heap priority queue from Python's heapq library. The algorithm keeps track of the shortest known distance to each vertex and also stores the previous vertex so the final path can be printed. The shortest path only uses vertices and edges that are currently up. If a vertex or edge is down, it is ignored by the algorithm.

Reachable Vertices:
The reachable command uses Breadth-First Search, not Dijkstra's algorithm. For each vertex that is up, the program runs BFS to find all vertices that can be reached using only up vertices and up edges. The reachable vertices are printed in alphabetical order.

What Works:
The program can read the initial graph from a file.
The program can print the graph in alphabetical order.
The program can add and delete directed edges.
The program can mark directed edges as up or down.
The program can mark vertices as up or down.
The program can find the shortest path between two up vertices using Dijkstra's algorithm.
The program can print reachable vertices using BFS.
The quit command exits the program.

Known Issues / Limitations:
The program assumes that the input file is formatted correctly.
The program does not save graph changes after quitting.
The program does not use a custom-built heap; it uses Python's heapq library.
The program does not heavily validate incorrect commands or missing arguments.





