import pygame
import inputbox
import numpy as np
import math
from pygame.locals import *

nodeImg = pygame.image.load('imgs/node.png')  # 42px by 42px sprite of a node
buttonImg = pygame.image.load('imgs/SolveButton.png')
logoImg = pygame.image.load('imgs/logo.png')
pinSuppImg=pygame.image.load('imgs/PinControl.png')


class Node:
    def __init__(self, (_x, _y), _id):
        self.x = _x
        self.y = _y
        self.id = _id
        self.moving = False
        self.connMembList = []
        self.fList = []
        # self.colour = (0, 0, 255)
        # self.thickness = 10

    def genLabel(self):
        # self.labelX = myFont.render("X: " + str(self.x), 2, (0, 0, 0))
        # self.labelY = myFont.render("Y: " + str(self.y), 2, (0, 0, 0))
        self.labelId = myFont.render("ID: " + str(self.id), 2, (0, 0, 0))
        if len(self.fList) >= 1:
            self.forceTakenLabel = myFont.render("Has Force", 2, (0, 0, 0))
        else:
            self.forceTakenLabel = myFont.render(" ", 2, (0, 0, 0))

    def display(self):
        # pygame.draw.circle(screen, self.colour, (self.x, self.y), self.size, self.thickness)
        if self.moving:
            self.moveMode()
        self.genLabel()
        screen.blit(nodeImg, (self.x, self.y))
        # screen.blit(self.labelX, (self.x - 21, self.y - 30))
        # screen.blit(self.labelY, (self.x - 21, self.y - 10))
        # screen.blit(self.labelId, (self.x - 21, self.y - 50))
        screen.blit(self.labelId, (self.x - 21, self.y - 20))
        if self.forceTakenLabel:
            screen.blit(self.forceTakenLabel, (self.x - 21, self.y - 70))

    def moveMode(self):
        # print("Move Mode")
        self.x = mouseX - 21
        self.y = mouseY - 21

    def takeMember(self, memb):
        self.connMembList.append(memb)

    def takeForce(self, force):
        self.fList.append(force)


class Member:
    def __init__(self, startNode, _id):
        self.startNode = startNode
        self.startTup = (startNode.x + 21, startNode.y + 21)
        self.id = _id
        self.moving = True
        (self.x, self.y) = self.startTup
        # print("Member Created")

    def display(self):
        if self.moving:
            self.color = (106, 135, 149)
            self.endTup = (mouseX, mouseY)
        else:
            if self.endNode:
                self.endTup = (self.endNode.x + 21, self.endNode.y + 21)
            self.color = (96, 125, 139)
        pygame.draw.line(screen, self.color, self.startTup, self.endTup, 21)
        # print("Member Drawn")


class Force:
    def __init__(self, startNode, value, theta):
        self.startTup = (startNode.x, startNode.y)
        (self.x, self.y) = self.startTup
        self.color = (52, 81, 94)
        self.value = value
        self.theta = -math.radians(theta)
        self.x1 = self.x + 21
        self.y1 = self.y + 21
        self.y2 = self.y1 + (self.value * math.sin(self.theta))
        self.x2 = self.x1 + (self.value * math.cos(self.theta))
        self.myArrow = Arrow(self.color, self.value, self.theta, (self.x1, self.y1), (self.x2, self.y2))

    def display(self):
        self.myArrow.display()
        self.fLabel = myFont.render("Force Value: " + str(self.value), 2, (0, 0, 0))
        screen.blit(self.fLabel, (self.x2 + 21, self.y2))


