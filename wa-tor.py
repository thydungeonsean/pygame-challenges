import pygame
from pygame.locals import *
import os
from random import *


SCREENWIDTH = 1100
SCREENHEIGHT = 700
FPS = 6
FPS_LIM = (1, 60)
PAUSE = False

FONT = None

WATER = (0, 160, 230)
RED = (255, 0 , 0)
YELLOW = (255, 240, 0)
BLACK = (0, 0, 0)


class Wa_Tor(object):
    
    def __init__(self, w=100, h=50, fish=500, sharks=500, use_image=True):
        
        self.w = w
        self.h = h
        
        self.map = [[0 for y in range(self.h)] for x in range(self.w)]
        
        self.shark_image = pygame.image.load('shark.png')
        self.shark_image = self.shark_image.convert()
        self.fish_image = pygame.image.load('fish.png')
        self.fish_image = self.fish_image.convert()
        self.fish_rect = self.fish_image.get_rect()
        
        self.use_image = use_image
        
        if self.use_image:        
            self.tile_w = self.fish_rect.w
            self.tile_h = self.fish_rect.h
        else:
            self.tile_w = 3
            self.tile_h = 3
            self.fish_rect = pygame.Rect((0, 0), (3, 3))
        
        self.image = pygame.Surface((self.w*self.tile_w, self.h*self.tile_h))
        self.rect = self.image.get_rect()
        self.image.fill(WATER)
        self.image = self.image.convert()
        
        self.fish = fish
        self.sharks = sharks
        self.chronon = 0
        
        self.graph = Graph(self)
        
        self.fish_grow_threshold = 10
        self.fish_energy = 3
        self.shark_grow_threshold = 8
        self.shark_energy_cap = 10
        
        self.seed_fish()
    
    def seed_fish(self):
    
        coords = []
        
        for y in range(self.h):
            for x in range(self.w):
                coords.append((x, y))
        
        print len(coords)
        print self.fish,
        print self.sharks
    
        selection = sample(coords, self.fish+self.sharks)
        fish_coords = selection[:self.fish]
        shark_coords = selection[self.fish+1:]
        
        for x, y in fish_coords:
            self.map[x][y] = randint(1, self.fish_grow_threshold-1)
        for x, y in shark_coords:
            new_shark = (self.fish_energy, 1)
            self.map[x][y] = new_shark
    
    def draw(self):
    
        self.image.fill(WATER)
        for y in range(self.h):
            for x in range(self.w):
                if self.is_shark((x, y)):
                    self.draw_shark((x, y))
                elif self.is_fish((x, y)):
                    self.draw_fish((x, y))
        
        return self.image, self.rect
        
    def draw_shark(self, (x, y)):
        self.fish_rect.topleft = (x*self.tile_w, y*self.tile_h)
        if not self.use_image:
            pygame.draw.rect(self.image, RED, self.fish_rect)
        else:
            self.image.blit(self.shark_image, self.fish_rect)
        
    def draw_fish(self, (x, y)):
        self.fish_rect.topleft = (x*self.tile_w, y*self.tile_h)
        if not self.use_image:
            pygame.draw.rect(self.image, YELLOW, self.fish_rect)
        else:
            self.image.blit(self.fish_image, self.fish_rect)
        
    def is_fish(self,(x,y)):
        
        if isinstance(self.map[x][y], int) and self.map[x][y] > 0:
            return True
        return False
        
    def is_shark(self, (x, y)):
    
        if isinstance(self.map[x][y], tuple):
            return True
        return False
        
    def update(self):
        
        self.chronon += 1
        
        fish = []
        sharks = []
        
        for y in range(self.h):
            for x in range(self.w):
                if self.is_shark((x, y)):
                    sharks.append((x, y))
                elif self.is_fish((x, y)):
                    fish.append((x, y))
                    
        self.update_fish(fish)
        self.update_sharks(sharks)
        
        self.graph.update()
        
    def update_fish(self, fish):
        
        for x, y in fish:
            adj = self.get_free_adj_spot((x, y))
            if not adj:
                self.map[x][y] += 1
                continue
            if self.map[x][y] >= self.fish_grow_threshold:
                self.map[x][y] = 1
                nx, ny = choice(adj)
                self.map[nx][ny] = 1
                self.fish += 1
            else:
                nx, ny = choice(adj)
                self.map[nx][ny] = self.map[x][y] + 1
                self.map[x][y] = 0
        
    def update_sharks(self, sharks):
        
        for x, y in sharks:
            old = self.map[x][y]  # status of shark before move
            adj_fish = self.get_adj_fish((x, y))  # try to eat
            if adj_fish:
                
                nx, ny = choice(adj_fish)
                new_energy = old[0] + self.fish_energy - 1
                if self.shark_energy_cap is not None:
                    if new_energy > self.shark_energy_cap:
                        new_energy = self.shark_energy_cap
                
                new = (new_energy, old[1]+1)
                self.map[nx][ny] = new
                self.fish -= 1
                
            elif not adj_fish:  # no food, move instead
                adj = self.get_free_adj_spot((x, y))
                if not adj:  # too crowded to move
                    nx, ny = x, y
                else:
                    nx, ny = choice(adj)
                new = (old[0]-1, old[1]+1)
                if new[0] <= 0:  # out of energy, starve
                    self.map[x][y] = 0
                    self.sharks -= 1
                    continue
                self.map[nx][ny] = new
                    
            if self.map[nx][ny][1] == self.shark_grow_threshold and (x, y) != (nx, ny):
                self.sharks += 1
                self.map[x][y] = (self.fish_energy, 1)
                post_birth = (new[0], 1)
                self.map[nx][ny] = post_birth
            else:
                self.map[x][y] = 0
                
    def get_adj_spot(self, (sx, sy)): 
    
        raw_adj = [(sx + 1, sy), (sx - 1, sy), (sx, sy + 1), (sx, sy - 1)]
        adj = []
        
        for x, y in raw_adj:
            if y < 0 or y == self.h:
                continue
            if x < 0:
                x = self.w - 1
            elif x == self.w:
                x = 0
            adj.append((x, y))
            
        return adj
    
    def get_free_adj_spot(self, (sx, sy)):
        
        raw_adj = self.get_adj_spot((sx, sy))
        adj = []
        for x, y in raw_adj: 
            if self.map[x][y] == 0:
                adj.append((x, y))
                
        return adj
        
    def get_adj_fish(self, (sx, sy)):
        
        raw_adj = self.get_adj_spot((sx, sy))
        adj = []
        for x, y in raw_adj: 
            if self.is_fish((x, y)):
                adj.append((x, y))
                
        return adj

        
