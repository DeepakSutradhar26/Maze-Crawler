"""Logic for factory movements with manhattan distance of 4"""
from robots.robot import Robot

# Used BFS algorithm to pridict most optimized path
# Did not take south boundary shrinking condition
class Factory:
    @staticmethod
    def move(row, col, obs, config, prevAction):
        return Robot.move(0, row, col, row, col, obs, config, prevAction)
    
    @staticmethod
    def jumpNorth():
        return "JUMP_NORTH"

    @staticmethod
    def buildScout():
        return "BUILD_SCOUT"

    @staticmethod
    def buildWorker():
        return "BUILD_WORKER"
    
    @staticmethod
    def buildMiner():
        return "BUILD_MINER"