import pygame
import pymongo
from threading import Thread


class MongoClient(Thread):
    def run(self):
        # Select DB
        self.client = pymongo.MongoClient("mongodb+srv://Editor:edit@cluster0-mhy2m.mongodb.net/test?retryWrites=true&w=majority")
        self.db = self.client['TonksDB']
        self.col = self.db['Levels']


mongo_client = MongoClient()
mongo_client.start()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
export = (255, 0, 0)
post = (60, 255, 90)
GREY = (150, 150, 150)

playerCols = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)]

players = {}
for i in range(4):
    players[str(i+1)] = {
        'x': 0,
        'y': 0
    }


BRICK = (204, 78, 92)
WOOD = (181, 144, 90)

b_BRICK = (224, 98, 92)
b_WOOD = (181, 144, 90)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20

# This sets the margin between each cell
MARGIN = 5

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
grid_w = 25
grid_h = 20
for row in range(grid_h):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(grid_w):
        grid[row].append(".")  # Append a cell
# Set row 1, cell 5 to one. (Remember rows and
# column numbers start at zero.)

# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [767, 632]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Array Backed Grid")
font = pygame.font.Font('freesansbold.ttf', 25)
playerfont = pygame.font.Font('freesansbold.ttf', 16)
# Loop until the user clicks the close button.
done = False
brushState = '.'
selectedpl = -1
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
clicked = True


# -------- Main Program Loop -----------

