#!/usr/bin/python
__author__ = "Ehsan Kourkchi"
__copyright__ = "Copyright 2017"
__credits__ = ["Ehsan Kourkchi"]
__version__ = "1.0"
__maintainer__ = "Ehsan Kourkchi"
__email__ = "ehsan@ifa.hawaii.edu"
__skip__ = "Production"

import sys
import os
import subprocess
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
from PIL import Image#, ImageTk
from subprocess import Popen, PIPE
import matplotlib.patches as patches
import scipy.misc as scimisc
#################################

def xcmd(cmd,verbose):

  if verbose: print '\n'+cmd

  tmp=os.popen(cmd)
  output=''
  for x in tmp: output+=x
  if 'abort' in output:
    failure=True
  else:
    failure=tmp.close()
  if False:
    print 'execution of %s failed' % cmd
    print 'error is as follows',output
    sys.exit()
  else:
    return output

#################################
# takes two axes and swaps their zoom properties
def swap_zoom_prop(myAX1, myAX2):
    
    tmp = myAX2.disp.x1
    myAX2.disp.x1 = myAX1.disp.x1
    myAX1.disp.x1 = tmp
    
    tmp = myAX2.disp.x2
    myAX2.disp.x2 = myAX1.disp.x2
    myAX1.disp.x2 = tmp
    
    myAX1.ax.set_xlim(myAX1.disp.x1, myAX1.disp.x2)
    myAX2.ax.set_xlim(myAX2.disp.x1, myAX2.disp.x2)
    
    tmp = myAX2.disp.y1
    myAX2.disp.y1 = myAX1.disp.y1
    myAX1.disp.y1 = tmp
    
    tmp = myAX2.disp.y2
    myAX2.disp.y2 = myAX1.disp.y2
    myAX1.disp.y2 = tmp            
    
    myAX1.ax.set_ylim(myAX1.disp.y1, myAX1.disp.y2)
    myAX2.ax.set_ylim(myAX2.disp.y1, myAX2.disp.y2)
    
    tmp = myAX2.angle
    myAX2.angle = myAX1.angle
    myAX1.angle = tmp
    
    tmp = myAX2.invert
    myAX2.invert = myAX1.invert
    myAX1.invert = tmp    
#################################################
class ImDisp:
  
  def __init__(self, Xmin, Xmax, Ymin, Ymax):
    self.Xmin = Xmin
    self.Xmax = Xmax
    self.Ymin = Ymin
    self.Ymax = Ymax
    
    self.x1 = Xmin
    self.x2 = Xmax
    self.y1 = Ymin
    self.y2 = Ymax
  
  def zoom(self, xc=None, yc=None, ratio=1):
    
    if xc== None:
        xc=0.5*(self.Xmin+self.Xmax)
    if yc== None:
        yc=0.5*(self.Ymin+self.Ymax)
    
    delta_x = self.x2 - self.x1
    delta_y = self.y2 - self.y1
    
    dx = 0.5 * ratio * delta_x
    dy = 0.5 * ratio * delta_y
    
    ###
    if xc + dx > self.Xmax:
      self.x2 = self.Xmax
      self.x1 = self.Xmax - 2. * dx
    elif xc - dx < self.Xmin:
      self.x1 = self.Xmin
      self.x2 = self.Xmin + 2. * dx
    else: 
      self.x1 = xc - dx
      self.x2 = xc + dx
    
    if self.x1 < self.Xmin:
      self.x1 = self.Xmin
    if self.x2 > self.Xmax:
      self.x2 = self.Xmax
    ###
    if yc + dy > self.Ymax:
      self.y2 = self.Ymax
      self.y1 = self.Ymax - 2. * dy
    elif yc - dy < self.Ymin:
      self.y1 = self.Ymin
      self.y2 = self.Ymin + 2. * dy
    else: 
      self.y1 = yc - dy
      self.y2 = yc + dy  
      
    if self.y1 < self.Ymin:
      self.y1 = self.Ymin
    if self.y2 > self.Ymax:
      self.y2 = self.Ymax
    ###
    
  def zoom_IN(self, xc=None, yc=None, ratio=0.9):
    
    if xc== None:
        xc=0.5*(self.Xmin+self.Xmax)
    if yc== None:
        yc=0.5*(self.Ymin+self.Ymax)
        
    self.zoom(xc=xc, yc=yc, ratio=ratio)
    return self.x1, self.x2, self.y1, self.y2
      
  def zoom_OUT(self, xc=None, yc=None, ratio=10./9):
      
    if xc== None:
        xc=0.5*(self.Xmin+self.Xmax)
    if yc== None:
        yc=0.5*(self.Ymin+self.Ymax)
        
    self.zoom(xc=xc, yc=yc, ratio=ratio)
    return self.x1, self.x2, self.y1, self.y2  

  def reset(self):
    self.x1 = self.Xmin
    self.x2 = self.Xmax
    self.y1 = self.Ymin
    self.y2 = self.Ymax
    return self.x1, self.x2, self.y1, self.y2
  
  def pan(self, xc, yc):
    self.zoom(xc, yc, ratio=1)
    return self.x1, self.x2, self.y1, self.y2 
    
    
    


