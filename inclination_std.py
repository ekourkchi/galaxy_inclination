#!/usr/bin/python
__author__ = "Ehsan Kourkchi"
__copyright__ = "Copyright 2017"
__credits__ = ["Ehsan Kourkchi"]
__version__ = "1.0"
__maintainer__ = "Ehsan Kourkchi"
__email__ = "ehsan@ifa.hawaii.edu"
__status__ = "Production"

import sys
import os
import subprocess
import getpass
from math import *
import numpy as np
from datetime import *
from pylab import *
import matplotlib as mpl
from matplotlib.widgets import Slider, Button, RadioButtons
import matplotlib.pyplot as plt
from astropy.table import Table, Column 
from mpl_toolkits.axes_grid1 import make_axes_locatable
from optparse import OptionParser
from random import random

from GUI_display import *


#################################
### Global Variables
filter='g'
std_folder='standards/'
gal_folder='galaxies/'
invert=False
flag_all=False
username = getpass.getuser()
#################################


def arg_parser():
    parser = OptionParser(usage="""\
\n
 - A GUI to sort galaxies based on their inclinations ...
 - Please visit the following URL for help and manual: https://github.com/ekourkchi/galaxy_inclination/blob/master/README.md

 - How to run: 
 
     $ python %prog -l [list_name] -g [galaxy_folder] -s [standard_folder] -f [filter] [-i]
 

 - Example(s): 
    
    $ python %prog -l list.csv -g ./galaxies -s ./standards -f g -i
    $ python %prog -h 
      To see help and all available options.
 
 - Author: "Ehsan Kourkchi"
 - Copyright 2017

""")
    
 
    parser.add_option('-l', '--list',
                      type='string', action='store',
                      help="""The input list """)
    
    parser.add_option("-g", "--galaxies",
                      type='string', action='store',
                      help="""The folder that contains galaxies images""")

    parser.add_option("-s", "--standards",
                      type='string', action='store',
                      help="""The folder that contains standards images""") 
    
    parser.add_option("-f", "--filter",
                      type='string', action='store',
                      help="""initial filter""")      
    
    parser.add_option("-i", action="store_true", help="initially invert images", default=False)
    
    parser.add_option("-a", action="store_true", help="allow flagging multiple images (except standards)", default=False)
    
    (opts, args) = parser.parse_args()
    return opts, args
########
#################################

def query_option():
    
    while True:
        
        print
        print "What is the reason for flagging this object (choose one)?"
        print "1 - Wrong Position Angle"
        print "2 - Too faint image"
        print "3 - Ambiguous, bad HI profile, not a good TF galaxy"
        print "4 - Cancel"
        print 
         
        sys.stdout.write('Please choose one (1-3): ')
        choice = str(raw_input().lower())
        
        if choice in ['1','2','3','4']:
            return int(choice)
        else:
            sys.stdout.write("Please respond with the option number\n")
    
#################################

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

#################################
# Definition of a galaxy
# each node contains all esseential property of a galaxy
# the context of this code
class GalxyNode:
  # Class constructor
  def __init__(self, pgc, inc=-1, flag=0, sort=0, reason=0, user='nan', dPA=0):
      
      self.pgc    = pgc     # PGC ID
      self.inc    = inc     # inclination (degree)
      self.flag   = flag    # =-1 for standards, >0 for flagged by user
      self.sort   = sort    # how many times it's displaced 
      self.reason = reason  # =1: bad Position Angle
                            # =2: too faint to determine the inclination
                            # =3: reject it, not a good TF galaxy
      self.user   = user
      self.dPA    = dPA     # difference in Position Angle (degree)
                            # This tells the GUI how much to rotate each galaxy
                            # when displaying
