from turtledemo.penrose import start
import numpy as np
from pico2d import *

import random
import game_framework
import game_world
import success_mode
from background import Lv1_Background
from grass import Grass, Grass2
from boy import Boy
from corn import *
import server
from snake import *
from snail import *
from bomb import *
from hp import *
import time
import fail_mode

font = None
start_time = None
time_limit = 30  # 제한 시간 30초

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            server.boy.handle_event(event)

def init():
    global running
    global start_time
    running = True
    start_time=time.time()

    global font
    font = load_font('ENCR10B.TTF', 24)

    server.background = Lv1_Background()
    game_world.add_object(server.background, 0)

    server.grass = Grass()
    game_world.add_object(server.grass, 1)

    server.grass2= Grass2()
    game_world.add_object(server.grass2, 1)

    server.boy = Boy()
    game_world.add_object(server.boy, 2)


    global snake

    # Snake and Snail generation with fixed spacing
    #snake_positions = [400 + i * 50 for i in range(5)]  # 5 snakes, 40 units apart


    # Create Snake objects
    for _ in range(3):
        snake = Snake(random.randint(300, 400), server.grass2.gy + 20)
        game_world.add_object(snake, 2)
        game_world.add_collision_pair('snake:boy', snake, None)
        game_world.add_collision_pair('snake:bomb', snake, None)
    game_world.add_collision_pair('grass:boy', server.boy, None)
    game_world.add_collision_pair('snake:boy', None, server.boy)

    global snail
    for _ in range(3):
        snail = Snail(random.randint(700, 800-10), server.grass2.gy + 20)
        game_world.add_object(snail, 2)
        game_world.add_collision_pair('snail:boy', snail, None)
        game_world.add_collision_pair('snail:bomb', snail, None)
    game_world.add_collision_pair('snail:boy', None, server.boy)

    #초기 폭탄
    global bombs
    bombs=[Bomb(random. randint(10, 700),450-10) for _ in range(3)]
    game_world.add_objects(bombs, 2)

    for bomb in bombs:
        game_world.add_collision_pair('bomb:boy', bomb, None)
        game_world.add_collision_pair('bomb:grass', bomb, None)
        game_world.add_collision_pair('snail:bomb', None, bomb)
        game_world.add_collision_pair('snake:bomb', None, bomb)
    game_world.add_collision_pair('bomb:boy', None, server.boy)
    game_world.add_collision_pair('bomb:grass', None, server.grass2)


    global bomb_spawn_timer
    bomb_spawn_timer = 0  # 폭탄 생성 타이머

    global hp_objects  # 전역 hp_objects 리스트를 수정할 수 있도록 선언
    x_positions = np.linspace(20, 80, num=3)
    hp_objects = [HP(x, 430) for x in x_positions]
    game_world.add_objects(hp_objects, 3)

    global corns
    corns=[Corn(150,server.grass2.gy+25), Corn(450,server.grass2.gy+25)]
    game_world.add_objects(corns, 2)

    for corn in corns:
        game_world.add_collision_pair('corn:boy', corn, None)
    game_world.add_collision_pair('corn:boy', None, server.boy)


def update():
    global bomb_spawn_timer

    # 게임 월드 업데이트
    game_world.update()

    # 폭탄 생성 타이머 증가
    bomb_spawn_timer += 1
    if bomb_spawn_timer > 200:  # 약 2초마다 폭탄 추가 생성
        for _ in range(3):  # 한 번에 5개의 폭탄 생성
            new_bomb = Bomb(random.randint(30, 800 - 30), 450 - 10)
            game_world.add_object(new_bomb, 2)

            # 충돌 그룹에 새 폭탄 추가
            game_world.add_collision_pair('bomb:boy', new_bomb, None)
            game_world.add_collision_pair('bomb:boy', None, server.boy)
            game_world.add_collision_pair('bomb:grass', new_bomb, None)
            game_world.add_collision_pair('bomb:grass', None, server.grass2)
            game_world.add_collision_pair('snail:bomb', None, new_bomb)
            game_world.add_collision_pair('snake:bomb', None, new_bomb)

        bomb_spawn_timer = 0

    global hp_objects  # 전역 hp_objects 리스트를 수정할 수 있도록 선언
    while len(hp_objects) > server.boy.hp:
        if hp_objects:  # hp_objects가 비어 있지 않은지 확인
            last_hp = hp_objects.pop()  # 리스트에서 마지막 HP 제거
            if last_hp in game_world.all_objects():  # 게임 월드에 실제로 존재하는지 확인
                game_world.remove_object(last_hp)  # 게임 월드에서 제거

    if server.boy.hp <= 0:
        print("Game Over: HP depleted!")
        running = False
        game_framework.change_mode(fail_mode)
        return

    snakes_remaining = any(isinstance(obj, Snake) for obj in game_world.all_objects())
    snails_remaining = any(isinstance(obj, Snail) for obj in game_world.all_objects())

    if not snakes_remaining and not snails_remaining:
        print("Success: All enemies defeated!")
        game_framework.change_mode(success_mode)  # success_mode로 전환
        return

    elapsed_time = time.time() - start_time
    if elapsed_time >= 30:
        print("Game Over: Time's up!")
        running = False  # 게임 루프 종료
        game_framework.change_mode(fail_mode)
    # 충돌 처리
    game_world.handle_collisions()
    delay(0.01)

def draw():
    clear_canvas()
    # 남은 시간 계산 및 표시
    elapsed_time = time.time() - start_time
    remaining_time = max(0, int(time_limit - elapsed_time))  # 0초 미만 방지

    # 남은 시간 표시 (화면 우측 상단)
    font.draw(700, 450, f'Time: {remaining_time}', (255, 255, 255))  # 흰색 글씨로 표시
    game_world.render()
    update_canvas()
    delay(0.01)

def finish():
    game_world.clear()
    pass

def pause(): pass
def resume():pass