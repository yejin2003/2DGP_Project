from pico2d import load_image, get_events, update_canvas, clear_canvas, load_music
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDLK_RETURN

import game_framework
import rule_mode


def init():
    global image
    image=load_image('img/title.png')
    global bgm
    bgm = load_music('sound/start_mode.mp3')
    bgm.set_volume(64)  # 볼륨 설정 (0~128 범위)
    bgm.repeat_play()  # 음악 반복 재생

def finish():
    global image
    del image
    bgm.stop()

def handle_events():
    events=get_events()
    for event in events:
        if event.type==SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key)==(SDL_KEYDOWN, SDLK_RETURN):
            game_framework.change_mode(rule_mode)

def draw():
    clear_canvas()
    image.draw(400,225)
    update_canvas()

def update(): pass

def pause(): pass
def resume():pass