def forceBuilder():
    collidedNode = checkCollide(nodeList, mouseX, mouseY, 42)
    if collidedNode:
        isValid = 0
        while not isValid:
            try:
                value = inputbox.ask(screen, "Force Value (int)")
                if value == 'pin':
                    print('unknown value')
                    theta = 't'
                    r1 = reactionForce(collidedNode)
                    reactList.append(r1)
                else:
                    value = int(value)
                # value = int(raw_input("Please enter an integer value for this new force:"))
                isValid = 1

            except ValueError:
                print("Pls try again (value)")
        isValid = 0
        while not isValid and value != 'pin':
            try:
                theta = inputbox.ask(screen, "Theta Value (int) (from pos X)")
                theta = int(theta)
                if theta < 360:
                    forceList.append(Force(collidedNode, value, theta))
                    collidedNode.takeForce(forceList[len(forceList) - 1])
                    isValid = 1
                else:
                    raise (ValueError)
            except ValueError:
                print("Pls try again (angle)")
        #print("Force value is: " + str(value))
        #print("theta:" + str(theta))


class reactionForce:
    def __init__(self, endNode):
        self.node = endNode
        self.startTup = (endNode.x + 21, endNode.y + 121)
        self.theta = '?'
        (self.x, self.y) = self.startTup
        self.color = (220, 200, 200)
        self.theta = -math.radians(90)
        self.value = '?'
        self.x1 = self.x
        self.y1 = self.y
        self.y2 = endNode.y + 42
        self.x2 = endNode.x + 21
        #self.myArrow = Arrow(self.color, 100, -math.radians(90), (self.x1, self.y1), (self.x2, self.y2))

    def display(self):
        #self.myArrow.display()
        screen.blit(pinSuppImg,(self.node.x-30,self.node.y+21))
        self.fLabel = myFont.render("Force Value: " + str(self.value), 2, (0, 0, 0))
        screen.blit(self.fLabel, (self.x2 + 21, self.y2))


def forceSolver():  # This func will solve for reaction forces
    xVals = []
    yVals = []
    mVals = []
    for f in forceList:
        xVals.append(f.value * math.cos(f.theta))
        yVals.append(f.value * math.sin((f.theta)))
    for n in nodeList:
        # print(nodeList[0].id)
        if nodeList.index(n) != 0:
            (pX, pY) = (nodeList[0].x - n.x, nodeList[0].y - n.y)
            for f in n.fList:
                (fX, fY) = (f.value * math.cos(f.theta), f.value * (math.sin(f.theta)))
                m = pX * fY - pY * fX
                #print(m)
                mVals.append(m)
    mSum = int(sum(mVals))
    xSum = int(sum(xVals))
    ySum = int(sum(yVals))
    print("--------------------------")
    if xSum!=0:
        print("Force in X not zero : " + str(xSum))
    if ySum!=0:
        print("Force in Y not zero : " + str(ySum))
    if xSum == 0 & ySum == 0 & mSum == 0:
        return True
    if mSum!=0:
        print("Moments not zero : " + str(mSum))
    elif len(reactList) == 1:
        value = math.sqrt(xSum ** 2 + ySum ** 2)
        posTup=(reactList[0].node.x,reactList[0].node.y)
        zeroTup=(nodeList[0].x,nodeList[0].y)
        (pX,pY)=getDistVec(posTup,zeroTup)
        #Matrix should look like this
        #[m -pY pX]
        #[Fx 1  0]
        #[Fy  0  1]
        A=np.array([[-pY,pX],[1,0],[0,1]])
        B=np.array([[mSum],[xSum],[ySum]])
        print(np.linalg.lstsq(A,B))

        #theta = math.degrees(math.atan(-ySum / -xSum))
        #reactInterest = reactList.pop(0)
        #nodeInInterest = reactInterest.node
        #forceList.append(Force(nodeInInterest, value, theta))
        return True
    else:
        return False


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


class Button:
    def __init__(self, pos, img, actionName):
        self.pos = pos
        (self.x, self.y) = self.pos
        self.img = img
        self.actionName = actionName
        self.success = False
        self.pressed = 0

    def display(self):
        screen.blit(self.img, self.pos)

    def action(self):
        self.pressed = self.pressed + 1
        if self.actionName == 'force':
            self.success = forceSolver()


