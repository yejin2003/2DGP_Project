from pico2d import *

import random
import game_framework
import game_world
from background import Lv1_Background
from grass import Grass, Grass2
from boy import Boy
import server
from snake import *
from snail import *
from bomb import *

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

    snakes = [Snake(random.randint(600, 800-10), server.grass2.gy+20) for _ in range(5)]
    game_world.add_objects(snakes,2)

    game_world.add_collision_pair('grass:boy', server.boy, None)

    for snake in snakes:
        game_world.add_collision_pair('snake:boy', snake, None)
    game_world.add_collision_pair('snake:boy', None, server.boy)

    global snailes
    snailes= [Snail(random.randint(600, 800-10), server.grass2.gy+20) for _ in range(5)]
    game_world.add_objects(snailes,2)

    for snail in snailes:
        game_world.add_collision_pair('snail:boy', snail, None)
    game_world.add_collision_pair('snail:boy', None, server.boy)

    global bombs
    bombs=[Bomb(random. randint(30, 800-30),450-10) for _ in range(5)]
    game_world.add_objects(bombs, 2)

    for bomb in bombs:
        game_world.add_collision_pair('bomb:boy', bomb, None)
        game_world.add_collision_pair('bomb:grass', bomb, None)
    game_world.add_collision_pair('bomb:boy', None, server.boy)
    game_world.add_collision_pair('bomb:grass', None, server.grass2)

    global bomb_spawn_timer
    bomb_spawn_timer = 0  # 폭탄 생성 타이머


def update():
    game_world.update()
    global bomb_spawn_timer
    # 폭탄 생성 타이머 증가
    bomb_spawn_timer += 1

    game_world.handle_collisions()
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