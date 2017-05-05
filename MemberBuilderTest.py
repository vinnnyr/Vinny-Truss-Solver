import pygame
import math
import os
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Member Builder Test")
clock = pygame.time.Clock()

# Font Stuff
defaultFont = pygame.font.get_default_font()
myFont = pygame.font.SysFont(defaultFont, 22)

# Main Global Variables
nodeList = []
nodeDict = {}
programMode = 0  # mode 0:Node Building
memberList=[]

done = False
checkForDelete = False

class member:
    def __init__(self,startTup):
        self.startTup=startTup
        self.moving=True
        #print("Member Created")
    def display(self):
        if self.moving:
            self.moveMode()
        pygame.draw.line(screen,(255,10,10),self.startTup,self.endTup,50)
        #print("Member Drawn")


    def moveMode(self):
        # print("Move Mode")
        (self.x1,self.y1)=self.startTup
        self.endTup = (mouseX,mouseY)

def memberBuilder():
    memberList.append(member((mouseX-21,mouseY-21)))

while not done:
    (mouseX, mouseY) = pygame.mouse.get_pos()
    color = (200, 200, 225)
    screen.fill(color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            memberBuilder()
    for m in memberList:
        m.display()
    pygame.display.flip()
    clock.tick(60)