#################################################
class My_ax:
    
    def __init__(self, fig, position, image, filter='', pgc=0, index=-2, im_folder='', angle=0):
        
        self.garbage = False
        self.position = position
        self.image = image
        
        self.ax = fig.add_axes(position)

        col = 'lightgray'
        self.ax.spines['bottom'].set_color(col)
        self.ax.spines['top'].set_color(col)
        self.ax.spines['right'].set_color(col)
        self.ax.spines['left'].set_color(col)
        self.ax.tick_params('off')
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        
        self.ax.set_xlim(0,400)
        self.ax.set_ylim(0,400)
        
        self.selpoint, = self.ax.plot([], [],  'o', color='orangered')
        self.ax.imshow(image)
        
        self.selected = False
        self.angle = angle
        self.invert = False
        
        self.pgc = pgc
        self.index = index+1
        
        self.im_folder = im_folder
        self.flag = None
        self.inc = None
        
        self.pgc_txt = self.ax.annotate('', (0.05,0.05), color='green', size=10, xycoords='axes fraction')
        self.index_txt = self.ax.annotate('', (0.05,0.920), color='green', size=10, xycoords='axes fraction')
        self.filter_txt = self.ax.annotate('', (0.875,0.920), color='green', size=10, xycoords='axes fraction')
        self.inc_txt = self.ax.annotate('', (0.70,0.05), color='green', size=10, xycoords='axes fraction')
        
        x_max, y_max, dimension = self.image.shape
        x_min = 0
        y_min = 0
        
        self.disp = ImDisp(x_min, x_max, y_min, y_max)
        
        
        if pgc>0:
            self.pgc_txt.set_text('pgc: '+str(pgc))
        if index>-1:
            self.index_txt.set_text(str(index))
            
        self.filter = filter
        if self.filter in ['g','r','i']:
            self.filter_txt.set_text(self.filter)
                
    def select(self, selected):
        
        if selected:
            self.selpoint.set_xdata([380])
            self.selpoint.set_ydata([20])
            self.selected = True
            
            col = 'orangered'
            self.ax.spines['bottom'].set_color(col)
            self.ax.spines['top'].set_color(col)
            self.ax.spines['right'].set_color(col)
            self.ax.spines['left'].set_color(col)
            
        else:
            
            col = 'lightgray'
            self.ax.spines['bottom'].set_color(col)
            self.ax.spines['top'].set_color(col)
            self.ax.spines['right'].set_color(col)
            self.ax.spines['left'].set_color(col)            
            self.selpoint.set_xdata([])
            self.selpoint.set_ydata([])
            self.selected = False
    
    def flip_garbage(self):
        
        if self.garbage:
            self.garbage = False
            self.pgc_txt.set_color('green')
            self.index_txt.set_color('green')
            self.index_txt.set_text(str(self.index))
            self.filter_txt.set_color('green')
            self.inc_txt.set_color('green')
            if self.index==5:
                self.index_txt.set_text('??')
        else:
            self.garbage = True
            self.pgc_txt.set_color('red')
            self.index_txt.set_color('red')
            self.index_txt.set_text(str(self.index)+' X')
            self.filter_txt.set_color('red')  
            self.inc_txt.set_color('red')
            if self.index==5:
                self.index_txt.set_text('!? x')
            #self.pgc_txt.set_position([200,200])
        return self.garbage
        
    
    def set_image(self, image, filter='', pgc=0, index=-2, only_image=False, garbage=False, im_folder=None, flag=None, inc=None):
        
        self.filter = filter   
        
        if im_folder!=None:
           self.im_folder = im_folder
        if flag!=None:
           self.flag = flag     
           
        if inc!=None:
           self.inc = inc               
        
        if self.filter == 'gri':
            inv = not self.invert
        else:
            inv = self.invert
                       
        
        image = scimisc.imrotate(image, self.angle, interp='bilinear')
        

        if inv:      
           self.image = 255-image
        else:
           self.image = image

            
         

        self.ax.imshow(self.image)

        

        if not only_image:
          self.pgc = pgc
          self.index = index+1  
          self.garbage = garbage
          
        if self.filter in ['g','r','i', '']:
           self.filter_txt.set_text(self.filter)
        
        if self.filter == 'gri':
           self.filter_txt.set_text('gri')
        
        if self.pgc>0:
            self.pgc_txt.set_text('pgc: '+str(self.pgc))
        else:
            self.pgc_txt.set_text('')
            
        if self.index>-1 and self.flag==-1:
            self.index_txt.set_text(str(self.index)+' ***')  
        elif self.index>-1:
            self.index_txt.set_text(str(self.index)) 
        else:
            self.index_txt.set_text('')
        
        if self.index==5:
            if not self.garbage:
               self.index_txt.set_text('??')
            else: self.index_txt.set_text('!? x')
        
        if self.inc>=0 and self.flag==-1:
            self.inc_txt.set_text(str(self.inc)+r'$^o$')
        elif self.inc>=0 and self.flag>=0:
            self.inc_txt.set_text('('+str(self.inc)+r'$^o )$')    
        else:
            self.inc_txt.set_text('')
        
        if self.garbage:
            self.pgc_txt.set_color('red')
            self.index_txt.set_color('red')
            self.index_txt.set_text(str(self.index)+' X')
            self.filter_txt.set_color('red')  
            self.inc_txt.set_color('red') 
            if self.index==5:
                self.index_txt.set_text('!? x')
        else:
            self.pgc_txt.set_color('green')
            self.index_txt.set_color('green')
            if self.index>-1 and self.flag==-1:
                self.index_txt.set_text(str(self.index)+' ***')  
            elif self.index>-1:
                self.index_txt.set_text(str(self.index)) 
            self.filter_txt.set_color('green')          
            self.inc_txt.set_color('green')
            if self.index==5:
                self.index_txt.set_text('??')
        

