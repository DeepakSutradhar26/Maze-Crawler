"""Logic for factory movements with manhattan distance of 4"""
from robots.robot import Robot

# Used BFS algorithm to pridict most optimized path
# Did not take south boundary shrinking condition
class Factory:
    @staticmethod
    def move(row, col, southBound, northBound, width, walls):
        return Robot.move(0, row, col, southBound, northBound, width, walls, row, col)

    @staticmethod
    def buildScout():
        return "BUILD_SCOUT"

    @staticmethod
    def buildWorker():
        return "BUILD_WORKER"
    
    @staticmethod
    def buildMiner():
        return "BUILD_MINER"