# 1) Exercise
import pygame 

exited = False # Flag for infinite cicle
pygame.init() # Initialize video environment for pygame

screen=pygame.display.set_mode((1080,720)) # use your own screen size

screenSize = screen.get_size()          # get your screen size
background = pygame.Surface(screenSize) # use that screen size for create surface
background.fill((0,0,0))                # fill the background black 
background = background.convert()       # just copy new background into new variable to easy access it

pygame.draw.circle(background, (228, 0, 228), (int(
    screenSize[0]/2), int(screenSize[1]/2)), int(screenSize[1]/2))
# Draw pink circle, using your screen size


screen.blit(background, (0, 0)) # draw our background with pink circle in middle of screen
pygame.display.flip()  # Update picture on your screen

while not exited:  # infinite cicle that make windown does't close

    for event in pygame.event.get():     # iterate all events
        if event.type == pygame.QUIT:    # if we close window with our application
            exited = True                # make exited flag = True
