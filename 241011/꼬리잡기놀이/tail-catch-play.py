import copy
from collections import defaultdict, deque

def inRange(r, c):
    return 0 <= r < n and 0 <= c < n

def make_route(team_id, route, n):
    q = deque()
    q.append(route[-1])
    visited[route[-1][0]][route[-1][1]] = True

    while q:
        r, c = q.pop()
        for i in range(4):
            nr, nc = r+dr[i], c+dc[i]
            if inRange(nr, nc) and visited[nr][nc] == False:
                if maps[nr][nc] == n:
                    q.append([nr, nc])
                    visited[nr][nc] = True
                    team_route[team_id].append([nr, nc])
                    team_v[team_id].append(n)

def move():
    global team_route
    for t_id, t_route in team_route.items():
        t_route.appendleft(t_route.pop())
        team_route[t_id] = t_route

        for i, tr in enumerate(t_route):
            nr, nc = tr[0], tr[1]
            maps[nr][nc] = team_v[t_id][i]

def meet_and_score(r, c):
    if maps[r][c] != 0 and maps[r][c] != 4:
        # 사람을 만났다.
        for t_id, tr in team_route.items():

            if [r, c] in tr:
                k = tr.index([r, c]) + 1

                team_score[t_id] += k ** 2


                tr = deque(reversed(tr))

                cnt = 0
                for tv in team_v[t_id]:
                    if tv != 4:
                        cnt += 1
                for i in range(cnt):
                    tr.appendleft(tr.pop())
                team_route[t_id] = tr


                return True
    return False

def check(type, num):
    if type == 1:
        for c in range(n):
            if meet_and_score(num-1, c): break
    elif type == 2:
        for r in range(n-1, -1, -1):
            if meet_and_score(r, num-1): break
    elif type == 3:
        for c in range(n-1, -1, -1):
            if meet_and_score(n-num, c): break
    elif type == 4:
        for r in range(n):
            if meet_and_score(r, n-num): break

def throw_ball(i):
    ni = i % (4*n)

    if 1 <= ni <= n:
        check(1, ni)
    elif n+1 <= ni <= 2*n:
        nni = ni % n
        if nni == 0: nni = n
        check(2, nni)
    elif 2*n+1 <= ni <= 3*n:
        nni = ni % n
        if nni == 0: nni = n
        check(3, nni)
    elif 3*n+1 <= ni <= 4*n or ni == 0:
        nni = ni % n
        if nni == 0: nni = n
        check(4, nni)

n, m, k = map(int, input().split())
maps = list()
for _ in range(n):
    maps.append(list(map(int, input().split())))

# 팀 구분하기
team_route = defaultdict(deque)
team_v = defaultdict(deque)
team_score = defaultdict(int)
idx = 0

# 팀별 머리사람 찾기
for r in range(n):
    for c in range(n):
        if maps[r][c] == 1:
            team_route[idx] = deque([[r, c]])
            team_v[idx] = deque([1])
            team_score[idx] = 0
            idx += 1

# 팀별 루트 저장
for team_id, route in team_route.items():
    visited = [[False] * n for _ in range(n)]
    dr, dc = [-1, 0, 1, 0], [0, -1, 0, 1]

    make_route(team_id, route, 2)
    make_route(team_id, route, 3)
    make_route(team_id, route, 4)

# 이동
for i in range(1, k+1):
    move()
    throw_ball(i)
answer = 0
for t_id, s in team_score.items():
    answer += s
print(answer)