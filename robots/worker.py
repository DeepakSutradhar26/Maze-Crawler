"""Ability to change the maze when it is not favorable"""
from robots.robot import Robot

# Did not consider the case when opponent build the wall in my path
class Worker:
    @staticmethod
    def move(
        workerRow, workerCol, southBound, northBound, width, walls, factoryRow, factoryCol
        ):
        return Robot.move(
            1, workerRow, workerCol, southBound, northBound, width, walls, factoryRow, factoryCol
            )

    @staticmethod
    def breakWall(workerRow, workerCol, southBound, northBound, width, walls):
        factoryIndex = (workerRow - southBound) * width + workerCol

        maxWt, optimalDir = 0, ""

        def compare(a, b, c, d):
            if a < c:
                a = c
                b = d
            return a, b

        if walls[factoryIndex] & 1 and workerRow+1 <= northBound:
            dir, wt = Robot.move(
                0, workerRow+1, workerCol, southBound, northBound, width, walls, -1, -1
            )
            maxWt, optimalDir = compare(maxWt, optimalDir, wt, dir)
        
        if walls[factoryIndex] & 2 and workerCol+1 < width:
            dir, wt = Robot.move(
                0, workerRow, workerCol+1, southBound, northBound, width, walls, -1, -1
            )
            maxWt, optimalDir = compare(maxWt, optimalDir, wt, dir)

        if walls[factoryIndex] & 8 and workerCol-1 >= 0:
            dir, wt = Robot.move(
                0, workerRow, workerCol-1, southBound, northBound, width, walls, -1, -1
            )
            maxWt, optimalDir = compare(maxWt, optimalDir, wt, dir)

        return optimalDir
