import pygame
import numpy as np
import math

def checkCollide(classList,pos, r):
    var = classList.__class__.__name__
    (x,y)=pos
    if (var != "list"): #if single var is to be checked, make it into a list
        classList = [classList]
    list = []
    for p in classList:
        className=p.__class__.__name__
        if className=='tuple': #if classList is a list of tups, unpack the tup
            (a,b)=p
            if abs(math.hypot(a - x, b - y)) <= r:
                list = list + [p]
        else: #otherwise cehck against the x and y pos
            if abs(math.hypot(p.x - x, p.y - y)) <= r:
                list = list + [p]
    if len(list) == 0:
        return None
    elif (len(list) == 1):
        var = list[0]
        return var
    else:
        return list

class Structure:
    def __init__(self):
        self.membList = []

    def create(self): #will be called when mouse is clicked
        if len(self.membList) > 0: #If membList is populated
            lastMemb = self.membList[len(self.membList) - 1] #get the last member
            if lastMemb.moving:
                self.startPosList=self.getStartPos()
                var=checkCollide(self.startPosList,(mouseX,mouseY),15)
                lastMemb.moving = False #If this was entered, the member is now "complete"
                if var:
                    if var.__class__.__name__=='list':
                        var=var[0] #this condition happens when you trace over members
                    lastMemb.endPos=var
            else:#Check collide with end of other memb (to connect) and then add new Memb
                var=checkCollide(lastMemb,(mouseX,mouseY),15)
                if var:
                    self.addMemb(lastMemb.endPos) #start new memb
        else: #No membList population, start one.
            self.addMemb((mouseX,mouseY))

    def addMemb(self,pos):
        self.membList.append(Member(pos))
    def getStartPos(self):
        list=[]
        for m in self.membList:
            list.append(m.startPos)
        return list
    def display(self):
        for m in self.membList:
            m.display()


class Member:
    def __init__(self, startPos):
        self.startPos = startPos
        self.endPos = (mouseX, mouseY)
        self.color = (255, 255, 255) #white
        self.moving = True

    def display(self):
        if self.moving:
            self.endPos = (mouseX, mouseY)
            (self.x,self.y)=self.endPos
        else:
            name=self.endPos.__class__.__name__
            if name!= 'tuple':
                print(name)
            pygame.draw.circle(screen, self.color, self.endPos, 5)
        pygame.draw.circle(screen, self.color, self.startPos, 5)
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
    screen.fill((0,0,0))#black
    mainStruct.display()
    pygame.display.flip()
    clock.tick(60)
