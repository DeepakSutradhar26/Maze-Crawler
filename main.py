"""Crawl starter agent: build a worker, march north, knock down walls."""
from robots.factory import Factory
from robots.worker import Worker

def agent(obs, config):
    actions = {}

    workers = []
    has_worker = False

    factoryUid, factoryData = None, None

    for uid, data in obs.robots.items():
        if data[4] == obs.player:
            rtype, col, row = data[0], data[1], data[2]

            if rtype == 0:
                factoryUid, factoryData = uid, data
            elif rtype == 2:
                has_worker = True
                workers.append([uid, col, row])

    rtype, col, row, energy = factoryData[0], factoryData[1], factoryData[2], factoryData[3]
    build_cd = factoryData[7]

    index = (row - obs.southBound) * config.width + col 

    direction, _ = Factory.move(
        row, col, obs.southBound, obs.northBound, config.width, obs.walls
        )
    
    if len(direction) > 0:
        actions[factoryUid] = direction
    elif has_worker:
        # Worker Logic
        minUid, minCol, minRow = -1, 100, 100

        for workerUid, workerRow, workerCol in workers:
            prevDist = abs(minRow - row) + abs(minCol - col)
            currDist = abs(workerRow - row) + abs(workerCol - col)
            if prevDist > currDist:
                minRow = workerRow
                minCol = workerCol
                minUid = workerUid

        workerAction, _ = Worker.move(
            minRow, minCol, obs.southBound, obs.northBound, config.width, obs.walls, row, col
            )
        
        if workerAction == "break_wall":
            actions[minUid] = Worker.breakWall(
                minRow, minCol, obs.southBound, obs.northBound, config.width, obs.walls
                )
        else:
            actions[minUid] = workerAction
    elif build_cd == 0:
        actions[factoryUid] = Factory.buildWorker()
    elif not obs.walls[index] & 2:
        actions[factoryUid] = "EAST"
        
    print("obs:", obs)
    print("config:", config)
    print("wall:", obs.walls[index])
    print("actions:",actions)
    return actions