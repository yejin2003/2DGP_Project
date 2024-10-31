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

def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a

class Idle:
    @staticmethod
    def enter(boy, e):
        boy.action=8
        boy.dir = 0
        boy.frame = 0
        boy.wait_time = get_time()
        pass

    @staticmethod
    def exit(boy,e):
        pass

    @staticmethod
    def do(boy):
        if get_time() - boy.wait_time > 3:
            boy.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 54, boy.action * 69, 54, 69, boy.x, boy.y)

class Run:
     @staticmethod
     def enter(boy, e):
         if right_down(e) or left_up(e):
             boy.dir, boy.action = 1, 9
         elif left_down(e) or right_up(e):
             boy.dir, boy.action = -1, 9
     @staticmethod
     def exit(boy, e):
         pass
     @staticmethod
     def do(boy):
         boy.frame = (boy.frame + 1) % 8
         boy.x += boy.dir * 5
         pass
     @staticmethod
     def draw(boy):
         boy.image.clip_draw(boy.frame * 44, boy.action * 69, 44, 69, boy.x, boy.y)

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
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()