def swap_lst(lst, i, j):
    
    N = len(lst)
    
    if i<0 or j<0: return lst
    if i>=N or i>=N: return lst
    if i==j: return lst
    
    ## to make sure i<j
    if j<i:  # swap them
        tmp = j
        j = i
        i = tmp
     
    lst = lst[0:i]+[lst[j]]+lst[i+1:j]+[lst[i]]+lst[j+1:N]
    return lst
    
    
    
    
#################################################
def open_image(file, flip=False):
   
   try:
      img = Image.open(file)
   except:
      img =  Image.open('logo/noImage.jpeg')
      flip = True
   
   #rsize = img.resize((img.size[0],img.size[1])) # Use PIL to resize 
   rsize = img.resize((400,400)) # Use PIL to resize 
   image = np.asarray(rsize)
   if flip:
      image = np.flipud(image)   # flips an array
   #gri_x_max, gri_y_max, dimension = gri_image.shape
   
   try:
     image = image[:,:,0:3]
   except:
     image = image
   
   return image
############################################
def initialFile_aux(im_folder, pgc, filter):
   
   if filter=='gri':
      name = 'pgc'+str(pgc)+'_d25x2_rot_gri.jpg'
   else:
      name = 'pgc'+str(pgc)+'_d25x2_rot_'+filter+'.png'
   
   fname = im_folder+name
   if not os.path.isfile(fname): return 'None'
   
   return name

######

def initialFile(im_folder, pgc, filter):
    
    filt = ['r','g','i','gri']
    name = initialFile_aux(im_folder, pgc, filter)
    if name == 'None':
        for filter in filt:
            name = initialFile_aux(im_folder, pgc, filter)
            if  name != 'None':
                return name, filter
    return name, filter


#################################################
def insert_image(im_folder, im_names, im_buffer, pgc, filter):
   
   
   if filter=='gri':
      name = 'pgc'+str(pgc)+'_d25x2_rot_gri.jpg'
   else:
      name = 'pgc'+str(pgc)+'_d25x2_rot_'+filter+'.png'
   
   fname = im_folder+name
   if not os.path.isfile(fname):
       return None, im_buffer, im_names, True#=notFound


   for i in range(len(im_names)):
       if name==im_names[i]:
         return im_buffer[i], im_buffer, im_names, False#=Found-already buffered
   
   imfile = open_image(im_folder+name)
   im_buffer.append(imfile)
   im_names.append(name)
   
   return imfile, im_buffer, im_names, False#=Found
############################################



images = []
images_pgc = []
images_ind = []
swap = -1
images_buffer = []
images_folders = []
images_names = []
filter_lst = []
garbage_lst = []

images_ = []
images_pgc_ = []
images_ind_ = []
filter_lst_ = []
garbage_lst_ = []

axes_lst = []
my_axes = []
   
nextButton_on = False
flagAll = False
status = 1
invert_original = False
info_txt = None
next_button = None
reset_button = None
skip_button = None
redo_button = None
exit_button = None
radio = None
fig = None

g_button = None
r_button = None
i_button = None
gri_button = None
invert_button = None
garbage_button = None

garbage1_icon = None
garbage2_icon = None

rotCWW_button = None
rotCW_button = None
rotCCWW_button = None
rotCCW_button = None

PA=[0,0,0,0,0]
############################################
def any_garbage(garbage_lst):
    
    for i in range(len(garbage_lst)):
        if garbage_lst[i]:
            return True
    
    return False

############################################

