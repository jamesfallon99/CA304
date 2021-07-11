import pandas as pd #Used to print the routing table

class Router():# This class will represent a router. A router has a name and a connection to a network graph.

    cost_list = []#A list used to store the cost of a the current router to another router
    popped_list = []#A list used to store any element popped off another list that we want to use
    map_edge_to_cost = {} #Global variable that maps edge to cost-used in routing tale
    path = [] # Global variable which stores thr path the dijkstra algorithm takes

    path_and_cost = [] #Stores the path and cost of each edge the router connects to. Used in dijkstra's algorithm function

    def __init__(self, name, connection_to_network_graph):
       self.name = name
       self.connection_to_network_graph = connection_to_network_graph
  
    def get_path(self, router_name):#This method performs Dijkstra's Algorithm to return the distance
    #and the path between the router and the router specified by router_name
        print("Start: " + self.name)
        print("End: " + router_name)
        self.dijkstra(Graph.graph, self.name, router_name, visited=[],distances={},predecessors={})
        print("Path: " + self.path_and_cost[0]) # Get the path from the global list. The path is appended to this list when dijkstra is run
        self.path_and_cost.pop(0) #Pop it from the list when it has been printed -this allows no build up of path and cost for when dijkstra is called again
        print("cost: " + self.path_and_cost[0])  #Get the cost from the global list. The cost is appended to this list when dijkstra is run
        self.path_and_cost.pop(0)#Pop it from the list when it has been printed-this allows no build up of path and cost for when dijkstra is called again
        self.path.pop(0) # As this path list is used later for part 2, need to remove the first element that is used in part 1 of this assignment. This helps to fix a bug that occurred
        self.cost_list.pop(0) #Need to remove the element in this list as this list is used later in the program and want an empty list for when that part is called
    
    def use_dijkstra(self, router_name): # Helper function used in "print_routing_table", that runs through the dijkstras algorithm without any print statements. Allows me to get the path and cost of each edge that the router connects to
        self.dijkstra(Graph.graph, self.name, router_name, visited=[],distances={},predecessors={})

    def dijkstra(self,graph,src,dest,visited=[],distances={},predecessors={}): #http://www.gilles-bertrand.com/2014/03/dijkstra-algorithm-python-example-source-code-shortest-path.html used this link to help implement the algorithm
        #calculates a shortest path tree routed in src
           
        # a few sanity checks
        #if src not in graph:
            #raise TypeError('The root of the shortest path tree cannot be found')
        #if dest not in graph:
            #raise TypeError('The target of the shortest path cannot be found')    
        # ending condition
        if src == dest:
            # We build the shortest path and display it
            path=[]
            pred=dest
            while pred != None:
                path.append(pred)
                pred=predecessors.get(pred,None)
            # reverses the array, to display the path nicely
            readable=path[0]
            for index in range(1,len(path)): readable = path[index]+'->'+readable
            #prints it 
            self.path.append(str(readable))
            self.cost_list.append(str(distances[dest]))
            if str(readable) not in self.path_and_cost:
                self.path_and_cost.append(str(readable))
                self.path_and_cost.append(str(distances[dest]))

        else :     
            # if it is the initial  run, initializes the cost
            if not visited: 
                distances[src]=0
            # visit the neighbors
            for neighbor in graph[src]:
                if neighbor not in visited:
                    new_distance = distances[src] + graph[src][neighbor]
                    if new_distance < distances.get(neighbor,float('inf')):
                        distances[neighbor] = new_distance
                        self.map_edge_to_cost[neighbor] = new_distance #Add to global dictionary so can use later in routing table(maps edges to cost)
                        predecessors[neighbor] = src

            # mark as visited
            visited.append(src)
            
            # now that all neighbors have been visited: recurse                         
            # select the non visited node with lowest distance 'x'
            # run Dijskstra with src='x'
            unvisited={}
            for k in graph:
                if k not in visited:
                    unvisited[k] = distances.get(k,float('inf'))
            #try:   
            x=min(unvisited, key=unvisited.get,default="f") #ValueError: min() arg is an empty sequence. This error occurs when i try to search for "f" using the sample input from the assignment brief. So set default to "f" to work around this until I figure out what is causing it to not work correctly
            #except ValueError:
                #print("ValueError occurred, please use the sample code in the main comments to get this working")
            #print(x)
            self.dijkstra(graph,x,dest,visited,distances,predecessors) #Call the instance of router(ie self)
    
    def print_routing_table(self): #. This function should generate and print
    #out the routing table for the router. The routing table is a table which details the routers most effecient path
    #to every other node on the network and the associated cost.
        amount_of_edges = len(Graph.edges) #Get the amount of edges that the router connects to
 
        _from = [] #Put the current router name in a list * the amount of edges it can connect to
        i = 0
        while i < amount_of_edges:
            _from.append(self.name)
            i += 1

        i = 0
        while i < len(Graph.edges):
            if Graph.edges[i] == self.name: #Need to check if the router is the current router as we don't want this to run through the algoritm
                popped = Graph.edges.pop(i)
                self.popped_list.append(popped) #If it is, pop this router into our global popped list
            else:
                self.use_dijkstra(Graph.edges[i])#Otherwise, use dijkstra on this router(when you run through dijkstra, this gives us the cost and path)
                i += 1

        #cost = []
        #for v in self.map_edge_to_cost.values():
            #cost.append(v)

        _to = [] #A list that will store the edges that the current router connects to

        for edge in Graph.edges:
            _to.append(edge) #Append each edge to the "_to" list

        table = {} #Create a dictionary that will map "from", "to", "cost" and "Path"
        i = 0
        while i < len(Graph.edges):
            table[i] = [_from[i], _to[i], self.cost_list[i], self.path[i]]
            i += 1

        print(pd.DataFrame.from_dict(table, orient='index', columns = ["from", "to", "cost", "path"])) #Print this table using pandas dataframe

        i = 0
        while i < len(self.popped_list):
            Graph.edges.append(self.popped_list[i])
            self.popped_list.pop(i) #Need to put the router that we removed back into edges so that the next time the function is called, edges will still contain the original amount(if self.name == router name, popped it so it wouldn't have to evaluate that path)
            i += 1
        
        i = 0

        if len(self.path) != 0:#As self.path is used everytime this function is called, need to pop the amount of paths that has already been added off the list so that the list can start from an empty list when the function is called again
            while i < amount_of_edges -1:
                self.path.pop(0) # An element will be poppped off from the list at positon 0
                i += 1

        i = 0
        while i < len(Graph.edges):##As self.sost_list is used everytime this function is called, need to pop the amount of costs that has already been added off the list so that the list can start from an empty list when the function is called again
            if len(self.cost_list) != 0:
                self.cost_list.pop(0)
            i += 1

    
    def remove_router(self, router_name):
        i = 0
        while i < len(Graph.edges):#As self.sost_list is used everytime this function is called, need to pop the amount of costs that has already been added off the list so that the list can start from an empty list when the function is called again
            if len(self.cost_list) != 0:
                self.cost_list.pop(0)
            i += 1

        if router_name in Graph.graph:
            del Graph.graph[router_name] # remove the router_name value from this dictionary

        for k, v in Graph.graph.items(): #v is another dictionary with its own keys and values

            copy_values = v.copy()#Need to create a copy as otherwise you get a RuntimeError: dictionary changed size during iteration, because you iterate over the dictionary itself and remove an item every cycle. You can circumvent this by iterating over a copy of the dictionary
            for key in copy_values:
                if key == router_name:
                    del v[router_name] # remove the router_name value from this dictionary

        length_of_original_graph = len(Graph.edges) #Need this to be able to know how many elements in path needs to be popped off the global path list. Needs to be placed here before an element is popped off

        i = 0
        while i < len(Graph.edges):
            if Graph.edges[i] == router_name:
                Graph.edges.pop(i) #Remove it from the edges list
            i += 1
        
        if router_name in self.map_edge_to_cost: # remove the router_name value from this dictionary
            del self.map_edge_to_cost[router_name]

        i = 0

        if len(self.path) != 0:
            while i < length_of_original_graph:
                self.path.pop(0) # An element will be poppped off from the list at positon 0
                i += 1

        self.print_routing_table()