#################################
def listWrite(outfile, list):
   
  NoGals = len(list)
  myTable = Table()
  
  empty = []
  myTable.add_column(Column(data=empty,name='pgc', dtype=np.dtype(int)))
  myTable.add_column(Column(data=empty,name='inc', format='%0.1f'))
  myTable.add_column(Column(data=empty,name='flag', dtype=np.dtype(int)))
  myTable.add_column(Column(data=empty,name='sort', dtype=np.dtype(int)))
  myTable.add_column(Column(data=empty,name='reason', dtype=np.dtype(int)))
  myTable.add_column(Column(data=empty,name='dPA', dtype=np.dtype(int)))
  myTable.add_column(Column(data=empty,name='user', dtype='S16'))
  
  ################### BEGIN - Modifying inclinations using standard inclinations
  inc_piv_top = -10
  inc_piv_bot = 100
  inc_piv = -10
  
  p = 0
  while p<NoGals:
     if list[p].flag==-1:
        inc_piv_bot=list[p].inc
        break
     p+=1 
  if p==NoGals:
     inc_piv_top=100
  
  for i in range(NoGals):
      galaxy = list[i]
      if galaxy.flag==0 and (galaxy.inc<inc_piv_top or galaxy.inc>inc_piv_bot or galaxy.inc<inc_piv):
            
            p = i-1
            inc1 = -1
            while p>=0:
                if list[p].inc>0 and list[p].flag<0:
                   inc1 = list[p].inc
                   break
                p-=1
            
            p = i+1
            inc2 = -1
            while p<NoGals:
                if list[p].inc>0 and list[p].flag<0:
                   inc2 = list[p].inc
                   break
                p+=1    
            
            if inc1!=-1 and inc2!=-1:
                galaxy.inc = 0.5*(inc1+inc2)
            
            if p==NoGals: 
                galaxy.inc = inc1  
            
            inc_piv = galaxy.inc
            
      if galaxy.flag==-1:  
          if galaxy.inc>=inc_piv_top: 
             inc_piv_top = galaxy.inc
          p = i+1
          while p<NoGals:
              if list[p].flag==-1:
                  if list[p].inc<=inc_piv_bot: 
                     inc_piv_bot=list[p].inc
                     break
              p+=1 
          if p==NoGals:
              inc_piv_top=100
  ################### END - Modifying inclinations
  
  
          

  flagged_lst = []
  unflagged_lst = []
  for i in range(NoGals):
      galaxy = list[i]
      if galaxy.flag<=0:
         unflagged_lst.append(galaxy)
      else:
         flagged_lst.append(galaxy)

  
  incls = []
  for i in range(len(unflagged_lst)):
      galaxy = unflagged_lst[i]
      incls.append(galaxy.inc)
  incls=np.asarray(incls)
  indices = np.argsort(incls, kind='mergesort')

  unflagged_lst_sort = []
  for i in range(len(indices)):
    unflagged_lst_sort.append(unflagged_lst[indices[i]])
  unflagged_lst = unflagged_lst_sort
  
  for i in range(len(unflagged_lst)):
      galaxy = unflagged_lst[i]
      myTable.add_row([galaxy.pgc, galaxy.inc, galaxy.flag, galaxy.sort, galaxy.reason, galaxy.dPA, galaxy.user])  
   
         
  for i in range(len(flagged_lst)):
      galaxy = flagged_lst[i]
      myTable.add_row([galaxy.pgc, galaxy.inc, galaxy.flag, galaxy.sort, galaxy.reason, galaxy.dPA, galaxy.user])
  
  myTable.write(outfile, format='ascii.fixed_width',delimiter=',', bookend=False, overwrite=True)
  
  unflag_index = len(unflagged_lst)
  
  return unflagged_lst+flagged_lst, unflag_index
 