def make_window():
    
    
   global swap, images, images_pgc, images_ind, images_buffer, images_folders, images_folders_, images_names, filter_lst, images_, images_pgc_, images_ind_, filter_lst_, garbage_lst, garbage_lst_
   global nextButton_on, axes_lst, my_axes
   global next_button, info_txt, reset_button, radio, fig
   global g_button, r_button, i_button, gri_button, invert_button, garbage_button, skip_button, redo_button, exit_button, rotCWW_button, rotCW_button, rotCCWW_button, rotCCW_button
   global garbage1_icon, garbage2_icon, next_on, next_off,  flags, flags_, incs, incs_, PA
   
   mpl.rcParams['toolbar'] = 'None'
   
   images = []
   images_pgc = []
   images_ind = []
   swap = -1
   images_buffer = []
   images_folders = []
   images_names = []
   filter_lst = []
   garbage_lst = []
   flags = []
   incs = []

   images_ = []
   images_pgc_ = []
   images_ind_ = []
   filter_lst_ = []
   garbage_lst_ = [] 
   images_folders_ = []
   flags_ = []
   incs_ = []
   
   axes_lst = []
   my_axes = []
   nextButton_on = False
   flagAll = False
   status = 1

   fig = plt.figure(figsize=(15, 9), dpi=100)
   
   fig.patch.set_facecolor('black')
   
   ax00 = fig.add_axes([0.15,0.740,0.70,0.015])
   ax00.tick_params('off')
   ax00.set_xticklabels([])
   ax00.set_yticklabels([])
   ax00.set_xticks([])
   ax00.set_yticks([])
   ax00.add_patch(patches.Rectangle((0, 0),1,1,fill=True, color='maroon') )     # remove background
   
   # top row
   gri100 = open_image('logo/1_400.png', flip=True)
   gri200 = open_image('logo/2_400.png', flip=True)
   gri300 = open_image('logo/3_400.png', flip=True)
   gri400 = open_image('logo/4_400.png', flip=True)
   gri500 = open_image('logo/5_400.png', flip=True)
   my_ax100 = My_ax(fig, [0.18, 0.75, 0.12, 0.20], gri100)
   my_ax200 = My_ax(fig, [0.31, 0.75, 0.12,  0.20], gri200)
   my_ax300 = My_ax(fig, [0.44, 0.75, 0.12,  0.20], gri300)
   my_ax400 = My_ax(fig, [0.57, 0.75, 0.12,  0.20], gri400)
   my_ax500 = My_ax(fig, [0.70, 0.75, 0.12,  0.20], gri500)  
   
   blank = gri100*0
   
   # buttom row
   my_ax1 = My_ax(fig, [0.03, 0.1, 0.18, 0.3], blank)
   my_ax2 = My_ax(fig, [0.22, 0.1, 0.18,  0.3], blank)
   my_ax3 = My_ax(fig, [0.41, 0.1, 0.18,  0.3], blank)
   my_ax4 = My_ax(fig, [0.60, 0.1, 0.18,  0.3], blank)
   my_ax5 = My_ax(fig, [0.79, 0.1, 0.18,  0.3], blank)
   
   # Middle row
   my_ax10 = My_ax(fig, [0.1425, 0.45, 0.135, 0.225], blank, angle=PA[0])
   my_ax20 = My_ax(fig, [0.2875, 0.45, 0.135,  0.225], blank, angle=PA[1])
   my_ax30 = My_ax(fig, [0.4325, 0.45, 0.135,  0.225], blank, angle=PA[2])
   my_ax40 = My_ax(fig, [0.5775, 0.45, 0.135,  0.225], blank, angle=PA[3])
   my_ax50 = My_ax(fig, [0.7225, 0.45, 0.135,  0.225], blank, angle=PA[4])   
   
   

   
   
   my_axes = [my_ax10, my_ax20, my_ax30, my_ax40, my_ax50, my_ax1, my_ax2, my_ax3, my_ax4, my_ax5]
   for my_ax in my_axes: axes_lst.append(my_ax.ax)   
      
      
         
   rax = axes([0.002, 0.75, 0.15, 0.15], facecolor='dimgray', aspect='equal')
   radio = RadioButtons(rax, ('g', 'r', 'i', 'gri', 'invert'), active=3, activecolor='maroon')
   for circle in radio.circles: # adjust radius here. The default is 0.05
    circle.set_radius(0.05)
   

   tmp = Image.open('logo/next_on.png')
   tmp_rsize = tmp.resize((tmp.size[0],tmp.size[1]))
   next_on = np.asarray(tmp_rsize)
   
   tmp = Image.open('logo/next_off.png')
   tmp_rsize = tmp.resize((tmp.size[0],tmp.size[1]))
   next_off = np.asarray(tmp_rsize)
   
   resetax = axes([0.9, 0.015, 0.07, 0.07])
   next_button = Button(resetax, '', color='black', hovercolor='black', image=next_off)
   
   
   resetax = axes([0.66, 0.015, 0.07, 0.07])
   exit_button = Button(resetax, 'Exit', color='maroon', hovercolor='Orange')   
   exit_button.label.set_fontsize(14)
   
   resetax = axes([0.74, 0.015, 0.07, 0.07])
   skip_button = Button(resetax, 'Skip', color='brown', hovercolor='Orange')
   skip_button.label.set_fontsize(14)
   
   resetax = axes([0.82, 0.015, 0.07, 0.07])
   redo_button = Button(resetax, 'Redo', color='Green', hovercolor='Orange')
   redo_button.label.set_fontsize(14)
   
   info_txt = annotate("", (0.7,0.04), xycoords='figure fraction', size=14, color='red')
   
   resetax = axes([0.04, 0.91, 0.07, 0.05])
   reset_button = Button(resetax, 'RESET', color='maroon', hovercolor='orange')
   
   
   tmp = Image.open('logo/garb1.png')
   tmp_rsize = tmp.resize((tmp.size[0],tmp.size[1]))
   garbage1_icon = np.asarray(tmp_rsize)  
   #garbage1_icon = np.flipud(garbage1_icon)
   resetax = axes([0.03, 0.42, 0.07, 0.07])
   garbage_button = Button(resetax, '', color='black', image=garbage1_icon, hovercolor='black')
   
   tmp = Image.open('logo/garb2.png')
   tmp_rsize = tmp.resize((tmp.size[0],tmp.size[1]))
   garbage2_icon = np.asarray(tmp_rsize)  
   #garbage2_icon = np.flipud(garbage2_icon)   
   
   

   resetax = axes([0.03, 0.65, 0.03, 0.05])
   g_button = Button(resetax, 'g', color='green', hovercolor='green')   

   resetax = axes([0.07, 0.65, 0.03, 0.05])
   r_button = Button(resetax, 'r', color='red', hovercolor='red')  
   
   resetax = axes([0.03, 0.58, 0.03, 0.05])
   i_button = Button(resetax, 'i', color='orange', hovercolor='orange')   
   
   resetax = axes([0.07, 0.58, 0.03, 0.05])
   gri_button = Button(resetax, 'gri', color='brown', hovercolor='brown')      
   
   resetax = axes([0.03, 0.51, 0.07, 0.05])
   invert_button = Button(resetax, 'invert', color='darkgrey', hovercolor='darkgrey')     
   
    
   resetax = axes([0.55, 0.41, 0.03, 0.03])
   rotCWW_button = Button(resetax, '>>', color='blue', hovercolor='blue')
   
   resetax = axes([0.515, 0.41, 0.03, 0.03])
   rotCW_button = Button(resetax, '>', color='blue', hovercolor='blue')

   resetax = axes([0.42, 0.41, 0.03, 0.03])
   rotCCWW_button = Button(resetax, '<<', color='blue', hovercolor='blue')
   
   resetax = axes([0.455, 0.41, 0.03, 0.03])
   rotCCW_button = Button(resetax, '<', color='blue', hovercolor='blue')
   
