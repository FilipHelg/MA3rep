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
    for i in range(0, n): 
        s = 0
        coords = [random.uniform(-1, 1) for _ in range(0, d)]
        for c in coords:
            s += c**2
        if s < 1:
            insideCount += 1
        
    result = (insideCount/n) * 2**d
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
def sphere_volume_parallel2(n,d, np=2):
        #n is the number of points
        # d is the number of dimensions of the sphere
        #np is the number of processes 
        with future.ProcessPoolExecutor() as ex:
            _n = [n//np for _ in range(0, np)]
            _d = [d for _ in range(0, np)]
            total = 0
            result = ex.map(check_rnd_points_inside, _n, _d)
            result = list(result)
            total += sum(result)
            return (total/n) * (2**d)
    
def check_rnd_points_inside(n, d):  
    total = 0
    for _ in range(0, n):
        s = 0
        coords = [random.uniform(-1, 1) for _ in range(0, d)]
        for c in coords:
            s += c**2  
        if s < 1:
            total += 1    
    return total
       
def main():
    #Ex1
    dots = [1000, 10000, 100000]
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
    print("What is parallel time?")
    
    start = pc()
    print(sphere_volume_parallel1(n, d, 10))
    stop = pc()
    
    print(f"Ex4: Parallel time of {d} and {n}: {stop-start}")

    #Ex4
    n = 1000000
    d = 11
    start = pc()
    sphere_volume(n,d)
    stop = pc()
    print(f"Ex4: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?")

    start = pc()
    print(sphere_volume_parallel2(n, d))
    stop = pc()
    
    print(f"Ex4: Parallel time of {d} and {n}: {stop-start}")
    
    

if __name__ == '__main__':
	main()
