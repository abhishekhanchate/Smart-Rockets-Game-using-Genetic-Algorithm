# Rylan Hunter
# ECEN 689 - Final Project Code

# THIS IS A SUPPORTING FILE FOR THE SMART_ROCKETS PROJECT
# It contains the classes "DOT", "POPULATION", "GOAL", "OBSTACLE", and "BRAIN"
# Dot is the object moving around,
# Brain is the 'DNA' of the dot, giving it direction,
# Population is a collection of dots,
# Goal is the target destination
# Obstacles are what they sound like

from PVector import PVector
import pygame
import math
import random

# Define global parameters.  Basically copy/paste from main.py.  I couldn't figure out how to get main.py to share
# these without passing them in as parameters, and got tired of doing so.
SCREENWIDTH  = 400
SCREENHEIGHT = 400

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

'''
Dot Class:  
A 'dot' has position, velocity, and acceleration vectors. 
The 'Brain' is the directions that the dot follows.  These apply forces (accelerations) to the dot.
The dot knows if it is dead, if it reached the goal, it's fitness, and whether or not it is the best.

The Dot can show itself, print its current pos/vel/accel to screen, move itself, 
update itself (test if done/collision), calculate its fitness, and clone itself
'''
class Dot:
    def __init__(self, xx=SCREENWIDTH/2, yy=SCREENHEIGHT-10):
        self.pos = PVector(xx,yy)
        self.vel = PVector(0,0,5)
        self.acc = PVector(0,0)
        self.brain = Brain(400)
        self.dead = False
        self.fitness = 0
        self.reachedGoal = False
        self.isBest = False

    def show(self, SCREEN):
        dotRad = 2
        if self.isBest:
            dotRad = 4
            surf1 = pygame.Surface((dotRad*2,dotRad*2))
            surf1 = surf1.convert()
            pygame.draw.circle(surf1, GREEN, (dotRad-1,dotRad-1), dotRad)
            SCREEN.blit(surf1,(self.pos.x-dotRad,self.pos.y-dotRad))
        else:
            surf1 = pygame.Surface((dotRad*2,dotRad*2))
            surf1 = surf1.convert()
            pygame.draw.circle(surf1, WHITE, (dotRad-1,dotRad-1), dotRad)
            SCREEN.blit(surf1,(self.pos.x-dotRad,self.pos.y-dotRad))

    def print(self):
        arr = [self.pos.getVec(),self.vel.getVec(),self.acc.getVec()]
        print(arr)

    def move(self):
        if (len(self.brain.directions)>self.brain.step):
            self.acc = self.brain.directions[self.brain.step]
            self.brain.step += 1
        else:
            self.dead = True
        self.vel.add(self.acc)
        self.pos.add(self.vel)
        
    def update(self, SCREENWIDTH, SCREENHEIGHT,Goal,Obstacles):
        if (not self.dead) and (not self.reachedGoal):
            self.move()
            x = self.pos.x
            y = self.pos.y
            if (x < 2) or (y < 2) or (x > SCREENWIDTH-2) or (y > SCREENHEIGHT-2):
                self.dead = True
            elif (PVector.dist(self.pos,Goal.pos) < Goal.size):
                self.reachedGoal = True
            for obs in Obstacles:
                if obs.collision(self):
                    self.dead = True

    def calculateFitness(self,Goal):
        if self.reachedGoal:
            self.fitness = 1.0/16.0 + 10000 / (self.brain.step * self.brain.step)
        else:
            distToGoal = PVector.dist(self.pos,Goal.pos)
            self.fitness = 1.0/(distToGoal * distToGoal)

    def gimmieBaby(self):
        baby = Dot()
        baby.brain = self.brain.clone()
        return baby

'''
Brain Class:  
A 'brain' contains the forces (acceleration vectors) applied to a dot. This is the "DNA" of the genetic algorithm
It can initialize itself, clone itself, and mutate itself
'''
class Brain:
    def __init__(self, size=100):
        self.directions = []
        self.step = 0
        for i in range (size):
            ang = random.uniform(0, 2*math.pi)
            self.directions.append(PVector.fromAngle(ang))

    def randomize(self,size):
        for i in range (size):
            ang = random.uniform(0, 2*math.pi)
            self.directions.append(PVector.fromAngle(ang))

    def clone(self):
        clone = Brain(len(self.directions))
        clone.directions = self.directions.copy()
        return clone

    def mutate(self,mutationRate):
        for i in range(len(self.directions)):
            rand = random.random()
            if rand < mutationRate:
                randAng = random.uniform(0,2*math.pi)
                self.directions[i] = PVector.fromAngle(randAng)

