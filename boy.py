from pico2d import *
import math



def space_down(e):
     return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

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
            boy.dir1, boy.action = 1, 9  # 오른쪽 이동
            boy.dir2=0
        elif left_down(e) or right_up(e):
            boy.dir1, boy.action = -1, 9  # 왼쪽 이동
            boy.dir2 = 0

        if up_down(e):
            boy.dir2, boy.action = 1, 9  # 위 이동
            boy.dir1 = 0
        elif up_up(e):
            boy.dir2 = 0
        elif down_down(e):  # 아래 이동 처리 추가
            boy.dir2, boy.action = -1, 9
            boy.dir1 = 0
        elif down_up(e):
            boy.dir2 = 0

    @staticmethod
    def exit(boy, e):
        if boy.dir1 != 0:
            boy.dir = boy.dir1
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 6
        boy.x += boy.dir1 * 5
        boy.y += boy.dir2 * 5  # y축 이동

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
    @staticmethod
    def enter(boy, e):
        if isinstance(boy.state_machine.cur_state, Run):  # Run 상태에서 전환된 경우
            boy.action = 4
            # 현재 이동 방향을 Idle 상태에서 유지하도록 설정
            boy.dir = boy.dir1  # dir1 값으로 Idle 상태에서 방향 설정
        else:
            boy.dir = 0  # Idle로 처음 진입 시 정지
            boy.frame = 0
            boy.action=4
        boy.wait_time = get_time()
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 4

    @staticmethod
    def draw(boy):
        if boy.dir1 == 1:
            boy.image.clip_composite_draw(
                boy.frame * 75, boy.action * 73, 80, 88, 0, 'h', boy.x, boy.y, 79, 88
            )
        else:
            boy.image.clip_draw(
                boy.frame * 75, boy.action * 73, 80, 88, boy.x, boy.y, 79, 88
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
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, up_down: Run, up_up:Run,down_down: Run, down_up:Run,x_down:Attack, x_up:Attack},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, up_down: Idle, up_up:Idle,down_down: Idle, down_up:Idle, x_down:Attack, x_up:Attack},
                Attack:{x_down:Idle, x_up:Idle}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()