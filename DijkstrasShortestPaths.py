#Dijkstras Shortest Paths in a Network RW rwood1@muskingum.edu

#I borowed some code from the last project. Mostly things related to Command Line Arguments.
import os
import sys
import heapq

#information needed for a directed graph.
#additionally has a flag if it is currently active.
#this program assumes they start active.
class Edge:
    def __init__(self,destination,weight):
        self.destination = destination
        self.weight = float(weight)
        self.is_up = True

#information needed for each "building."
#contains their name and the edges they have.
#like Edge, has a flag for if it is active.        
class Vertex:
    def __init__(self,name):
        self.name = name
        self.is_up = True
        self.edges = {}
    
#        
class Graph:
    def __init__(self):
        self.vertices = {}
        
    #changes to graph
    
    #adds an additional vertex.
    #not directly accessed by a user
    def addVertex(self, name):
        if name not in self.vertices:
            self.vertices[name] = Vertex(name)

    #adds an edge.
    def addEdge(self, tailVertex, headVertex, transmitTime):
        self.addVertex(tailVertex)
        self.addVertex(headVertex)
        
        self.vertices[tailVertex].edges[headVertex] = Edge(headVertex,transmitTime)
    
    #Inital set up when reading from the file.
    def initialLink(self,v1,v2,weight):
        self.addEdge(v1,v2,weight)
        self.addEdge(v2,v1,weight)

    #deletes an edge
    def deleteEdge(self, tailVertex,headVertex):
        if tailVertex in self.vertices and headVertex in self.vertices[tailVertex].edges:
            del self.vertices[tailVertex].edges[headVertex]

    #lowers flag on an edge
    def edgeDown(self, tailVertex,headVertex): #flags edge as unavaliable\
        if tailVertex in self.vertices and headVertex in self.vertices[tailVertex].edges:
            self.vertices[tailVertex].edges[headVertex].is_up = False

    #raises flag on an edge
    def edgeUp(self, tailVertex,headVertex) : #flags edge as available
        if tailVertex in self.vertices and headVertex in self.vertices[tailVertex].edges:
            self.vertices[tailVertex].edges[headVertex].is_up = True

    #lowers flag on a vertex
    def vertexDown(self, vertex): #marks Vertex as down, no edges may be used
        if vertex in self.vertices:
            self.vertices[vertex].is_up = False
    
    #raises flag on a vertex
    def vertexUp(self, vertex): #makrs Vertex as up.
        if vertex in self.vertices:
            self.vertices[vertex].is_up = True
    
    #prints the graph in full, including down edges and vertices
    def printGraph(self):
        for vertex_name in sorted(self.vertices.keys()):
            vertex = self.vertices[vertex_name]
            
            if vertex.is_up:
                print(vertex.name)
            else:
                print(vertex.name, "DOWN")
                
            for dest_name in sorted(vertex.edges.keys()):
                edge = vertex.edges[dest_name]
                
                if edge.is_up:
                    print(" " + dest_name + " " + str(edge.weight))
                else:
                    print(" " + dest_name + " " + str(edge.weight) + " DOWN")
    
    #finds the shortest path considering only active edges and vertices
    #This is Dijksrta's.                
    def shortestPath(self, start, end):
        if start not in self.vertices or end not in self.vertices:
            print("One or more vertices you selected do not exist.")
            return
        
        if not self.vertices[start].is_up or not self.vertices[end].is_up:
            print("One or more vertices you selected are down!")
            return
        
        #dist = [sys.maxsize] * V
        dist = {}
        prev = {}
        
        for vertex_name in self.vertices:
            dist[vertex_name] = float("inf")
            prev[vertex_name] = None
        #distance from start is 0    
        dist[start] = 0
        
        minHeap = []
        heapq.heappush(minHeap,(0,start))
        
        while minHeap:
            curDist, curName = heapq.heappop(minHeap)
            
            if curDist > dist[curName]:
                continue
            
            if curName == end:
                break
            
            curLocal = self.vertices[curName]
            
            if not curLocal.is_up:
                continue
            
            for curNeighbor in curLocal.edges:
                edge = curLocal.edges[curNeighbor]
                curNeighborVertex = self.vertices[curNeighbor]
                
                if not edge.is_up:
                    continue
                
                if not curNeighborVertex.is_up:
                    continue
                
                newDist = curDist + edge.weight
                
                if newDist < dist[curNeighbor]:
                    dist[curNeighbor] = newDist
                    prev[curNeighbor] = curName
                    heapq.heappush(minHeap, (newDist,curNeighbor))
                    
        if dist[end] == float("inf"):
            print("No such path.")
            return
        
        path = []
        current = end
        
        while current is not None:
            path.append(current)
            current = prev[current]
            
        path.reverse()
        
        for allmynames in path:
            print(allmynames, end=" ")
            
        print(round(dist[end], 2))
    
    #determines if an edge and vertices are reachable.
    def reachableBFS(self, start):
        visited = set()
        queue = []
        
        visited.add(start)
        queue.append(start)
        
        reachVertices = []
        
        while queue:
            curName = queue.pop(0)
            curVertex = self.vertices[curName]
            
            for nextName in sorted(curVertex.edges.keys()):
                edge = curVertex.edges[nextName]
                nextVertex = self.vertices[nextName]
                
                if not edge.is_up:
                    continue
                
                if not nextVertex.is_up:
                    continue
                
                if nextName not in visited:
                    visited.add(nextName)
                    reachVertices.append(nextName)
                    queue.append(nextName)
                    
        return sorted(reachVertices)
    
    #prints the reachable vertices
    def reachable(self):
        for vertex_name in sorted(self.vertices.keys()):
            vertex = self.vertices[vertex_name]
            
            if not vertex.is_up:
                continue
            print(vertex_name)
            
            reached = self.reachableBFS(vertex_name)
            
            for name in reached:
                print("  " + name)

