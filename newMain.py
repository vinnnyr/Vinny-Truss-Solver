import pygame
import numpy as np
import math


class Structure:
    def __init__(self):
        self.membList = []

    def create(self):
        if len(self.membList) > 0:
            lastMemb = self.membList[len(self.membList) - 1]
            if lastMemb.moving:
                lastMemb.moving = False
            else:
                self.addMemb()
        else:
            self.addMemb()

    def addMemb(self):
        self.membList.append(Member((mouseX, mouseY)))

    def display(self):
        for m in self.membList:
            m.display()


class Member:
    def __init__(self, startPos):
        self.startPos = startPos
        self.endPos = (mouseX, mouseY)
        self.color = (255, 250, 250)
        self.moving = True

    def display(self):
        if self.moving:
            self.endPos = (mouseX, mouseY)
        pygame.draw.line(screen, self.color, self.startPos, self.endPos, 5)


# Pygame Stuff
pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Vinny's Truss Solver")
clock = pygame.time.Clock()
# defaultFont = pygame.font.get_default_font()
myFont = pygame.font.SysFont('Futura',
                             18)  # IF this doesnt work, replace the string 'Futura' with the variable defaultFont
mainStruct = Structure()  # init structure
done = False
while not done:
    (mouseX, mouseY) = pygame.mouse.get_pos()  # Global Variables mouseX and mouseY
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mainStruct.create()

    # Display, Flip, Tick
    screen.fill((0,0,0))
    mainStruct.display()
    pygame.display.flip()
    clock.tick(60)
