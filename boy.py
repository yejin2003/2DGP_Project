from pico2d import *
import math

def space_down(e):
     return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE
def space_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_SPACE

def time_out(e):
     return e[0] == 'TIME_OUT'

def a_down(e):
     return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a
def a_up(e):
     return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a
def d_down(e):
     return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d
def d_up(e):
     return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d

def s_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s
def s_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s

class Idle:
    @staticmethod
    def enter(boy, e):
        if isinstance(boy.state_machine.cur_state, Run):  # Run 상태에서 전환된 경우
            boy.action = 9
            boy.dir = boy.dir1  # dir1 값으로 Idle 상태에서 방향 설정
        else:
            boy.frame = 0
            boy.action=9
        boy.wait_time = get_time()

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        if get_time() - boy.wait_time > 3:
            boy.state_machine.handle_event(('TIME_OUT', 0))
        boy.frame = (boy.frame + 1) % 4

    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_composite_draw(
                boy.frame * 62, boy.action * 68, 62, 72, 0, 'h', boy.x, 70, 62, 69
            )
        else:
            boy.image.clip_draw(
                boy.frame * 62, boy.action * 68, 62, 72, boy.x, 70
            )


class Run:
    @staticmethod
    def enter(boy, e):
        if d_down(e) or a_up(e):
            boy.dir1, boy.action = 1, 9  # 오른쪽 이동
            boy.dir2=0
        elif a_down(e) or d_up(e):
            boy.dir1, boy.action = -1, 9  # 왼쪽 이동
            boy.dir2 = 0

    @staticmethod
    def exit(boy, e):
        if boy.dir1 != 0:
            boy.dir = boy.dir1
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 4
        boy.x += boy.dir1 * 5
        boy.y += boy.dir2 * 5  # y축 이동

    @staticmethod
    def draw(boy):
        if boy.dir1 == 1:
            boy.image.clip_composite_draw(
                boy.frame * 62, boy.action * 68, 62, 72, 0, 'h', boy.x, boy.y, 62, 69
            )
        else:
            boy.image.clip_draw(
                boy.frame * 62, boy.action * 68, 62, 72, boy.x, boy.y
            )

class Attack:
    @staticmethod
    def enter(boy, e):
        if isinstance(boy.state_machine.cur_state, Run):  # Run 상태에서 전환된 경우
            boy.dir = boy.dir1  # Run 상태의 방향을 유지
            boy.action=7
        else:
            boy.frame = 0
            boy.action=7
        boy.wait_time = get_time()

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 4
        pass

    @staticmethod
    def draw(boy):
        if boy.dir == 1:  # 오른쪽
            boy.image.clip_composite_draw(
                boy.frame * 62, boy.action * 65, 63, 72, 0, 'h', boy.x, boy.y, 62, 69
            )
        else:  # 왼쪽
            boy.image.clip_draw(
                boy.frame * 62, boy.action * 65, 63, 72, boy.x, boy.y
            )

class Jump:
    @staticmethod
    def enter(boy, e):
        if space_down(e):  # 스페이스키를 눌러서 점프 시작
            boy.jump_velocity = 10
            if a_down(e):# 왼쪽으로 점프
                boy.dir = -1
                boy.x -= 10  # 왼쪽으로 이동 거리 조정
            if d_down(e):
                boy.dir = 1
                boy.x += 10

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.y += boy.jump_velocity
        boy.jump_velocity += boy.gravity

        if boy.y <= 70:  # 점프가 끝났을 때
            boy.is_jumping = False
            boy.jump_velocity = 0
            boy.y = 70

    @staticmethod
    def draw(boy):
        if boy.dir1 == 1:
            boy.image.clip_composite_draw(
                boy.frame * 62, boy.action * 68, 62, 72, 0, 'h', boy.x, boy.y, 62, 69
            )
        else:
            boy.image.clip_draw(
                boy.frame * 62, boy.action * 68, 62, 72, boy.x, boy.y
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
        self.x, self.y = 400, 70
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.jump_velocity = 10
        self.jump_height = 10
        self.gravity = -1
        self.is_jumping = False
        self.velocity_x, self.velocity_y = 30, 30
        self.image = load_image('img/boy.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {d_down: Run, a_down: Run, a_up: Run, d_up: Run, space_down: Jump, s_down: Attack, s_up: Attack},
                Run: {d_down: Idle, a_down: Idle, d_up: Idle, a_up: Idle, space_down: Jump, s_down: Attack, s_up: Attack},
                Attack: {s_down: Idle, s_up: Idle},
                Jump: {lambda e: space_down(e) and d_down(e): Jump, lambda e: space_down(e) and a_down(e): Jump, d_up: Run, a_up: Run, space_down: Jump, s_down: Attack}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()