"""Logic common to all bots"""
from collections import deque

class Robot:
    directionMap = {
        0 : "NORTH",
        1 : "EAST",
        2 : "SOUTH",
        3 : "WEST"
    }

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

        # def saveEnergy(row, obs, config):
        #     distance = row - obs.southBound
        #     turnsLeft = config.episodeSteps - obs.step
        #     rateBoundary = config.scrollStartInterval + \
        #         obs.step * (config.scrollEndInterval - \
        #         config.scrollStartInterval)/config.scrollRampSteps
        #     return distance > turnsLeft/rateBoundary

        currIndex = (row - obs.southBound) * config.width + col

        if rtype == 2:
            if row == factoryRow and col == factoryCol and obs.walls[currIndex] & 1:
                return "BREAK_WALL", 0

        # For handling vis out of bound
        minCol     = max(0, col - 4)
        minRow     = max(obs.southBound, row - 4)
        leftBound  = max(0, col - 4)
        rightBound = min(config.width - 1, col + 4)
        upperBound = min(obs.northBound, row + 4)
         
        dirWts = [0] * 4
        vis = [[0] * 9 for _ in range(9)]
        q = deque()

        vis[row-minRow][col-minCol] = 1

        if col - 1 >= 0 and not (obs.walls[currIndex] & 8):
            q.append([3, row, col-1])

        if col + 1 < config.width and not (obs.walls[currIndex] & 2):
            q.append([1, row, col+1])

        if row + 1 <= obs.northBound and not (obs.walls[currIndex] & 1):
            q.append([0, row+1, col])

        while q:
            dir, r, c = q.popleft()

            if vis[r-minRow][c-minCol]: continue
            vis[r-minRow][c-minCol] = 1

            workerWt = 10 * (factoryRow == r and factoryCol == c) if rtype == 2 else 0

            dirWts[dir] = abs(r - row) + workerWt

            index = (r - obs.southBound) * config.width + c

            if c-1 >= leftBound and not (obs.walls[index] & 8):
                q.append([dir, r, c-1])

            if c+1 <= rightBound and not (obs.walls[index] & 2):
                q.append([dir, r, c+1])

            if r+1 <= upperBound and not (obs.walls[index] & 1):
                q.append([dir, r+1, c])

        prevIndex = next((k for k,v in Robot.directionMap.items() if v == prevAction), None)

        def reverseDirection(index):
            if prevAction is None:
                return False
            if prevIndex is None:
                return False
            return abs(index - prevIndex) == 2

        result, wt = "", 0

        if rtype == 0:
            result = "IDLE"
        else:
            result = "BREAK_WALL"


        for i in range(4):
            if dirWts[i] > wt and not reverseDirection(i):
                wt = dirWts[i]
                result = Robot.directionMap[i]

        return result, wt