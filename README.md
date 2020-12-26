# Machine Learning Race Game!

This project was something I started to get into simple ML in python, in it's current state it's just a very simple top-down view car game, but eventually I'll add a Neural Network to it!

# Keep in mind:

1. The collision detection is kinda weird with the cars, the collision math is designed for rect to line, so the hitbox gets bigger when the car gets an angle, and smaller when it's horizontally or vertically, it tries to make the rect as small as possible

# Key binds:

1. E to quit game 
2. Hold G to use map editor mode (Left click for adding lines(This will automatically have collision in it), it then converts the coordinates from a tuple into the map.json file, where it will later get added when you launch the game)
3. R to reset Map 
4. O to save current map 
5. P to create car instance 