############################################

def load_images(pgc_lst, Flags=None, INCS=None, filter='g', std_folder='standards/', gal_folder='galaxies/', invert=False):
   
   global images, images_pgc, images_ind, images_buffer, images_folders, images_folders_, images_names, filter_lst, images_, images_pgc_, images_ind_, filter_lst_, garbage_lst, garbage_lst_, my_axes, flags, flags_, incs, incs_
   global garbage1_icon, garbage2_icon
  
      
   ind_lst = [0,1,2,3,4]
   
   images_folders = []
   if Flags != None:
       for i in ind_lst:
           if Flags[i]!=-1: images_folders.append(gal_folder)
           else: images_folders.append(std_folder)
   else:
       for i in ind_lst: images_folders.append(gal_folder)
           
   for i in ind_lst: images_folders.append('')
   
   images_names   = []
   filter_lst = []
   for i in ind_lst:
       name, f = initialFile(images_folders[i], pgc_lst[i], filter)
       images_names.append(name)
       filter_lst.append(f)

   images_buffer = []
   for i in ind_lst:
       im = open_image(images_folders[i]+images_names[i])
       if invert: 
           my_axes[i].invert = True
       images_buffer.append(im)

   
   blank = im*0
   
   images = images_buffer + [blank, blank, blank, blank, blank]
   images_pgc = pgc_lst+[0,0,0,0,0]
   images_ind = ind_lst+[-2,-2,-2,-2,-2]
   filter_lst += ['','','','','']
   garbage_lst = [False,False,False,False,False,False,False,False,False,False]
   
   flags = []
   for i in range(5):
       flags.append(Flags[i])
       if Flags[i]>0:
           garbage_lst[i]=True
   for i in range(5):
       flags.append(-100)   
       
   incs = []
   for i in range(5):
       incs.append(INCS[i])
   for i in range(5):
       incs.append(-100)         
           
   
   images_         = list(images)
   images_pgc_     = list(images_pgc)
   images_ind_     = list(images_ind)
   filter_lst_     = list(filter_lst)
   garbage_lst_    = list(garbage_lst)
   images_folders_ = list(images_folders)
   flags_          = list(flags)
   incs_           = list(incs)
   
   
   
   for i in range(len(my_axes)): 
     my_axes[i].set_image(images[i], filter= filter_lst[i], pgc=images_pgc[i], index=images_ind[i], garbage=garbage_lst[i], im_folder=images_folders[i], flag=flags[i], inc=incs[i])   

   if any_garbage(garbage_lst):
       garbage_button.ax.imshow(garbage2_icon)
   else:
       garbage_button.ax.imshow(garbage1_icon)
###########################################
def on_click(event): 
       
       global swap, images, images_pgc, images_ind, filter_lst, garbage_lst, my_axes, images_folders
       global nextButton_on, garbage1_icon, garbage2_icon, next_on, next_off,  garbage_button, flags, incs, flagAll
       
       
       if not event.dblclick and event.button == 3 and not event.key=='control' and not event.key=='ctrl+alt' and not event.key=='alt+control':
           
           #print 'dbl click'
           for i in range(len(my_axes)):
               if event.inaxes == my_axes[i].ax and my_axes[i].index>-1:
                   my_axes[i].invert = not my_axes[i].invert
                   my_axes[i].set_image(images[i], filter=my_axes[i].filter, only_image=True)
           
       
       # Ctrl + Left click (rotate)
       elif not event.dblclick and event.button == 1 and event.key=='control' :
           for i in range(len(my_axes)):
               if event.inaxes == my_axes[i].ax:
                   
                   my_axes[i].angle-=5
                   print '(pgc'+str(my_axes[i].pgc)+')', "PA-5: ", my_axes[i].angle
                   my_axes[i].set_image(images[i], filter=my_axes[i].filter, only_image=True)                   

                   
       elif not event.dblclick and event.button == 3 and event.key=='control' :
           for i in range(len(my_axes)):
               if event.inaxes == my_axes[i].ax:

                   my_axes[i].angle+=5
                   print '(pgc'+str(my_axes[i].pgc)+')', "PA+5: ", my_axes[i].angle
                   my_axes[i].set_image(images[i], filter=my_axes[i].filter, only_image=True)
                   
                   
       # Ctrl + Left click (rotate)
       elif not event.dblclick and event.button == 1 and (event.key=='ctrl+alt' or event.key=='alt+control'):
           for i in range(len(my_axes)):
               if event.inaxes == my_axes[i].ax:
                   
                   my_axes[i].angle-=1
                   print '(pgc'+str(my_axes[i].pgc)+')', "PA-1: ", my_axes[i].angle
                   my_axes[i].set_image(images[i], filter=my_axes[i].filter, only_image=True)                   

                   
       elif not event.dblclick and event.button == 3 and (event.key=='ctrl+alt' or event.key=='alt+control'):
           for i in range(len(my_axes)):
               if event.inaxes == my_axes[i].ax:

                   my_axes[i].angle+=1
                   print '(pgc'+str(my_axes[i].pgc)+')', "PA+1: ", my_axes[i].angle
                   my_axes[i].set_image(images[i], filter=my_axes[i].filter, only_image=True)       
       
       # Middle click    
       elif not event.dblclick and event.button == 2:
           for i in range(len(my_axes)):
               if event.inaxes == my_axes[i].ax:

                   if (flagAll and my_axes[i].flag>=0) or (not flagAll and images_ind[i]==4):  # do not flag standards, or blanks or  # just flag the 4th panel
                       garbage_lst[i] = my_axes[i].flip_garbage()
                   
                       if any_garbage(garbage_lst):
                         garbage_button.ax.imshow(garbage2_icon)
                       else:
                         garbage_button.ax.imshow(garbage1_icon)
                   
         
       elif not event.dblclick and event.button == 1:
           
           for i in range(len(my_axes)):
               if event.inaxes == my_axes[i].ax:
                  if not my_axes[i].selected:
                     if swap>=0:
                        #print 'SWAP'
                        j = swap
                        images = swap_lst(images, i, j)
                        images_pgc = swap_lst(images_pgc, i, j)
                        images_ind = swap_lst(images_ind, i, j)
                        filter_lst = swap_lst(filter_lst, i, j)
                        garbage_lst = swap_lst(garbage_lst, i, j)
                        images_folders = swap_lst(images_folders, i, j)
                        flags = swap_lst(flags, i, j)
                        incs = swap_lst(incs, i, j)
                        swap_zoom_prop(my_axes[i], my_axes[j])   # goes before set_image commands
                        my_axes[i].set_image(images[i], filter= filter_lst[i], pgc=images_pgc[i], index=images_ind[i], garbage=garbage_lst[i], im_folder=images_folders[i], flag=flags[i], inc=incs[i])
                        my_axes[j].set_image(images[j], filter= filter_lst[j], pgc=images_pgc[j], index=images_ind[j], garbage=garbage_lst[j], im_folder=images_folders[j], flag=flags[j], inc=incs[j])
                        
                        
                        info_txt.set_text('')
                        
                        if sum(images_ind[5:])==10:
                            
                            activateNext = True
                            inc_p = -1
                            for i in [5,6,7,8,9]:
                                if flags[i]==-1 and incs[i]<inc_p:
                                    activateNext = False
                                if flags[i]==-1:
                                    inc_p = incs[i]
                            if activateNext:
                                nextButton_on=True
                                next_button.ax.imshow(next_on)
                                next_button.color='black'
                                next_button.hovercolor='orangered'
                            else:
                                print "Warning: Please make sure that the standard galaxies are sorted !? x"
                                nextButton_on=False
                                next_button.color='black'
                                next_button.hovercolor='black'
                                next_button.ax.imshow(next_off)
                        else:
                            nextButton_on=False
                            next_button.color='black'
                            next_button.hovercolor='black' 
                            next_button.ax.imshow(next_off)      
                        swap = -1
                     else: 
                        if my_axes[i].index>-1:
                          my_axes[i].select(True)
                          swap = i
                          
                  else: 
                      my_axes[i].select(False)
                      swap = -1
               elif event.inaxes in axes_lst:
                  my_axes[i].select(False)


       draw() 


