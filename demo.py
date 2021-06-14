from mclp import *
import numpy as np
Npoints = 300
from sklearn.datasets import make_moons
points,_ = make_moons(Npoints,noise=0.15)

# Number of sites to select
K = 20

# Service radius of each site
radius = 0.2

# Candidate site size (random sites generated)
M = 100

# Run mclp 
# opt_sites is the location of optimal sites 
# f is the number of points covered
#opt_sites,f = mclp(points,K,radius,M)
opt_sites,f = mclp(points,K,radius,M)
# Plot the result 
plot_result(points,opt_sites,radius)
