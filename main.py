import pygame
import math
import os
from pygame.locals import *


class Node:
    def __init__(self, (_x, _y), _id):
        self.x = _x
        self.y = _y
        self.id = _id
        self.moving = False
        # self.colour = (0, 0, 255)
        # self.thickness = 10

    def genLabel(self):
        self.labelX = myFont.render("X: " + str(self.x), 2, (0, 0, 0))
        self.labelY = myFont.render("Y: " + str(self.y), 2, (0, 0, 0))
        self.labelId = myFont.render("ID: " + str(self.id), 2, (0, 0, 0))

    def display(self):
        # pygame.draw.circle(screen, self.colour, (self.x, self.y), self.size, self.thickness)
        if self.moving:
            self.moveMode()
        self.genLabel()
        screen.blit(nodeImg, (self.x, self.y))
        screen.blit(self.labelX, (self.x - 21, self.y - 30))
        screen.blit(self.labelY, (self.x - 21, self.y - 10))
        screen.blit(self.labelId, (self.x - 21, self.y - 50))

    def moveMode(self):
        # print("Move Mode")
        self.x = mouseX - 21
        self.y = mouseY - 21


class Member:
    def __init__(self, startTup):
        self.startTup = startTup
        (self.x, self.y) = self.startTup
        self.moving = True
        # print("Member Created")

    def display(self):
        if self.moving:
            self.moveMode()
        pygame.draw.line(screen, (100, 100, 110), self.startTup, self.endTup, 21)
        # print("Member Drawn")

    def moveMode(self):
        # print("Move Mode")
        (self.x1, self.y1) = self.startTup
        self.endTup = (mouseX, mouseY)
        (self.x, self.y) = self.endTup

def worldLabelDisplay():
    nodeLengthLabel=myFont.render("Number of Nodes: "+ str(len(nodeList)),2, (0, 0, 0))
    memberLengthLabel=myFont.render("Number of Members: "+ str(len(memberList)),2, (0, 0, 0))
    gameModeLabel=myFont.render("Game Mode: "+ str(programMode),2, (0, 0, 0))

    screen.blit(nodeLengthLabel,(10,10))
    screen.blit(memberLengthLabel,(10,30))
    screen.blit(gameModeLabel, (10, 50))



def checkCollide(classList, x, y):
    var=classList.__class__.__name__
    if(var!="list"):
        classList=[classList]
    for p in classList:
        if math.hypot(p.x - x, p.y - y) <= 50:
            return p
    return None


def nodeBuilder():
    collidedNode = checkCollide(nodeList, mouseX, mouseY)  # checks to see mouse pos in relation to a node
    # print("Mouse Pressed")
    if not collidedNode:  # if the variable DOES NOT exist then add a new Node
        nodeListLength = len(nodeList)
        nodeList.append(Node((mouseX - 21, mouseY - 21), nodeListLength))
        # print("New node added")
    else:
        collidedNode.moving = not collidedNode.moving
        indexToDel = nodeList.index(collidedNode)
        if collidedNode.moving:
            return indexToDel
        return None


def memberBuilder():
    collidedMember = checkCollide(memberList, mouseX, mouseY)
    if not collidedMember:
        nodeInInterest = memberSnapToNode(Member((mouseX - 21, mouseY - 21)))
        if nodeInInterest:
            print("Collided with: " + nodeInInterest.__class__.__name__ + " " + str(nodeInInterest.id))
            memberList.append(Member((nodeInInterest.x + 21, nodeInInterest.y + 21)))
    else:
        collidedMember.moving = not collidedMember.moving
        memToDel = memberList.index(collidedMember)
        if collidedMember.moving:
            return memToDel
        return None


def memberSnapToNode(memberToCheck):
    for p in nodeList:
        nodeInInterest = checkCollide(memberToCheck, p.x, p.y)
        if nodeInInterest:
            return p
    return None


# Pygame Stuff
pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Vinny's Truss Solver")
clock = pygame.time.Clock()

# Font Stuff
defaultFont = pygame.font.get_default_font()
myFont = pygame.font.SysFont(defaultFont, 22)

# Main Global Variables
nodeList = []
memberList = []
nodeDict = {}
programMode = 0  # mode 0:Node Building
# mode 1: Member Connecting

done = False
checkForDelete = False
nodeImg = pygame.image.load('node.png')  # 42px by 42px sprite of a node

while not done:
    (mouseX, mouseY) = pygame.mouse.get_pos()  # Global Variables mouseX and mouseY
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if programMode == 0:
                indexToDel = nodeBuilder()  # This function builds nodes, returns the moving node as indexToDel
                if not indexToDel:
                    checkForDelete = False
                else:
                    checkForDelete = True
            elif programMode == 1:
                memberBuilder()
        if event.type == pygame.KEYDOWN:
            if programMode == 0 and event.key == pygame.K_d and checkForDelete:  # Known Bug: Can't delete the first node
                # print("Deleting Index" + str(indexToDel))
                nodeList.pop(indexToDel)
                checkForDelete = False
            elif event.key == pygame.K_1:
                programMode = 1  # program mode 1: Truss Building
            elif event.key == pygame.K_0:
                programMode = 0

    if programMode == 0:
        color = (125, 125, 120)
    else:
        color = (200, 200, 225)
    screen.fill(color)
    for m in memberList:
        m.display()
    for p in nodeList:
        p.display()
    worldLabelDisplay()
    pygame.display.flip()
    clock.tick(60)
