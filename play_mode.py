from pico2d import *

import game_framework
import game_world
from grass import Grass
from boy import Boy
import server

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            server.boy.handle_event(event)


def init():
    global running
    running = True

    server.grass = Grass()
    game_world.add_object(server.grass, 0)

    server.boy = Boy()
    game_world.add_object(server.boy, 1)

    game_world.add_collision_pair('grass:hero', server.boy, None)

def update():
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
    delay(0.01)

def finish():
    game_world.clear()
    pass

def pause(): pass
def resume():pass