def checkCollide(classList, x, y, r):
    var = classList.__class__.__name__
    if (var != "list"):
        classList = [classList]
    list = []
    for p in classList:
        if abs(math.hypot(p.x - x, p.y - y)) <= r:
            list = list + [p]
    if len(list) == 0:
        return None
    elif (len(list) == 1):
        var = list[0]
        return var
    else:
        return list


def worldLabelDisplay():
    nodeLengthLabel = myFont.render("Number of Nodes: " + str(len(nodeList)), 2, (0, 0, 0))
    memberLengthLabel = myFont.render("Number of Members: " + str(len(memberList)), 2, (0, 0, 0))
    gameModeLabel = myFont.render("Game Mode: " + str(programMode), 2, (0, 0, 0))
    if solveButton.success:
        staticLabel = myFont.render(("Static Equilibrium"), 2, (0, 0, 0))
    elif solveButton.pressed == 0:
        staticLabel = myFont.render(("Not solved"), 2, (0, 0, 0))
    else:
        staticLabel = myFont.render(("Not in static equilibrium "), 2, (0, 0, 0))
    # mouseLabelX = myFont.render("mouseX :" + str(mouseX), 2, (0, 0, 0))
    # mouseLabelY = myFont.render("mouseY :" + str(mouseY), 2, (0, 0, 0))

    if programMode == 1:
        descriptionLabel = myFont.render("Node Building", 2, (0, 0, 0))
    elif programMode == 2:
        descriptionLabel = myFont.render("Member Connecting", 2, (0, 0, 0))
    elif programMode == 3:
        descriptionLabel = descriptionLabel = myFont.render("Force input", 2, (0, 0, 0))
    else:
        descriptionLabel = myFont.render("NULL", 2, (0, 0, 0))

    screen.blit(staticLabel, (400, 30))

    screen.blit(descriptionLabel, (400, 10))
    screen.blit(gameModeLabel, (10, 10))
    screen.blit(nodeLengthLabel, (10, 30))
    screen.blit(memberLengthLabel, (10, 50))
    # screen.blit(logoImg,(300,600))
    # screen.blit(mouseLabelX, (mouseX, mouseY + 10))
    # screen.blit(mouseLabelY, (mouseX, mouseY + 30))


def nodeBuilder():
    collidedNode = checkCollide(nodeList, mouseX, mouseY,42)  # checks to see mouse pos in relation to a node
    # print("Mouse Pressed")
    if not collidedNode:  # if the variable DOES NOT exist then add a new Node
        nodeListLength = len(nodeList)
        nodeList.append(Node((mouseX - 21, mouseY - 21), nodeListLength))
        # print("New node added")
    else:
        if not checkCollide(memberList, mouseX, mouseY,42):
            collidedNode.moving = not collidedNode.moving
            indexToDel = nodeList.index(collidedNode)
        if collidedNode.moving:
            return indexToDel
        return None


def memberBuilder2():
    collidedNode = checkCollide(nodeList, mouseX, mouseY,42)
    if collidedNode:
        memberList.append(Member(collidedNode, len(memberList)))
        memInInterest = memberList[len(memberList) - 1]
        collidedNode.takeMember(memInInterest)
        memInInterest.moving = True
        print("Started at: " + str(collidedNode.id))
        makingMember = True
    else:
        makingMember = False
    return makingMember


def memberEnder():
    collidedNode = checkCollide(nodeList, mouseX, mouseY,42)
    if collidedNode:
        print("ended on: " + str(collidedNode.id))
        memInInterest = memberList[len(memberList) - 1]
        memInInterest.moving = False
        memInInterest.endNode = collidedNode
        collidedNode.takeMember(memInInterest)


