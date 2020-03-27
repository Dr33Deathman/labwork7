# 4) Exercise
import pygame 

exited = False # Flag for infinite cicle
pygame.init() # Initialize video environment for pygame

screen = pygame.display.set_mode((1080, 720))  # use your own screen size

screenSize = screen.get_size()          # get your screen size
background = pygame.Surface(screenSize) # use that screen size for create surface
background.fill((0,0,0))                # fill the background black 
background = background.convert()       # just copy new background into new variable to easy access it


pygame.draw.arc(background, (228, 228, 228), (0, 0, screenSize[0]*2, (screenSize[1]*2.1)), 0, 3.14)
# draw an arc from the topright to the lower-left corner on the background

screen.blit(background, (0, 0))  # draw on screen our background with arc
pygame.display.flip()  # Update picture on your screen


while not exited: # infinite cicle that make windown does't close
        
    for event in pygame.event.get():     # iterate all events 
        if event.type == pygame.QUIT:    # if we close window with our application
            exited = True                # make exited flag = True
