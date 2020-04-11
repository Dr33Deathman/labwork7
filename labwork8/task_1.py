#                   Lab 8
import pygame 

running = True # Flag for infinite cicle
pygame.init() # Initialize video environment for pygame

screen=pygame.display.set_mode((1080,720))   # use your own screen size

screen_size = screen.get_size()              # get your screen size
background = pygame.Surface(screen_size)     # use that screen size for create surface
background.fill((255, 255, 255))             # fill the background with white color 
background = background.convert()            # just copy new background into new variable to easy access it

circle_x = screen_size[0]//2 # start in center of your screen
circle_y = screen_size[1]//2        

ball_speed = 20
radius = 25 # our ball radius
FPS = 60 # desired framerate in frames per second. 
clock = pygame.time.Clock() # Initializing clock for usin specific frame 

while running:  # infinite cicle that make windown does't close

    milliseconds = clock.tick(FPS) # do not go faster than this framerate

    for event in pygame.event.get():     # iterate all events
        if event.type == pygame.QUIT:    # if we close window with our application
            running = False              # make your program turn off

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False     # make your program turn off, when you press ESCAPE Button


            # version with 1 press == 1 move

            # if event.key == pygame.K_RIGHT and circle_x + radius < screen_size[0]:   # Checking pressed button and screen borders for moving ball
            #     circle_x += ball_speed        # move to the right
            # if event.key == pygame.K_LEFT and circle_x > radius:
            #     circle_x -= ball_speed        # move to the left
            # if event.key == pygame.K_UP and circle_y > radius:
            #     circle_y -= ball_speed        # goin up
            # if event.key == pygame.K_DOWN and circle_y + radius < screen_size[1]: 
            #     circle_y += ball_speed        # goin down


    # version whith holding pressed key

    keys = pygame.key.get_pressed() # grab all pressed keys
    # it return tuple with in information, which keys are pressed

    if keys[pygame.K_RIGHT] and circle_x + radius < screen_size[0]: # Checking pressed button and screen borders for moving ball
        circle_x += ball_speed      # move to the right
    if keys[pygame.K_LEFT] and circle_x > radius:
        circle_x -= ball_speed      # move to the left
    if keys[pygame.K_UP] and circle_y > radius:
        circle_y -= ball_speed      # goin up
    if keys[pygame.K_DOWN] and circle_y + radius < screen_size[1]:
        circle_y += ball_speed      # goin down


    screen.blit(background, (0, 0)) # draw our background
    pygame.draw.circle(screen, (176, 26, 26), (circle_x, circle_y), radius)  # draw our red circle 
    pygame.display.flip()  # Update picture on your screen
