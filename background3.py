import server

from pico2d import *

screen_width, screen_height = 800, 450

class Lv3_Background():
    def __init__(self):
        self.bgm = load_music('sound/play_mode1.mp3')
        self.image =  load_image('img/Lv3_background.png')
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h
        self.bgm.repeat_play()
        pass


    def draw(self):
        for x in range(0, self.cw, self.w):
            for y in range(0, self.ch, self.h):
                self.image.draw_to_origin(x, y)

    def update(self):
        self.window_left = clamp(0, int(server.boy.x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(server.boy.y) - self.ch // 2, self.h - self.ch - 1)
        pass


    def clear(self):
        self.bgm.stop()
        pass