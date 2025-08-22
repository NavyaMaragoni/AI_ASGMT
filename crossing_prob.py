class Member:
    def __init__(self, name, time):
        self.name = name
        self.time = time

def allCrossed(state):
    return all(not p for p in state['left']) and state['torch'] == 'right'

def movePeople(current):
    states = []
    if current['torch'] == 'left':
        left = current['left']
        for i in range(len(left)):
            for j in range(i + 1, len(left)):
                p1, p2 = left[i], left[j]
                newLeft = left[:i] + left[i+1:j] + left[j+1:]
                newRight = current['right'] + [p1, p2]
                time = max(p1.time, p2.time)
                newState = {
                    'left': newLeft,
                    'right': newRight,
                    'torch': 'right',
                    'time': current['time'] + time,
                    'path': current['path'] + [f"{p1.name} and {p2.name} cross -> ({time} min)"]
                }
                states.append(newState)
    else:
        right = current['right']
        for k in range(len(right)):
            p = right[k]
            newRight = right[:k] + right[k+1:]
            newLeft = current['left'] + [p]
            time = p.time
            newState = {
                'left': newLeft,
                'right': newRight,
                'torch': 'left',
                'time': current['time'] + time,
                'path': current['path'] + [f"{p.name} returns <- ({time} min)"]
            }
            states.append(newState)
    return states

def bfsBridgeTorch(start):
    possibilities = [start]
    visited = []
    optimal = None

    while possibilities:
        current = possibilities.pop(0)
        key = (tuple(sorted([p.name for p in current['left']])), current['torch'])
        if key in visited:
            continue
        visited.append(key)

        if allCrossed(current):
            if optimal is None or current['time'] < optimal['time']:
                optimal = current
            continue

        nextMoves = movePeople(current)
        possibilities.extend(nextMoves)

    return optimal

def dfsBridgeTorch(current, visited, optimal):
    key = (tuple(sorted([p.name for p in current['left']])), current['torch'])
    if key in visited:
        return optimal
    visited.append(key)

    if allCrossed(current):
        if optimal is None or current['time'] < optimal['time']:
            return current
        return optimal

    nextMoves = movePeople(current)
    for nxt in nextMoves:
        optimal = dfsBridgeTorch(nxt, visited[:], optimal)
    return optimal

A = Member('A', 1)
B = Member('B', 2)
C = Member('C', 5)
D = Member('D', 10)

initialState = {
    'left': [A, B, C, D],
    'right': [],
    'torch': 'left',
    'time': 0,
    'path': []
}

bfs_result = bfsBridgeTorch(initialState)
print("BFS Bridge and Torch Path:")
for step in bfs_result['path']:
    print(step)
print(f"Total time: {bfs_result['time']} minutes")

print("\n" + "-"*40 + "\n")

dfs_result = dfsBridgeTorch(initialState, [], None)
print("DFS Bridge and Torch Path:")
for step in dfs_result['path']:
    print(step)
print(f"Total time: {dfs_result['time']} minutes")

