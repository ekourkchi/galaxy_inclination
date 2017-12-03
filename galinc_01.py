#!/usr/bin/python
import sys
import os
import subprocess
from math import *
import matplotlib.pyplot as plt
import numpy as np
import random

###########################
counter = 0


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
def insert_lst(list, value, i, manual=False):
    
    if manual:
        print
        print '************************'
        print 'Bingo: insering '+str(value)
        print '************************'
    
    N = len(list)
    if i<0 or i>N:
        return list
    
    if i == 0 : return [value]+list
    
    return list[0:i]+[value]+list[i:N]


##  [0 ... ]   [i_min value i_max]    [ ... N-1]
def insert_value(list, value, i_min, i_max, manual=False):
    
    N = len(list)
    
    if i_min>=i_max: 
        return insert_lst(list, value, N, manual=manual)          
    

    
    if i_max-i_min <3:
       while i_max-i_min <3:
            
           if i_min-1>-1:
               i_min-=1
           if i_max-i_min<3  and i_max+1<N:
               i_max+=1
       
           
    if i_max-i_min ==3:
       
       I = [i_min,i_min+1,i_min+2,i_max]
       n, quality, I = disp(list, I, value, sort=True, manual=manual)  # quality=True, I=unchanged
       return insert_lst(list, value, i_min+n, manual=manual)          
        
        
    
    elif i_max-i_min >3:  
       
       
       P = i_max-i_min+1
       
       i0 = P/5+i_min
       i1 = 2*P/5+i_min
       if i1<=i0: i1=i0+1
       i2 = 3*P/5+i_min
       if i2<=i1: i2=i1+1
       i3 = 4*P/5+i_min
       if i3<=i2: i3=i2+1
       
       I = [i0,i1,i2,i3]
       quality = False
       while quality==False:
          n, quality, I = disp(list, I, value, sort=False, manual=manual)  # if quality=False then I=changed
       
       if n>0 and n<4:
           i_min = I[n-1]
           i_max = I[n]
       elif n==0:
           i_max = I[0]
       elif n==4:
           i_min = I[3]
       
       return insert_value(list, value, i_min, i_max, manual=manual)
        
###########################  
def user_display(lst):
    
    for i in range(len(lst)):
        print str(i)+': ', lst[i]
    
    sort = np.argsort(lst) 
    print 'Suggested sort: ['+str(sort[0])+', '+str(sort[1])+', '+str(sort[2])+', '+str(sort[3])+', '+str(sort[4])+']'
    p = 0
    while p!= 5:
      ind = input('Enter your sort: ')
      p = len(ind)
      
      if sum(ind) != 10: p = 0 
    
    return np.asarray(ind) 

###########################  
   
def  disp(list, I, value, sort=True, manual=False):
    global counter 
    counter+=1
    
    if manual:
        print
        print '*** DISP ***'
        print 'Current list: ', list
        print 'selected inddices: ', I

    
    lst = [list[I[0]],list[I[1]],list[I[2]],list[I[3]], value]
     
     
    ## Machine sorting
    if not manual:
      ind = np.argsort(lst)   
    
    ## Manual Sorting
    else:
      ind = user_display(lst)
    

    
    ## Updating the list based on what users think
    m = 0
    for i in range(5):
       if ind[i] < 4:
          list[I[m]] = lst[ind[i]]
          m+=1 

    
    if sort:
        quality = True
    else:   
        quality, I = disp_modify(list, lst, I, ind)
    
    
    n = np.where(ind==4)[0][0]
    return  n, quality, I
    
###########################     
    
def  disp_modify(list, lst, I, ind):
    
    N = len(list)
    n = np.where(ind==4)[0][0]
    if n==0 or n==4: return True, I
    
    quality = False
    
    if n == 1:
      if list[I[0]]!=lst[0] or list[I[1]]!=lst[2]: 
        quality=True
      else:
        I[1]+=1
        I[0]+=1
    elif n == 2: 
      if list[I[1]]!=lst[1] or list[I[2]]!=lst[3]: 
        quality=True
      else:
        I[1]+=1
        I[2]+=1
    elif n == 3: 
      if list[I[2]]!=lst[2] or list[I[3]]!=lst[4]: 
        quality=True
      else:
        I[2]+=1
        I[3]+=1
    
    
    ## Taking care of boundary conditions
    if I[1]==I[0] : I[1]=I[0]+1
    if I[1]==I[2] : I[2]=I[1]+1
    if I[3]==I[2] : I[3]=I[2]+1
    
    if I[3]==N: 
        I[3]-=2
        if I[3]<=I[2] : I[2]=I[3]-1
        if I[2]<=I[1] : I[1]=I[2]-1
        if I[1]<=I[0] : I[0]=I[1]-1
    
    
    
    return quality, I
    
    
###########################
if __name__ == '__main__':
    
    print 'Welcome ...'
    
    ndisp = []
    Ngal_list = [10,100,200,400,800,1000,2000,4000,6000,8000,10000,12000,15000]
    
    for Ngal in Ngal_list:
        counter = 0
        list = [0,3,6,10,20]
        N = 4
        while N < Ngal:
            value = int(random.uniform(0, 100000))
            if not value in list:
              list = insert_value(list, value, 0, N, manual=False)
              N += 1
        
        
        #print list
        print 'Ngal, # disp: ', Ngal, counter
        ndisp.append(counter)
    
    
    
    fig = plt.figure(figsize=(7,6), dpi=100)
    ax = fig.add_axes([0.15, 0.12, 0.8,  0.8])
    
    ax.plot(Ngal_list, ndisp, 'o')
    
    x = np.asarray(Ngal_list)
    y = x*np.log10(x)/np.log10(5.)
    ax.plot(x,y)
    
    ax.set_xlabel('# of galaxies')
    ax.set_ylabel('# of displays')
    #plt.yscale('log')
    #plt.xscale('log')
    
    plt.show()

    
    
 
