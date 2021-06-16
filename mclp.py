"""

Python implementation of the maximum coverage location problem.

The program randomly generates a set of candidate sites, among 
which the K optimal candidates are selected. The optimization 
problem is solved by integer programming. 

Author: Can Yang
Date: 2019-11-22

MIT License

Copyright (c) 2019 Can Yang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""


import numpy as np
from mip import *


def mclp(points, sites, distance_matrix, K, max_distance):
    """
    Solve maximum covering location problem
    Input:
        points: input points, Numpy array in shape of [N,2]
        sites: input sites, Numpy array in shape of [N,2]
        distance_matrix: distance matrix Numpy array in shape of [N,2]
        K: the number of sites to select
        max_distance: maximum distance a site can serve
    Return:
        opt_sites: locations K optimal sites, Numpy array in shape of [K,2]
        f: the optimal value of the objective function
    """
    print('----- Configurations -----')
    print('  Number of points %g' % points.shape[0])
    print('  Number of sites %g' % sites.shape[0])
    print('  Amount of sites to select %g' % K)
    print('  Maximum distance (m) %g' % max_distance)
    import time
    start = time.time()
    J = sites.shape[0]
    I = points.shape[0]

    mask1 = distance_matrix<=max_distance
    distance_matrix[mask1]=1
    distance_matrix[~mask1]=0

    # Build model
    m = mip.Model()
    # Add variables
    x = {}
    y = {}
    for i in range(I):
      y[i] = m.add_var(var_type=mip.BINARY, name="y%d" % i)
    for j in range(J):
      x[j] = m.add_var(var_type=mip.BINARY, name="x%d" % j)

    #m.update()
    # Add constraints
    m.add_constr(mip.xsum(x[j] for j in range(J)) == K)
    

    for i in range(I):
        m.add_constr(mip.xsum(x[j] for j in np.where(distance_matrix[i]==1)[0]) >= y[i])

    m.objective = mip.maximize(mip.xsum(y[i] for i in range(I)))
    
    #m.setParam('OutputFlag', 0)
    
    m.optimize()
    end = time.time()
    print('----- Output -----')
    print('  Running time : %s seconds' % float(end-start))
    print('  Optimal coverage points: %g' % m.objective_value)
    
    solution = []
    if m.status == mip.OptimizationStatus.OPTIMAL:
        for v in m.vars:
            #print(v.x)
            if v.x==1 and v.name[0]=="x":
               solution.append(int(v.name[1:]))
    opt_sites = sites[solution]
    return opt_sites, solution, m.objective_value
