# Race AI Neural Network
import pygame, sys, math, os, json
from os import path
from json import JSONEncoder

config = {
    "map": []
}

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def translate_along_rotation(self, rotation, distance):
        self.x += math.cos(rotation * math.pi/180) * distance
        self.y += math.sin(rotation * math.pi/180) * distance

        

if path.exists('map.json') == False:
    with open('map.json','x') as File:
        json.dump(config, File, indent=4)
else: 
    with open('map.json','r') as File:
        config = json.load(File)
        for i in range(len(config['map'])):
            new_vec = Vector2(config['map'][i]['x'],config['map'][i]['y'])
            config['map'][i] = new_vec

def rot_center(image, rect, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect


class Car:
    def __init__(self, spawn: Vector2):
        self.spawn = spawn
        self.rotation = 0
        self.speed = 5
        self.is_driving = True
        self.car = pygame.Surface((480, 920))
        self.image = pygame.image.load(os.path.join('cars', 'car1.png'))
        self.car.blit(self.image, (0, 0))
        self.car = pygame.transform.scale(self.car, (round(480*0.05), round(920*0.05)))

        self.hitbox = (1,2)

    def update(self):
        if self.is_driving:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_s]:
                self.spawn.translate_along_rotation(self.rotation, -self.speed)
            if keys[pygame.K_w]:
                self.spawn.translate_along_rotation(self.rotation, self.speed)
            if keys[pygame.K_a]:
                self.rotation -= self.speed
            if keys[pygame.K_d]:
                self.rotation += self.speed


    def draw(self):
        if not self.is_driving:
            return
        img, rect = rot_center(self.car, self.car.get_rect(), -self.rotation - 90)
        size = (rect[2],rect[3])
        self.hitbox = size
        window.blit(img, (self.spawn.x, self.spawn.y))
        pygame.draw.line(window, ([255,0,0]), (self.spawn.x,self.spawn.y), (self.spawn.x + size[0], self.spawn.y))
        pygame.draw.line(window, ([255,0,0]), (self.spawn.x + size[0],self.spawn.y), (self.spawn.x + size[0], self.spawn.y + size[1]))
        pygame.draw.line(window, ([255,0,0]), (self.spawn.x + size[0], self.spawn.y + size[1]), (self.spawn.x, self.spawn.y + size[1]))
        pygame.draw.line(window, ([255,0,0]), (self.spawn.x, self.spawn.y + size[1]), (self.spawn.x, self.spawn.y))


    def distance_to_wall(self):
        pass


    def does_collide(self, pos_start, pos_end):
        if not self.is_driving:
            return False

        def lineLine(x1, y1, x2, y2, x3, y3, x4, y4):
            
            _t1 = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3))
            _t2 = ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))

            _r1 = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3))
            _r2 = ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))


            if _t1 == 0:
                _t1 = 0.001
            if _t2 == 0:
                _t2 = 0.001
            if _r1 == 0:
                _r1 = 0.001
            if _r2 == 0:
                _r2 = 0.001
            

            uA = _t1 / _t2
            uB = _r1 / _r2
            if uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1:
                return True
            return False

        _x1 = pos_start.x
        _y1 = pos_start.y
        _x2 = pos_end.x
        _y2 = pos_end.y

        _rx = self.spawn.x
        _ry = self.spawn.y
        
        _rh = self.hitbox[1]
        _rw = self.hitbox[0]


        left = lineLine(_x1,_y1,_x2,_y2, _rx,_ry,_rx, _ry+_rh)
        right = lineLine(_x1,_y1,_x2,_y2, _rx+_rw,_ry, _rx+_rw,_ry+_rh)
        top = lineLine(_x1,_y1,_x2,_y2, _rx,_ry, _rx+_rw,_ry)
        bottom = lineLine(_x1,_y1,_x2,_y2, _rx,_ry+_rh, _rx+_rw,_ry+_rh)
        return left or right or top or bottom

    def kill(self):
        print('Killed')
        self.is_driving = False


prev_mouse = None

def create_car(name=None):
    if len(cars) < 100:
        pos = Vector2(50, 80)
        name = Car(pos)
        cars.append(name)

def draw_map():
    global prev_mouse
    global config
    mouse = pygame.mouse.get_pressed()
    if prev_mouse == None:
        prev_mouse = mouse
    if mouse[0] and not prev_mouse[0]:
        mouse_pos = pygame.mouse.get_pos()
        config['map'].append(Vector2(mouse_pos[0], mouse_pos[1]))
    prev_mouse = mouse
        
def clear_map():
    global config
    config['map'] = []

def reset_cars():
    print('reset cars')
    for x in range(len(cars)):
        car = cars[x]
        car.kill()

def save_map():
    with open('map.json', 'w') as File:
        json.dump(config, File, indent=4, default=lambda o: o.__dict__)

if __name__ == '__main__':
    WIDTH = 900
    HEIGHT = 900
    pygame.font.init()
    pygame.display.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Race Game!')
    cars = []
    black = [0, 0, 0]
    FPS = 30
    play = True
    font = pygame.font.SysFont('calibri', 12)
    # pos = Vector2(50, 50)
    # player1 = Car(pos)

    
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        text = font.render(f'E to quit game - Hold G to enter map editor mode - R to reset Map - O to save current map - P to create car instance - Cars Spawned: {len(cars)}', True, [255,255,255])

        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            play = False
        if keys[pygame.K_g]:
            draw_map()
        if keys[pygame.K_r]:
            clear_map()
        if keys[pygame.K_o]:
            save_map()
        if keys[pygame.K_p]:
            create_car()
        if keys[pygame.K_h]:
            reset_cars()


        pygame.time.delay(FPS)
        window.fill(black)
        window.blit(text, (20, 20))
        if len(cars) > 0:
            for car in cars:
                car.update()
                car.draw()

        for x in range(len(config['map'])):
            next = x+1
            if next == len(config['map']):
                next = 0
            pos1 = config['map'][x]
            pos2 = config['map'][next]
            
            for x in range(len(cars)):
                car = cars[x]
                if car.does_collide(pos1, pos2):
                    car.kill()
            
            pygame.draw.line(window, ([255, 255, 255]), (pos1.x, pos1.y), (pos2.x, pos2.y))

        pygame.display.update()
