# Race AI Neural Network
import pygame, sys, math, os, json, neat
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


def where_does_lines_intersect(start_first, end_first, start_second, end_second):
    x1 = start_first[0]
    y1 = start_first[1]
    x2 = end_first[0]
    y2 = end_first[1]
    x3 = start_second[0]
    y3 = start_second[1]
    x4 = end_second[0]
    y4 = end_second[1]

    qA = ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))

    if qA == 0: qA = 0.00001

    uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / qA 
    uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / qA

    if (uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1):
        intersectionX = x1 + (uA * (x2-x1))
        intersectionY = y1 + (uA * (y2-y1))
        return Vector2(intersectionX, intersectionY)
        
    return None

def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

class Car:
    def __init__(self, spawn: Vector2):
        self.spawn = spawn
        self.rotation = 0
        self.speed = 0.2
        self.is_driving = True
        self.car = pygame.Surface((480/2, 920/2))
        self.image = pygame.image.load(os.path.join('cars', 'car1.png'))
        self.car.blit(self.image, (0, 0))
        self.car = pygame.transform.scale(self.car, (round(480*0.05), round(920*0.05)))

        self.checkpoint_one = False
        self.checkpoint_two = False
        self.checkpoint_three = False
        self.checkpoint_four = False
        self.checkpoint_five = False

        self.hitbox = (1,2)
    
    def move(self, direction):
        if self.is_driving:
            if direction == "forward":
                self.spawn.translate_along_rotation(self.rotation, self.speed)
            elif direction == "backward":
                self.spawn.translate_along_rotation(self.rotation, -self.speed)
            elif direction == "accelerate":
                self.spawn.translate_along_rotation(self.rotation, self.speed)
            elif direction == "brake":
                self.spawn.translate_along_rotation(self.rotation, -self.speed)
            elif direction == "left":
                self.rotation -= 1
            elif direction == "right":
                self.rotation += 1


    def update(self):
        if self.is_driving:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_s]:
                self.spawn.translate_along_rotation(self.rotation, -self.speed)
            if keys[pygame.K_w]:
                self.spawn.translate_along_rotation(self.rotation, self.speed)
            if keys[pygame.K_a]:
                self.rotation -= self.speed * 5
            if keys[pygame.K_d]:
                self.rotation += self.speed * 5


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

        ray_length = 500

        self.draw_line_angle(-90, ray_length)
        self.draw_line_angle(90, ray_length)
        self.draw_line_angle(45, ray_length)
        self.draw_line_angle(-45, ray_length)
        self.draw_line_angle(0, ray_length)

        rays = [
            self.get_intersection_at_angle(-90, ray_length),
            self.get_intersection_at_angle(90, ray_length),
            self.get_intersection_at_angle(45, ray_length),
            self.get_intersection_at_angle(-45, ray_length),
            self.get_intersection_at_angle(0, ray_length),
        ]


        for ray in rays:
            if ray != None:
                pygame.draw.circle(window, (255,0,0), (int(ray.x), int(ray.y)), 5)


    def distance_from_wall(self, angle, ray_length):
        point = self.get_intersection_at_angle(angle, ray_length)
        if point == None:
            return ray_length
        return distance((point.x, point.y), (self.spawn.x, self.spawn.y))


    def draw_line_angle(self, angle_offset, length = 100):
        pygame.draw.line(window, ([0,255,0]), (self.spawn.x, self.spawn.y), self.translate_along_rotation(angle_offset, length))

    
    def translate_along_rotation(self, angle_offset, length = 100):
        return (self.spawn.x + math.cos((self.rotation + angle_offset) * math.pi / 180) * length,  self.spawn.y + math.sin((self.rotation + angle_offset) * math.pi / 180) * length)


    def get_intersection_at_angle(self, angle_offset, length = 100):
        intersect = None

        for index, point in enumerate(config['map']):
            next_point = config['map'][(index + 1) % len(config['map'])]

            test_point = where_does_lines_intersect((self.spawn.x, self.spawn.y), self.translate_along_rotation(angle_offset, length), (point.x, point.y), (next_point.x, next_point.y))
            if test_point != None:
                if intersect != None:
                    if distance((test_point.x, test_point.y), (self.spawn.x, self.spawn.y)) < distance((intersect.x, intersect.y), (self.spawn.x, self.spawn.y)):
                        intersect = test_point
                else:
                    intersect = test_point
        return intersect


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
    
    def distance_to_wall_right(self):

        for x in range(len(config['map'])):
            next = x+1
            if next == len(config['map']):
                next = 0
            pos1 = config['map'][x]
            pos2 = config['map'][next]

            if self.spawn.x < pos1.x and pos2.x:
                for n in range(pos1.y, pos2.y):
                    if int(self.spawn.y) == n:
                        y = n
                        pygame.draw.rect(window, (0, 255, 0), (pos1.x, pos1.y, 10, pos2.y), width=2)
                        dist = math.sqrt((pos1.x-self.spawn.x)**2 + (y-self.spawn.y)**2)

                        print(dist)
                        pygame.draw.rect(window, (0, 255, 0), (self.spawn.x, self.spawn.y, dist, 1), width=2)


    def kill(self):
        #print('Killed') 
        self.is_driving = False

