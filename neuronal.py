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
    def updatecell(neighborcoords):
        neighbors = []
        for item in neighborcoords:
            pass
        if self.state == "body":
            c = body(neighbors)
        elif self.state == "dendrite":
            c = dendrite(neighbors)
        else:
            c = axon(neighbors)
        return c
    def body(neighbors):
        if self.charge >= threshhold:
            return 0
        neigborsum = 0
        for neighbor in neighbors:
            if neighbor.state == "dendrite":
                neighborsum += neighbor.charge
        charge = self.charge + neighborsum
        return charge

    def dendrite(neighbors):
        neigborsum = 0
        for neighbor in neighbors:
            if neighbor.state == "axon":
                neighborsum += neighbor.charge
        return neighborsum

    def axon(neighbors):
        neigborsum = 0
        for neighbor in neighbors:
            if neighbor.state == "body":
                if neighbor.charge >= threshhold:
                    return 1
                else:
                    return 0

neighborcoords = [(-2, 0), (2, 2), (-1, -1), (-1, 1), (1, 1), (1, -1)]
world = []
nextworld = []
for i in range(10):
    row = []
    if i % 2 == 0:
        for x in range(10):
            row.append(cell("body", 5, (x*2, i)))
    else:
        for x in range(10):
            row.append(cell("body", 5, (x*2 + 1, i)))
    world.append(row)

#set hex center screen coordinates and define a drawing function for each
pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
 

def drawhex(co, state, charge):
    col = [0, 0, 0]
    if state == "dendrite":
        col[0] = 55 + charge*20
    elif state == "body":
        col[1] = 55 + charge*20
    elif state == "axon":
        col[2] = 55 + charge*20
    pygame.draw.polygon(screen, (col[0], col[1], col[2]), [(50 + co[0], 0 + co[1]), (25 + co[0], 12.5 + co[1]), (25 + co[0], 37.5 + co[1]), (50 + co[0], 50 + co[1]), (75 + co[0], 37.5 + co[1]), (75 + co[0], 12.5 + co[1])])
# Game loop.
while True:
    screen.fill((0, 0, 0))
  
    for event in pygame.event.get():
        print(event.type)
  
  # Update.
  
  # Draw.
    for row in world:
        for h in row:
            drawhex((h.position[0]*25, h.position[1]*37.4), ["body", "axon", "dendrite"][random.randrange(0, 3)], random.randrange(0, 10))
    pygame.display.flip()
    fpsClock.tick(fps)