from pico2d import *
import math


def space_down(e):
     return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE
def space_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_SPACE


def time_out(e):
     return e[0] == 'TIME_OUT'

def right_down(e):
     return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):
     return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_down(e):
     return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):
     return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT
def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP
def up_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP
def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN
def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN

def x_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_x
def x_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_x


class Idle:
    @staticmethod
    def enter(boy, e):
        if isinstance(boy.state_machine.cur_state, Run):  # Run 상태에서 전환된 경우
            boy.action = 8
            boy.dir = boy.dir1  # dir1 값으로 Idle 상태에서 방향 설정
        else:
            boy.frame = 0
            boy.action=8
        boy.wait_time = get_time()

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        if get_time() - boy.wait_time > 3:
            boy.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        if boy.dir == 1:  # 오른쪽
            boy.image.clip_composite_draw(
                boy.frame * 62, boy.action * 69, 62, 69, 0, 'h', boy.x, boy.y, 62, 69
            )
        else:  # 왼쪽
            boy.image.clip_draw(
                boy.frame * 62, boy.action * 69, 62, 69, boy.x, boy.y
            )


class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e):
            boy.is_jumping = False
            boy.dir1, boy.action = 1, 9  # 오른쪽 이동
            boy.dir2=0
        elif left_down(e) or right_up(e):
            boy.is_jumping = False
            boy.dir1, boy.action = -1, 9  # 왼쪽 이동
            boy.dir2 = 0

        if up_down(e):
            boy.is_jumping = False
            boy.dir2, boy.action = 1, 9  # 위 이동
            boy.dir1 = 0
        elif up_up(e):
            boy.is_jumping = False
            boy.dir2 = 0

        if down_down(e):  # 아래 이동 처리 추가
            boy.dir2, boy.action = -1, 9
            boy.is_jumping = False
            boy.dir1 = 0
        elif down_up(e):
            boy.is_jumping = False
            boy.dir2 = 0

        if space_down(e):
            boy.is_jumping = True
            boy.jump_start_y = boy.y
            boy.jump_time = 0
        elif space_up(e):
            boy.is_jumping = False


    @staticmethod
    def exit(boy, e):
        if boy.dir1 != 0:
            boy.dir = boy.dir1
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 6
        if not boy.is_jumping:
            boy.x += boy.dir1 * 5
            boy.y += boy.dir2 * 5  # y축 이동

        if boy.is_jumping:
            boy.y += 0.1  # 매 프레임마다 상승
            if boy.y >= boy.jump_start_y + 100:  # 목표 높이에 도달
                boy.y= boy.jump_start_y
                boy.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        if boy.dir1 == 1:
            boy.image.clip_composite_draw(
                boy.frame * 62, boy.action * 69, 62, 69, 0, 'h', boy.x, boy.y, 62, 69
            )
        else:
            boy.image.clip_draw(
                boy.frame * 62, boy.action * 69, 62, 69, boy.x, boy.y
            )

class Attack:
    # 각 프레임의 왼쪽 하단 시작 좌표와 너비 및 높이를 정의
    sprite_frames = [
        (0, 292, 50, 94),  # 첫 번째 프레임
        (44, 292, 50, 94),  # 두 번째 프레임
        (89, 292, 85, 94),  # 세 번째 프레임
        (154, 292, 85, 94),  # 네 번째 프레임
        (219, 292, 85, 94),  # 다섯 번째 프레임
        (284, 292, 85, 94)  # 여섯 번째 프레임
    ]

    @staticmethod
    def enter(boy, e):
        if isinstance(boy.state_machine.cur_state, Run):  # Run 상태에서 전환된 경우
            boy.dir = boy.dir1  # Run 상태의 방향을 유지
        else:
            boy.frame = 0
        boy.wait_time = get_time()

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        # 프레임 업데이트
        boy.frame = (boy.frame + 1) % len(Attack.sprite_frames)

    @staticmethod
    def draw(boy):
        # 현재 프레임의 좌표와 크기 가져오기
        frame = Attack.sprite_frames[boy.frame]
        x, y, width, height = frame

        if boy.dir1 == 1:  # 오른쪽 방향
            boy.image.clip_composite_draw(
                x, y, width, height, 0, 'h', boy.x, boy.y, width, height
            )
        else:  # 왼쪽 방향
            boy.image.clip_draw(
                x, y, width, height, boy.x, boy.y
            )

class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.event_que = []

    def start(self,state):
        self.cur_state=state
        self.cur_state.enter(self.boy, ('START', 0))
        pass

    def add_event(self, e):
        self.event_que.append(e)

    def set_transitions(self,transitions):
        self.transitions = transitions

    def update(self):
        self.cur_state.do(self.boy)
        if self.event_que:
            event=self.event_que.pop(0)
            self.handle_event(event)

    def draw(self):
        self.cur_state.draw(self.boy)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.boy,e)
                self.cur_state = next_state
                self.cur_state.enter(self.boy,e)
                return


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('boy.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, up_down: Run, up_up: Run, space_down: Run, space_up: Run,
                       down_down: Run, down_up: Run, x_down: Attack, x_up: Attack},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, up_down: Idle, up_up: Idle, space_down: Idle, space_up: Idle,
                      down_down: Idle, down_up: Idle, x_down: Attack, x_up: Attack,},
                Attack: {x_down: Idle, x_up: Idle},
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()