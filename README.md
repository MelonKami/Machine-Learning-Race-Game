# Machine Learning Race Game!

This project was something I started, to get into simple ML in python, in it's current state it's just a very simple top-down view car game made in pygame, but eventually I'll add a Neural Network to it!

## Keep in mind:

* The collision detection is kinda weird with the cars, the collision math is designed for rect to line, so the hitbox gets bigger when the car gets an angle, and smaller when it's horizontally or vertically, it tries to make the rect as small as possible, which is why it shrinks when it can

* I am absolutely no professional and I am creating this to test out what I can create with ML and have fun xD

## Key binds: 

| Keybinds      | Description     |
| :------------- | :------------------------------ | 
| E | Quits game and exites window |
| G | Hold to use map editor mode (Left click for adding lines (This will automatically have collision in it), it then converts the coordinates from a tuple into the map.json file, where it will later get added when you launch the game) |
| H | Resets all the cars |
| R | Resets Map |
| O | Saves current map |
| P | Creates car instance |

<!-- * E - to quit game 

* G - hold to use map editor mode (Left click for adding lines (This will automatically have collision in it), it then converts the coordinates from a tuple into the map.json file, where it will later get added when you launch the game)

* H - Resets all the cars

* R - to reset Map 

* O - to save current map 

* P - to create car instance  -->