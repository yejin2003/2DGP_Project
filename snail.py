from pico2d import *
import random

import game_framework
import game_world
from server import boy
from server import grass, grass2

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 11

class Snail:
    def __init__(self,x,y):
        import server
        self.x, self.y= x,y
        self.frame = 0
        self.action = 4
        self.speed= random.uniform(0.1,0.5)
        self.size=2
        self.range=28
        self.dir = 1
        self.action = 3
        self.on_ground= False
        self.image = load_image('img/snail_monster.png')
        self.max= 800-10
        self.min= 10

    def update(self):

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        # x 좌표 자동 이동
        self.x += self.speed * self.dir
        # 경계 확인 및 방향 전환
        if self.x <= self.min:  # 최소 경계
            self.x -=self.speed * self.dir
            self.dir = 1  # 오른쪽으로 방향 전환
        elif self.x >= self.max:  # 최대 경계
            self.x += self.speed * self.dir
            self.dir = -1
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())
        if self.dir == -1:
            self.image.clip_draw(int(self.frame) , self.action ,
                                 41 , 42 , self.x, self.y, self.size * 17, self.size*17)
        elif self.dir == 1:
            self.image.clip_composite_draw(int(self.frame), self.action,
                                 41, 42, 0, 'h', self.x, self.y, self.size*17, self.size*17)
        pass

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20
        pass

    def shrink(self):
        if self.size==2:
            self.size=1.5
        elif self.size==1.5:
             self.size=1
        elif self.size==1:
            self.size=0.5
        elif self.size==0.5:
            game_world.remove_object(self)

    def handle_collision(self, group, other):
        if group == 'snail:boy':
            print("충돌")
            pass