###########################
# This function inserts the new value at the index of i into the original list
# list: the original list
# value: the new value 
# i: the index at which the new value would be inserted
def insert_lst(list, value, i, status=0):
    

    if status>0:
        return list
       
    N = len(list)

    if i<0 or i>N:
        return list
    
    if i == 0 : return [value]+list
    
    p = i-1
    inc1 = -1
    while p>=0:
        if list[p].inc>0 and list[p].flag<0:
           inc1 = list[p].inc
           break
        p-=1
    
    p = i
    inc2 = -1
    while p<N:
        if list[p].inc>0 and list[p].flag<0:
           inc2 = list[p].inc
           break
        p+=1    
    
    if inc1!=-1 and inc2!=-1:
        value.inc = 0.5*(inc1+inc2)
    
    if p==N: 
        value.inc = inc1
        
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
def insert_value(list, value, i_min, i_max, N_max):
    

    # base case
    if i_min>=i_max: 
        return insert_lst(list, value, N_max)          
    

    # [i_min ... i_max] sub-array should have at least 4 members before adding the value
    if i_max-i_min <3:
       while i_max-i_min <3:
            
           if i_min>0:
               i_min-=1
           if i_max-i_min<3  and i_max+1<N_max:
               i_max+=1
       
    # recursive case 
    # all the chosen members are next to each other (easy)   
    if i_max-i_min ==3:
       
       I = [i_min,i_min+1,i_min+2,i_max]
       I = modBoundary(list, I, N_max)
       n, quality, I, status = disp(list, I, value, N_max, sort=True)  # quality=True, I=unchanged
       
       return insert_lst(list, value, I[0]+n, status=status), status          
        
        
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
       
       I = modBoundary(list, I, N_max)
       
       quality = False
       
       # while user is updating the original list
       while quality==False:   

          n, quality, I, status = disp(list, I, value, N_max, sort=False)  # if quality=False then I=changed
          if status>0: return list, status
       
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
       
       return insert_value(list, value, i_min, i_max, N_max)
        


###########################  
# This functions play the role of user display
# I: the indices of the list, whose values woule be displayed
# value: the new introduced value
# sort: true: when comparing the new value with all neighboring values in the list,
#       in this case updating and inserting takes place at the same time
#       false: the new value is compared to members are the list that are not next to 
#       each other 

def  disp(list, I, value, N_max, sort=True):

    global std_folder, gal_folder, filter, invert, flag_all, username
    
    lst = [list[I[0]],list[I[1]],list[I[2]],list[I[3]], value]

    ## Manual Sorting (GUI)
    galaxies = [lst[0].pgc,lst[1].pgc,lst[2].pgc,lst[3].pgc,lst[4].pgc]
    Flags = [lst[0].flag,lst[1].flag,lst[2].flag,lst[3].flag,lst[4].flag]
    INCS  = [lst[0].inc,lst[1].inc,lst[2].inc,lst[3].inc,lst[4].inc]
    PAA   = [lst[0].dPA,lst[1].dPA,lst[2].dPA,lst[3].dPA,lst[4].dPA]
    ind, flag, status, PA =  display(galaxies, Flags=Flags, INCS=INCS, filter=filter, std_folder=std_folder, gal_folder=gal_folder, invert=invert, flag_all=flag_all, dPA=PAA)
    
      
          
    if status>0:
        return 0, True, [0,1,2,3], status
    
    ind = np.asarray(ind)

    for i in range(5):
        lst[ind[i]].dPA = PA[i]
    
    ## Updating the list based on what users think
    m = 0
    exit = False
    for i in range(5):
       if ind[i] < 4:
          if list[I[m]].pgc!=lst[ind[i]].pgc:
             list[I[m]] = lst[ind[i]]
             if list[I[m]].flag!= -1:  # if non-standardsa are moved
               list[I[m]].sort+=1
               list[I[m]].user = username
          if flag[i]:                  # if an already listed non-standard is flagged
             list[I[m]].flag=1
             list[I[m]].reason=3
             list[I[m]].user = username
          elif list[I[m]].flag>0:      # if a non-standard is unflagged
             list[I[m]].flag=0
             list[I[m]].reason=0
             list[I[m]].user = username
          m+=1 
       elif flag[i]:
           exit = True

    if exit:
        value.flag = 1
        return 0, True, [0,1,2,3], True
    
    lst_ = [] 
    for i in range(5):
       lst_.append(lst[ind[i]])
    
    if sort:
        quality = True
    else:   
        # update I, i.e. use the neighboring values
        quality, I = disp_modify(list, lst_, I, ind, N_max)
    
    
    n = np.where(ind==4)[0][0]
    return  n, quality, I, status
    