############################################

def g_func(event):
    
      global swap, images, images_pgc, images_ind, images_buffer, images_folders, images_folders_, images_names, filter_lst, my_axes
      
      label = 'g'
      if swap>=0:
          j = swap
          pgc = my_axes[j].pgc
          filter = label
          if not filter==my_axes[j].filter:
              im_folder = my_axes[j].im_folder
              new_image, images_buffer, images_names, notFound = insert_image(im_folder, images_names, images_buffer, pgc, filter)
              
              if notFound: 
                  print "Not found: pgc"+str(pgc)+" "+filter+"-band"
                  return 
              
              my_axes[j].set_image(new_image, filter=filter, only_image=True)
              images[j] = new_image
              filter_lst[j] = filter
              my_axes[j].select(False)
              swap = -1          
       
          draw()
############################################
def r_func(event):
    
      global swap, images, images_pgc, images_ind, images_buffer, images_folders, images_folders_, images_names, filter_lst, my_axes
      
      label = 'r'
      if swap>=0:
          j = swap
          pgc = my_axes[j].pgc
          filter = label
          if not filter==my_axes[j].filter:
              im_folder = my_axes[j].im_folder
              new_image, images_buffer, images_names, notFound = insert_image(im_folder, images_names, images_buffer, pgc, filter)
              
              if notFound: 
                  print "Not found: pgc"+str(pgc)+" "+filter+"-band"
                  return

              my_axes[j].set_image(new_image, filter=filter, only_image=True)
              images[j] = new_image
              filter_lst[j] = filter
              my_axes[j].select(False)
              swap = -1          
       
          draw()
############################################
def i_func(event):
    
      global swap, images, images_pgc, images_ind, images_buffer, images_folders, images_folders_, images_names, filter_lst, my_axes
      
      label = 'i'
      if swap>=0:
          j = swap
          pgc = my_axes[j].pgc
          filter = label
          if not filter==my_axes[j].filter:
              im_folder = my_axes[j].im_folder
              new_image, images_buffer, images_names, notFound = insert_image(im_folder, images_names, images_buffer, pgc, filter)
              
              if notFound: 
                  print "Not found: pgc"+str(pgc)+" "+filter+"-band"
                  return
              
              my_axes[j].set_image(new_image, filter=filter, only_image=True)
              images[j] = new_image
              filter_lst[j] = filter
              my_axes[j].select(False)
              swap = -1          
       
          draw()    
############################################
          
def gri_func(event):
    
      global swap, images, images_pgc, images_ind, images_buffer, images_folders, images_folders_, images_names, filter_lst, my_axes
      
      label = 'gri'
      if swap>=0:
          j = swap
          pgc = my_axes[j].pgc
          filter = label
          if not filter==my_axes[j].filter:
              im_folder = my_axes[j].im_folder
              new_image, images_buffer, images_names, notFound = insert_image(im_folder, images_names, images_buffer, pgc, filter)
              
              if notFound: 
                  print "Not found: pgc"+str(pgc)+" "+filter+"-band"
                  return
     
              my_axes[j].set_image(new_image, filter=filter, only_image=True)
              images[j] = new_image
              filter_lst[j] = filter
              my_axes[j].select(False)
              swap = -1          
       
          draw()  
          
