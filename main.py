"""Crawl starter agent: build a worker, march north, knock down walls."""
from robots.factory import Factory
from robots.worker import Worker

prevActions = {}

def agent(obs, config):
    global prevActions
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
                workers.append([uid, row, col])

    rtype, col, row, energy = factoryData[0], factoryData[1], factoryData[2], factoryData[3]
    build_cd = factoryData[7]

    index = (row - obs.southBound) * config.width + col 

    direction, _ = Factory.move(
        row, col, obs, config, prevActions.get(factoryUid, None)
        )
    
    actions[factoryUid] = direction

    if has_worker:
        # Worker Logic
        minUid, minCol, minRow = -1, 1000, 1000

        for workerUid, workerRow, workerCol in workers:
            prevDist = abs(minRow - row) + abs(minCol - col)
            currDist = abs(workerRow - row) + abs(workerCol - col)
            if prevDist > currDist:
                minRow = workerRow
                minCol = workerCol
                minUid = workerUid

        workerAction, _ = Worker.move(
            minRow, minCol, row, col, obs, config, prevActions.get(minUid, None)
            )
        
        if workerAction == "BREAK_WALL":
            actions[minUid] = Worker.breakWall(
                minRow, minCol, obs, config
                )
        else:
            actions[minUid] = workerAction
    elif build_cd == 0:
        actions[factoryUid] = Factory.buildWorker()
    elif not obs.walls[index] & 2:
        actions[factoryUid] = "EAST"

    prevActions = actions

    return actions