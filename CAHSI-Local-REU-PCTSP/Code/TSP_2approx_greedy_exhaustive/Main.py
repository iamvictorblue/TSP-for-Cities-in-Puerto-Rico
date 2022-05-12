from GraphsMST import Graph
from GoogleORTSP import create_data_model 
from GoogleORTSP import print_solution
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import pywrapcp
import CSVHandler
import GoogleORTSP
import GreedyTSP
import RL_TSP
import numpy as np
from numpy import random

def main():
    #adjacency_matrix = CSVHandler.read_csv_file("input/graph.csv")
    distance_matrix = CSVHandler.read_csv_file("input/prcitiesgraph.csv")
    graph = Graph(distance_matrix)

    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    # search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)
    
    #Adjacency Matrix    
    n_dest = 13 # Set number of destinations. 12 cities including the starting point.
    tsp = np.array(
        [[0, 29, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 21],
        [29, 0, 33 , 100, 100, 47, 100, 100, 100, 100, 100, 100, 100],
        [100, 33 , 0, 42, 100, 20, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 42, 0, 66, 35, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 66, 0, 100, 82, 100, 100, 100, 100, 100, 100],
        [100, 47, 20, 35, 100, 0, 40, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 82, 40, 0, 63, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 63, 0, 86, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 86, 0, 79, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 79, 0, 70, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 70, 0, 53, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 53, 0, 21],
        [40, 100, 100, 100, 100, 100, 100, 90, 100, 100, 100, 21, 0]])     

    # RL Implementation
    def update_q(q, tsp, state, action, alpha=0.012, gamma=0.4):
        imm_reward = rew = 1./ tsp[state,action]
        delayed_reward = q[action,:].max()
        q[state,action] += alpha * (imm_reward + gamma * delayed_reward - q[state,action])
        return q

    q = np.zeros([n_dest,n_dest])
    epsilon = 1. # Exploration parameter
    n_train = 1000
    for i in range(n_train):
        traj = [0] # initial state = wharehouse
        state = 0
        possible_actions = [ dest for dest in range(n_dest) if dest not in traj]
        while possible_actions: # until all destinations are visited
            if random.random() < epsilon:
                action = random.choice(possible_actions)
            else:       
                best_action_index = q[state, possible_actions].argmax()
                action = possible_actions[best_action_index]
            q = update_q(q, tsp, state, action)
            traj.append(action)
            state = traj[-1]
            possible_actions = [ dest for dest in range(n_dest) if dest not in traj]

    # Last trip: from last destination to wharehouse
    action = 0
    q = update_q(q, tsp, state, action)
    traj.append(0)
    epsilon = 1. - i * 1/n_train

    # Run: Use model to find optimum trajectory
    traj = [0]
    state = 0
    distance_travel = 0.
    possible_actions = [ dest for dest in range(n_dest) if dest not in traj ]
    while possible_actions: # until all destinations are visited
        best_action_index = q[state, possible_actions].argmax()
        action = possible_actions[best_action_index]
        distance_travel += tsp[state, action]
        traj.append(action)
        state = traj[-1]
        possible_actions = [ dest for dest in range(n_dest) if dest not in traj ] 
    # Back to warehouse
    action = 0
    distance_travel += tsp[state, action]
    traj.append(action)
    

    # Print to terminal
    print()
    print("------------------------------------------------------------------------------")
    print()
    print("Solving the TSP using Greedy, 2-approx, and exhaustive algorithms")
    print()
    print("------------------------------------------------------------------------------")
    print("The graph built from reading prcitiesgraph.csv has " + str(graph.vertices_num) + " vertices.")
    print("The vertices are " + str(graph.vertices) + ", and they form the following distance matrix: ")
    graph.print_matrix()
    print("After applying Prim's algorithm to find an MST based on the graph, we get that the MST is: ")
    print()
    graph.prims_mst()
    print()
    print("------------------------------------------------------------------------------")
    print()
    print("Using an exhaustive approach with Google OR tools, we get that the total amount of miles and the route needed is: ")
    if solution:
        print_solution(manager, routing, solution)
    graph = Graph(distance_matrix)
    print("------------------------------------------------------------------------------")
    print()
    print("Using a greedy algorithm we get that the total amount of miles and the route needed is:  ")
    print()
    GreedyTSP.findMinRoute(tsp)
    GreedyTSP.print_solution(manager, routing, solution)
    print()
    print("------------------------------------------------------------------------------")
    print()
    print("Now with a reinforcement learning based approach using q-learning, we get the following result:")
    print()
    print(f'Minimum Cost is: {distance_travel} miles')
    print('Route for vehicle:')
    print(' -> '.join([str(b) for b in traj]))
    print()



if __name__ == "__main__":
    main()


