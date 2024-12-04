from pico2d import *
import random

import game_framework
import game_world
from server import boy
from server import grass, grass2

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 11

class Snake:
    def __init__(self,x,y):
        import server
        self.x, self.y= x,y
        self.speed= random.uniform(0.5,0.8)
        self.on_ground= False
        self.image = load_image('img/bomb.png')
        self.min= server.grass2

    def update(self):
        self.y -= self.speed
        # 경계 확인 및 방향 전환
        if self.y <= self.min:  # 최소 경계
            self.x -=self.speed * self.dir
            self.dir = 1  # 오른쪽으로 방향 전환
        elif self.x >= self.max:  # 최대 경계
            self.x += self.speed * self.dir
            self.dir = -1
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())
        if self.dir == -1:
            self.image.clip_draw(int(self.frame) , self.action * 32 ,
                                 32 , 32 , self.x, self.y, self.size * 17, self.size*17)
        elif self.dir == 1:
            self.image.clip_composite_draw(int(self.frame), self.action * 32,
                                 32, 32, 0, 'h', self.x, self.y, self.size*17, self.size*17)
        pass

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10
        pass

    def shrink(self):
        game_world.remove_object(self)

    def handle_collision(self, group, other):
        if group == 'snake:boy':
            print("충돌")
            pass