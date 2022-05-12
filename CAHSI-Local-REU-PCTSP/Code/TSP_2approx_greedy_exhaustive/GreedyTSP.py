from typing import DefaultDict
 
 
INT_MAX = 2147483647
 
# Function to find the minimum
# cost path for all the paths
def findMinRoute(tsp):
    sum = 0
    counter = 0
    j = 0
    i = 0
    min = INT_MAX
    visitedRouteList= DefaultDict(int)
    visitedRouteList[0] = 0
    route = [0] * len(tsp)
 
    # Traverse the adjacency
    # matrix tsp[][]
    while i < len(tsp) and j < len(tsp[i]):
 
        # Corner of the Matrix
        if counter >= len(tsp[i]) - 1:
            break
 
        # If this path is unvisited then
        # and if the cost is less then
        # update the cost
        if j != i and (visitedRouteList[j] == 0):
            if tsp[i][j] < min:
                min = tsp[i][j]
                route[counter] = j + 1
 
        j += 1
 
        # Check all paths from the
        # ith indexed city
        if j == len(tsp[i]):
            sum += min
            min = INT_MAX
            visitedRouteList[route[counter] - 1] = 1
            j = 0
            i = route[counter] - 1
            counter += 1
 
    i = route[counter - 1] - 1
 
    for j in range(len(tsp)):
 
        if (i != j) and tsp[i][j] < min:
            min = tsp[i][j]
            route[counter] = j + 1
 
    sum += min
 
    # Started from the node where
    # we finished as well.
    print("Minimum Cost is :", sum)
 
def print_solution(manager, routing, solution):
    """Prints solution on console."""
    index = routing.Start(0)
    plan_output = 'Route for vehicle:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    print(plan_output)
    plan_output += 'Route distance: {}miles\n'.format(route_distance)

# Driver Code
if __name__ == "__main__":
 
    # Input Matrix
	# "100" denotes that there doesn’t exist a path between those two indexed cities.
    tsp = [[0, 29, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 21],
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
        [40, 100, 100, 100, 100, 100, 100, 90, 100, 100, 100, 21, 0]]
 
    # Function Call
    findMinRoute(tsp)

