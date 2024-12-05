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
        self.x=0

    def update(self):
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())
        screen_width = 800  # 화면의 너비 (필요에 따라 변경)
        tile_width = 107  # 타일 너비

        # 화면 너비를 채울 때까지 타일을 그립니다.
        for self.x in range(0, screen_width, tile_width):
            self.image.clip_draw(0, 0, 89, 20, self.x, self.gy, 200, 17)

    def get_bb(self):
        screen_width = 800  # 화면 너비
        left = 0  # 왼쪽 x좌표
        bottom = self.gy - 8.5  # 바운딩 박스 하단
        right = screen_width  # 오른쪽 x좌표
        top = self.gy+10  # 바운딩 박스 상단

        return left, bottom, right, top

    def handle_collision(self, group, other):
        if group=='grass:bomb':
            pass