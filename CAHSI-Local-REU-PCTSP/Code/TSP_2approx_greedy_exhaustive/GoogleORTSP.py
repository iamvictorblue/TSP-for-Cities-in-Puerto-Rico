
def create_data_model():
    """Stores the data for the problem."""
    data = {}
    # "100" refers to unknown locations in adjacency matrix.
    data['distance_matrix'] = [
        [0, 29, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 21],
        [29, 0, 33 , 100, 100, 47, 100, 100, 100, 100, 100, 100, 100],
        [100, 33 , 0, 42, 100, 20, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 42, 0, 66, 35, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 66, 0, 82, 100, 100, 100, 100, 100, 100, 100],
        [100, 47, 20, 35, 100, 0, 40, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 82, 40, 0, 63, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 63, 0, 86, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 86, 0, 79, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 79, 0, 70, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 70, 0, 53, 100],
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 53, 0, 21],
        [40, 100, 100, 100, 100, 100, 100, 90, 100, 100, 100, 21, 0]
    ]  # yapf: disable
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data

def print_solution(manager, routing, solution):
    """Prints solution on console."""
    print()
    print('Minimum Cost is : {} miles'.format(solution.ObjectiveValue()))
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


      



