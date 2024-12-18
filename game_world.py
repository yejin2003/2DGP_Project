import boy
from snake import Snake

world = [[] for _ in range(4)]
collision_pairs={} # 빈 딕셔너리

def add_collision_pair(group,a,b):
    if group not in collision_pairs:
        print(f'Added new group {group}')
        collision_pairs[group]=[[],[]]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)


def add_object(o, depth = 0):
    world[depth].append(o)

def add_objects(ol, depth = 0):
    world[depth] += ol

def all_objects():
    for layer in world:  # 각 레이어를 순회
        for o in layer:  # 레이어 내의 객체를 순회
            yield o  # 객체를 반환

def update():
    for layer in world:
        for o in layer:
            o.update()


def render():
    for layer in world:
        for o in layer:
            o.draw()

def objects_at_layer(layer):
    return world[layer]

def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o) # world에서 o를 삭제
            remove_collision_object(o) #collision pairs에서 o를 삭제
            del o #메모리에서 객체 자체를 삭제
            return
    raise ValueError('Cannot delete non existing object')


def clear():
    for layer in world:
        layer.clear()

# fill here
def collide(a, b):
    left_a, bottom_a, right_a, top_a= a.get_bb()
    left_b, bottom_b, right_b, top_b= b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def handle_collisions():
    # for group, pairs in collision_pairs.items():
    #     for a in pairs[0]:
    #         for b in pairs[1]:
    #             if collide(a,b):
    #                 a.handle_collision(group,b)
    #                 b.handle_collision(group,a)
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    if hasattr(a, 'handle_collision'):
                        a.handle_collision(group, b)
                    if hasattr(b, 'handle_collision'):
                        b.handle_collision(group, a)

                    # 충돌 후 제거된 객체를 다시 처리하지 않도록 방지
                    if a not in all_objects() or b not in all_objects():
                        break  # 충돌 처리 종료