############################################
def press_key(event):
    
    global swap, images, images_pgc, images_ind, images_buffer, images_folders, images_folders_, images_names, filter_lst, my_axes
        
    if swap>=0:
        j = swap
        if event.key in ['up', 'down']:
            im = np.flipud(my_axes[j].image)
            my_axes[j].image = im
            my_axes[j].ax.imshow(im)
            my_axes[j].select(False)
            swap = -1
        if event.key in ['left', 'right']:
            im = np.fliplr(my_axes[j].image)
            my_axes[j].image = im
            my_axes[j].ax.imshow(im)  
            my_axes[j].select(False)
            swap = -1
        draw()
############################################    
def invert_func(event):
    
      global swap, images, images_pgc, images_ind, images_buffer, images_folders, images_folders_, images_names, filter_lst, my_axes
      
      label = 'invert'
      if swap>=0:
          i = swap
          if my_axes[i].index>-1:
               my_axes[i].invert = not my_axes[i].invert
               my_axes[i].set_image(images[i], filter=my_axes[i].filter, only_image=True)
               my_axes[i].select(False)
               swap = -1         
       
          draw()  
          
############################################
def rotCCWW_func(event):
      global swap, images, images_pgc, images_ind, images_buffer, images_folders, images_folders_, images_names, filter_lst, my_axes
      
      if swap>=0:
        
        i = swap
        if my_axes[i].index>-1:
           my_axes[i].angle-=5
           print '(pgc'+str(my_axes[i].pgc)+')', "PA-5: ", my_axes[i].angle
           my_axes[i].set_image(images[i], filter=my_axes[i].filter, only_image=True)                   
      
      draw()   
############################################

def rotCCW_func(event):
      global swap, images, images_pgc, images_ind, images_buffer, images_folders, images_folders_, images_names, filter_lst, my_axes
      
      if swap>=0:
        
        i = swap
        if my_axes[i].index>-1:
           my_axes[i].angle-=1
           print '(pgc'+str(my_axes[i].pgc)+')', "PA-1: ", my_axes[i].angle
           my_axes[i].set_image(images[i], filter=my_axes[i].filter, only_image=True)                   
      
      draw()   
############################################
def rotCWW_func(event):
      global swap, images, images_pgc, images_ind, images_buffer, images_folders, images_folders_, images_names, filter_lst, my_axes
      
      if swap>=0:
        
        i = swap
        if my_axes[i].index>-1:
           my_axes[i].angle+=5
           print '(pgc'+str(my_axes[i].pgc)+')', "PA+5: ", my_axes[i].angle
           my_axes[i].set_image(images[i], filter=my_axes[i].filter, only_image=True)                   
      
      draw()   
############################################
def rotCW_func(event):
      global swap, images, images_pgc, images_ind, images_buffer, images_folders, images_folders_, images_names, filter_lst, my_axes
      
      if swap>=0:
        
        i = swap
        if my_axes[i].index>-1:
           my_axes[i].angle+=1
           print '(pgc'+str(my_axes[i].pgc)+')', "PA+1: ", my_axes[i].angle
           my_axes[i].set_image(images[i], filter=my_axes[i].filter, only_image=True)                   
      
      draw()         
############################################
def garbage_func(event):
    
      global swap, images, images_pgc, images_ind, images_buffer, images_folders, images_folders_, images_names, filter_lst, my_axes, garbage1_icon, garbage2_icon, next_on, next_off,  garbage_button
      
      label = 'garbage'
      if swap>=0:
          i = swap
          if my_axes[i].index>-1:
             if my_axes[i].flag>=0:  # do not flag standards, or blanks
                garbage_lst[i] = my_axes[i].flip_garbage()
                my_axes[i].select(False)
                swap = -1 
               
                if any_garbage(garbage_lst):
                   garbage_button.ax.imshow(garbage2_icon)
                else:
                   garbage_button.ax.imshow(garbage1_icon)
             else: return 
       
          draw()           
                                       
############################################
def scroll_event(event):
       
      global swap, images, images_pgc, images_ind, images_buffer, images_folders, images_folders_, images_names, filter_lst, my_axes
      
      for i in range(len(my_axes)):
      
         if event.inaxes == my_axes[i].ax: 
            if event.key is None and event.button == 'up':

                i1, i2, j1, j2 = my_axes[i].disp.zoom_OUT()
                my_axes[i].ax.set_xlim(i1,i2)
                my_axes[i].ax.set_ylim(j1,j2)
                draw()
            elif event.key is None and event.button == 'down':

                i1, i2, j1, j2 = my_axes[i].disp.zoom_IN()
                my_axes[i].ax.set_xlim(i1,i2)
                my_axes[i].ax.set_ylim(j1,j2)
                draw()
         

