from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDL_KEYUP, SDLK_a, SDLK_d, SDLK_s


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

class StateMachine:
    def __init__(self, o):
        self.o = o
        self.event_que = []
        self.active_states = set()

    def add_event(self, e):
        self.event_que.append(e)

    def set_transitions(self, transitions):
        self.transitions = transitions

    def update(self):
        for state in self.active_states:
            state.do(self.o)

        if self.event_que:

            for state in list(self.active_states):
                e = self.event_que.pop(0)
                for check_event, next_state in self.transitions[state].items():
                    if check_event(e):
                        state.exit(self.o, e)
                        print(f'    exit from{state}')
                        self.active_states.discard(state)

                        self.active_states.add(next_state)
                        next_state.enter(self.o, e)
                        print(f'    enter into {next_state}')
                        break


    def start(self, start_states):
        for state in start_states:
            self.active_states.add(state)
            state.enter(self.o, ('START', 0))  # 더미 이벤트
            print(f'    enter into {state}')

    def draw(self, o):
        for state in self.active_states:
            state.draw(self.o)