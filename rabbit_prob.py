class Config:
    def __init__(self, state, journey=None):
        self.state = state[:]
        if journey is None:
            self.journey = [state[:]]
        else:
            self.journey = journey[:] + [state[:]]

def isFinal(cfg):
    return cfg.state == ['W', 'W', 'W', '_', 'E', 'E', 'E']

def generateMoves(cfg):
    current = cfg.state
    results = []

    for pos in range(len(current)):
        if current[pos] == 'E':
            if pos + 1 < 7 and current[pos + 1] == '_':
                temp = current[:]
                temp[pos], temp[pos + 1] = '_', 'E'
                results.append(Config(temp, cfg.journey))
            if pos + 2 < 7 and current[pos + 2] == '_' and current[pos + 1] in ('E', 'W'):
                temp = current[:]
                temp[pos], temp[pos + 2] = '_', 'E'
                results.append(Config(temp, cfg.journey))

        elif current[pos] == 'W':
            if pos - 1 >= 0 and current[pos - 1] == '_':
                temp = current[:]
                temp[pos], temp[pos - 1] = '_', 'W'
                results.append(Config(temp, cfg.journey))
            if pos - 2 >= 0 and current[pos - 2] == '_' and current[pos - 1] in ('E', 'W'):
                temp = current[:]
                temp[pos], temp[pos - 2] = '_', 'W'
                results.append(Config(temp, cfg.journey))

    return results

def breadthSearch(start_input):
    explored = []
    queue = [Config(start_input)]

    while queue:
        current = queue.pop(0)
        if current.state in explored:
            continue
        explored.append(current.state)

        if isFinal(current):
            return current.journey

        nextSteps = generateMoves(current)
        for nxt in nextSteps:
            if nxt.state not in explored:
                queue.append(nxt)
    return None

def depthSearch(cfg, visited):
    if isFinal(cfg):
        return cfg.journey
    visited.append(cfg.state)

    nextSteps = generateMoves(cfg)
    for nxt in nextSteps:
        if nxt.state not in visited:
            result = depthSearch(nxt, visited)
            if result is not None:
                return result
    return None

initial_state = ['E', 'E', 'E', '_', 'W', 'W', 'W']

bfs_result = breadthSearch(initial_state)
print("BFS Solution Path:")
for step in bfs_result:
    print(step)

print("\n" + "-"*40 + "\n")

dfs_result = depthSearch(Config(initial_state), [])
print("DFS Solution Path:")
for step in dfs_result:
    print(step)

