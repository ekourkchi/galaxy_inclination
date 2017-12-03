# Galaxy Inclination
A set of tools (+GUI) to determine the inclination of the Spiral Galaxies

 ![GUI demo](https://user-images.githubusercontent.com/13570487/33522035-a237c686-d786-11e7-9efc-df7e53b24940.png "GUI demo")

 
  * How it works:
      The goal is to find the best position for the galaxy on the rightmost panel (the panel with '?' mark). Normally it takes ~4 times (sorts) to introduce a new galaxy. Looking at other galaxies with known inclinations, user is able to visually find the best position for the galaxy.
      
      Standard galaxies are those with already known inclinations. These galaxies are denoted by asterisks. The goal is to find the position of the unknown galaxy in between the other galaxies. The user cannot swap the standards and sort them out of order. If standard galaxies are out of order or all galaxies are not in the bottom row, the "Next" button is inativated and does not let the user to move on. Also, the user can update the position of all other non-standard galaxies at any time. 



 1) The GUI actions
 
   - Inclination standard galaxies are denoted by asterisks next to their panel number
   - To select/unselect a galaxy clicking on it (left click)
   - If a galaxy is selected, you can swap it with other galaxies just by clicking on their panel or on a blank panel
   - In order to activate the 'Next' button, you need to move all galaxies from the middle row to the bottom row
   - To change the wave-band of all images, use the radio buttons
   - To change the wave-band of an individual image, use a colored button (from the left toolbar) once a panel is selected
   - You can also use your "right mouse button" to invert an image (once your mouse pointer is on a panel)

   - You can flag out a galaxy (put a galaxy in the trash bin), by selecting a panel and then click on the recycling bin icon. If you repeat the action, you can unflag a panel. Once a galaxy is chosen to be flagged, all the label colors turn into red.
   - You can also press the middle mouse button to flag/unflag a panel
   - Once your mouse pointer is on a panel, scrolling up/down using the middle mouse key, you can zoom in/out.



 2) What you see on each panel
 
 ![Panel Labels](https://user-images.githubusercontent.com/13570487/33522617-f9e62040-d794-11e7-82a8-f9a294169844.png "Panel Labels")
 ![Panel Labels](https://user-images.githubusercontent.com/13570487/33522626-21c0b544-d795-11e7-88b8-e74e599a054b.png "Panel Labels")
 
  1 and 2) Panel index. The target galaxy is denoted by "??" sign. 
        3) Filter badn
        4) Panel index. In the case of standard galaxies, "***" is on the right side the index number
        5) PGC id 
  6 and 7) Inclination in degree. The number is in parentheses in the case of non-standard galaxies. User can change the inclination value of non-standard galaxies at any time by moving these galaxies around (based on their inclinations).
        8) A target galaxy that is going to be flagged.
        9) All the label fonts are in red when a galaxy is about to be flagged.
        
  3) FAQ
   - What Happens when you flag a galaxy? That galaxy would be removed from the list for further inspections. User is asked to answer a simple questions why the galaxy is falgged. 
   
       !!! !!! !!! !!! !!! !!! !!! !!! !!! !!! !!! !!! !!! !!! !!!
       Are you sure you want to flag pgc52412? [y/N] y

       What is the reason for flagging this object (choose one)?
       1 - Wrong Position Angle
       2 - Too faint image
       3 - Ambiguous, bad HI profile, not a good TF galaxy
       4 - Cancel


    
    
    
    
    
- - - -
 * Copyright 2017

 * Author: Ehsan Kourkchi <ekourkchi@gmail.com>
