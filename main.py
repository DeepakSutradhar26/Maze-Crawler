"""Crawl starter agent: build a worker, march north, knock down walls."""
from robots.factory import Factory
from robots.worker import Worker
from robots.miner import Miner
from robots.robot import Robot

prevActions = {}
minerTransform = {}
prevRow, prevCol = 0, 0

def agent(obs, config):
    global prevActions, prevRow, prevCol
    actions = {}

    miners = []
    workers = []

    factoryUid, factoryData = None, None

    # Mines Location
    mines = []
    for key, val in obs.mines.items():
        if val[2] == obs.player:
            rowMine, colMine = key.split(',')
            mines.append[rowMine, colMine]

    # Search Workers
    for uid, data in obs.robots.items():
        if data[4] == obs.player:
            rtype, col, row = data[0], data[1], data[2]

            if rtype == 0:
                factoryUid, factoryData = uid, data
            elif rtype == 2:
                workers.append([uid, row, col])
            elif rtype == 3:
                miners.append([uid, row, col])

    # Factory Information
    rtype, col, row, energy = factoryData[0], factoryData[1], factoryData[2], factoryData[3]
    build_cd = factoryData[7]

    # Factory Direction
    direction, _ = Factory.move(
        row, col, obs, config, prevActions.get(factoryUid, None)
        )

    # Cooldown, Index And Enegy Constraints
    isMoving = (row + 1 == prevRow and col == prevCol)

    # Miner Logic
    adjx = [-1, 0, 1, 0]
    adjy = [0, 1, 0, -1]
    minerRowInd = -1
    factoryNeighbour = False
    for minerUid, minerRow, minerCol in miners:
        for i in len(adjx):
            ni = row + adjx[i]
            nj = col + adjy[i]

            if ni>=obs.southBound and ni<obs.northBound and nj>=0 and nj<config.width:
                if ni == minerRow and nj == minerCol:
                    actions[minerUid] = Miner.transfer(Robot.directionMap[i])
                    factoryNeighbour = True
                    minerRowInd = minerRow

        if not minerTransform.get(minerUid, False):
            for mineRow, mineCol in mines:
                if minerRow == mineRow and minerCol == mineCol:
                    actions[minerRow][minerCol] = Miner.transform()
        else:
            actions[minerUid] = Miner.move(
                minerRow, minerCol, -1, -1, obs, config, prevActions[minerUid]
            )
    
    # Factory Movement And Spawn Worker
    if direction == "IDLE" and build_cd == 0 and row < obs.northBound-1:
        actions[factoryUid] = Factory.jumpNorth()

    elif isMoving and len(workers) < 1 and energy > Worker.cost and row < obs.northBound-1:
        actions[factoryUid] = Factory.buildWorker()

    elif direction == "IDLE" and not isMoving and row < obs.northBound-1:
        actions[factoryUid] = "SOUTH"
    
    elif factoryNeighbour and Robot.profitableEnergy(9, minerRowInd, 1, obs, config):
        actions[factoryUid] = "IDLE"

    else:
        actions[factoryUid] = direction

    # Worker Logic
    if len(workers):
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