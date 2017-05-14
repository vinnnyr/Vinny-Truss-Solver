import pygame
import math

white = (255, 255, 255)
grey = (96, 125, 139)
red = (244, 67, 54)
black = (0, 0, 0)


# A Structure has a list of Members, and a member has a list of nodes
class Structure:
    def __init__(self):
        self.membList = []

    def createMemb(self, pos):  # will be called when mouse is clicked
        if len(self.membList) > 0:  # If membList is populated
            lastMemb = self.membList[len(self.membList) - 1]  # get the last member
            if lastMemb.moving:
                self.startPosList = self.getStartPos()
                var = checkCollide(self.startPosList, pos, 15)
                lastMemb.moving = False  # If this was entered, the member is now "complete"
                if var:
                    if var.__class__.__name__ == 'list':
                        var = var[0]  # this condition happens when you trace over members
                    lastMemb.endPos = var
            else:  # Check collide with end of other memb (to connect) and then add new Memb
                # var = checkCollide(lastMemb, (mouseX, mouseY), 15)
                var = checkCollide(self.membList, pos, 15)
                if var:
                    if var.__class__.__name__ == 'list':
                        var = var[0]  # this condition happens when you trace over members
                    # self.addMemb(lastMemb.endPos)  # start new memb
                    self.addMemb(var.endPos)
        else:  # No membList population, start one.
            self.addMemb((mouseX, mouseY))

    def createForce(self, pos, type):
        var = checkCollide(self.structNodes, pos, 50)
        if var:
            if var.__class__.__name__ == 'list':
                var = var[0]  # this condition happens when you trace over members
            nodeInInterest = var
            nodeInInterest.addForce((nodeInInterest.x, nodeInInterest.y), type)

    def addMemb(self, pos):
        self.membList.append(Member(pos))

    def forceMembPos(self, pos1, pos2):
        self.addMemb(pos1)
        membInFocus = self.membList[len(self.membList) - 1]
        membInFocus.moving = False
        membInFocus.endPos = pos2

    def testingScenario(self):  # This function generates a known truss
        a = 300
        b = 150
        self.forceMembPos((a, a), (a, a + b))
        self.forceMembPos((a, a + b), (a + b, a))
        self.forceMembPos((a, a + b), (a + b, a + b))
        self.forceMembPos((a, a), (a + b, a))
        self.forceMembPos((a + b, a), (a + b, a + b))
        self.createForce((a, a + b), 'roller')
        self.createForce((a + b, a + b), 'pin')

    def getStartPos(self):
        list = []
        for m in self.membList:
            list.append(m.startPos)
        return list

    def display(self):
        self.structNodes = []  # running list of all the nodes of the struct
        for m in self.membList:
            m.display()
            self.structNodes = self.structNodes + m.nodeList


class Member:
    def __init__(self, startPos):
        self.startPos = startPos
        # self.endPos = (mouseX, mouseY)
        self.nodeList = []
        self.nodeList.append(Node(self.startPos, True))  # pygame.draw.circle(screen, grey, self.startPos, 15)
        self.color = white  # white
        self.moving = True

    def display(self):
        if self.moving:
            self.endPos = (mouseX, mouseY)
            (self.x, self.y) = self.endPos
        pygame.draw.line(screen, self.color, self.startPos, self.endPos, 5)
        if self.moving == False & len(self.nodeList) < 2:  # Each member only has two nodes
            self.nodeList.append(Node(self.endPos, False))  # pygame.draw.circle(screen, grey, self.endPos, 15)
            (self.x, self.y) = self.endPos
        for n in self.nodeList:
            n.display()


class Node:
    def __init__(self, pos, isStart):
        self.isStart = isStart
        self.pos = pos
        self.r = 15
        (self.x, self.y) = pos
        self.color = grey
        self.forceList = []

    def addForce(self, pos, type):
        # print(type)
        if type == 'pin':
            self.forceList.append(PinSupport(pos))
        elif type == 'roller':
            self.forceList.append(Roller(pos))

    def display(self):
        pygame.draw.circle(screen, self.color, self.pos, self.r)
        for f in self.forceList:
            f.display()


# The following 3 classes are types of Forces

class PinSupport:
    def __init__(self, pos):
        self.pos = pos
        (self.x, self.y) = self.pos
        self.color = red

    def display(self):
        self.p1 = self.pos
        self.p2 = (self.x - 37, self.y + 50)
        self.p3 = (self.x + 37, self.y + 50)
        pygame.draw.polygon(screen, self.color, (self.p1, self.p2, self.p3), 0)


class Roller:
    def __init__(self, pos):
        self.pos = pos
        (self.x, self.y) = self.pos
        self.color = red

    def display(self):
        self.p1 = self.pos
        self.p2 = (self.x - 37, self.y + 35)
        self.p3 = (self.x + 37, self.y + 35)
        self.p4 = (self.x + 22, self.y + 40)
        self.p5 = (self.x - 22, self.y + 40)
        pygame.draw.polygon(screen, self.color, (self.p1, self.p2, self.p3), 0)
        pygame.draw.circle(screen, self.color, self.p4, 10, 0)
        pygame.draw.circle(screen, self.color, self.p5, 10, 0)


def checkCollide(classList, pos, r):
    var = classList.__class__.__name__
    (x, y) = pos
    if (var != "list"):  # if single var is to be checked, make it into a list
        classList = [classList]
    list = []
    for p in classList:
        className = p.__class__.__name__
        # print(className)
        if className == 'tuple':  # if classList is a list of tups, unpack the tup
            (a, b) = p
            if abs(math.hypot(a - x, b - y)) <= r:
                list = list + [p]
        else:  # otherwise cehck against the x and y pos
            if abs(math.hypot(p.x - x, p.y - y)) <= r:
                list = list + [p]
    if len(list) == 0:
        return None
    elif (len(list) == 1):
        var = list[0]
        return var
    else:
        return list


# Pygame Stuff
pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Vinny's Truss Solver")
clock = pygame.time.Clock()
# defaultFont = pygame.font.get_default_font()
myFont = pygame.font.SysFont(
    'Futura',
    18)  # IF this doesnt work, replace the string 'Futura' with the variable defaultFont
mainStruct = Structure()  # init structure
count = 0
done = False
mode = 0
while not done:
    # Following section is to generte the intial testing struct
    count = count + 1
    if count > 1:
        if count < 5:
            mainStruct.testingScenario()

    # Main Program:
    (mouseX, mouseY) = pygame.mouse.get_pos()  # Global Variables mouseX and mouseY
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if mode == 0:
                mainStruct.createMemb((mouseX, mouseY))
            else:
                if mode == 1:
                    fType = 'pin'
                elif mode == 2:
                    fType = 'roller'
                mainStruct.createForce((mouseX, mouseY), fType)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                mode = 0
            elif event.key == pygame.K_1:
                mode = 1
            elif event.key == pygame.K_2:
                mode = 2
            print("Game Mode:" + str(mode))

    # Display, Flip, Tick
    screen.fill((0, 0, 0))  # black
    mainStruct.display()
    pygame.display.flip()
    clock.tick(60)
