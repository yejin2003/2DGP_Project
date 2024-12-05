from fontTools.merge.util import current_time
from pico2d import *
import math

import game_framework
import game_world
import grass
from statemachine import start_event, a_down, a_up, d_down, d_up, s_down, s_up, space_down, space_up, StateMachine, time_out, attacked
import server

PIXEL_PER_METER = (10.0 / 0.2)  # 10 pixel 20 cm
RUN_SPEED_KMPH = 20  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Idle:
    @staticmethod
    def enter(boy, e):
        boy.cur_state = Idle
        if isinstance(boy.state_machine.cur_state, Run):  # Run 상태에서 전환된 경우
            boy.action = 10
            boy.dir = boy.dir1  # dir1 값으로 Idle 상태에서 방향 설정
        else:
            boy.frame = 2
            boy.action=10
        boy.wait_time = get_time()

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        if get_time() - boy.wait_time > 3:
            boy.state_machine.handle_event(('TIME_OUT', 0))
        boy.frame = 2

    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_composite_draw(
                boy.frame * 61, boy.action * 71, 60, 78, 0, 'h', boy.x, 90, 62, 75
            )
        else:
            boy.image.clip_draw(
                boy.frame * 61, boy.action * 71, 60, 78, boy.x, 90 ,62, 75
            )


class Run:
    @staticmethod
    def enter(boy, e):
        boy.cur_state = Run
        boy.is_moving=True
        if d_down(e) or a_up(e):
            boy.dir1, boy.action = 1, 9  # 오른쪽 이동
            boy.dir2=0
        elif a_down(e) or d_up(e):
            boy.dir1, boy.action = -1, 9  # 왼쪽 이동
            boy.dir2 = 0

    @staticmethod
    def exit(boy, e):
        boy.is_moving = False
        boy.dir = boy.dir1
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 4
        boy.x += boy.dir1 * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(boy):
        if boy.dir1 == 1:
            boy.image.clip_composite_draw(
                boy.frame * 62, boy.action * 68, 62, 72, 0, 'h', boy.x, 90, 62, 69
            )
        else:
            boy.image.clip_draw(
                boy.frame * 62, boy.action * 68, 62, 72, boy.x, 90, 62, 69
            )

class Attack:
    @staticmethod
    def enter(boy, e):
        boy.cur_state = Attack
        boy.is_Attack=True
        if isinstance(boy.state_machine.cur_state, Run):  # Run 상태에서 전환된 경우
            boy.dir = boy.dir1  # Run 상태의 방향을 유지
            boy.action=7
        else:
            boy.frame = 0
            boy.action=7
        if isinstance(boy.state_machine.cur_state, Jump):  # Run 상태에서 전환된 경우
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
                boy.frame * 62, boy.action * 65, 63, 72, 0, 'h', boy.x, 90, 62, 69
            )
        else:  # 왼쪽
            boy.image.clip_draw(
                boy.frame * 62, boy.action * 65, 63, 72, boy.x, 90
            )

class Jump:
    @staticmethod
    def enter(boy, e):
        boy.cur_state = Jump
        boy.jump_velocity = 10
        boy.is_jumping=True
        if space_down(e): #스페이스키를 눌러서 점프 시작
            boy.action=9
            boy.jump_velocity = 10
        if d_down(e):
            boy.dir=-1
        if a_down(e):
            boy.dir=1

    @staticmethod
    def exit(boy, e):
        boy.dir = boy.dir1
        boy.cur_state = Idle
        pass

    @staticmethod
    def do(boy):
        boy.x +=boy.dir*RUN_SPEED_PPS*game_framework.frame_time
        boy.y += boy.jump_velocity
        boy.jump_velocity += boy.gravity

        if boy.y <= 90:  # 점프가 끝났을 때
            boy.is_jumping = False
            boy.on_ground= True
            boy.jump_velocity = 0
            boy.y = 90
            boy.dir=0 #정지 상태로 만들어주기


    @staticmethod
    def draw(boy):
        if boy.dir1 == 1:
            boy.image.clip_composite_draw(
                boy.frame * 62, boy.action * 68, 62, 72, 0, 'h', boy.x, boy.y, 62, 69
            )
        else:
            boy.image.clip_draw(
                boy.frame * 62, boy.action * 68, 62, 72, boy.x, boy.y, 62, 69
            )

