from pico2d import *

import random
import game_framework
import game_world
from background import Lv1_Background
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

    server.background = Lv1_Background()
    game_world.add_object(server.background, 0)

    server.grass = Grass()
    game_world.add_object(server.grass, 1)

    server.grass2= Grass2()
    game_world.add_object(server.grass2, 1)

    server.boy = Boy()
    game_world.add_object(server.boy, 2)

    global snakes
    snakes = [Snake(random.randint(500, 800-10), server.grass2.gy+20) for _ in range(5)]
    game_world.add_objects(snakes,2)

    game_world.add_collision_pair('grass:boy', server.boy, None)

    for snake in snakes:
        game_world.add_collision_pair('snake:boy', snake, None)

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