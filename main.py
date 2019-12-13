# Rylan Hunter
# ECEN 689 - Final Project Code

# THIS IS THE MAIN FILE FOR THE SMART_ROCKETS PROJECT
# To run, you will need to install pygame with the command 'python -m pip install pygame'
# It relies on two supporting files: PVector.py, and SmartRockets.py

import pygame
from pygame.locals import *
import sys
from SmartRockets import Population, Goal, Obstacle

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

FPS = 60
SCREENWIDTH  = 400
SCREENHEIGHT = 400

def main():
    # Initialize pygame
    global SCREEN, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Smart Dots')

    # Define background
    background = pygame.Surface(SCREEN.get_size())
    background = background.convert()
    background.fill(BLACK)

    # Define a population of dots, and where they start
    test = Population(1000, SCREENWIDTH/2,SCREENHEIGHT-10)

    # Define goal location
    goal = Goal(SCREENWIDTH/2,10)

    # Define obstacles array -> [X,Y,width,height]
    obstacles = []
    # Add specific obstacles
    obstacle = Obstacle(100,125,200,20)
    obstacles.append(obstacle)

    # Print generation number to screen & console
    print("Generation: ", test.generation)
    font = pygame.font.Font(None, 36)
    genDisp = font.render("Gen: "+str(test.generation), 1, WHITE)
    text_width, text_height = font.size("Gen: "+str(test.generation))

    # Main Loop - check for exit condition, else process population
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        # Draw background, obstacles, goal
        SCREEN.blit(background,(0,0))
        goal.show(SCREEN)
        for obs in obstacles:
            obs.show(SCREEN)

        # Population
        if test.allDotsDead():
            # Genetic Algorithm
            test.calculateFitness(goal)
            test.naturalSelection() #also prints out stats
            test.mutateDemBabies(0.01)
            print("Generation: ", test.generation)

            # Change text to display new generation number to screen
            font = pygame.font.Font(None, 36)
            genDisp = font.render("Gen: "+str(test.generation), 1, WHITE)
            text_width, text_height = font.size("Gen: "+str(test.generation))
        else:
            # Update dots (progress them forward in time), then show the new locations
            test.update(SCREENWIDTH,SCREENHEIGHT,goal,obstacles)
            test.show(SCREEN)

        # Display Generation Number on screen
        SCREEN.blit(genDisp, (SCREENWIDTH-text_width-10,20))
        pygame.display.update()
        FPSCLOCK.tick(FPS)

    # End Main Function

# Call main()
if __name__ == "__main__":
    main()
