# Galaxy Inclination

A set of tools (+GUI) to determine the inclination of Spiral Galaxies. To see some notes on how the algorithm works, [Click Here](https://github.com/ekourkchi/galaxy_inclination/files/1524526/galaxy_sorting.pdf)

## DEMO
Please [Click here](https://github.com/ekourkchi/galaxy_inclination/tree/master/DEMO), and follow the instruction in the README file to run the DEMO version of this program. This DEMO may not have all features of the final product. 

## How it works:
    
The goal is to find the best position of the galaxy on the rightmost panel (the panel with '?' mark). Normally it takes ~4 rounds of sorting to introduce a new galaxy. Looking at other galaxies with known inclinations, user is able to visually find the best position of the galaxy.
      
Standard galaxies are those with already known inclinations. These galaxies are denoted by asterisks. The goal is to find the position of the unknown galaxy relative to other galaxies. User cannot swap standard galaxies and put them out of order. If standard galaxies are out of order or all galaxies are not in the bottom row, the "Next" button is inactivated and does not let the user move on. Also, user can update the position of all other non-standard galaxies at any time. 

 ![GUI demo](https://user-images.githubusercontent.com/13570487/34751095-a0cbb3b2-f54e-11e7-99bb-e82764160319.png "GUI demo")
 
## What you need in addition to above codes [to be completed]:
    
   - A folder containing images of standard galaxies
   - A folder containing images of all target galaxies
   - List of target galaxis. This list has only one column, i.e. PGC number of galaxies. For example, a text file like **pgc.100.lst**:
           
           pgc
           10002   
           100768
           10208
           10215
           10139
           10209

   - Outputs would be stored in <input-list>.output, e.g. **pgc.100.lst.output**
   
## How to run:

           $ python inclination_std.py -l [list_name] -g [galaxy_folder] -s [standard_folder] -f [filter] [-i]

   - To get help
   
           $ python inclination_std.py -h
   
   - Command line options:
           
           -h, --help            show this help message and exit
           -l LIST, --list=LIST  The input list
           -g GALAXIES, --galaxies=GALAXIES
                        The folder that contains galaxies images
           -s STANDARDS, --standards=STANDARDS
                        The folder that contains standards images
           -f FILTER, --filter=FILTER
                        initial filter
           -i                    initially invert images
           -a                    allow flagging multiple images (except standards)

   - Example(s):
       
           python inclination_std.py -l list.csv -g ./galaxies -s ./standards -f g -i
           

## What user sees on each panel
 
 ![Panel Labels](https://user-images.githubusercontent.com/13570487/33522617-f9e62040-d794-11e7-82a8-f9a294169844.png "Panel Labels")
 ![Panel Labels](https://user-images.githubusercontent.com/13570487/33522626-21c0b544-d795-11e7-88b8-e74e599a054b.png "Panel Labels")

* 1 and 2- Panel index. The target galaxy is denoted by "??" sign. 
* 3- Filter band
* 4- Panel index. In the case of standard galaxies, "***" is on the right side the index number
* 5- PGC id 
* 6 and 7- Inclination in degree. The number is in parentheses in the case of non-standard galaxies. User can change the inclination value of non-standard galaxies at any time by moving these galaxies around (based on their inclinations).
* 8- A target galaxy that is going to be flagged.
* 9- All the label fonts are in red when a galaxy is about to be flagged.
 
 ![GUI Buttons](https://user-images.githubusercontent.com/13570487/33522891-5660f80c-d79c-11e7-89c7-0539f4d3c975.png "GUI Buttons")
 
1. Exit: Quits the program
2. Skip: Skips the current galaxy (denoted by '??'). If the user agrees to continue, another galaxy would be chosen randomly.
3. Redo: Starts the entire process for the current galaxy. 
4. Next: If activated, closes the GUI and moves onto next set. If the position of target galaxy is completely clear, a new galaxy would be drawn randomly.


## The GUI actions
 
   - Inclination standard galaxies are denoted by asterisks next to their panel number.
   - To select/unselect a galaxy click on its panel (left click).
   - If a galaxy is selected, you can swap it with other galaxies just by clicking on their panel or on a blank panel.
   - In order to activate the 'Next' button, you need to move all galaxies from the middle row to the bottom row.
   - To change the wave-band of all images, use the radio buttons.
   - To change the wave-band of an individual image, once a panel is selected use a colored button (from the left toolbar) 
   - You can also use your "right mouse button" to invert the color map an image (once your mouse pointer is on a panel).

   - You can flag out a galaxy (put a galaxy in the trash bin), by choosing a panel and then clicking on the recycling bin icon. If you repeat the same action, you can unflag a panel. When a galaxy is chosen to be flagged, all of its label colors turn into red.
   - You can also easily press the middle mouse button to flag/unflag a panel.
   - Once your mouse pointer is on a panel, scrolling up/down using the middle mouse key you can zoom in/out. All modifications to the scale of images would be recorded in the output file and they become permanent. This means that once you resize an image, you will always see it in the same scale, unless you change the scale again.
   
   ### Extra GUI features
   
   ![GUI Rotation DEMO](https://user-images.githubusercontent.com/13570487/33802665-2568c232-dd20-11e7-927e-e39c28e4a2bc.png "GUI Rotation DEMO")
   
   - Hold the "Control" key on your keyboard, and click on a panel to rotate its image by (+/-)5 degrees. Use the right/left mouse buttons to control the rotation direction, i.e. clockwise or counter clockwise. *[not working on Mac systems]*
   - To fine-tune Position Angles (PAs), hold both "Control" and "Alt" keys together, and click on a panel to make a rotation by (+/-)1 degrees. *[not working on Mac systems]*
   - All modifications to the Position Angles would be recorded in the output file and they become permanent. This means that once you rotate a galaxy, you will always see it in its rotated state. 
   - To (right/left) up/down flipping, select an image by clicking on its panel and then use the (right/left) up/down arrow keys on your keyboard. These changes are temporary and would not be saved. *[not working on Mac systems]*
   
   ![Rotation Buttons](https://user-images.githubusercontent.com/13570487/34551536-0cdc9542-f0bf-11e7-8da9-7e225c09b778.png "GUI rotation buttons")
   
   - You can also use the rotation buttons, in order to rotate the selected image. To make 5 or 1 degree(s) counter clockwise rotations, use "<<" or "<", respectively. Use ">>" or ">" for clockwise rotations.
   
   ![flip up/lr buttons](https://user-images.githubusercontent.com/13570487/34751101-b70a12b8-f54e-11e7-8c9e-f75758fcf3f9.png "flip up/lr buttons")
   - You can also use the flip buttons (up/down and right/left), in order to accordingly flip the image of the selected panel.


## FAQ
   
   - What is the best strategy for introducing new galaxies? The best strategy is to first add those clean clear galaxies with spiral structures. If you are in doubt about the shape of a galaxy or it's faint or even if you don't like it (it's hard/challenging), it's better to skip. If you add those galaxies to your list, it makes it harder for you to use them as the reference to find the inclination of the others. Therefore, do the easiest one first.
   
   - What Happens when I flag a galaxy? That galaxy would be removed from the list for further inspections. User is then asked to answer a simple question why the galaxy is being flagged. 
   
           !!! !!! !!! !!! !!! !!! !!! !!! !!! !!! !!! !!! !!! !!! !!!
           Are you sure you want to flag pgc###? [y/N] y

           What is the reason for flagging this object (choose one)?
           1 - Not Sure, use b/a for inclination
           2 - Get a better image
           3 - Ambiguous, bad HI profile, not a good TF galaxy
           4 - Cancel


   - What to do if I feel lost and need to repeat the whole process for the target galaxy, i.e. the galaxy with '??' sign? Click on the "Redo" button and repeat the process from beginning.
   
   - What to do if I am not confident enough with the results I am getting for the current galaxy? Click on the "Skip" button. The program will choose another galaxy randomly.
   
   - What to do to completely quit the program? Click on the "Exit" button, and take a break. 

           No object added ....
           Number of remaining galaxies:  ###

             Thanks a lot. Bye :)

   - What happens if I accidentally close the GUI window? The program "Skips" the current galaxy and offers to work on another galaxy.
           
           No object added ....
           Number of remaining galaxies:  ###
           Do you want to continue? [Y/n] y


- - - -
 * Copyright 2018

 * Author: Ehsan Kourkchi <ehsan@ifa.hawaii.edu>
