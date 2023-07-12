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
threshhold = 5
class cell:
    def __init__(self, state, charge, position):
        self.state = state
        self.charge = charge
        self.position = position
    def updatecell(self, w):
        neighbors = []
        if self.position[0] % 2 == 0:
            neighborcoords = [(1, 0), (-1, 0), (0, 1), (1, 1), (0, -1), (1, -1)]
        else:
            neighborcoords = [(1, 0), (-1, 0), (-1, 1), (0, 1), (-1, -1), (0, -1)]
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
        for neighbor in neighbors:
            if neighbor.state == "dendrite":
                csum += neighbor.charge
        charge = self.charge + csum
        return charge

    def dendrite(self, neighbors):
        csum = 0
        for neighbor in neighbors:
            if neighbor.state == "axon":
                print("axon")
                csum += neighbor.charge
        return csum

    def axon(self, neighbors):
        global threshhold
        activation = False
        for neighbor in neighbors:
            if neighbor.state == "body":
                if neighbor.charge >= threshhold:
                    activation = True
        if activation:
            return 2
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
        b = brightness
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
        row.append(cell(["void", "body", "dendrite", "axon"][random.randrange(0, 4)], random.randrange(0, 10), (x, i)))
    world.append(row)
while True:
    chargesum = 0
    nextworld = []
    screen.fill((255, 255, 255))

    for row in world:
        for h in row:
            S = h.position[0] % 2
            drawhex(((h.position[1] + .5*S)*25, h.position[0]*37.4), h.state, h.charge)

    for event in pygame.event.get():
        pass
    for row in world:
        nr = []
        for item in row:
            updatedcharge = item.updatecell(world)
            chargesum += updatedcharge
            nr.append(cell(item.state, updatedcharge, item.position))
        nextworld.append(nr)
    print(chargesum)
    world = nextworld
  # Update.
  
  # Draw.
    pygame.display.flip()
    fpsClock.tick(fps)
    time.sleep(1)