class Graph(object):
    
    def __init__(self, sim):
        
        self.sim = sim
        
        self.fish_data = {}
        self.shark_data = {}
        
        self.w = self.sim.w * self.sim.tile_w
        self.h = SCREENHEIGHT - self.sim.h * self.sim.tile_h
        
        self.image = pygame.Surface((self.w, self.h))
        self.image.fill(BLACK)
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, self.sim.h* self.sim.tile_h)
        
        self.red_dot = pygame.Surface((1, 1))
        self.red_dot.fill(RED)
        self.red_dot = self.red_dot.convert()
        self.dot_rect = self.red_dot.get_rect()
        
        self.yellow_dot = pygame.Surface((1, 1))
        self.yellow_dot.fill(YELLOW)
        self.yellow_dot = self.yellow_dot.convert()
        
    def convert_to_pixel(self, value):
        c = (value / 10000.0) * self.h
        return c
        
    def draw_fish(self, chronon):
        x = chronon
        y = self.fish_data[chronon]
        self.dot_rect.topleft = (x, y)
        self.image.blit(self.yellow_dot, self.dot_rect)
    
    def draw_shark(self, chronon):
        x = chronon
        y = self.shark_data[chronon]
        self.dot_rect.topleft = (x, y)
        self.image.blit(self.red_dot, self.dot_rect)
    
    def update(self):
        
        print "fish: %s, sharks: %s" % (self.sim.fish, self.sim.sharks)
        
        self.fish_data[self.sim.chronon] = self.convert_to_pixel(self.sim.fish)
        self.shark_data[self.sim.chronon] = self.convert_to_pixel(self.sim.sharks)
        
        self.draw_shark(self.sim.chronon)
        self.draw_fish(self.sim.chronon)
        
    def draw(self):
        return self.image, self.rect
        

def draw_demo(screen, sim):
    
    i, r = sim.draw()
    screen.blit(i, r)
    
    i, r = sim.graph.draw()
    screen.blit(i, r)


def write(text, color):
    
    i = FONT.render(text, False, color)
    r = i.get_rect()

    return i, r


def pause(clock):
    
    global PAUSE
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit() 
            
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
                elif event.key == K_SPACE:
                    PAUSE = False
                    return
        clock.tick(FPS)
    
    
def increment_speed():
    global FPS, FPS_LIM
    if FPS <= 6:
        FPS += 1
    else:
        FPS += 5
    if FPS > FPS_LIM[1]:
        FPS = FPS_LIM[1]


def decrement_speed():
    global FPS, FPS_LIM
    if FPS <= 6:
        FPS -= 1
    else:
        FPS -= 5
    if FPS < FPS_LIM[0]:
        FPS = FPS_LIM[0]
    
    
def handle_input():
        
    global PAUSE
        
    for event in pygame.event.get():
        if event.type == QUIT:
            exit() 
        
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
            elif event.key == K_SPACE:
                PAUSE = True
            elif event.key == K_PERIOD:
                increment_speed()
            elif event.key == K_COMMA:
                decrement_speed()

            
def set_screen():
    
    screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Wa-Tor')
    
    return screen

    
def main():
    
    global FONT
    
    os.environ["SDL_VIDEO_CENTERED"] = '1'
    pygame.init()
    
    clock = pygame.time.Clock()
    FONT = pygame.font.Font('oryxtype.ttf', 32)
    
    screen = set_screen()
    sim = Wa_Tor()
    
    while True:
        
        sim.update()
        
        draw_demo(screen, sim)
        handle_input()
        
        if PAUSE:
            pause(clock)
        
        pygame.display.update()
        
        clock.tick(FPS)
        
main()