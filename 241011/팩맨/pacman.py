import copy
from collections import defaultdict

def inRange(r, c):
    return 0 <= r < 4 and 0 <= c < 4

def duplicate_monster():
    for rc, d in monsters.items():
        r, c = rc
        d = d
        maps_e[r][c].append(d)

def move_monster():
    temp = copy.deepcopy(monsters)
    for rc, direction in monsters.items():
        r, c = rc
        for idx, d in enumerate(direction):
            for i in range(8):
                nd = (d+i) % 8
                nr, nc = r + dr[nd], c + dc[nd]

                if inRange(nr, nc):
                    if len(maps_d[nr][nc]) > 0 or (nr == packman[0] and nc == packman[1]): continue
                    else:
                        temp[(r, c)].pop(idx)
                        temp[(nr, nc)].append(nd)
                        maps_m[r][c] -= 1
                        maps_m[nr][nc] += 1
                        break
    return temp

def move_packman(t, packman):
    # 3칸만 이동 (상하좌우) 하되, 몬스터를 가장 많이 먹을 수 있는 방향..
    r, c = packman
    dr, dc = [-1, 1, 0, 0], [0, 0, -1, 1]
    max_m = 0
    max_route = list()

    for i in range(4):
        for j in range(4):
            for k in range(4):
                temp = 0
                temp_route = list()
                nr, nc = r + dr[k], c + dc[k]

                if inRange(nr, nc):
                    temp += maps_m[nr][nc]
                    temp_route.append([nr, nc])

                    nr, nc = nr + dr[j], nc + dc[j]

                    if inRange(nr, nc):
                        temp += maps_m[nr][nc]
                        temp_route.append([nr, nc])

                        nr, nc = nr + dr[i], nc + dc[i]

                        if inRange(nr, nc):
                            temp += maps_m[nr][nc]
                            temp_route.append([nr, nc])

                            if max_m < temp:
                                max_m = temp
                                max_route = temp_route

    for route in max_route:
        r, c = route
        if maps_m[r][c] > 0:
            maps_d[r][c].append([maps_m[r][c], t + 2])
            maps_m[r][c] = 0
            monsters[(r, c)] = []
        packman = [r, c]
    return packman

def delete_deadmonster(t):
    for r in range(4):
        for c in range(4):
            dead = maps_d[r][c]
            for i, v in enumerate(dead):
                deadnum, deadt = v
                if deadt == t: dead.pop(i)

def born_monster():
    for r in range(4):
        for c in range(4):
            value = maps_e[r][c]
            for d in value:
                if d:
                    maps_m[r][c] += 1
                    monsters[(r, c)].append(d[0])
            maps_e[r][c] = []

m, time = map(int, input().split())
maps_m = [[0] * 4 for _ in range(4)]
maps_d = [[[] for _ in range(4)] for _ in range(4)]
maps_e = [[[] for _ in range(4)] for _ in range(4)]

# packman
r, c = map(int, input().split())
packman = [r-1, c-1]

dr, dc = [-1, -1, 0, 1, 1, 1, 0, -1], [0, -1, -1, -1, 0, 1, 1, 1]

monsters = defaultdict(list)
for idx in range(m):
    r, c, d = map(int, input().split())
    maps_m[r-1][c-1] += 1
    monsters[(r-1, c-1)].append(d-1)

for t in range(time):
    duplicate_monster()
    monsters = move_monster()
    packman = move_packman(t, packman)
    delete_deadmonster(t)
    born_monster()
    
answer = 0
for r in range(4):
    for c in range(4):
        answer += maps_m[r][c]
print(answer)