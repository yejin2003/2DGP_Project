from pico2d import *

class Grass:
    def __init__(self):
        self.image = load_image('grass.png')  # 이미지 경로 설정

    def update(self):
        pass

    def draw(self):
        screen_width = 800  # 화면의 너비 (필요에 따라 변경)
        y_position = 16  # 바닥에 맞춰 위치 조정

        # 화면 너비를 채울 때까지 타일을 그립니다.
        x = 0
        while x < screen_width:
            self.image.clip_draw(107, 30, 107, 30, x, y_position, 300, 40)
            x += 107 # 확대된 타일 너비만큼 오른쪽으로 이동
