import numpy as np
from numpy import random

# Set problem
n_dest = 13 # Set number of destinations
dist_mat = np.array([[0, 29, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 21],
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

# Training
def update_q(q, dist_mat, state, action, alpha=0.012, gamma=0.4):
    imm_reward = rew = 1./ dist_mat[state,action]
    delayed_reward = q[action,:].max()
    q[state,action] += alpha * (imm_reward + gamma * delayed_reward - q[state,action])
    return q

q = np.zeros([n_dest,n_dest])
epsilon = 1. # Exploration parameter
n_train = 2000
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
        q = update_q(q, dist_mat, state, action)
        traj.append(action)
        state = traj[-1]
        possible_actions = [ dest for dest in range(n_dest) if dest not in traj]

    # Last trip: from last destination to wharehouse
    action = 0
    q = update_q(q, dist_mat, state, action)
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
    distance_travel += dist_mat[state, action]
    traj.append(action)
    state = traj[-1]
    possible_actions = [ dest for dest in range(n_dest) if dest not in traj ] 
# Back to warehouse
action = 0
distance_travel += dist_mat[state, action]
traj.append(action)

#Print Results:
print(f'Minimum Cost is: {distance_travel}')
print('Route for vehicle:')
print(' -> '.join([str(b) for b in traj]))
