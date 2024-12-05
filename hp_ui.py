from pico2d import load_image

class HP:
    def __init__(self,x,y):
        self.image = load_image('img/hp.png')
        self.x=x
        self.y=y

    def draw(self):
        
        pass

    def update(self):
        pass