import pygame
from pygame.locals import *
import os
from random import *


SCREENWIDTH = 1200
SCREENHEIGHT = 650
FPS = 6
FPS_LIM = (1, 60)
PAUSE = False

FONT = None

WATER = (0, 160, 230)
RED = (255, 0 , 0)
YELLOW = (255, 240, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Menu(object):
    
    def __init__(self, screen):
        
        self.screen = screen
        
        self.stats = { 'fish': 1000, 'sharks':100, 'fish grow': 4, 'shark grow': 5, 'fish energy': 3,'shark energy cap': None}
        
        self.menu_codex = {0:'fish', 1:'sharks', 2:'fish grow', 3:'shark grow', 4:'fish energy', 5:'shark energy cap'}
        
        self.menu = ['number of fish', 'number of sharks', 'fish reproduction threshold', 'shark reproduction threshold', 'fish energy', 'shark energy limit']
        self.cursor = 0
        
        self.hold_right = 0
        self.hold_left = 0
        
        self.clock = pygame.time.Clock()
    
    def reset(self):
        self.cursor = 0
    
    def clear_screen(self):
    
        self.screen.fill(BLACK)
        
    def main_menu(self):
        
        update = True
        
        while True:
            
            if update:
                self.draw_menu()
                update = False
                
            self.clock.tick(60)
            
            update = self.handle_input()
            
            if update == "complete":
                return
                           
    def cursor_up(self):
        self.cursor -= 1
        if self.cursor < 0:
            self.cursor = 5
    
    def cursor_down(self):
        self.cursor += 1
        if self.cursor > 5:
            self.cursor = 0
            
    def cursor_right(self, speed=1):
        
        if self.cursor < 2:

            self.stats[self.menu_codex[self.cursor]] += speed
            self.check_max(speed)
            
        elif self.cursor < 5:
            self.stats[self.menu_codex[self.cursor]] += 1
        elif self.cursor == 5:
            if self.stats[self.menu_codex[self.cursor]] is None:
                self.stats[self.menu_codex[self.cursor]] = 1
            else:
                self.stats[self.menu_codex[self.cursor]] += 1
    
    def cursor_left(self, speed=1):
        
        if self.cursor < 2:

            self.stats[self.menu_codex[self.cursor]] -= speed
            self.check_min()
            
        elif self.cursor < 5:
            self.stats[self.menu_codex[self.cursor]] -= 1
            self.check_min()
        elif self.cursor == 5:
            if self.stats[self.menu_codex[self.cursor]] == 1:
                self.stats[self.menu_codex[self.cursor]] = None
            elif self.stats[self.menu_codex[self.cursor]] is None:
                pass
            else:
                self.stats[self.menu_codex[self.cursor]] -= 1
        
    def check_max(self, increment):
        if self.stats['fish'] + self.stats['sharks'] > 8000:
            #self.stats[self.menu_codex[self.cursor]] -= increment
            if self.menu_codex[self.cursor] == 'fish':
                self.stats[self.menu_codex[self.cursor]] -= (self.stats['fish'] + self.stats['sharks']) - 8000
            else:
                self.stats[self.menu_codex[self.cursor]] -= (self.stats['fish'] + self.stats['sharks']) - 8000       
            
    def check_min(self):
        if self.stats[self.menu_codex[self.cursor]] < 1:
            self.stats[self.menu_codex[self.cursor]] = 1
        
    def handle_input(self):
        update = False
        for event in pygame.event.get():
            if event.type == QUIT:
                exit() 
            
            elif event.type == KEYDOWN:
                update = True
                if event.key == K_ESCAPE:
                    exit()
                elif event.key == K_UP:
                    self.cursor_up()
                elif event.key == K_DOWN:
                    self.cursor_down()
                elif event.key == K_RIGHT:
                    self.hold_right = 1
                    self.cursor_right()
                elif event.key == K_LEFT:
                    self.hold_left = 1
                    self.cursor_left()
                elif event.key == K_RETURN:
                    return 'complete'
                    
            elif event.type == KEYUP:
                if event.key == K_RIGHT:
                    self.hold_right = 0
                elif event.key == K_LEFT:
                    self.hold_left = 0
        
        if self.hold_right > 10:
            update = True
            if self.hold_right > 100:
                self.cursor_right(speed=100)
            elif self.hold_right > 60:
                self.cursor_right(speed=50)
            elif self.hold_right > 30:
                self.cursor_right(speed=10)
            else:
                self.cursor_right()
        
        if self.hold_left > 10:
            update = True
            if self.hold_left > 100:
                self.cursor_left(speed=100)
            elif self.hold_left > 60:
                self.cursor_left(speed=50)
            elif self.hold_left > 30:
                self.cursor_left(speed=10)
            else:
                self.cursor_left()
                
        if self.hold_right > 0:
            self.hold_right += 1
        if self.hold_left > 0:
            self.hold_left += 1
        
        if update:
            return True
        
        return False
    
    def menu_value(self, i):
        if i == 0:
            return self.stats['fish']
        elif i == 1:
            return self.stats['sharks']
        elif i == 2:
            return self.stats['fish grow']
        elif i == 3:
            return self.stats['shark grow']
        elif i == 4:
            return self.stats['fish energy']
        elif i == 5:
            return self.stats['shark energy cap']
    
    def draw_menu(self):
        
        self.clear_screen()
        
        x = SCREENWIDTH/2 -40
        y = 100
        i, r = write('WA-TOR', (x, y), RED)
        self.screen.blit(i, r)
        
        for i in range(6):
            y = i * 20 + 200
            x = SCREENWIDTH/2 -100
            if self.cursor == i:
                color = RED
            else:
                color = WHITE
            line = self.menu[i] + ': ' + str(self.menu_value(i))
        
            i, r = write(line, (x,y), color)
            self.screen.blit(i, r)
            
        self.draw_instructions()
            
        pygame.display.update()
        
    def draw_instructions(self):
        
        instr = ['Use the arrow keys to adjust the simulations settings.',
                 'Press enter to begin the simulation.',
                 'Press escape to exit.',
                 'Sharks and fish reproduce if they survive to their reproduction threshold.',
                 'Sharks starve if they run out of energy.', 
                 'They get energy equal to the fish energy stat upon eating a fish.',
                 'The shark energy cap is the max energy a shark can store from eating fish.',
                 'If there is no cap there is no limit.'
                ]
        l = 0
        x = 30
        for line in instr:
            y = l * 20 + 450
            i, r = write(line, (x,y))
            
            self.screen.blit(i, r)
            
            l += 1
        
    def start_sim(self):
        
        self.main_menu()
        
        self.reset()
        self.clear_screen()
        
        return Wa_Tor(settings=self.stats)


class Wa_Tor(object):
    
    def __init__(self, w=100, h=80, use_image=True, settings={'fish':1000,'sharks':100,'fish grow': 4, 
                 'fish energy': 3, 'shark grow': 5, 'shark energy cap': None}):
        
        self.w = w
        self.h = h
        self.max_fish = self.w * self.h
        
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
        self.rect.bottomleft = (0, SCREENHEIGHT)
        self.image.fill(WATER)
        self.image = self.image.convert()
        
        self.fish = settings['fish']
        self.sharks = settings['sharks']
        self.chronon = 0
        
        self.graph = Graph(self)
        
        self.fish_grow_threshold = settings['fish grow']
        self.fish_energy = settings['fish energy']
        self.shark_grow_threshold = settings['shark grow']
        self.shark_energy_cap = settings['shark energy cap']
        
        self.seed_fish()
    
    def seed_fish(self):
    
        coords = []
        
        for y in range(self.h):
            for x in range(self.w):
                coords.append((x, y))
    
        selection = sample(coords, self.fish+self.sharks)
        fish_coords = selection[:self.fish]
        shark_coords = selection[self.fish:]
        
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
                    
        
        self.fish = len(fish)
        self.sharks = len(sharks)
        
        if self.fish == self.max_fish:
            self.end()
        elif self.fish == 0 and self.sharks == 0:
            self.end()
        
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
                
            elif not adj_fish:  # no food, move instead
                adj = self.get_free_adj_spot((x, y))
                if not adj:  # too crowded to move
                    nx, ny = x, y
                else:
                    nx, ny = choice(adj)
                new = (old[0]-1, old[1]+1)
                if new[0] <= 0:  # out of energy, starve
                    self.map[x][y] = 0
                    continue
                self.map[nx][ny] = new
                    
            if self.map[nx][ny][1] == self.shark_grow_threshold and (x, y) != (nx, ny):
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

    def end(self):
        pass

        
class Graph(object):
    
    def __init__(self, sim):
        
        self.sim = sim
        
        self.fish_data = {}
        self.shark_data = {}
        
        self.w = self.sim.w * self.sim.tile_w
        self.h = SCREENHEIGHT - (self.sim.h * self.sim.tile_h) - 10
        
        self.max_pixel = float(self.sim.max_fish)
        
        self.slide = 0
        
        self.image = pygame.Surface((self.w, self.h))
        self.image.fill(BLACK)
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        
        self.offset = 0
        
    def convert_to_pixel(self, value):
        c = (value / self.max_pixel) * (self.h-10) * -1 + self.h -1
        return c
        
    def draw_fish(self, chronon):
        x1 = chronon - 1 - (100 * self.offset)
        try: 
            y1 = self.fish_data[chronon-1]
        except KeyError:
            y1 = self.h
            
        x2 = chronon - (100 * self.offset)
        y2 = self.fish_data[chronon]
        
        pygame.draw.line(self.image, YELLOW, (x1, y1), (x2, y2))
    
    def draw_shark(self, chronon):
        x1 = chronon - 1 - (100 * self.offset)
        try: 
            y1 = self.shark_data[chronon-1]
        except KeyError:
            y1 = self.h
            
        x2 = chronon - (100 * self.offset)
        y2 = self.shark_data[chronon]
        
        pygame.draw.line(self.image, RED, (x1, y1), (x2, y2))
    
    def update(self):
        
        # print "fish: %s, sharks: %s" % (self.sim.fish, self.sim.sharks)
        
        self.fish_data[self.sim.chronon] = self.convert_to_pixel(self.sim.fish)
        self.shark_data[self.sim.chronon] = self.convert_to_pixel(self.sim.sharks)
        
        if self.sim.chronon - 1 - (100 * self.offset) >= self.w:
            self.offset += 1
            self.slide_graph()
        
        self.draw_shark(self.sim.chronon)
        self.draw_fish(self.sim.chronon)
        
    def draw(self):
        return self.image, self.rect
        
    def slide_graph(self):
        new = pygame.Surface((self.w, self.h))
        new = new.convert()
        new.fill(BLACK)
        r = new.get_rect()
        r.topleft = (-100, 0)
        
        new.blit(self.image, r)
        
        self.image = new
        
        
def draw_demo(screen, sim):
    
    i, r = sim.draw()
    screen.blit(i, r)
    
    i, r = sim.graph.draw()
    screen.blit(i, r)
    
    draw_population(sim, screen)
    
    draw_instructions(screen)


def draw_population(sim, screen):
        
    x = 880
    y = 10
    line = 'fish: %i' % (sim.fish)
    i, r = write(line, (x, y), YELLOW)
    screen.blit(i, r)
    
    y = 40
    line = 'sharks: %i' % (sim.sharks)
    i, r = write(line, (x, y), RED)
    screen.blit(i, r)
    
    
def draw_instructions(screen):
    
    instr = ['Press escape to return',
             'to settings screen.',
             'Press space to pause.',
             'Press < and > to adjust',
             'speed.'
            ]
            
    x = 1005
    l = 0
    for line in instr:
        y = l * 20 + 160
        i, r = write(line, (x, y))
        
        screen.blit(i, r)
        l += 1
        
    

def write(text, (x, y), color=WHITE):
    
    i = FONT.render(text, False, color)
    r = i.get_rect()
    r.topleft = (x, y)

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
                return True
            elif event.key == K_SPACE:
                PAUSE = True
            elif event.key == K_PERIOD:
                increment_speed()
            elif event.key == K_COMMA:
                decrement_speed()
    
    return False
    
            
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
    
    menu = Menu(screen)
    
    while True:
    
        sim = menu.start_sim()
        
        while True:
            
            sim.update()
            
            draw_demo(screen, sim)
            escape = handle_input()
            
            if escape:
                break
                
            if PAUSE:
                pause(clock)
            
            pygame.display.update()
            
            clock.tick(FPS)
     
     
main()