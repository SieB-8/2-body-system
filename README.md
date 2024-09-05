# 2 body system
This is a visual 2D python simulation of a two body system.
At the moment, there is no user interface.

At lines 59 and 60, you can adjust the variables of the two bodies.
The structure is as follows:

Object(x-coordinate, y-coordinate, mass, radius, color, starting_velocity*)  *must be a vector element, which can be defined using "vector(x,y)"

At lines 17, 18 and 19, you can change the gravitational constant (which defines the strength of gravity), the speed of the simulation, and whether or not the trajectory of the bodies should be drawn.

Pressing [ESC] will toggle fullscreen mode.

Pressing [SPACE] will add the time and parameters of both objects to a csv-file.

When the two bodies collide, they will stop updating, but the program will keep running until you close it manually. This way, you can still observe the trajectories.
