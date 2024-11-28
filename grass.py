from pico2d import *
import server

class Grass:
    def __init__(self):
        self.image = load_image('img/bottom.png')
        self.by= 20

    def update(self):
        pass

    def draw(self):
        screen_width = 800  # 화면의 너비 (필요에 따라 변경)
        tile_width = 107  # 타일 너비

        # 화면 너비를 채울 때까지 타일을 그립니다.
        for x in range(0, screen_width, tile_width):
            self.image.clip_draw(0, 0, 89, 56, x, self.by, 200, 56)

class Grass2:
    def __init__(self):
        self.image = load_image('img/grass.png')
        self.gy= 50

    def update(self):
        pass

    def draw(self):
        screen_width = 800  # 화면의 너비 (필요에 따라 변경)
        tile_width = 107  # 타일 너비

        # 화면 너비를 채울 때까지 타일을 그립니다.
        for x in range(0, screen_width, tile_width):
            self.image.clip_draw(0, 0, 89, 20, x, self.gy, 200, 17)

