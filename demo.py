from mclp import *
import numpy as np
from utils import generate_random_points, generate_candidate_sites, generate_distance_matrix, plot_result

Npoints = 300

# Candidate site size (random sites generated)
M = 30

points = generate_random_points(Npoints)

sites = generate_candidate_sites(points, M)

distance_matrix = generate_distance_matrix(points, sites)

# Number of sites to select
K = 5


# Maximum distance to be traveled to each site in meters
max_dist = 15000

# Run mclp 
# opt_sites is the location of optimal sites 
# f is the number of points covered
opt_sites, opt_sites_indices, f = mclp(points, sites, distance_matrix, K, max_dist)

print(opt_sites, opt_sites_indices, f)
         
# removing sites from the distance matrix which are not part of the solution
distance_matrix = np.delete(distance_matrix, [x for x in range(M) if x not in opt_sites_indices], 1)

#filtered_points = 
print(distance_matrix.shape)
print(distance_matrix)

point_allocations = {}

for s_idx, x in enumerate(distance_matrix.T):
    print(s_idx, opt_sites_indices[s_idx])
    point_allocations[opt_sites_indices[s_idx]] = []
    for idx, y in enumerate(x):
        if y == 1.0:
            point_allocations[opt_sites_indices[s_idx]].append(idx)

print(point_allocations)
# Plot the result 
plot_result(points, point_allocations, opt_sites)
