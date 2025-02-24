import random

def collision_prob(n, k):
    prob = 1.0
    for i in range(1, k):
        prob *= ((n - i)/n)
    return 1 - prob

print(collision_prob(1000, 50))

def sim_insertions(num_indices, num_insertions):
    choices = range(num_indices)
    used = set()
    for i in range(num_insertions):
        hash_val = random.choice(choices)
        if hash_val in used:
            return 1
        else: used.add(hash_val)
    return 0

def find_prob(num_indices, num_insertions, num_trials):
    collision = 0
    for t in range(num_trials):
        collision += sim_insertions(num_indices, num_insertions)
    return collision/num_trials

print('Actual probability of a collision = ', collision_prob(1000, 50))
print("Est. probability of a collision = ", 
      find_prob(1000, 50, 10000))

print('Actual probability of a collision = ', collision_prob(1000, 200))
print("Est. probability of a collision = ", 
      find_prob(1000, 200, 10000))



