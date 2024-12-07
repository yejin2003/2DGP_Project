from pico2d import load_image, get_events, update_canvas, clear_canvas
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDLK_RETURN

import game_framework
import play_mode


def init():
    global image
    image=load_image('img/success.png')

def finish():
    global image
    del image

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.key == SDLK_ESCAPE:  # ESC 키
            game_framework.quit()  # 게임 종료


def draw():
    clear_canvas()
    image.draw(400,225)
    update_canvas()

def update(): pass

def pause(): pass
def resume():pass