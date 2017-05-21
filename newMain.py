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
        self.structNodes = []  # running list of all the nodes of the struct
        self.memberAdded = False
        self.display()
        # self.testingScenario()

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
        else:
            print('something weird happened')  # This is where a force is not attached to a node

    def addMemb(self, pos):
        self.membList.append(Member(pos, self))
        self.memberAdded = True

    def forceMembPos(self, pos1, pos2):
        self.addMemb(pos1)
        membInFocus = self.membList[len(self.membList) - 1]
        membInFocus.moving = False
        membInFocus.endPos = pos2
        membInFocus.endMember(pos2)
        self.memberAdded= True

    def testingScenario(self):  # This function generates a known truss
        a = 300
        b = 150
        self.forceMembPos((a, a), (a, a + b))
        self.printMembInfo()
        self.forceMembPos((a, a + b), (a + b, a))
        self.printMembInfo()
        self.forceMembPos((a, a + b), (a + b, a + b))
        self.printMembInfo()
        self.forceMembPos((a, a), (a + b, a))
        self.printMembInfo()
        self.forceMembPos((a + b, a), (a + b, a + b))
        self.printMembInfo()
        self.createForce((a, a + b), 'roller')
        #self.printMembInfo()
        self.createForce((a + b, a + b), 'pin')
        #self.printMembInfo()
        self.createForce((a + b, a), 'vec')
        #self.printMembInfo()

    def getStartPos(self):
        list = []
        for m in self.membList:
            list.append(m.startPos)
        return list
    def printMembInfo(self):
        self.display()
        self.membInInterest=self.membList[len(self.membList)-1]
        print("Member Numb: " + str(len(self.membList)))
        print('....')
        self.tempNodeList=self.membInInterest.nodeList
        for n in self.tempNodeList:
            print(n)
        print('-----------------')

    def printInfo(self):
        print("Number of Nodes: " + str(len(self.structNodes)))
        # for n in self.structNodes:
        #     print(n)
        print("Number of Members: " + str(len(self.membList)))

    def display(self):
        # self.structNodes = []  # running list of all the nodes of the struct
        if self.memberAdded:
            self.structNodes = self.structNodes + self.membList[len(self.membList) - 1].nodeList
            self.memberAdded = False
            self.structNodes = list(set(self.structNodes))  # This is a a trick to remove duplicates
        for m in self.membList:
            m.display()
            # self.structNodes = self.structNodes + m.nodeList  # This is inefiicient, creatign a whole new list everytime


class Member:
    def __init__(self, startPos, struct):
        self.startPos = startPos
        self.myStruct = struct
        # self.endPos = (mouseX, mouseY)
        self.nodeList = []
        # self.nodeList.append(Node(self.startPos, True))
        self.addNode(startPos, True)
        self.color = white  # white
        self.moving = True

    def addNode(self, pos, isStartNode):  # Create new node if there isn't one in the pos in question
        self.var = checkCollide(self.myStruct.structNodes, pos, 2)
        if self.var:
            if self.var.__class__.__name__ == 'list':
                self.var = self.var[0]  # To take care of duplicaes
            self.nodeList.append(self.var)
        else:
            self.nodeList.append(Node(pos, isStartNode))  # Create new Node

    def endMember(self, pos):
        if len(self.nodeList) < 2:  # Each member only has two nodes
            # print(len(self.nodeList))
            self.addNode(self.endPos, False)
        (self.x, self.y) = self.endPos

    def display(self):
        if self.moving:
            self.endPos = (mouseX, mouseY)
            (self.x, self.y) = self.endPos
        pygame.draw.line(screen, self.color, self.startPos, self.endPos, 5)
        if self.moving == False:
            self.endMember(self.endPos)
        if len(self.nodeList) == 2:
            self.startNode = self.nodeList[0]
            self.endNode = self.nodeList[1]

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
        self.label=myFont.render(str(self.pos),1, red)

    def addForce(self, pos, type):
        # print(type)
        if type == 'pin':
            self.forceList.append(PinSupport(pos))
        elif type == 'roller':
            self.forceList.append(Roller(pos))
        elif type == 'vec':
            self.forceList.append(VectorForce(pos, 50, 0))

    def display(self):
        pygame.draw.circle(screen, self.color, self.pos, self.r)
        screen.blit(self.label,self.pos)
        for f in self.forceList:
            f.display()


# The following 3 classes are types of Forces

#Can support x and y forces
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

#Can only support one force in a certain direction (typically straight up)
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

#A vector force defined by value and angle from horz X axis
class VectorForce:
    def __init__(self, pos, value, angle):
        self.pos = pos
        self.value = value
        self.theta = -math.radians(angle)
        self.color = red
        (self.x, self.y) = self.pos
        self.x2 = self.x + (self.value * math.cos(self.theta))
        self.y2 = self.y + (self.value * math.sin(self.theta))
        self.myArrow = Arrow(self.color, self.value, self.theta, self.pos, (self.x2, self.y2))

    def display(self):
        self.myArrow.display()
        self.fLabel = myFont.render("Force Value: " + str(self.value), 2, red)
        screen.blit(self.fLabel, (self.x2 + 21, self.y2))

#Arrow used for VectorForce
class Arrow:
    def __init__(self, color, val, theta, (x1, y1), (x2, y2)):
        self.color = color
        self.theta = theta
        self.value = val
        (self.x1, self.y1) = (x1, y1)
        (self.x2, self.y2) = (x2, y2)
        self.x3 = self.x2 + (.15 * self.value * math.sin(-self.theta)) - 2 * math.cos(self.theta)
        self.y3 = self.y2 + (.15 * self.value * math.cos(-self.theta)) - 2 * math.sin(self.theta)
        self.x4 = self.x2 - (.15 * self.value * math.sin(-self.theta)) - 2 * math.cos(self.theta)
        self.y4 = self.y2 - (.15 * self.value * math.cos(-self.theta)) - 2 * math.sin(self.theta)
        self.x5 = self.x2 + (.15 * self.value * math.cos(self.theta))
        self.y5 = self.y2 + (.15 * self.value * math.sin(self.theta))

    def display(self):
        pygame.draw.line(screen, self.color, (self.x1, self.y1), (self.x2, self.y2), 10)
        pygame.draw.polygon(screen, self.color, ((self.x3, self.y3),
                                                 (self.x4, self.y4), (self.x5, self.y5)), 0)


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
                elif mode == 3:
                    fType = 'vec'

                mainStruct.createForce((mouseX, mouseY), fType)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                mode = 0
                mainStruct.printInfo()
            elif event.key == pygame.K_1:
                mode = 1  # pin
            elif event.key == pygame.K_2:
                mode = 2  # roller
            elif event.key == pygame.K_3:
                mode = 3  # ved
            elif event.key == pygame.K_a:
                mainStruct.testingScenario()
            print("Game Mode:" + str(mode))

    # Display, Flip, Tick
    screen.fill((0, 0, 0))  # black
    mainStruct.display()
    pygame.display.flip()
    clock.tick(60)
