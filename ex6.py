# 6) Exercise
import pygame 

exited = False # Flag for infinite cicle
pygame.init() # Initialize video environment for pygame

screen = pygame.display.set_mode((1080, 720))  # use your own screen size

screenSize = screen.get_size()          # get your screen size
background = pygame.Surface(screenSize) # use that screen size for create surface
background.fill((0,0,0))                # fill the background black 
background = background.convert()       # just copy new background into new variable to easy access it


for point in range(0, 641, 64):  # range(start, stop, step)
    pygame.draw.line(background, (228, point//4, 228), (0, 0), (screenSize[0]//2, point), 1)
    # from left top corner
for point in range(0, 641, 64):
    pygame.draw.line(background, (point//4, 0, 228), (screenSize[0], 0), (screenSize[0]//2, point), 1)
    # from right top corner
for point in range(0, 641, 64):
    pygame.draw.line(background, (228, 0, point//4), (0, screenSize[1]), (screenSize[0]//2, point), 1)
    # from left bot corner
for point in range(0, 641, 64):
    pygame.draw.line(background, (point//4, 255 - point//4, point // 4), (screenSize[0], screenSize[1]), (screenSize[0]//2, point), 1)
    # from right bot corner


screen.blit(background, (0, 0))  # draw on screen our background with colorful pretty pattern
pygame.display.flip()  # Update picture on your screen


while not exited: # infinite cicle that make windown does't close
        
    for event in pygame.event.get():     # iterate all events 
        if event.type == pygame.QUIT:    # if we close window with our application
            exited = True                # make exited flag = True

