from pico2d import *
import server

class Corn:
    def __init__(self,x,y):
        self.image = load_image('img/corn.png')
        self.x=x
        self.y=y

    def update(self):
        pass

    def draw(self):
        # draw_rectangle(*self.get_bb())
        self.image.clip_draw(0, 0, 845, 1529, self.x, self.y, 25, 45)

    def get_bb(self):
        left = self.x - 12.5  # 중앙에서 왼쪽으로 반폭
        right = self.x + 12.5  # 중앙에서 오른쪽으로 반폭
        bottom = self.y - 22.5  # 중앙에서 아래로 반높이
        top = self.y + 22.5  # 중앙에서 위로 반높이
        return left, bottom, right, top

    def handle_collision(self, group, other):
        if group=='corn:boy':
            pass