'''
Population Class:  
A 'population' is a collection of dots. It can calculate the statistics of the dots, call update on the dots, etc. 
'''
class Population:
    def __init__(self, size=100, dotStartX=0, dotStartY=0):
        self.dots = []
        for i in range (size):
            self.dots.append(Dot(dotStartX,dotStartY))
        self.fitnessSum = 0
        self.generation = 1
        self.bestDot = 0
        self.bestSteps = len(self.dots[0].brain.directions)
        self.avgFitness = 0
        self.stdDevFitness = 0
        self.maxFitness = 0

    def show(self,SCREEN):
        for i in range (1,len(self.dots)):
            self.dots[i].show(SCREEN)
        self.dots[0].show(SCREEN)

    def update(self, SCREENWIDTH, SCREENHEIGHT,Goal,Obstacles):
        for i in range (len(self.dots)):
            if self.dots[i].brain.step > self.bestSteps:
                self.dots[i].dead = True
            else:
                self.dots[i].update(SCREENWIDTH,SCREENHEIGHT,Goal,Obstacles)

    def calculateAvgFitness(self):
        self.avgFitness = self.fitnessSum / len(self.dots)

    def calculateStdDevFitness(self):
        runningSum = 0
        for dot in self.dots:
            runningSum += math.pow(dot.fitness - self.avgFitness,2)
        self.stdDevFitness = math.sqrt(runningSum/len(self.dots))

    def printStats(self):
        print("Generation: ",self.generation)
        print("Best Fit:   ",self.maxFitness)
        print("Best Steps: ",self.bestSteps)
        print("Mean Fit:   ",self.avgFitness)
        print("StdDev Fit: ",self.stdDevFitness)
        print(" ")

    def naturalSelection(self):
        # Print stats of the generation
        Population.setBestDot(self)
        Population.calculateFitnessSum(self)
        Population.calculateAvgFitness(self)
        Population.calculateStdDevFitness(self)
        Population.printStats(self)

        # Generate new dot list (next generation)
        newDots = []
        newDots.append(self.dots[self.bestDot].gimmieBaby())
        newDots[0].isBest = True
        for i in range(1,len(self.dots)):
            # Select Parent based on fitness
            parent = Population.selectParent(self)

            # Get baby from them
            baby = parent.gimmieBaby()
            newDots.append(baby)
        self.dots = newDots.copy()
        self.generation += 1

    def mutateDemBabies(self,mutationRate):
        for i in range(1,len(self.dots)):
            self.dots[i].brain.mutate(mutationRate)

    def setBestDot(self):
        maxScore = 0
        maxIdx = 0
        for i in range (len(self.dots)):
            if self.dots[i].fitness > maxScore:
                maxScore = self.dots[i].fitness
                maxIdx = i
        self.bestDot = maxIdx
        self.maxFitness = maxScore

        if self.dots[self.bestDot].reachedGoal:
            self.bestSteps = self.dots[self.bestDot].brain.step

    def calculateFitness(self,Goal):
        for i in range (len(self.dots)):
            self.dots[i].calculateFitness(Goal)

    def calculateFitnessSum(self):
        self.fitnessSum = 0
        for dot in self.dots:
            self.fitnessSum += dot.fitness

    def selectParent(self):
        rand = random.uniform(0,self.fitnessSum)
        runningSum = 0
        for dot in self.dots:
            runningSum += dot.fitness
            if runningSum > rand:
                return dot
        # Should never get to this point
        print ("HALP YOU BROKE IT - natural selection & select parent")
        return None

    def allDotsDead(self):
        for i in range (len(self.dots)):
            if (not self.dots[i].dead) and (not self.dots[i].reachedGoal):
                return False
        return True

'''
Goal Class:  
A 'goal' is a simple class that can draw itself, has a position, and size.
'''
class Goal:
    def __init__(self, xx=200, yy=20):
        self.pos = PVector(xx,yy)
        self.size = 5

    def show(self, SCREEN):
        surf1 = pygame.Surface((self.size*2,self.size*2))
        surf1 = surf1.convert()
        pygame.draw.circle(surf1, RED, (self.size-1,self.size-1), self.size)
        SCREEN.blit(surf1,(self.pos.x-self.size,self.pos.y-self.size))

'''
Obstacle Class:  
A 'obstacle' is a rectangle, similar to the goal.  Given a dot, it can test if that dot has collided with itself.
'''
class Obstacle:
    def __init__(self,x=0,y=0,width=0,height=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def collision(self,dot):
        if (dot.pos.x > self.x) and (dot.pos.x < self.x + self.width) and (dot.pos.y > self.y) and (dot.pos.y < self.y + self.height):
            return True
        return False

    def show(self,SCREEN):
        surf1 = pygame.Surface((self.width,self.height))
        surf1 = surf1.convert()
        #pygame.draw.rect(surf1, BLUE, [0,0,self.width,self.height])
        surf1.fill(BLUE)
        SCREEN.blit(surf1,(self.x,self.y))
