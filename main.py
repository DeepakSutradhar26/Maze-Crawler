"""Crawl starter agent: build a worker, march north, knock down walls."""
from robots.factory import Factory
from robots.worker import Worker

prevActions = {}
prevRow, prevCol = 0, 0

def agent(obs, config):
    global prevActions, prevRow, prevCol
    actions = {}

    workers = []
    has_worker = False

    factoryUid, factoryData = None, None

    # Search Workers
    for uid, data in obs.robots.items():
        if data[4] == obs.player:
            rtype, col, row = data[0], data[1], data[2]

            if rtype == 0:
                factoryUid, factoryData = uid, data
            elif rtype == 2:
                has_worker = True
                workers.append([uid, row, col])

    # Factory Information
    rtype, col, row, energy = factoryData[0], factoryData[1], factoryData[2], factoryData[3]
    build_cd = factoryData[7]

    # Factory Index
    index = (row - obs.southBound) * config.width + col 

    # Factory Direction
    direction, _ = Factory.move(
        row, col, obs, config, prevActions.get(factoryUid, None)
        )

    # Cooldown, Index And Enegy Constraints
    isMoving = (row + 1 == prevRow and col == prevCol)

    # Task: Write logic when factory is at northBound and Miner logic
    
    # Factory Movement And Spawn Worker
    if direction == "IDLE" and build_cd == 0:
        actions[factoryUid] = Factory.jumpNorth()

    elif isMoving and len(workers) < 1 and energy > Worker.cost:
        actions[factoryUid] = Factory.buildWorker()

    elif direction == "IDLE" and not isMoving:
        actions[factoryUid] = "SOUTH"
        
    else:
        actions[factoryUid] = direction

    # Worker Logic
    if has_worker:
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
            actions[minUid] = Worker.breakNorth()
        else:
            actions[minUid] = workerAction

    # Track Previous Actions
    prevRow, prevCol = row, col
    prevActions = actions

    return actions