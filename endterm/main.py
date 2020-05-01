from enum import Enum
from threading import Thread
import pygame
import random
import pymongo
import colorsys
import os

pygame.init()
screen_width = 800
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
FPS = 60

pygame.display.set_caption("Пажылые танки")
################################
# FLAG
ROFL_mode = True
################################

################################
# images
################################
wall_brick = pygame.image.load('assets/img/wall_brick.png')
wall_plank = pygame.image.load('assets/img/wall_plank.png')
tank_base_0 = pygame.image.load('assets/img/tank_base_1.png')
tank_base_1 = pygame.image.load('assets/img/tank_base_2.png')


################################

###############################
# pymongo


class MongoClient(Thread):
    def run(self):
        self.levels = []
        client = pymongo.MongoClient(
            "mongodb+srv://Player:guest@cluster0-mhy2m.mongodb.net/test?retryWrites=true&w=majority")
        db = client['TonksDB']
        col = db['Levels']

        for i in col.find({}, {'_id': 0}):
            self.levels.append(i)

        # print(self.levels)


mongo_client = MongoClient()
mongo_client.start()
################################

################################
# sounds
shoot_sounds = []
for i in range(6):
    shoot_sounds.append(pygame.mixer.Sound(f'assets/sounds/shoot_{i}.wav'))

################################

################################
# fonts
large_font = pygame.font.SysFont("comicsansms", 50)
medium_font = pygame.font.Font('freesansbold.ttf', 32)
small_font = pygame.font.Font('freesansbold.ttf', 23)


#################################


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Tank:

    def __init__(self, x, y, speed, bullet_limit, color, bullet_speed, health, d_right=pygame.K_RIGHT,
                 d_left=pygame.K_LEFT,
                 d_up=pygame.K_UP, d_down=pygame.K_DOWN, fire=pygame.K_SPACE):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.width = 32
        self.direction = Direction.RIGHT
        self.fire_key = fire
        self.bullet_limit = bullet_limit
        self.bullet_list = []
        self.bullet_speed = bullet_speed
        self.first_img = True
        self.health = health
        self.max_health = health

        self.KEY = {d_right: Direction.RIGHT, d_left: Direction.LEFT,
                    d_up: Direction.UP, d_down: Direction.DOWN}

        self.tank_texture = pygame.Surface((self.width, self.width))
        pygame.draw.rect(self.tank_texture, color, (0, 0, 32, 32))

    def draw(self):
        texture = self.tank_texture
        texture.set_colorkey((255, 255, 255))

        if self.first_img:
            texture.blit(tank_base_0, (0, 0))
            self.first_img = False
        else:
            texture.blit(tank_base_1, (0, 0))
            self.first_img = True

        if self.direction == Direction.RIGHT:
            texture = pygame.transform.rotate(texture, -90)

        if self.direction == Direction.LEFT:
            texture = pygame.transform.rotate(texture, 90)

        if self.direction == Direction.DOWN:
            texture = pygame.transform.rotate(texture, 180)

        screen.blit(texture, (round(self.x), round(self.y)))

        drawhealthbar(round(self.x), round(self.y - 11), self.width, 8, self.health, self.max_health, (150, 150, 150))

    def change_direction(self, direction):
        self.direction = direction

    def move(self, sec):
        can_move = True

        for wall in walls:
            if is_bump(self, wall.x, wall.y, wall.x + wall.width, wall.y + wall.width):
                can_move = False

        if can_move:
            for tank in tanks:
                if is_bump(self, tank.x, tank.y, tank.x + tank.width, tank.y + tank.width):
                    can_move = False

        if can_move:
            if self.direction == Direction.LEFT:
                self.x -= self.speed * sec
            if self.direction == Direction.RIGHT:
                self.x += self.speed * sec
            if self.direction == Direction.UP:
                self.y -= self.speed * sec
            if self.direction == Direction.DOWN:
                self.y += self.speed * sec

        if self.x < -self.width:
            self.x = screen_width
        if self.x > screen_width:
            self.x = 0
        if self.y < -self.width:
            self.y = screen_height
        if self.y > screen_height:
            self.y = -self.width

    def fire(self):
        if len(self.bullet_list) < self.bullet_limit:
            if ROFL_mode:
                shoot_sounds[5].play()
            else:
                shoot_sounds[random.randint(0, 4)].play()
            self.bullet_list.append(
                Bullet(self.x + self.width // 2 + 1, self.y + self.width // 2 + 1, self.bullet_speed, self.color,
                       self.direction, self.bullet_list))