prev_mouse = None

def create_car(cars, name=None):
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

def reset_cars(cars, ge, nets):
    print('reset cars')
    for x, car in enumerate(cars):
        car = cars[x]
        ge[x].fitness -= 1
        car.kill()
        cars.pop(x)
        nets.pop(x)
        ge.pop(x)

def save_map():
    with open('map.json', 'w') as File:
        json.dump(config, File, indent=4, default=lambda o: o.__dict__)

def main(genomes, neat_config):
    nets = []
    ge = []
    cars = []
    pos = Vector2(50, 80)

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, neat_config)
        nets.append(net)
        cars.append(Car(pos))
        g.fitness = 0
        ge.append(g)

    black = [0, 0, 0]

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        FPS = 30
        font = pygame.font.SysFont('calibri', 12)

        text = font.render(f'E to quit game - Hold G to enter map editor mode - R to reset Map - O to save current map - P to create car instance - Cars Spawned: {len(cars)}', True, [255,255,255])
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            run = False
        if keys[pygame.K_g]:
            draw_map()
        if keys[pygame.K_r]:
            clear_map()
        if keys[pygame.K_o]:
            save_map()
        # if keys[pygame.K_p]:
            # create_car(cars)
        if keys[pygame.K_h]:
            reset_cars(cars, ge, nets)


        pygame.time.delay(FPS)
        window.fill(black)
        window.blit(text, (20, 20))
        if len(cars) > 0:
            for car in cars:
                car.update()
                car.draw()
        else:
            run = False
            break
        
        for x, car in enumerate(cars):
            car.move('forward')

            #print(car.distance_from_wall(0, 300))

            output = nets[x].activate((car.rotation, car.distance_from_wall(-90, 300), car.distance_from_wall(90, 300), car.distance_from_wall(45, 300), 
                car.distance_from_wall(-45, 300), car.distance_from_wall(0, 300))) # Input nodes


            if car.checkpoint_one != True:
                if car.spawn.y > 85:
                    ge[x].fitness += 10
                    car.checkpoint_one = True
            elif car.checkpoint_two != True:
                if car.spawn.y > 110:
                    ge[x].fitness += 30
                    car.checkpoint_two = True
            elif car.checkpoint_three != True:
                if car.spawn.y > 150:
                    ge[x].fitness += 10
                    car.checkpoint_three = True
            

            if output[0] > 0:
                #car.speed += 0.01
                #print('Moving forward')
                car.move('accelerate')


            # self.spawn.translate_along_rotation(self.rotation, self.speed)


            # car.spawn.translate_along_rotation(car.rotation, output[0])


            if output[0] > -0.2:
                #print('Left')
                car.move('left')
            elif output[0] < 0.2:
                #print('Right')
                car.move('right')

#            car.rotation = output[1]


        for x in range(len(config['map'])):
            next = x+1
            if next == len(config['map']):
                next = 0
            pos1 = config['map'][x]
            pos2 = config['map'][next]

            # print(ge[x].fitness)


            for x, car in enumerate(cars):
                car = cars[x]

                if car.does_collide(pos1, pos2):
                    ge[x].fitness -= 1
                    car.kill()
                    cars.pop(x)
                    nets.pop(x)
                    ge.pop(x)

            #for g in ge:
                #g.fitness += 0.001
                
            pygame.draw.line(window, ([255, 255, 255]), (pos1.x, pos1.y), (pos2.x, pos2.y))

        pygame.display.update()


def run(config_path):
    neat_config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                config_path)
    
    p = neat.Population(neat_config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 100)

if __name__ == '__main__':
    WIDTH = 900
    HEIGHT = 900
    pygame.font.init()
    pygame.display.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Race Game!')
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)

    