class Attacked:
    @staticmethod
    def enter(boy, e):
        boy.cur_state = Attacked
        boy.start_time=get_time()
        boy.is_moving=False
        boy.frame=2
        if isinstance(boy.state_machine.cur_state, Run):  # Run 상태에서 전환된 경우
            boy.dir = boy.dir1  # Run 상태의 방향을 유지
            boy.action=1
        if isinstance(boy.state_machine.cur_state, Idle):  # Idle 상태에서 전환된 경우
            boy.dir = boy.dir1  # Run 상태의 방향을 유지
            boy.action=1
        if isinstance(boy.state_machine.cur_state, Attack):  # Idle 상태에서 전환된 경우
            boy.dir = boy.dir1  # Run 상태의 방향을 유지
            boy.action =1
        pass

    @staticmethod
    def exit(boy, e):
        if boy.hp > 0:  # HP가 남아있을 경우
            boy.hp -= 1  # HP 감소
            boy.is_Attacked = False
            print(f"Attacked 상태 종료. 현재 HP: {boy.hp}")

        if boy.hp <= 0:  # HP가 0일 경우 게임 종료
            print("게임 종료")
            game_framework.quit()
        pass

    @staticmethod
    def do(boy):
        current_time=get_time()
        if current_time-boy.frame_update_time>=0.10:
            boy.frame_update_time=current_time
            boy.frame = boy.frame % 4 + 2

            if get_time()-boy.start_time>1.2:
                boy.frame=3

        if boy.is_Attacked:
            boy.attacked_back()

        boy.attacked_time -= pico2d.get_time() - boy.last_time
        if boy.attacked_time<=0:
            boy.is_Attacked=False
            boy.attacked_time = 0
            boy.state_machine.add_event(('TIME_OUT', 0))
            print("무적 상태 해제")

        boy.last_time=get_time()

    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_composite_draw(
                boy.frame * 65, 7, 60, 72, 0, 'h', boy.x, 90, 62, 69
            )
        else:
            boy.image.clip_draw(
                boy.frame * 65, 7, 60, 72, boy.x, 90, 62, 69
            )
        pass

class Boy:
    def __init__(self):
        self.x, self.y = 20, server.grass2.gy+30
        self.max = 800 - 10
        self.min = 10
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.hp=3
        self.cur_state= Idle
        self.jump_velocity = 10
        self.jump_height = 10
        self.gravity = -1
        self.is_jumping = False
        self.is_moving= True
        self.on_ground= False
        self.is_Attacked=False
        self.frame_update_time=0
        self.last_time=0
        self.attacked_time=0
        self.image = load_image('img/boy.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {d_down: Run, a_down: Run, a_up: Idle, d_up: Idle, space_down: Jump, space_up: Jump, s_down: Attack, s_up: Idle, attacked:Attacked},
                Run: {d_down: Idle, a_down: Idle, d_up: Idle, a_up: Idle, space_down: Jump, space_up: Jump, s_down: Attack, s_up: Attack, attacked: Attacked},
                Attack: {s_down: Idle, s_up: Idle},
                Jump: {space_down: Jump, space_up: Jump, d_down: Idle, a_down:Idle, a_up:Idle, d_up:Idle, s_down:Attack, attacked: Attacked},
                Attacked: {time_out: Idle}
            }
        )

    def update(self):
        self.state_machine.update()
        if self.x <= self.min:  # 최소 경계
            self.x = self.min
            self.dir = 1  # 오른쪽으로 방향 전환
        elif self.x >= self.max:  # 최대 경계
            self.x = self.max
            self.dir = -1

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))
        if event.type == 'LAND':  # 점프가 끝난 경우
            self.cur_state = Idle
            self.cur_state.enter(self.boy, event)

    def draw(self):
        draw_rectangle(*self.get_bb())
        self.state_machine.draw()

    def get_bb(self):
        # fill here
        return self.x - 20, self.y - 20, self.x + 20, self.y + 40
        pass

    def attacked_back(self):
        self.x-=20
        pass

    def handle_collision(self, group, other):
        if group == 'grass:boy':
            self.is_jumping = False
            self.on_ground = True

        if group in ('snake:boy', 'snail:boy'):  # snake와 snail 공통 처리
            if not self.is_Attacked:  # 무적 상태가 아닌 경우
                if self.cur_state in (Idle, Run, Jump):  # 현재 상태 체크
                    self.is_Attacked = True  # 무적 상태 활성화
                    self.attacked_time = 2.0  # 무적 시간 초기화
                    self.last_time = get_time()  # 시간 기록
                    self.state_machine.add_event(('ATTACKED', 0))  # Attacked 상태 전환
                    print(f"충돌 발생: {group}, 현재 HP: {self.hp}, 무적 상태 시작")

            if self.cur_state == Attack:  # 공격 상태인 경우
                print(f"소년의 공격 성공: {group}")
                other.shrink()  # 다른 객체에 공격 효과 적용

        if group =='bomb:boy':
            if self.cur_state in (Idle, Run, Jump, Attack):  # 현재 상태 체크
                self.is_Attacked = True  # 무적 상태 활성화
                self.attacked_time = 2.0  # 무적 시간 초기화
                self.last_time = get_time()  # 시간 기록
                self.state_machine.add_event(('ATTACKED', 0))  # Attacked 상태 전환
                print(f"충돌 발생: {group}, 현재 HP: {self.hp}, 무적 상태 시작")
            pass