class Bullet:

    def __init__(self, x, y, speed, color, direction, owner_bullets):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.direction = direction
        self.owner = owner_bullets

    def move(self, sec):
        if self.direction == Direction.LEFT:
            self.x -= self.speed * sec
        if self.direction == Direction.RIGHT:
            self.x += self.speed * sec
        if self.direction == Direction.UP:
            self.y -= self.speed * sec
        if self.direction == Direction.DOWN:
            self.y += self.speed * sec
        self.draw()

        if self.x > screen_width or self.x < 0 or self.y > screen_height or self.y < 0:
            self.owner.remove(self)
            del self
            return

        for h in range(len(walls)):
            if (walls[h].x <= self.x <= walls[h].x + walls[h].width and
                    walls[h].y <= self.y <= walls[h].y + walls[h].width):

                if not walls[h].durable: walls[h].remove()
                self.remove()
                return

    def draw(self):
        pygame.draw.circle(screen, self.color, (round(self.x), round(self.y)), 3)

    def remove(self):
        self.owner.remove(self)
        del self


class Wall:
    def __init__(self, x, y, width, durable=False):
        self.x = x
        self.y = y
        self.width = width
        self.durable = durable
        self.hit_box = pygame.Rect(self.x, self.y, width, width)

    def draw(self):
        if self.durable:
            screen.blit(wall_brick, (self.x, self.y))
        else:
            screen.blit(wall_plank, (self.x, self.y))

    def remove(self):
        walls.remove(self)
        del self


def is_bump(a: Tank, x1, y1, x2, y2) -> bool:
    if a.direction == Direction.LEFT:
        return x1 < a.x < x2 and (y1 < a.y + a.width - 2 < y2 or y1 < a.y + 2 < y2)

    if a.direction == Direction.RIGHT:
        return x1 < a.x + a.width < x2 and (y1 < a.y + a.width - 2 < y2 or y1 < a.y + 2 < y2)

    if a.direction == Direction.UP:
        return y1 < a.y < y2 and (x1 < a.x + 2 < x2 or x1 < a.x + a.width - 2 < x2)

    if a.direction == Direction.DOWN:
        return y1 < a.y + a.width < y2 and (x1 < a.x + 2 < x2 or x1 < a.x + a.width - 2 < x2)


def drawhealthbar(x, y, w, h, value, max_value, fill_bg):
    if value <= 0:
        return
    col = colorsys.hsv_to_rgb(((value / max_value) * 128) / 360, 1.0, 1.0)
    if (fill_bg):
        pygame.draw.rect(screen, (180, 180, 180), (x - 1, y - 1, w + 2, h + 2), 0)
    pygame.draw.rect(screen, (col[0] * 255, col[1] * 255, col[2] * 255), (x, y, int(w * (value / max_value)), h), 0)


def get_from_DB(name):
    request = col.find_one({'name': name})
    if request is None:
        output = []
        print('Level Not Found')
    else:
        output = request['level']
    return output


def read_level(level=[]):
    temp_list = ""
    if level == []:
        with open(if_no_level, 'r+', encoding='utf-8') as map:
            for i in map:
                temp_list += i.strip()

    level_width_in_tiles = screen_width // 32
    j = 0

    for i in level:
        for h in i:
            temp_list += h.strip()

    for i in range(len(temp_list)):

        if i % level_width_in_tiles == 0 and i != 0:
            j += 1

        if temp_list[i] == "#":
            walls.append(Wall((i % level_width_in_tiles) * 32, j * 32, 32, True))
        elif temp_list[i] == "@":
            walls.append(Wall((i % level_width_in_tiles) * 32, j * 32, 32, False))


level_names = []
walls = []


def get_local_levels():
    x = os.scandir(os.getcwd() + '/assets/levels')
    for i in x:
        if i.name[-4:] == '.txt':
            level_names.append(i.name[:-4])


get_local_levels()
print(level_names)
level = []  # get_from_DB('Pac-Man')
if_no_level = 'assets/levels/2_level.txt'
read_level(level)
main_menu = True
mainloop = True

SELECTED = (156, 150, 145)
NOT_SELECTED = (74, 72, 70)
GREEN = (60, 255, 90)
TANK_COL = (60, 255, 90)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

img_width, img_height = tank_base_0.get_rect().width, tank_base_0.get_rect().height


