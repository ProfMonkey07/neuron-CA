#represent hexagonal plane using axial coordinates and vertical hexes
#the axials will be the horizontal axis and the left slanted vertical
#the state of a neuron holds 2 pieces of data: a charge, and a cell type
#cell types include cell body, axions, dendrits, and unipolar cells
#dendrites or unipolars will have charge set to x, where x is the sum of the charges of dendrites and unipolars
#REMINDER, 2 UNIPOLARS THAT ARE NEIGHBORS WILL OSCILLATE, FIX THIS OR LEAVE UNIPOLARS OUT FOR NOW
#cell bodies will increase in charge x for each neighboring dendrite with charge x
#axions will gain a charge of 1 if a nearby cell body has a charge greater than a where a is the action potential
#if a cell body has above the action potential, it goes back to 0
import pygame
import sys
import time
import random
import math
threshhold = 2
class cell:
    def __init__(self, state, charge, position):
        self.state = state
        self.charge = charge
        self.position = position
    def updatecell(self, w):
        neighbors = []
        if self.position[0] % 2 == 0:
            neighborcoords = [(1, 0), (-1, 0), (0, 1), (-1, -1), (0, -1), (1, -1)]
        else:
            neighborcoords = [(1, 0), (-1, 0), (-1, 1), (0, 1), (1, 1), (0, -1)]
        for item in neighborcoords:
            if 0 < self.position[0] + item[0] < 10 and 0 < self.position[1] + item[1] < 10:
                neighbors.append(w[self.position[1] + item[1]][self.position[0] + item[0]])
        if self.state == "body":
            c = self.body(neighbors)
        elif self.state == "dendrite":
            c = self.dendrite(neighbors)
        elif self.state == "axon":
            c = self.axon(neighbors)
        else:
            c = 0
        return c
    def body(self, neighbors):
        csum = 0
        global threshhold
        if self.charge >= threshhold:
            return 0
        else:
            for neighbor in neighbors:
                if neighbor.state == "dendrite":
                    csum += neighbor.charge
            charge = self.charge + csum
            return charge

    def dendrite(self, neighbors):
        csum = 0
        for neighbor in neighbors:
            if neighbor.state == "axon":
                csum += neighbor.charge
        if csum == 0:
            for neighbor in neighbors:
                print(self.position, neighbor.position, neighbor.state, neighbor.charge)
        return csum

    def axon(self, neighbors):
        global threshhold
        activation = False
        for neighbor in neighbors:
            if neighbor.state == "body":
                if neighbor.charge >= threshhold:
                    activation = True
        if activation:
            return 1
        else:
            return 0

#set hex center screen coordinates and define a drawing function for each
pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
 

def drawhex(co, state, charge):
    r, g, b = 0, 0, 0   # NOTE: is this the correct order?
    brightness = charge*5 + 55
    if state == "dendrite":
        r = brightness
    elif state == "body":
        g = brightness
    elif state == "axon":
        if charge != 0:
            b = 255
        else:
            b = 55
    else:
        r, g, b = 100, 100, 100
    x, y = co
    coords = [
        (2*x + 50, y +  0  ), 
        (2*x + 25, y + 12.5), 
        (2*x + 25, y + 37.5), 
        (2*x + 50, y + 50), 
        (2*x + 75, y + 37.5), 
        (2*x + 75, y + 12.5)]
    pygame.draw.polygon(screen, (r, g, b), coords)
# Game loop.
world = []
nextworld = []
for i in range(10):
    row = []
    for x in range(10):
        row.append(cell("void", 0, (x, i)))
    world.append(row)

paused = False

def getnearest(position):
    closest = 1000
    a, b = 0, 0
    tp = (0, 0)
    for y in range(10):
        for x in range(10):

            S = y % 2
            p = ((x + .5*S)*50 + 50, y*37.5 + 25)
            dist = math.sqrt((p[1] - position[1])**2 + (p[0]-position[0])**2)
            if dist < closest:
                closest = dist
                a, b = y, x
                tp = p
    return[b, a]


while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if paused:
                    paused = False
                else:
                    paused = True
            else:
                nearest = getnearest(pygame.mouse.get_pos())
                match event.key:
                    case pygame.K_0:
                        world[nearest[0]][nearest[1]].state = "void"
                    case pygame.K_1:
                        world[nearest[0]][nearest[1]].state = "dendrite"
                    case pygame.K_2:
                        world[nearest[0]][nearest[1]].state = "body"
                    case pygame.K_3:
                        world[nearest[0]][nearest[1]].state = "axon"
                    case pygame.K_q:
                        world[nearest[0]][nearest[1]].charge += 1
                    case pygame.K_w:
                        world[nearest[0]][nearest[1]].charge -= 1


    if not paused:
        chargesum = 0
        nextworld = []
        screen.fill((255, 255, 255))

        for row in world:
            nr = []
            for item in row:
                updatedcharge = item.updatecell(world)
                chargesum += updatedcharge
                nr.append(cell(item.state, updatedcharge, item.position))
            nextworld.append(nr)
        world = nextworld
        time.sleep(1)
    # Update.
    
    # Draw.
    for row in world:
            for h in row:
                S = h.position[0] % 2
                p = ((h.position[1] + .5*S)*25, h.position[0]*37.5)
                drawhex(p, h.state, h.charge)
                pygame.Surface.set_at(screen, (int(p[0])*2 + 50, int(p[1] + 25)), (255, 192, 1))
    pygame.display.flip()
    fpsClock.tick(fps)