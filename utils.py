import random
import json
import numpy as np
from shapely.geometry import shape, Polygon, Point
from scipy.spatial import distance_matrix, ConvexHull
from matplotlib import pyplot as plt
import requests
from itertools import cycle


def generate_random_point(polygon):
      minx, miny, maxx, maxy = polygon.bounds
      pnt = [random.uniform(minx, maxx), random.uniform(miny, maxy)]
      return pnt

def generate_random_points(amount=100):
  
    f = open('berlin_poly.geojson',)
    poly = shape(json.load(f))
    random_pts = []
    for i in range(amount):
      r_coord = generate_random_point(poly)
      random_pts.append(r_coord)

    return np.array(random_pts)

def generate_candidate_sites(points, M=100):
    '''
    Generate M candidate sites with the convex hull of a point set
    Input:
        points: a Numpy array with shape of (N,2)
        M: the number of candidate sites to generate
    Return:
        sites: a Numpy array with shape of (M,2)
    '''
    hull = ConvexHull(points)
    polygon_points = points[hull.vertices]
    poly = Polygon(polygon_points)
    min_x, min_y, max_x, max_y = poly.bounds
    sites = []
    while len(sites) < M:
        random_point = Point([np.random.uniform(min_x, max_x),
                             np.random.uniform(min_y, max_y)])
        if (random_point.within(poly)):
            sites.append(random_point)
    return np.array([(p.x,p.y) for p in sites])


def generate_distance_matrix(points, sites):
    
    sources = list(range(points.shape[0]))
    destinations = list(range(points.shape[0], sites.shape[0] + points.shape[0]))
    coordinates = np.concatenate((points, sites), axis=0).tolist()

    POST_PAYLOAD = {'sources': sources, 'destinations': destinations, 'annotations': ['duration','distance'], 'coordinates': coordinates}

    resp = requests.post('http://localhost:5000/table', json=POST_PAYLOAD)
    distance_matrix = resp.json()['distances']
    return np.array(distance_matrix)


def plot_input(points):
    '''
    Plot the result
    Input:
        points: input points, Numpy array in shape of [N,2]
        opt_sites: locations K optimal sites, Numpy array in shape of [K,2]
        radius: the radius of circle
    '''
    fig = plt.figure(figsize=(8,8))
    plt.scatter(points[:,0],points[:,1],c='C0')
    ax = plt.gca()
    ax.axis('equal')
    ax.tick_params(axis='both',left=False, top=False, right=False,
                       bottom=False, labelleft=False, labeltop=False,
                       labelright=False, labelbottom=False)

def plot_result(points, point_allocations, opt_sites):
    '''
    Plot the result
    Input:
        points: input points, Numpy array in shape of [N,2]
        opt_sites: locations K optimal sites, Numpy array in shape of [K,2]
    '''
    fig = plt.figure(figsize=(8,8))
    plt.scatter(points[:,0],points[:,1], c='black', s=4)
    ax = plt.gca()
       
    plt.scatter(opt_sites[:,0],opt_sites[:,1],c='C1', s=200, marker='*')

    cycol = cycle('bgrcmk')

    for k, v in point_allocations.items():
        color = next(cycol)
        for point_idx in v:
            plt.scatter(points[point_idx][0],points[point_idx][1], c=color, marker='+')        

    # for site in opt_sites:
    #     circle = plt.Circle(site, radius, color='C1',fill=False,lw=2)
    #     ax.add_artist(circle)
    ax.axis('equal')
    ax.tick_params(axis='both',left=False, top=False, right=False,
                       bottom=False, labelleft=False, labeltop=False,
                       labelright=False, labelbottom=False)
    plt.show()