def create_button(text, button_x, button_y, font, txt_col, colour, static_w=0, static_h=0, color_per=(74, 72, 70)):
    global screen

    txt = font.render(str(text), True, txt_col)
    x, y, w, h = txt.get_rect()

    if static_w and static_h:
        pygame.draw.rect(screen, colour, (button_x, button_y, static_w, static_h))
        pygame.draw.rect(screen, color_per, (button_x, button_y, static_w, static_h), 2)
        screen.blit(txt, (int(button_x + static_w // 2 - w // 2), int(button_y + 2 + static_h // 2 - h // 2)))
    elif static_w:
        pygame.draw.rect(screen, colour, (button_x, button_y, static_w, h + 4))
        pygame.draw.rect(screen, color_per, (button_x, button_y, static_w, h + 4), 2)
        screen.blit(txt, (int(button_x + static_w // 2 - w // 2), int(button_y + 2)))
    elif static_h:
        pygame.draw.rect(screen, colour, (button_x, button_y, w + 2, static_h))
        pygame.draw.rect(screen, color_per, (button_x, button_y, w + 2, static_h), 2)
        screen.blit(txt, (int(button_x + 2), int(button_y + 2 + static_h // 2 - h // 2)))
    else:
        pygame.draw.rect(screen, colour, (button_x, button_y, w + 4, h + 4))
        pygame.draw.rect(screen, color_per, (button_x, button_y, w + 4, h + 4), 2)
        screen.blit(txt, (int(button_x + 2), int(button_y + 2)))


def create_colour(h):
    colour = colorsys.hsv_to_rgb(h / 360, 1.0, 1.0)
    return colour[0] * 255, colour[1] * 255, colour[2] * 255


while main_menu:
    screen.fill(BLACK)
    milliseconds = clock.tick(FPS)

    texture = pygame.Surface((img_width, img_height))
    texture.set_colorkey(WHITE)
    pygame.draw.rect(texture, TANK_COL, tank_base_0.get_rect())

    texture.blit(tank_base_0, (0, 0))

    screen.blit(texture, (screen_width - 150, 120))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = main_menu = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                main_menu = False

    # Pick color Text
    txt = large_font.render('Pick your colour', True, WHITE)
    screen.blit(txt, (screen_width // 2 - txt.get_rect().width // 2, 10))

    # Colour Bar
    for i in range(180):
        pygame.draw.rect(screen, create_colour(i * 2), (28 + 3 * i, 120, 5, 25), 0)

    # Select colour
    if pygame.mouse.get_pressed()[0] == 1:
        pos = pygame.mouse.get_pos()
        # color picker
        if 28 <= pos[0] <= 28 + 3 * 180 and 120 <= pos[1] <= 145:
            h = (pos[0] - 28) / 1.5
            TANK_COL = create_colour(h)
        # play , , 120, 70
        if screen_width // 2 - 40 <= pos[0] <= screen_width // 2 + 80 and screen_height - 100 <= pos[
            1] <= screen_height - 30:
            main_menu = False

    txt = medium_font.render('Choose map', True, WHITE)
    screen.blit(txt, (screen_width // 2 - txt.get_rect().width // 2, 160))

    # Local lvl
    txt = medium_font.render('Local levels:', True, WHITE)
    screen.blit(txt, (70, 200))

    # Database lvl
    txt = medium_font.render('Database levels:', True, WHITE)
    screen.blit(txt, (screen_width - txt.get_rect().width - 30, 200))

    for i in range(len(level_names)):
        create_button(level_names[i], 50, 240 + i * 29, small_font, WHITE, (77, 132, 168), static_w=200)

    if mongo_client.levels:
        for i in range(len(mongo_client.levels)):
            name = mongo_client.levels[i]['name']
            create_button(name, screen_width - 270, 240 + i * 29, small_font, WHITE, (77, 132, 168), static_w=200)

    # Play
    create_button('Play', screen_width // 2 - 40, screen_height - 100, medium_font, WHITE, GREEN, static_w=120,
                  static_h=70)
    pygame.display.flip()


tank1 = Tank(500, 500, 100, 5, TANK_COL, 200, 10, fire=pygame.K_SPACE)
tank2 = Tank(100, 100, 100, 5, (33, 196, 22), 200, 5, pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s, pygame.K_f)
tank3 = Tank(200, 200, 100, 5, (88, 86, 176), 200, 3, pygame.K_l, pygame.K_j, pygame.K_i, pygame.K_k, pygame.K_u)
tanks = [tank1, tank2, tank3]


while mainloop:
    screen.fill((255, 255, 255))
    milliseconds = clock.tick(FPS)
    seconds = milliseconds / 1000
    a = b = c = 0
    tank_hit = False

    for wall in walls:
        wall.draw()

    for i in range(len(tanks)):
        tanks[i].draw()  # рисуем все танки
        tanks[i].move(seconds)

        for bullet in tanks[i].bullet_list:
            bullet.move(seconds)

        for j in range(len(tanks)):
            if i != j:
                for h in range(len(tanks[i].bullet_list)):
                    if (tanks[j].x <= tanks[i].bullet_list[h].x <= tanks[j].x + tanks[j].width) and (
                            tanks[j].y <= tanks[i].bullet_list[h].y <= tanks[j].y + tanks[j].width):
                        a, b, c = i, j, h  # проверяем попал ли какой-то танк в другой, перебирая все пули
                        tank_hit = True

    if tank_hit:
        del tanks[a].bullet_list[c]
        tanks[b].health -= 1
        if tanks[b].health == 0:
            del tanks[b]
        tank_hit = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False

            for tank in tanks:
                if event.key in tank.KEY.keys():
                    tank.change_direction(tank.KEY[event.key])
                if event.key == tank.fire_key:
                    tank.fire()

    pygame.display.flip()

pygame.quit()
