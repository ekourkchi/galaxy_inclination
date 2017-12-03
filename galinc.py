#!/usr/bin/python
import sys
import os
import subprocess
import math
import matplotlib.pyplot as plt
import numpy as np
import random

###########################
def randDegree(A):
    
    N = len(A)
    s = 0.
    for i in range(N):
        s += abs(i-A[i])
    
    return s/N**2

###########################

def randomize(A, p):
   
    N = len(A)
    
    for m in range(int(round(N*p))):
        
        i = int(random.uniform(0, N))
        j = int(random.uniform(0, N))
        tmp = A[i]
        A[i] = A[j]
        A[j] = tmp

    return A

###########################
def display(A, a_ind, P=None, Yes=False):
    
    a     = []
    p     = []
    
    # the number of images to display
    n_ind = len(a_ind)
    
    for i in range(n_ind):
        a.append(A[a_ind[i]])
        if Yes: p.append(P[a_ind[i]])
        
    
    a = np.asarray(a)
    a_ind = np.asarray(a_ind)
    if Yes: p = np.asarray(p)
    
        
    ind = np.argsort(a_ind)
    a_ind = a_ind[ind]
    a = a[ind]
    if Yes: p = p[ind]
        
    ind = np.argsort(a)
    a_new =  a[ind]
    if Yes: p_new = p[ind]
    
    for i in range(n_ind):
            A[a_ind[i]] = a_new[i]
            if Yes: P[a_ind[i]] = p_new[i]
    
    return A



###########################
def new_order(A, n):
    
    P = A*0
    N = len(A)
    n_disp_tot = 0 
    do = True
    #for iter in range(n):
    while do:
    
        a_ind = []
        n_disp = 0
        
        prob = []
        for i in range(N):
            m = 1
            if P[i] <10: m=11-P[i] 
            #if m==0: m+=1
            for j in range(m):
                prob.append(i)
          
        
        while n_disp<5:
            i_prob = int(random.uniform(0, len(prob)))
            i = prob[i_prob]
            if not i in a_ind:
                P[i] += 1
                a_ind.append(i)
                n_disp+=1
                
        n_disp_tot+=1
        display(A, a_ind, P=P, Yes=True)
        
        do = False
        for p in P:
            if p < 10: do = True
    
    print n_disp_tot
    return A

###########################


def order(A, n):
    
    N = len(A)
    P = A*0
    
    n_disp_tot = 0 
    do = True
    #for iter in range(n):
    while do:
        
        
        a_ind = []
        n_disp = 0
        
        while n_disp<5:
            i = int(random.uniform(0, N))
            if not i in a_ind:
                a_ind.append(i)
                n_disp+=1
                P[i] +=1
        
        display(A, a_ind, P=P, Yes=True)
        n_disp_tot +=1
        
        do = False
        for p in P:
            if p < 5: do = True
        
        
        
        
    
    print n_disp_tot
    return A
###########################

def esn_order(A, n):
    
    N = len(A)
    for iter in range(n):
       ty = int(random.uniform(0, 3))
       
       if ty == 0:
           a_ind = []
           m = int(random.uniform(0, N-125))
           a_ind.append(int(random.uniform(m, m+25)))
           a_ind.append(int(random.uniform(m+25, m+50)))
           a_ind.append(int(random.uniform(m+50, m+75)))
           a_ind.append(int(random.uniform(m+75, m+100)))
           a_ind.append(int(random.uniform(m+100, m+125)))
           display(A, a_ind)
       elif ty == 1:
           a_ind = []
           m = int(random.uniform(0, N-25))
           a_ind.append(int(random.uniform(m, m+5)))
           a_ind.append(int(random.uniform(m+5, m+10)))
           a_ind.append(int(random.uniform(m+10, m+15)))
           a_ind.append(int(random.uniform(m+15, m+20)))
           a_ind.append(int(random.uniform(m+20, m+25)))
           display(A, a_ind)
       elif ty == 2:
           m = int(random.uniform(0, N-5))
           a_ind = range(m,m+5)
           display(A, a_ind)
        
    return A