###########################     
# This is an auxiliary function that updates I (i.e. the indices of the list choosen for compariosn)
# If needed, the neighboring indices would be chosen until no more update is necessary, i.e. quality = True
def  disp_modify(list, lst, I, ind, N_max):
    
    N = len(list)
    n = np.where(ind==4)[0][0]
    

    
    ## case 1
    if n==0 or n==4: return True, I
    
    quality = False
    
    ## case 2 and 3
    ## If user 
    if n == 1:
      if list[I[0]].pgc==lst[0].pgc and list[I[1]].pgc==lst[2].pgc: 
        quality=True
      else:
        I[1]+=1
        I[0]+=1
    elif n == 2: 
      if list[I[1]].pgc==lst[1].pgc and list[I[2]].pgc==lst[3].pgc: 
        quality=True
      else:
        I[1]+=1
        I[2]+=1
    elif n == 3: 
      if list[I[2]].pgc==lst[2].pgc and list[I[3]].pgc==lst[4].pgc: 
        quality=True
      else:
        I[2]+=1
        I[3]+=1
    

    ## Taking care of boundary conditions
    I = modBoundary(list, I, N_max, mod=True)

    return quality, I
    # if quality=True (no further update is necessary)
    # if quality=False (I has been updated) - repeating the process (display)
   
#################################################################  
def modBoundary(list, I, N_max, mod=False):


    i0,i1,i2,i3 = modBoundary_rute(I[0],I[1],I[2],I[3],N_max, mod=mod)
    counter = 0
    
    while counter<10 and (list[i0].flag>0 or list[i1].flag>0 or list[i2].flag>0 or list[i3].flag>0):
           
           counter+=1
           
           if list[i0].flag>0:
               i0+=1
               i0,i1,i2,i3 = modBoundary_rute(i0,i1,i2,i3,N_max, mod=mod)
           if list[i1].flag>0:
               i1+=1
               i0,i1,i2,i3 = modBoundary_rute(i0,i1,i2,i3,N_max, mod=mod)           
           if list[i2].flag>0:
               i2+=1
               i0,i1,i2,i3 = modBoundary_rute(i0,i1,i2,i3,N_max, mod=mod)
           if list[i3].flag>0:
               i3+=1
               i0,i1,i2,i3 = modBoundary_rute(i0,i1,i2,i3,N_max, mod=mod)
           

    I = [i0,i1,i2,i3]
    
    return I
################################################################# 
def modBoundary_rute(i0,i1,i2,i3,N_max, mod=False):
    
    ## Taking care of boundary conditions
    if i1==i0 : i1=i0+1
    if i1==i2 : i2=i1+1
    if i3==i2 : i3=i2+1
    
    if i3>=N_max: 
        i3=N_max-1
        if i3<=i2 : i2=i3-1
        if i2<=i1 : i1=i2-1
        if i1<=i0 : i0=i1-1       
    
    if mod and i3==N_max-1 and i0==i3-3:
        i0-=2
        i1-=2
        i2-=2
        i3-=2
        
    return i0,i1,i2,i3
 
#################################################################

if __name__ == '__main__':
    
   ## Example run:
   ## python inclination_std.py -l PNG_rotate.lst -g PNG_rotate -s standards -f g -i
    
   opts, args =  arg_parser()
   
   listName   = opts.list
   std_folder = opts.standards
   gal_folder = opts.galaxies
   filter     = opts.filter
   invert     = opts.i
   flag_all   = opts.a

   if filter==None:
       filter = 'gri'
   
   print
   print "List Name      : ", listName
   print "Galaxie        : ", gal_folder
   print "Standards      : ", std_folder
   print "Default Filter : ", filter
   print "Invert Image   : ", invert 
   print "Multiple Flags : ", flag_all   
   print
   if None in [listName, std_folder, gal_folder]:
       print "\nNot enough input arguments ..."
       print >> sys.stderr, "Use \"python "+sys.argv[0]+" -h\" for help ...  \n"
       sys.exit(1)
       
   

   
   
   #std_folder='standards/'
   #gal_folder='PNG_rotate/'
   #listName = 'PNG_rotate.lst'
   #filter='g'
   #invert=True
   

   
   
