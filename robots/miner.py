"""Generates 50 unit energy per turn from mining nodes"""
from robots.robot import Robot

class Miner:
    @staticmethod
    def move(row, col, obs, config, prevAction):
        return Robot.move(3, row, col, -1, -1, obs, config, prevAction)

    @staticmethod
    def transform():
        return "TRANSFORM"