from pico2d import *

class Grass:
    def __init__(self):
        self.image = load_image('img/grass.png')  # 이미지 경로 설정

    def update(self):
        pass

    def draw(self):
        screen_width = 800  # 화면의 너비 (필요에 따라 변경)
        tile_width = 107  # 타일 너비

        # 화면 너비를 채울 때까지 타일을 그립니다.
        for x in range(0, screen_width, tile_width):
            self.image.clip_draw(107, 30, 107, 30, x, 30, 300, 60)