###########################

def merge5(list):
    
    list = np.asarray(list)
    
    N = len(list)
    m = N/5
    
    n_disp = 0
    
    for t in range(m,0,-1):
        
        #print ' t: ', t
        flag = list * 0
        i=0
        while i < N:
           
           
           if flag[i] == 1: 
               i +=1
               continue
           a_ind = [i]
           flag[i] == 1
           j1=i
           j2=i+t
           while j2 <  N:
             if flag[j2] == 1: break
             if j2/m == j1/m + 1: 
                 a_ind.append(j2)
                 flag[j2] = 1 
                 j1 = j2
                 j2 = j1+t
             else: break
           
           # evaluate a_ind
           if len(a_ind) > 1: 
               n_disp+=1
               list = display(list, a_ind)
               #print a_ind
               
           i+=1
             
    return n_disp, list    
        
###########################
###########################

def merge3(list):
    
    list = np.asarray(list)
    
    N = len(list)
    m = N/3
    
    n_disp = 0
    
    for t in range(m,0,-1):
        
        #print ' t: ', t
        flag = list * 0
        i=0
        while i < N:
           
           
           if flag[i] == 1: 
               i +=1
               continue
           a_ind = [i]
           flag[i] == 1
           j1=i
           j2=i+t
           while j2 <  N:
             if flag[j2] == 1: break
             if j2/m == j1/m + 1: 
                 a_ind.append(j2)
                 flag[j2] = 1 
                 j1 = j2
                 j2 = j1+t
             else: break
           
           # evaluate a_ind
           if len(a_ind) > 1: 
               n_disp+=1
               list = display(list, a_ind)
               #print a_ind
               
           i+=1
             
    return n_disp, list    
        
###########################    
    
def khafan_sort(list, n_disp):
    
    N = len(list)
    
    if N == 5:
        n_disp+=1
        return n_disp, display(list, [0,1,2,3,4])
    
    n = N / 5 
    n1, L1 = khafan_sort(list[0:n], n_disp)
    n2, L2 = khafan_sort(list[n:2*n], n_disp)
    n3, L3 = khafan_sort(list[2*n:3*n], n_disp)
    n4, L4 = khafan_sort(list[3*n:4*n], n_disp)
    n5, L5 = khafan_sort(list[4*n:N], n_disp)
    
    L = np.concatenate((L1,L2,L3,L4,L5))
    
    n0, L_sort = merge5(L)
    n_disp += n0 + n1 + n2 + n3 + n4 + n5 
    print n0, len(L)
    
    return n_disp, L_sort
     
    
    


###########################
if __name__ == '__main__':
    
    N = 625
    
    A = range(N)
    A = np.asarray(A)
    randomize(A, 1)
    B = np.copy(A)
    C = np.copy(A)
    print ' original:', randDegree(A)
    
    for iter in range(1):
      order(B, 1000)
      print '    order: ', randDegree(B)
  
    new_order(C, 1000)
    print 'new order: ', randDegree(C)
    #new_order(C, 1000)
    #print 'new order: ', randDegree(C)
        
    #list = [1,7,13,4,5,10,11,12,14,6,8,15,2,3,9]
    #n_disp, list = merge5(list)
    #print n_disp, list
    
    #A = range(N)
    #A = np.asarray(A)
    #randomize(A, 1)
    
    ###A = [ 3,  7,  2,  0,  18,  5,  23,  1, 8,  9, 10, 11, 12, 13, 14, 24, 16, 17, 4, 19, 20, 21, 22, 6, 15]
    #n_disp, L =  khafan_sort(A,0)
    #print 'khof order: ', randDegree(L)
    #print n_disp
    
    #A = [1,7,9,11]
    #B = [3,6,8,12]
    #C = [2,4,5,10]
    #D = A+B+C
    #n_disp, list = merge3(D)
    #print n_disp, list
    
