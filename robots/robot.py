"""Logic common to all bots: Dijistra Algorithm"""
import math
from collections import deque

class Robot:
    directionMap = {
        0 : "NORTH",
        1 : "EAST",
        2 : "SOUTH",
        3 : "WEST"
    }

    @staticmethod
    def getTurnsLeft(row, obs, config):
        distance = row - obs.southBound
        initialChange = config.scrollStartInterval
        rateOfChange = (config.scrollEndInterval - \
            config.scrollStartInterval)/config.scrollRampSteps
        turns = (-initialChange + \
            math.sqrt(initialChange ** 2 + 2 * distance * rateOfChange))/rateOfChange
        return turns
    
    @staticmethod
    def profitableEnergy(profitNumber, rowMine, steps, obs, config):
        totalSteps = Robot.getTurnsLeft(rowMine, obs, config)
        miningSteps = 2*steps - 1 + profitNumber
        return miningSteps < totalSteps
    
    @staticmethod
    def reverseDirection(prevIndex, prevAction, index):
        if prevAction is None:
            return False
        if prevIndex is None:
            return False
        return abs(index - prevIndex) == 2

    @staticmethod
    def move(
        rtype,
        row,
        col,
        factoryRow,
        factoryCol,
        obs,
        config,
        prevAction
        ):

        minerPresent = False
        # Put Mines In Map
        if rtype == 0:
            mines = {}

            for key, val in obs.mines.items():
                if val[2] == obs.player:
                    rowMine, colMine = key.split(',')
                    mines[(rowMine, colMine)] = val[1]

            for _, data in obs.robots.items():
                if data[4] == obs.player:
                    rtype, col, row = data[0], data[1], data[2]
                    if rtype == 3:
                        minerPresent = True          

        currIndex = (row - obs.southBound) * config.width + col

        if rtype == 2:
            if row == factoryRow and col == factoryCol and obs.walls[currIndex] & 1:
                return "BREAK_WALL", 0

        # For Out Of Bound
        minCol     = max(0, col - 4)
        minRow     = max(obs.southBound, row - 4)
        leftBound  = max(0, col - 4)
        rightBound = min(config.width - 1, col + 4)
        upperBound = min(obs.northBound, row + 4)
         
        dirWts = [0] * 4
        dis = [[float('inf')] * 9 for _ in range(9)]
        q = deque()

        dis[row-minRow][col-minCol] = 0

        if col - 1 >= 0 and not (obs.walls[currIndex] & 8):
            dis[row-minRow][col-1-minCol] = 1
            q.append([3, 1, row, col-1])

        if col + 1 < config.width and not (obs.walls[currIndex] & 2):
            dis[row-minRow][col+1-minCol] = 1
            q.append([1, 1, row, col+1])

        if row + 1 <= obs.northBound and not (obs.walls[currIndex] & 1):
            dis[row+1-minRow][col-minCol] = 1
            q.append([0, 1, row+1, col])

        while q:
            dir, steps, r, c= q.popleft()

            # Scoring Strategy
            factoryWt = abs(r - row) if not rtype == 3 else 0
            workerWt = 5 * (factoryRow == r and factoryCol == c) if rtype == 2 else 0
            minerWt = 10 * mines.get((r, c), 0)/(config.mineMaxEnergy * steps)

            isProfitableEnergy = Robot.profitableEnergy(9, r, steps, obs, config)

            if rtype == 0 and not minerPresent and isProfitableEnergy:
                return "BUILD_MINER"

            dirWts[dir] = factoryWt + workerWt if not isProfitableEnergy else minerWt 

            index = (r - obs.southBound) * config.width + c

            if obs.walls[index] == -1: continue

            if c-1 >= leftBound and not (obs.walls[index] & 8):
                if dis[r-minRow][c-1-minCol] > dis[r-minRow][c-minCol]+1:
                    dis[r-minRow][c-1-minCol] = dis[r-minRow][c-minCol]+1
                    q.append([dir, steps+1, r, c-1])

            if c+1 <= rightBound and not (obs.walls[index] & 2):
                if dis[r-minRow][c+1-minCol] > dis[r-minRow][c-minCol]+1:
                    dis[r-minRow][c+1-minCol] = dis[r-minRow][c-minCol]+1
                    q.append([dir, steps+1, r, c+1])

            if r+1 <= upperBound and not (obs.walls[index] & 1):
                if dis[r+1-minRow][c-minCol] > dis[r-minRow][c-minCol]+1:
                    dis[r+1-minRow][c-minCol] = dis[r-minRow][c-minCol]+1
                    q.append([dir, steps+1, r+1, c])

        prevIndex = next((k for k,v in Robot.directionMap.items() if v == prevAction), None)

        result, wt = "", 0

        if rtype == 0:
            result = "IDLE"
        elif rtype == 3:
            result = "IDLE"
        else:
            result = "BREAK_WALL"

        for i in range(4):
            if dirWts[i] > wt and not Robot.reverseDirection(prevIndex, prevAction, i):
                wt = dirWts[i]
                result = Robot.directionMap[i]

        return result, wt