def createTesting():
    nodeList.append(Node((200, 200), 0))
    nodeList.append(Node((500, 500), 1))
    nodeList.append(Node((500, 200), 2))

    p = 0
    for n in nodeList:
        while p < len(nodeList) - 1:
            memberList.append(Member(n, p))
            memInInterest = memberList[len(memberList) - 1]
            n.takeMember(memInInterest)
            memInInterest.moving = False
            memInInterest.endNode = nodeList[p + 1]
            nodeList[p + 1].takeMember(memInInterest)
            p = p + 1
    memberList.append(Member(nodeList[1], p))
    memInInterest = memberList[len(memberList) - 1]
    nodeList[1].takeMember(memInInterest)
    memInInterest.moving = False
    memInInterest.endNode = nodeList[2]
    nodeList[2].takeMember(memInInterest)
    forceList.append(Force(nodeList[2], 100, 180))
    p = p + 1


def printOwners():
    for n in nodeList:
        print("Node Id: " + str(n.id))
        print("Owns: ")
        for m in n.connMembList:
            print("Memb" + str(m.id))
        for f in n.fList:
            print("Force" + str(f.value))


def buttonChecker():
    buttonCollided = checkCollide(buttonList, mouseX, mouseY, 100)
    if buttonCollided:
        buttonCollided.action()

def getDist(tup1,tup2):
    (x1,y1)=tup1
    (x2,y2)=tup2
    dx=abs(x2-x1)
    dy=abs(y2-y1)
    dist=math.sqrt((dx**2)+(dy**2))
    theta=math.atan(dy/dx)
    return (dist,theta)
def getDistVec(tup1,tup2):
    (x1,y1)=tup1
    (x2,y2)=tup2
    dx=(x2-x1)
    dy=(y2-y1)
    return (dx,dy)
# Pygame Stuff
pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Vinny's Truss Solver")
clock = pygame.time.Clock()

# Font Stuff
# defaultFont = pygame.font.get_default_font()
myFont = pygame.font.SysFont('Futura',
                             18)  # IF this doesnt work, replace the string 'Futura' with the variable defaultFont

# Main Global Variables
nodeList = []
memberList = []
forceList = []
buttonList = []
reactList = []
programMode = 3  # mode 1:Node Building
# mode 2: Member Connecting
# mode 3: Force

done = False
checkForDelete = False
makingMember = False

createTesting()
solveButton = Button((10, 75), buttonImg, 'force')
buttonList.append(solveButton)
while not done:
    (mouseX, mouseY) = pygame.mouse.get_pos()  # Global Variables mouseX and mouseY
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if programMode == 1:
                indexToDel = nodeBuilder()  # This function builds nodes, returns the moving node as indexToDel
                if not indexToDel:
                    checkForDelete = False
                else:
                    checkForDelete = True
            elif programMode == 2:
                if makingMember:
                    memberEnder()
                    makingMember = False
                else:
                    makingMember = memberBuilder2()
                    # debugger()
            elif programMode == 3:
                forceBuilder()
                buttonChecker()
        if event.type == pygame.KEYDOWN:
            if programMode == 1 and event.key == pygame.K_d and checkForDelete:  # Known Bug: Can't delete the first node
                # print("Deleting Index" + str(indexToDel))
                nodeList.pop(indexToDel)
                checkForDelete = False
            elif event.key == pygame.K_1:
                programMode = 1  # program mode 1: Node Building
            elif event.key == pygame.K_2:
                programMode = 2  # Member connecting
                # printOwners()
            elif event.key == pygame.K_3:
                programMode = 3  # force inputting

    if programMode == 1:
        color = (255, 255, 255)
    elif programMode == 2:
        color = (207, 216, 220)
    elif programMode == 3:
        color = (158, 167, 170)
    screen.fill(color)
    for m in memberList:
        m.display()
    for f in forceList:
        f.display()
    for p in nodeList:
        p.display()
    for r in reactList:
        r.display()
    if programMode == 3:
        for b in buttonList:
            b.display()
    worldLabelDisplay()
    pygame.display.flip()
    clock.tick(60)
