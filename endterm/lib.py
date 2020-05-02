import pygame
from enum import Enum

screen_width = 800
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Button:

    def __init__(self, text, button_x, button_y, font, txt_col, colour, func, static_w, static_h,
                 color_per=(74, 72, 70)):
        global screen
        self.text = text
        self.button_x = button_x
        self.button_y = button_y
        self.font = font
        self.txt = font.render(str(text), True, txt_col)
        self.txt_col = txt_col
        self.colour = colour
        self.color_per = color_per
        self.run = func
        x, y, w, h = self.txt.get_rect()
        self.button_w = static_w
        self.button_h = static_h
        self.txt_x = button_x + static_w // 2 - w // 2
        self.txt_y = button_y + static_h // 2 - h // 2

    def draw(self):
        self.txt = self.font.render(str(self.text), True, self.txt_col)
        pygame.draw.rect(screen, self.colour, (self.button_x, self.button_y, self.button_w, self.button_h))
        pygame.draw.rect(screen, self.color_per, (self.button_x, self.button_y, self.button_w, self.button_h), 2)
        screen.blit(self.txt, (self.txt_x, self.txt_y))


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