""" MA3.py

Student:
Mail:
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc
import numpy as np

def approximate_pi(n): # Ex1
    #n is the number of points
    
    #inside circle
    xc = []
    yc = []
    
    #outside circle
    xo = []
    yo = []
    
    for i in range(0, n):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        
        if x**2 + y**2 < 1:
            xc.append(x)
            yc.append(y)
        else:
            xo.append(x)
            yo.append(y)
        
    plt.plot(xc, yc, 'o', color='red')
    plt.plot(xo, yo, 'o', color='blue')
    
    return 4 * (len(xc)/(len(xc) + len(xo)))

def sphere_volume(n, d): #Ex2, approximation
    insideCount = 0
    outsideCount = 0
    
    for i in range(0, n):
        
        s = 0
        
        coords = [random.uniform(-1, 1) for _ in range(0, d)]
        for c in coords:
            s += c**2
            
        if s < 1:
            insideCount += 1
        
    result = (insideCount/n) * 2**d
    print(result)
    return result

def hypersphere_exact(d): #Ex2, real value    
    return (np.pi**(d/2))/m.gamma((d/2) + 1)

#Ex3: parallel code - parallelize for loop
def sphere_volume_parallel1(n,d,np):
    #n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes
    with future.ProcessPoolExecutor() as ex:
        _n = [n for _ in range(0, np)]
        _d = [d for _ in range(0, np)]
        result = ex.map(sphere_volume, _n, _d)
        return sum(result)/np
    
    

#Ex4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel2(n,d,np=2):
        #n is the number of points
        # d is the number of dimensions of the sphere
        #np is the number of processes
        
        
        
        
        """with future.ProcessPoolExecutor() as ex:
            _n = [n for _ in range(0, np)]
            _d = [d for _ in range(0, np)]
            result = ex.map(one_sphere_parallell, _n, _d)
            print(result)
            return sum(list(result))/np"""
        
        resultLst = []
        
        for i in range(0, np):
            resultLst.append(one_sphere_parallell(n, d))
         
        #print(resultLst)
        return(sum(resultLst)/np)
        
def one_sphere_parallell(n, d):
    with future.ProcessPoolExecutor() as ex:
        _d = [d for _ in range(0, n)]
        result = ex.map(check_rnd_point_inside, _d)
        result = list(result)
        print(type(result))
        print(len(list(result)))
        print(sum(list(result)))
        return (sum(list(result))/len(list(result))) * (2**d)    
    
def check_rnd_point_inside(d):
    s = 0
    coords = [random.uniform(-1, 1) for _ in range(0, d)]
    for c in coords:
        s += c**2  
    if s < 1:
        return 1
    else:
        return 0    
    
def main():
    #Ex1
    """ dots = [1000, 10000, 100000]
    for n in dots:
        approximate_pi(n)
    #Ex2
    n = 100000
    d = 2
    sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)}")

    n = 100000
    d = 11
    sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)}")

    #Ex3
    n = 100000
    d = 11
    start = pc()
    for y in range (10):
        sphere_volume(n,d)
    stop = pc()
    print(f"Ex3: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?")"""

    #Ex4
    n = 1000000
    d = 11
    start = pc()
    sphere_volume(n,d)
    stop = pc()
    print(f"Ex4: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?")

    print(sphere_volume_parallel2(n, d))
    
    

if __name__ == '__main__':
	main()