#########################################   
   
   std_folder+='/'
   gal_folder+='/'
   outFile = listName+'.output'
   if not os.path.isfile(outFile):
       print outFile+' is not availabe, generating ...'
       try: 
          xcmd('cp .std.73.lst '+outFile,True)
       except:
          print 'Error: Could not generate '+outFile
          print
          sys.exit(1)
          
#########################################   
   mytable = np.genfromtxt(outFile , delimiter=',', filling_values=None, names=True, dtype=None )
   pgc    = mytable['pgc']
   inc    = mytable['inc']
   flag   = mytable['flag']
   sort   = mytable['sort']
   reason = mytable['reason']
   user   = mytable['user']
   

   try:
      dPA = mytable['dPA']
   except:
      print "[Warning] OLD output file, it'll be updated ..." 
      dPA    = inc*0.
   
   
   
   for i in range(len(user)):
       user[i] = ''.join(user[i].split())
   
   
   n = len(pgc)
   list = []
   N_max = 0
   for i in range(n):
       if flag[i]<=0: N_max+=1
       list.append(GalxyNode(pgc[i],inc=inc[i], flag=flag[i], sort=sort[i], reason=reason[i], user=user[i], dPA=dPA[i]))
       

   mytable = np.genfromtxt(listName , delimiter=',', filling_values=None, names=True, dtype=None )
   PGC_   = mytable['pgc']
   N = PGC_.size
   
   if N==0:
       print "There is no more object in the list ...."
       sys.exit()
   
   seed(np.random.random_integers(0,N-1))
   
   PGC = []
   if N>1:
       for i in range(N):
           PGC.append(PGC_[i])
   elif N>0: 
       PGC=[PGC_]

      
   cntnu = True
   while len(PGC)>0 and cntnu:
       
       n = len(list)
       N = len(PGC)
       i = int(np.floor(uniform(0,N)))
       value = GalxyNode(PGC[i], user=username)
       status= 2 # 3:exit, 2:redo, 1:flag, 0:done
       unexpected = False
       
       while status==2: # redo
           try: 
             list, status = insert_value(list, value, 0, N_max, N_max)
             if value.flag > 0 :   # flagged
                 print
                 print '!!! !!! !!! !!! !!! !!! !!! !!! !!! !!! !!! !!! !!! !!! !!!'
                 if query_yes_no("Are you sure you want to flag pgc"+str(value.pgc)+"?", default='no'):
                   
                   choice = query_option()
                   if choice!=4:
                       value.reason = choice 
                       print "pgc"+str(value.pgc)+' was flagged successfully ...'
                       list = insert_lst(list, value, 0)
           except:
             print "GUI was closed unexpectedly ..."
             unexpected = True
             status=0
           

       if status<2 and not unexpected:   #  1:flag, 0:done
           list, N_max = listWrite(outFile, list)
           print 'Updated output file: '+outFile
       
       m = len(list)
       
       if m==n:
           print "No object added ...."
           print "Number of remaining galaxies: ", len(PGC)
       if m==n+1:
           print "Thanks, pgc"+str(value.pgc)+" ... added successfully"
           PGC.pop(i)
           PGC_ = np.asarray(PGC)
           
           if len(PGC_)==0: 
               with open(listName, 'w') as the_file:
                   the_file.write('pgc\n')
           else: 
               myTable = Table()
               myTable.add_column(Column(data=PGC_,name='pgc', dtype=np.dtype(int)))
               myTable.write(listName, format='ascii.fixed_width',delimiter=',', bookend=False, overwrite=True)
           print "Number of remaining galaxies: ", len(PGC)
       
       
       if status!=3 and len(PGC)>0:
          cntnu = query_yes_no("Do you want to continue?")

       
       if status==3 or not cntnu:  # Exit
          print
          print "  Thanks a lot. Bye :)"
          print
          break       

   

      
   
   
   
   
   

     
     
     
