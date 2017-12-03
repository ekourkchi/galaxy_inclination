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
# This function inserts the new value at the index of i into the original list
# list: the original list
# value: the new value 
# i: the index at which the new value would be inserted
def insert_lst(list, value, i, manual=False):
    
    if manual:
        print
        print '************************'
        print 'Bingo: inserting '+str(value)
        print '************************'
    
    N = len(list)
    if i<0 or i>N:
        return list
    
    if i == 0 : return [value]+list
    
    return list[0:i]+[value]+list[i:N]

###########################
# The main Iterative function, with divides the original array to 5
# sub-arrays and tries to find the best palce for the givel value
##  
# list: the original array
# value: the new value
# i_min and i_max define the indices to define the sub-array where the value 
# would be finally inserted
# [0 ... i_min-1]   [i_min value i_max]    [i_max+1 ... N-1]
def insert_value(list, value, i_min, i_max, manual=False):
    
    N = len(list)
    
    # base case
    if i_min>=i_max: 
        return insert_lst(list, value, N, manual=manual)          
    

    # [i_min ... i_max] sub-array should have at least 4 members before adding the value
    if i_max-i_min <3:
       while i_max-i_min <3:
            
           if i_min-1>-1:
               i_min-=1
           if i_max-i_min<3  and i_max+1<N:
               i_max+=1
       
    # recursive case 
    # all the chosen members are next to each other (easy)   
    if i_max-i_min ==3:
       
       I = [i_min,i_min+1,i_min+2,i_max]
       n, quality, I = disp(list, I, value, sort=True, manual=manual)  # quality=True, I=unchanged
       return insert_lst(list, value, i_min+n, manual=manual)          
        
        
    # recursive case
    # the chosen members are far from each other 
    elif i_max-i_min >3:  
       
       
       P = i_max-i_min+1
       
       i0 = P/5+i_min
       i1 = 2*P/5+i_min
       if i1<=i0: i1=i0+1
       i2 = 3*P/5+i_min
       if i2<=i1: i2=i1+1
       i3 = 4*P/5+i_min
       if i3<=i2: i3=i2+1
       
       I = [i0,i1,i2,i3]  # I carries the indices of the chosen members form list
       quality = False
       
       # while user is updating the original list
       while quality==False:   
          n, quality, I = disp(list, I, value, sort=False, manual=manual)  # if quality=False then I=changed
       
       # n is the position of the new value from the perspective of the user
       # n=0 is the lowest number
       # n=4 is the largest number
       # 0<n<4: the new value falls between the chosen members
       if n>0 and n<4:
           i_min = I[n-1]
           i_max = I[n]
       elif n==0:
           i_max = I[0]
       elif n==4:
           i_min = I[3]
       
       return insert_value(list, value, i_min, i_max, manual=manual)
        
###########################  
# This functions simulates the experience of users
def user_display(lst):
    
    print
    print 'What users see ...'
    for i in range(len(lst)):
        print str(i)+': ', lst[i]
    
    sort = np.argsort(lst) 
    
    
    print 'Suggested sort by machine: ['+str(sort[0])+', '+str(sort[1])+', '+str(sort[2])+', '+str(sort[3])+', '+str(sort[4])+']'
    p = 0
    while p!= 5:
      print 'Enter the indices in a list ...'
      ind = input('Enter your manual sort: ')
      p = len(ind)
      
      if sum(ind) != 10: p = 0 
    
    return np.asarray(ind) 

###########################  
# This functions play the role of user display
# I: the indices of the list, whose values woule be displayed
# value: the new introduced value
# sort: true: when comparing the new value with all neighboring values in the list,
#       in this case updating and inserting takes place at the same time
#       false: the new value is compared to members are the list that are not next to 
#       each other 
# manual: False: machine does the comaprsions (for complexity analysis)
#         True: to simulate the user experience
def  disp(list, I, value, sort=True, manual=False):
    global counter 
    counter+=1
    
    if manual:
        print
        print '******* DISPLAY *******'
        print 'Current list: ', list
        print 'selected inddices: ', I
        print 'Introducing:', value
        print '***********************'

    
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
        # update I, i.e. use the neighboring values
        quality, I = disp_modify(list, lst, I, ind)
    
    
    n = np.where(ind==4)[0][0]
    return  n, quality, I
    