#reads from file to construct the graph
def buildGraph(myFile):
    graph = Graph()
    
    with open(myFile, "r") as file:
        for line in file:
            parts = line.split()
            
            if len(parts) == 0:
                continue
            
            vertex1 = parts[0]
            vertex2 = parts[1]
            weight = parts[2]
            
            graph.initialLink(vertex1,vertex2,weight)
    
    return graph

#Menu 
def Commands(graph):
    print("If unsure what each command does, use 'help'")
    
    for line in sys.stdin:
        parts = line.split()
        
        if len(parts) == 0:
            continue
        command = parts[0].lower()
        
        if command == "help":
            print("CommandName <arguments>:")
            print("What it does.")
            print("help:")
            print("Brings up the list of commands.")
            print("print:")
            print("Prints the graph of the network, including downed infastructure.")
            print("reachable:")
            print("Prints only the active parts of the network.")
            print("path <Vertex1> <Vertex2>:")
            print("Determines the fastest path between two active parts of the network.")
            print("addedge <tailVertex> <headVertex> <Weight>:")
            print("Adds an edge pointing from argument 1 to argument 2.")
            print("deleteedge <tailVertex> <headVertex>:")
            print("Deletes the edge pointing from argumet 1 to argument 2.")
            print("edgedown <tailVertex> <headVertex>:")
            print("Marks the edge from argument 1 to argument 2 as down.")
            print("edgeup <tailVertex> <headVertex>:")
            print("Marks the edge from argument 1 to argument 2 as active.")
            print("vertexdown <Vertex>:")
            print("Marks the vertex as down.")
            print("vertexup <Vertex>:")
            print("Marks the vertex as active.")
            print("quit:")
            print("Exits the progarm. No status of the network is saved.")
            
        elif command == "quit":
            break
        elif command == "print":
            graph.printGraph()
        elif command == "reachable":
            graph.reachable()
        elif command == "path":
            graph.shortestPath(parts[1],parts[2])
        elif command == "addedge":
            graph.addEdge(parts[1],parts[2],parts[3])
        elif command == "deleteedge":
            graph.deleteEdge(parts[1],parts[2])
        elif command == "edgedown":
            graph.edgeDown(parts[1],parts[2])
        elif command == "edgeup":
            graph.edgeUp(parts[1],parts[2])
        elif command == "vertexdown":
            graph.vertexDown(parts[1])
        elif command == "vertexup":
            graph.vertexUp(parts[1])
        else:
            print("Not a recognized command.")
        #Note to self - think about a match statement

def main():
    #if the arguments aren't the proper size show what we're looking for
    if len(sys.argv) != 2:
        print("Use:")
        print("python DijkstrasShortestPaths.py <networkfile>")
        sys.exit()
        
    input_filename = sys.argv[1]
    networkGraph = buildGraph(input_filename)
    
    Commands(networkGraph)
    
            
if __name__ == "__main__":
    main()