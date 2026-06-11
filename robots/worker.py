"""Ability to change the maze when it is not favorable"""
from robots.robot import Robot

# Did not consider the case when opponent build the wall in my path
class Worker:
    @staticmethod
    def move(
        workerRow, workerCol, factoryRow, factoryCol, obs, config, prevAction
        ):
        return Robot.move(
            1, workerRow, workerCol, factoryRow, factoryCol, obs, config, prevAction
            )

    @staticmethod
    def breakWall(workerRow, workerCol, obs, config):
        factoryIndex = (workerRow - obs.southBound) * config.width + workerCol

        maxWt, optimalDir = 0, ""

        def compare(a, b, c, d):
            if a < c:
                a = c
                b = d
            return a, b

        if obs.walls[factoryIndex] & 1 and workerRow+1 <= obs.northBound:
            dir, wt = Robot.move(
                0, workerRow+1, workerCol, workerRow+1, workerCol, obs, config, "NORTH"
            )
            maxWt, optimalDir = compare(maxWt, optimalDir, wt, dir)
        
        if obs.walls[factoryIndex] & 2 and workerCol+1 < config.width:
            dir, wt = Robot.move(
                0, workerRow, workerCol+1, workerRow, workerCol+1, obs, config, "EAST"
            )
            maxWt, optimalDir = compare(maxWt, optimalDir, wt, dir)

        if obs.walls[factoryIndex] & 8 and workerCol-1 >= 0:
            dir, wt = Robot.move(
                0, workerRow, workerCol-1, workerRow, workerCol-1, obs, config, "WEST"
            )
            maxWt, optimalDir = compare(maxWt, optimalDir, wt, dir)

        return "REMOVE_DIR_" + optimalDir