###########################     
# This is an auxiliary function that updates I (i.e. the indices of the list choosen for compariosn)
# If needed, the neighboring indices would be chosen until no more update is necessary, i.e. quality = True
def  disp_modify(list, lst, I, ind):
    
    N = len(list)
    n = np.where(ind==4)[0][0]
    
    ## case 1
    if n==0 or n==4: return True, I
    
    quality = False
    
    ## case 2 and 3
    ## If user 
    if n == 1:
      if list[I[0]]==lst[0] and list[I[1]]==lst[1]: 
        quality=True
      else:
        I[1]+=1
        I[0]+=1
    elif n == 2: 
      if list[I[1]]==lst[1] and list[I[2]]==lst[2]: 
        quality=True
      else:
        I[1]+=1
        I[2]+=1
    elif n == 3: 
      if list[I[2]]==lst[2] and list[I[3]]==lst[3]: 
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
    # if quality=True (no further update is necessary)
    # if quality=False (I has been updated) - repeating the process (display)

    
###########################
# Testing the degree of randomness of an array A=[0 ... N-1] 
def randDegree(A):
    
    N = len(A)
    s = 0.
    for i in range(N):
        s += abs(i-A[i])
    
    return s/N**2

###########################
# Randomizing a sorted array 
# p: is the degree of randomness
# N is the array length
# N*p is the number of pair that would be swapped
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
###########################
# This function update the array A, based on the indices in a_ind
# The corresponding elements in A, would be sorted
# The traditional display function 
def display(A, a_ind):
    
    a     = []
    p     = []
    
    # the number of images to display
    n_ind = len(a_ind)
    
    for i in range(n_ind):
        a.append(A[a_ind[i]])
        
    
    a = np.asarray(a)
    a_ind = np.asarray(a_ind)
    
        
    ind = np.argsort(a_ind)
    a_ind = a_ind[ind]
    a = a[ind]
        
    ind = np.argsort(a)
    a_new =  a[ind]
    
    for i in range(n_ind):
            A[a_ind[i]] = a_new[i]
    
    return A

###########################
###########################
# This fucntion, randmply chooses 5 items for  the list A
# and then sorts them, while it updates the list
# n: The number of iterations (# of 5-sorts)
def random_order(A, n):
    
    N = len(A)
    
    n_disp_tot = 0 
    do = True
    
    for iter in range(n):
        
        
        a_ind = []
        n_disp = 0
        
        while n_disp<5:
            i = int(random.uniform(0, N))
            if not i in a_ind:
                a_ind.append(i)
                n_disp+=1
        
        display(A, a_ind)
        n_disp_tot +=1
          
    return A
###########################
###########################
if __name__ == '__main__':
    
    
    N = 200
    
    A = range(N)
    randomize(A, 0.05)   # 10% randmized
    print 'original randomness degree:', randDegree(A)  
    
    B = np.asarray(A)
    
    
    
    list = A
    insertions_lst = []
    V = 100    # the length of the original list
    while len(list)>V:
        N = len(list)
        i = int(random.uniform(0, N))
        x = list.pop(i)
        insertions_lst.append(x)
    
    counter = 0
    N = len(list)-1
    while len(insertions_lst)>0:
        value = insertions_lst.pop(0)
        list = insert_value(list, value, 0, N, manual=False)
        N += 1
    
    
    print '# of dispplays: ', counter
    print '  binary order: ', randDegree(list)   # the randomness degree after sort
     
    random_order(B, counter)
    print '  random order: ', randDegree(B)      # the randomness degree after sort
    
    
    
    #print
    #print 'Welcome ...'
      
    
    ## the number of calls to "disp" function above
    #counter = 0  # this counts the number of times users have to see the display
    
    
    ## This is the original list of galaxies
    ## the inclination of the galaxies is simulated by numbers
    ## to showe that the algorithm works
    ## at least 5 galaxies must be already available in the list
    #list = [10,30,40,50,60]
    #N = 4
   
    ## introducing 4 more galaxies (we have already 5 galaxies in the list)
    #while N < 10:
       #value = int(random.uniform(10, 100))
       ## numbers in the list must be unique
       #if not value in list:
         #list = insert_value(list, value, 0, N, manual=True)
         #N += 1
        
        
    #print list
    #print '# of dispplays: ', counter
    
    
    

    
    
 
