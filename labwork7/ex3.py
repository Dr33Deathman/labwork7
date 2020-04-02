# 3) Exercise
import pygame
import math
import itertools

exited = False  # Flag for infinite cicle
pygame.init()  # Initialize video environment for pygame

screen = pygame.display.set_mode((1080, 720))  # use your own screen size

screenSize = screen.get_size()          # get your screen size
background = pygame.Surface(screenSize) # use that screen size for create surface
background.fill((0, 0, 0))                # fill the background black 
background = background.convert()       # just copy new background into new variable to easy access it


# just simple math :DDDDDDD
vertices = 17
angle = 360 / vertices  # angle for 1 vertice
radius = round(screenSize[1]/2 - 20)  # radius of pentagram
coords = [(round(screenSize[0]/2 + radius*math.cos(math.radians(90+n*angle))),
           round(screenSize[1]/2 + radius*math.sin(math.radians(90+n*angle)))) for n in range(vertices)]
# coordinates by math formula

# a = list(itertools.permutations(coords))  # all permutation of coordinates

# a = [(100, 300), (200, 60), (300, 300), (75, 150), (325, 150), (100, 300)]
# pygame.draw.polygon(background, (0,180,0), ((100, 300), (200, 60), (300, 300), (75, 150), (325, 150)), 5)  # by using polygon
# for i in range(1, len(a)):
#     pygame.draw.line(background, (255,255,255), a[i-1], a[i], 1)

for j in range(0, len(coords)):     # More faster algorithm
    for i in range(0, len(coords)):
        pygame.draw.line(background, (102, 0, 0), coords[i], coords[j], 4)

# for i in a:  # Draw all permutations
#     for j in range(1, len(i)):
#         pygame.draw.line(background, (102, 0, 0), i[j-1], i[j], 5)


# draw our background with pentagram
screen.blit(background, (0, 0))
pygame.display.flip()  # Update picture on your screen


while not exited:  # infinite cicle that make windown does't close

    for event in pygame.event.get():     # iterate all events
        if event.type == pygame.QUIT:    # if we close window with our application
            exited = True                # make exited flag = True
