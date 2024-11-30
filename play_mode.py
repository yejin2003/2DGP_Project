from pico2d import *

import random
import game_framework
import game_world
from grass import Grass, Grass2
from boy import Boy
import server
from snake import *

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

    server.grass2= Grass2()
    game_world.add_object(server.grass2, 0)

    server.boy = Boy()
    game_world.add_object(server.boy, 1)

    global snakes
    snakes = [Snake(random.randint(500, 800-10), server.grass2.gy+40) for _ in range(1)]
    for snake in snakes:
        game_world.add_object(snake,1)

    game_world.add_collision_pair('grass:hero', server.boy, None)

def update():
    game_world.update()
    #handle_collisions()
    delay(0.01)

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