from pico2d import load_image

class HP:
    def __init__(self,x,y):
        self.image = load_image('img/hp.png')
        self.x=x
        self.y=y

    def draw(self):
        self.image.clip_draw(0, 0, 128, 123, self.x, self.y, 25, 30)
        pass

    def update(self):
        pass