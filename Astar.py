# Author: Christian Careaga (christian.careaga7@gmail.com)
# A* Pathfinding in Python (2.7)
# Please give credit if used

import numpy
from math import *
from heapq import *


def heuristic(a, b):
    
    xd = b[0] - a[0]    
    yd = b[1] - a[1]   
    xd = abs(xd) 
    yd = abs(yd)
    d = sqrt(2)*min(xd,yd) + max(xd,yd) + min(xd,yd)
    return(d)

def movement(array,a, b):

    #Determining direction, 1 for diagonal, 0 for horizontal-vertical
    if(abs(b[1]-a[1]) + abs(b[0]-a[1]))==2:
        direction = 1
    else:
        direction = 0

    #cost from unblocked to unblocked
    if array[a[0]][a[1]]==1 and array[b[0]][b[1]]==1:
        if direction==1:
            cost = sqrt(2)
        else:
            cost = 1

    #cost from hard to unblocked or vice versa
    if (array[a[0]][a[1]]==1 and array[b[0]][b[1]]==2) or (array[a[0]][a[1]]==2 and array[b[0]][b[1]]==1):
        if direction==1:
            cost = 1.5*sqrt(2)
        else:
            cost = 1.5

    #cost from hard to hard
    if (array[a[0]][a[1]]==2 and array[b[0]][b[1]]==2):
        if direction==1:
            cost = 2*sqrt(2)
        else:
            cost = 2

    river_regular = [3,5,7,9]
    river_hard = [4,6,8,10]

    #cost from hard to river_regular or vice versa
    if ((array[a[0]][a[1]] in river_regular) and array[b[0]][b[1]]==2) or ((array[b[0]][b[1]] in river_regular) and array[a[0]][a[1]]==2):
        if direction==1:
            cost = 1.5*sqrt(2)
        else:
            cost = 1.5

    #cost from unblocked to river_regular or vice versa
    if ((array[a[0]][a[1]] in river_regular) and array[b[0]][b[1]]==1) or ((array[b[0]][b[1]] in river_regular) and array[a[0]][a[1]]==1):
        if direction==1:
            cost = sqrt(2)
        else:
            cost = 1

    #cost from hard to river_hard or vice versa
    if ((array[a[0]][a[1]] in river_hard) and array[b[0]][b[1]]==2) or ((array[b[0]][b[1]] in river_hard) and array[a[0]][a[1]]==2):
        if direction==1:
            cost = 2*sqrt(2)
        else:
            cost = 2

    #cost from unblocked to river_hard or vice versa
    if ((array[a[0]][a[1]] in river_hard) and array[b[0]][b[1]]==1) or ((array[b[0]][b[1]] in river_hard) and array[a[0]][a[1]]==1):
        if direction==1:
            cost = 1.5*sqrt(2)
        else:
            cost = 1.5

    #cost from river_regular to river_regular
    if ((array[a[0]][a[1]] in river) and array[b[0]][b[1]] in river)
        if direction==1:
            cost = 0.25*sqrt(2)
        else:
            cost = 0.25

    #cost from river_hard to river_hard
    if ((array[a[0]][a[1]] in river_hard) and array[b[0]][b[1]] in river_hard)
        if direction==1:
            cost = 0.5*sqrt(2)
        else:
            cost = 0.5

    #cost from river_hard to river_regular and vice versa
    if ((array[a[0]][a[1]] in river_hard) and array[b[0]][b[1]] in river_regular) or ((array[a[0]][a[1]] in river_regular) and array[b[0]][b[1]] in river_hard)
        if direction==1:
            cost = 0.375*sqrt(2)
        else:
            cost = 0.375

def astar(array, start, goal):

    neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

    close_set = set()
    came_from = {}
    gscore = {start:0}
    fscore = {start:heuristic(start, goal)}
    oheap = []

    heappush(oheap, (fscore[start], start))
    
    while oheap:

        current = heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j            
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:                
                    if array[neighbor[0]][neighbor[1]] == 0:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue
            
            tentative_g_score = gscore[current] + movement(array, current, neighbor)                
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue
    
            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heappush(oheap, (fscore[neighbor], neighbor))
                
    return False

'''Here is an example of using my algo with a numpy array,
   astar(array, start, destination)
   astar function returns a list of points (shortest path)'''

nmap = numpy.array([
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
    
print astar(nmap, (0,0), (10,13))