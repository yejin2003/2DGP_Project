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
    def __init__(self):
        import server
        self.x, self.y = 400, server.grass2.gy+40
        self.frame = 0
        self.action = 4
        self.speed=5
        self.range=20
        self.dir = 0
        self.action = 3
        self.on_ground= False
        self.image = load_image('img/snake_monster.png')
        self.max=self.x+self.range
        self.min=self.x-self.range

    def update(self):

        self.frame = (
                (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3)
        # x 좌표 자동 이동
        self.x += self.speed * self.dir
        # 경계 확인 및 방향 전환
        if self.x <= self.min:  # 최소 경계
            self.x = self.min
            self.dir = 1  # 오른쪽으로 방향 전환
        elif self.x >= self.max:  # 최대 경계
            self.x = self.max
            self.dir = -1
        pass

    def draw(self):
        if self.dir == 1:
            self.image.clip_draw(int(self.frame) * 34 , self.action * 33 ,
                                 34 , 33 , self.x, self.y, 80, 80)
        elif self.dir == -1:
            self.image.clip_composite_draw(int(self.frame) * 34, self.action * 33,
                                 34, 33, 0, 'h', self.x, self.y, 80, 80)
        pass

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20
        pass

    def handle_collision(self, group, other):
        if group == 'boy:snake':
            pass