def renderGrid():
    for row in range(grid_h):
        for column in range(grid_w):

            if grid[row][column] == "#":
                pygame.draw.rect(screen,
                                 BRICK,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])
            if grid[row][column] == "@":
                pygame.draw.rect(screen,
                                 WOOD,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])
            if grid[row][column] == ".":
                pygame.draw.rect(screen,
                                 (255, 255, 255),
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])
            for i in range(1, 5):
                if grid[row][column] == str(i):
                    pygame.draw.rect(screen,
                                     playerCols[i - 1],
                                     [(MARGIN + WIDTH) * column + MARGIN,
                                      (MARGIN + HEIGHT) * row + MARGIN,
                                      WIDTH,
                                      HEIGHT])
                    playerlabel = playerfont.render('P' + str(i), True, BLACK)
                    screen.blit(playerlabel, ((MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN))


def txt_maker(mapa, name):
    with open(name + '.txt', "w") as output:
        for line in mapa:
            for i in line:
                output.write(i)
            output.write("\n")


# Post function
def PostToDB(mylevel, name):
    topost = {'name': name, 'level': mylevel}
    mongo_client.col.insert_one(topost)
    print('Posted')


def menuName():
    global screen
    menu = True
    menufont = pygame.font.Font('freesansbold.ttf', 42)
    txt = menufont.render("Enter your level name:", True, (255, 255, 255))

    selectcol = (100, 100, 100)
    playcol = (40, 40, 40)
    level_name = ""
    while menu:
        screen.fill(BLACK)
        screen.blit(txt, (WINDOW_SIZE[0] // 2 - 250, WINDOW_SIZE[1] // 2 - 180))
        y = WINDOW_SIZE[1] // 2 - 106
        x = WINDOW_SIZE[0] // 2 - 241

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                menu = False

            if selectcol == (180, 180, 180):
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        selectcol = (100, 100, 100)
                    elif event.key == pygame.K_BACKSPACE:
                        level_name = level_name[:-1]
                    else:
                        if len(level_name) < 19:
                            level_name += event.unicode

        if pygame.mouse.get_pressed()[0] == 1:
            pos = pygame.mouse.get_pos()

            if playcol == post:
                # Export to Database button
                if x - 30 <= pos[0] <= x + 70 and y + 200 <= pos[1] <= y + 245:
                    menu = False
                    #PostToDB(grid, level_name)
                    insert = Thread(target=PostToDB, args=(grid, level_name))
                    insert.start()

                # export to file
                if x + 170 <= pos[0] <= x + 270 and y + 200 <= pos[1] <= y + 245:
                    menu = False
                    txt_maker(grid, level_name)

            # hitbox text
            if x <= pos[0] <= x + 442 and y <= pos[1] <= y + 42:
                selectcol = (180, 180, 180)
            else:
                selectcol = (100, 100, 100)

            # back
            if x + 370 <= pos[0] <= x + 470 and y + 200 <= pos[1] <= y + 245:
                menu = False

        if len(level_name) > 0:
            playcol = post
        else:
            playcol = (40, 40, 40)

        # level name text and hit box
        level_txt = menufont.render(level_name, True, WHITE)
        pygame.draw.rect(screen, selectcol, (x - 4, y - 4, 450, 50), 0)
        pygame.draw.rect(screen, (0, 0, 0), (x, y, 442, 42), 0)
        screen.blit(level_txt, (x + 8, y + 3))

        # export to text
        export_to = menufont.render('Export to:', True, WHITE)
        screen.blit(export_to, (WINDOW_SIZE[0] // 2 - 100, WINDOW_SIZE[1] // 2))

        y = y + 200
        # export to database
        pygame.draw.rect(screen, playcol, (x - 30, y, 100, 45))
        pygame.draw.rect(screen, GREY, (x - 30, y, 100, 45), 3)
        txt_base = font.render('Database', True, WHITE)
        screen.blit(txt_base, (x - 38, y + 60))

        # export to file
        pygame.draw.rect(screen, playcol, (x + 200 - 30, y, 100, 45))
        pygame.draw.rect(screen, GREY, (x + 200 - 30, y, 100, 45), 3)
        txt_to_file = font.render('File', True, WHITE)
        screen.blit(txt_to_file, (x + 200, y + 60))

        # back to editor
        pygame.draw.rect(screen, (240, 50, 50), (x + 400 - 30, y, 100, 45))
        pygame.draw.rect(screen, GREY, (x + 400 - 30, y, 100, 45), 3)
        txt_back = font.render('Back', True, WHITE)
        screen.blit(txt_back, (x + 392, y + 60))

        pygame.display.flip()


while not done:
    for event in pygame.event.get():  # User did something

        # User clicks the mouse. Get the position
        # Change the x/y screen coordinates to grid coordinates
        pos = pygame.mouse.get_pos()
        column = pos[0] // (WIDTH + MARGIN)
        row = pos[1] // (HEIGHT + MARGIN)

        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        if event.type == pygame.MOUSEBUTTONDOWN:
            if 30 <= pos[0] <= 130 and 540 <= pos[1] <= 590:
                brushState = '#'
                selectedpl = -1
                b_BRICK = (224, 98, 92)
                b_WOOD = WOOD
                print('clicked brick')

            elif 210 <= pos[0] <= 310 and 540 <= pos[1] <= 590:
                brushState = '@'
                selectedpl = -1
                b_WOOD = (230, 230, 180)
                b_BRICK = BRICK
                print('clicked wood')

            elif 390 <= pos[0] <= 490 and 540 <= pos[1] <= 590:
                brushState = '.'
                selectedpl = -1
                b_BRICK = BRICK
                b_WOOD = WOOD
                print('clicked erase')

            elif 600 <= pos[0] <= 700 and 540 <= pos[1] <= 590:
                print('clicked export')
                menuName()

            elif pos[0] > 625 or pos[1] > 500:
                b_BRICK = BRICK
                b_WOOD = WOOD

        # If left click is pressed
        if pygame.mouse.get_pressed()[0] == 1:
            try:
                if brushState in players:
                    p = players[brushState]
                    if brushState == grid[p['x']][p['y']] and pos[0] < 625:
                        grid[p['x']][p['y']] = '.'

                    grid[row][column] = brushState
                    players[brushState]['x'] = row
                    players[brushState]['y'] = column
                else:
                    grid[row][column] = brushState  # Draw

                #print("Click ", pos, "Grid coordinates: ", row, column)
            except:
                pass

    # Set the screen background
    screen.fill(BLACK)

    # players
    txt_players = font.render("Players:", True, WHITE)
    screen.blit(txt_players, (646, 4))
    for i in range(4):
        pygame.draw.rect(screen, playerCols[i], (660 + 40 * (i % 2), 40 + 40 * (i // 2), 30, 30))
        mp = pygame.mouse.get_pos()
        if (mp[0] >= 660 + 40 * (i % 2) <= 690 + 40 * (i % 2)) and (40 + 40 * (i // 2) <= mp[1] <= 70 + 40 * (i // 2)):
            if pygame.mouse.get_pressed()[0]:
                selectedpl = i
                brushState = str(i + 1)

        if selectedpl == i:
            pygame.draw.rect(screen, WHITE, (660 + 40 * (i % 2), 40 + 40 * (i // 2), 30, 30), 2)

        ptxt = playerfont.render("P" + str(i + 1), True, BLACK)

        screen.blit(ptxt, (660 + 4 + 40 * (i % 2), 40 + 8 + 40 * (i // 2)))

    # Brick
    txt_brick = font.render("Brick", True, WHITE)
    pygame.draw.rect(screen, b_BRICK, (30, 540, 100, 50))
    screen.blit(txt_brick, (50, 515))
    pygame.draw.rect(screen, GREY, (30, 540, 100, 50), 3)

    # Wood
    pygame.draw.rect(screen, b_WOOD, (210, 540, 100, 50))
    txt_plank = font.render("Plank", True, WHITE)
    screen.blit(txt_plank, (226, 515))
    pygame.draw.rect(screen, GREY, (210, 540, 100, 50), 3)

    # Erase
    pygame.draw.rect(screen, WHITE, (390, 540, 100, 50))
    pygame.draw.rect(screen, GREY, (390, 540, 100, 50), 3)
    txt_erase = font.render("Erase", True, WHITE)
    screen.blit(txt_erase, (405, 515))

    # Export
    pygame.draw.rect(screen, post, (600, 540, 100, 50))
    txt_export = font.render("Export", True, WHITE)
    screen.blit(txt_export, (610, 515))
    pygame.draw.rect(screen, GREY, (600, 540, 100, 50), 3)

    renderGrid()
    # Draw the grid
    # Limit to 30 frames per second
    clock.tick(30)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