############################################
def filt_func(label):
       
      global swap, images, images_pgc, images_ind, images_buffer, images_folders, images_folders_, images_names, filter_lst, my_axes

      if label!='invert':
         for j in range(len(my_axes)):
            if my_axes[j].index>-1:
              pgc = my_axes[j].pgc
              filter = label
              if not filter==my_axes[j].filter:
                  im_folder = my_axes[j].im_folder
                  new_image, images_buffer, images_names, notFound = insert_image(im_folder, images_names, images_buffer, pgc, filter)
                  
                  if notFound: 
                      print "Not found: pgc"+str(pgc)+" "+filter+"-band"
                      return 
                  
                  my_axes[j].set_image(new_image, filter=filter, only_image=True)
                  images[j] = new_image
                  filter_lst[j] = filter
                  my_axes[j].select(False)
                  swap = -1 
      
      else: 
         for i in range(len(my_axes)):          
            if my_axes[i].index>-1:
              my_axes[i].invert = not my_axes[i].invert
              my_axes[i].set_image(images[i], filter=my_axes[i].filter, only_image=True)
              my_axes[i].select(False)
              swap = -1 


      draw()
############################################
def next_func(event):
       global nextButton_on, status 
       
       if nextButton_on:
          
          status = 0
          info_txt.set_text('Bingo ...') 
          plt.close('all')
############################################
def skip_func(event):
       global status

       status = 1
       plt.close('all')
############################################
def redo_func(event):
       global status

       status = 2
       plt.close('all')
############################################
def exit_func(event):
       global status

       status = 3
       plt.close('all')

############################################
def reset_func(event):
       global images, images_pgc, images_ind, filter_lst, images_folders
       global images_, images_pgc_, images_ind_, filter_lst_, garbage_lst, garbage_lst_, images_folders_, my_axes
       global swap, nextButton_on, flags, flags_, incs, incs_, invert_original
       
       swap = -1
       nextButton_on = False
       next_button.color='dimgrey'
       next_button.hovercolor='dimgrey' 
       images = list(images_)
       images_pgc = list(images_pgc_)
       images_ind = list(images_ind_)
       filter_lst = list(filter_lst_)
       garbage_lst = list(garbage_lst_)
       images_folders = list(images_folders_)
       flags = list(flags_)
       incs = list(incs_)
       
       
       for i in range(len(my_axes)):
          
          if i<5:
              my_axes[i].invert=invert_original
              my_axes[i].angle = PA[i] 
          else:
              my_axes[i].invert=False
          
          my_axes[i].set_image(images[i], filter= filter_lst[i], pgc=images_pgc[i], index=images_ind[i], garbage=False, im_folder=images_folders[i], flag=flags[i], inc=incs[i])
          my_axes[i].select(False)
############################################


############################################

def main(pgc_lst, Flags=None, INCS=None, filter='g', std_folder='standards/', gal_folder='galaxies/', invert=False):
   
   global swap, images, images_pgc, images_ind, images_buffer, images_folders, images_folders_, images_names, filter_lst, images_, images_pgc_, images_ind_, filter_lst_, garbage_lst, garbage_lst_
   global nextButton_on, axes_lst, my_axes, status
   global next_button, info_txt, reset_button, radio, fig
   global g_button, r_button, i_button, gri_button, invert_button, garbage_button, skip_button, redo_button, exit_button, rotCWW_button, rotCW_button, rotCCWW_button, rotCCW_button

   
   #pgc_lst = [55981, 91643, 12041, 37617, 50942]
   
   load_images(pgc_lst, Flags=Flags, INCS=INCS, filter=filter, std_folder=std_folder, gal_folder=gal_folder, invert=invert)
 
   radio.on_clicked(filt_func)   
   

   next_button.on_clicked(next_func)
   skip_button.on_clicked(skip_func)
   redo_button.on_clicked(redo_func)
   exit_button.on_clicked(exit_func)
   reset_button.on_clicked(reset_func)
   
   g_button.on_clicked(g_func)
   r_button.on_clicked(r_func)
   i_button.on_clicked(i_func)
   gri_button.on_clicked(gri_func)
   invert_button.on_clicked(invert_func)
   garbage_button.on_clicked(garbage_func)
   
   rotCWW_button.on_clicked(rotCWW_func)
   rotCW_button.on_clicked(rotCW_func)
   rotCCWW_button.on_clicked(rotCCWW_func)
   rotCCW_button.on_clicked(rotCCW_func)
   
   
   fig.canvas.mpl_connect('button_press_event', on_click)
   fig.canvas.mpl_connect('scroll_event', scroll_event)
   fig.canvas.mpl_connect('key_press_event', press_key)
    
   plt.show()  
   
   return status


################################################################

    
def display(pgc_lst, Flags=None, INCS=None, filter='g', std_folder='standards/', gal_folder='galaxies/', invert=False, flag_all=False, dPA=[0,0,0,0,0]):
   
   global status, images_ind, garbage_lst, flagAll, invert_original, PA, my_axes
   
   
   flagAll = flag_all
   PA  = dPA
   
   make_window()    # this also sets PAs (using PA)
   
   invert_original = invert
   main(pgc_lst, Flags=Flags, INCS=INCS, filter=filter, std_folder=std_folder, gal_folder=gal_folder, invert=invert)
   
   # Here is where I control how to exit the GUI
   if sum(images_ind[5:])==10:
       PA = [my_axes[5].angle,my_axes[6].angle,my_axes[7].angle,my_axes[8].angle,my_axes[9].angle]
       return images_ind[5:], garbage_lst[5:], status, PA
   
   
   
   return None, None, status, PA

#################################################################

#if __name__ == '__main__':
  
   
   
   #mytable = np.genfromtxt('pgc.100.lst' , delimiter=',', filling_values=None, names=True, dtype=None )
   #PGC = mytable['pgc']
   #N = len(PGC)
   

   #for iter in range(10):
       #galaxies = []
       #while len(galaxies) < 5:
         #i = np.random.random_integers(0,N)
         #if not PGC[i] in galaxies: 
             #galaxies.append(PGC[i])
             
       #display(galaxies)
  
  
  
  
  
  
  
  