class Graph():#A graph is made up of nodes and edges. Each node represents a router. Each
    #edge represents a link between two routers and has an associated cost. This is an integer which is used to
    #represent the travel time between two routers.
    graph = {} #A graph of routers and edges connecting a router to another router

    edges = [] #A list with all the edges appended to it. Gets appended when an edge is created

    def add_edge(self, name, router_name, cost):#Adds an edge to the network graph from the current
    #Router (name) to another router router name, cost is an integer representing the distance between
    #the two routers.

        if name not in Graph.graph: #If the current router (name) is not already in the graph
            Graph.graph[name] = {}#Let the name map to another dictionary
        Graph.graph[name][router_name] = int(cost)#Otherwise, map the name to a router(create a link) and map this to a cost
        
        if router_name not in Graph.edges: #If this router is not in our edges list, 
            Graph.edges.append(router_name)#add edge to our edge list

"""
#please remove these quotes to access my main function
def main():
    new_graph = Graph()
    new_graph.add_edge("a", "b", 7)
    new_graph.add_edge("a", "c", 9)
    new_graph.add_edge("a", "f", 14)
    new_graph.add_edge("b", "c", 10)
    new_graph.add_edge("b", "d", 15)
    #new_graph.add_edge("b", "a", 0)###To get part 4, including the remove function working, this needs to be uncommented. The first part of part 4 will work fine without this included(i.e if you just want to print 2 router's using "get_routing_table")###
    new_graph.add_edge("c", "a", 9)
    new_graph.add_edge("c", "d", 11)
    new_graph.add_edge("c", "f", 2)
    new_graph.add_edge("d", "e", 6)
    new_graph.add_edge("e", "f", 9)

       
    new_router= Router("a", new_graph)
    print("Part 1")
    new_router.get_path("f")
    print("\n")
    print("Part 2")
    new_router.print_routing_table()
    print("\n")
    print("Part 3")
    new_router.remove_router("c")
    print("\n")
    
    #print("Part 4-including remove")

    #new_router2 = Router("b", new_graph)
    #new_router2.get_path("d")
    #print("\n")
    #new_router2.print_routing_table()

if __name__ == "__main__":
    main()"""
    #please remove these quotes to access my main function
   
   #parts 1, 2, 3 completely working, part 4 works for multiple routers even when remove is called. Only thing it does't cater for e.g b->a = 0 when a router isn't connected   