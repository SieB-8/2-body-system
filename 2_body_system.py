import math
import datetime
import pygame
pygame.init()
vector = pygame.math.Vector2
clock = pygame.time.Clock()

# display
WIDTH = 1280
HEIGHT = 720
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2 body system")

# variables
distance = 0
gravity = 0
G = 3   # gravity constant ≠ real gravity constant
TICK_SPEED = 60    # tickspeed
DRAW_PATH = True
dots = []
file = open("log.csv", "w")
running = True

# objects class
class Object():
    def __init__(self, x, y, mass, radius, color, starting_velocity, fixed=False):
        self.mass = mass      # solor masses
        self.radius = radius  # pixels
        self.color = color
        self.position = vector(x,y)
        self.velocity = starting_velocity   # vector element
        self.acceleration = vector(0,0)     # start without acceleration
        self.dots = [(x,y)]
        self.fixed = fixed

    def calculate_unit_vector(self, x2, y2, r):
        self.unit_vector = vector((x2 - self.position[0]), (y2 - self.position[1])) / r

    def draw(self):
        if DRAW_PATH and not self.fixed:
            self.dots.append( ( int(self.position[0]), int(self.position[1]) ) )
            pygame.draw.lines(DISPLAY, (255, 255, 255), False, self.dots)
        pygame.draw.circle(DISPLAY, self.color, self.position, self.radius)

    def update(self, gravity, x2, y2, r):
        self.calculate_unit_vector(x2, y2, r)

        # calculate acceleration in function of gravity
        self.acceleration = gravity/self.mass * self.unit_vector

        # calculate velocity and position
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration # kinematic equation for position

    def fix(self):
        central_vector = vector(WIDTH/2, HEIGHT/2)
        correction = central_vector - self.position
        self.position += correction
        return correction

# create objects
object1 = Object(100, HEIGHT/2, 8, 3, (228, 31, 40), vector(-0.2,2), False)
object2 = Object(WIDTH/2 - 100, HEIGHT/2 - 100, 10, 12, (56, 137, 199), vector(0.2,-2), True)
if object1.fixed:
    correction = object1.fix()
    object2.position += correction
    object2.dots[0] = (object2.dots[0][0] + correction[0], object2.dots[0][1] + correction[1])
elif object2.fixed:
    correction = object2.fix()
    object1.position += correction
    object1.dots[0] = (object1.dots[0][0] + correction[0], object1.dots[0][1] + correction[1])

# functions
# write a csv log file with data about the time and the objects
def log():
    global file
    d = str(calculate_distance(object1.position[0], object2.position[0], object1.position[1], object2.position[1]))
    file.write(str(datetime.datetime.now())+"\n")
    file.write("object;position;velocity;acceleration;unit_vector;mass;distance\n")
    file.write("object1;" + str(object1.position) + ";" + str(object1.velocity) + ";" + str(object1.acceleration) + ";" + str(object1.unit_vector) + ";" + str(object1.mass) + ";" + d + "\n")
    file.write("object2;" + str(object2.position) + ";" + str(object2.velocity) + ";" + str(object2.acceleration) + ";" + str(object2.unit_vector) + ";" + str(object2.mass) + ";" + d + "\n\n")

# calculate values
def calculate_distance(x1, x2, y1, y2):
    distance = math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
    return distance

def calculate_gravity(G, m1, m2, r):
    f = G * (m1 * m2) / r
    return f

# handle events
def handle_event(event):
    if event.type == pygame.QUIT:
        global running
        running = False
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            pygame.display.toggle_fullscreen()
        elif event.key == pygame.K_SPACE:
            log()

# iteration
while running:
    # events
    for event in pygame.event.get():
        handle_event(event)
    
    # calculate gravity and distance
    distance = calculate_distance(object1.position[0], object2.position[0], object1.position[1], object2.position[1])
    gravity = calculate_gravity(G, object1.mass, object2.mass, distance)

    # render
    if distance > (object1.radius + object2.radius):
        DISPLAY.fill((0,0,0))
        object1.update(gravity, object2.position[0], object2.position[1], distance)
        object2.update(gravity, object1.position[0], object1.position[1], distance)
        if object1.fixed:
            correction = object1.fix()
            object2.position += correction
        elif object2.fixed:
            correction = object2.fix()
            object1.position += correction
        object1.draw()
        object2.draw() 

    # finish iteration
    pygame.display.update()
    clock.tick(TICK_SPEED)

# quit pygame and close files
file.close()
pygame.quit()