from pico2d import *
import random

import game_framework
import game_world
from server import boy
from server import grass, grass2

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 11

class Bomb:
    def __init__(self,x,y):
        import server
        self.x, self.y= x,y
        self.speed= random.uniform(2.0,3.0)
        self.on_ground= False
        self.image = load_image('img/bomb.png')
        self.min= 90
        self.removed = False

    def update(self):
        self.y -= self.speed

    def draw(self):
        draw_rectangle(*self.get_bb())
        self.image.clip_draw(0,0,106, 114, self.x, self.y, 40, 40)

    def get_bb(self):
        return self.x - 15, self.y - 20, self.x + 15, self.y + 20
        pass

    def shrink(self):
        game_world.remove_object(self)

    def handle_collision(self, group, other):
        if group == 'bomb:boy':
            print("충돌")
            pass

        if group=='bomb:grass':
            if not self.removed:
                game_world.remove_object(self)
                self.removed=True
            pass

        if group=='snail:bomb':
            if not self.removed:
                game_world.remove_object(self)
                self.removed=True
            pass

        if group=='snake:bomb':
            if not self.removed:
                game_world.remove_object(self)
                self.removed=True

        if group=='snail2:bomb':
            if not self.removed:
                game_world.remove_object(self)
                self.removed=True
            pass

        if group=='snake2:bomb':
            if not self.removed:
                game_world.remove_object(self)
                self.removed=True
        if group=='snail3:bomb':
            if not self.removed:
                game_world.remove_object(self)
                self.removed=True
            pass

        if group=='snake3:bomb':
            if not self.removed:
                game_world.remove_object(self)
                self.removed=True