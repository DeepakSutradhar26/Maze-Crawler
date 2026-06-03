"""Crawl starter agent: build a worker, march north, knock down walls."""
from bots.factory import north_possible

def agent(obs, config):
    actions = {}
    width = config.width
    my_robots = {
        uid: data for uid, data in obs.robots.items()
        if data[4] == obs.player
    }

    for uid, data in my_robots.items():
        rtype, col, row, energy = data[0], data[1], data[2], data[3]
        build_cd = data[7] if len(data) > 7 else 0

        if rtype == 0:
            index = (row - obs.southBound) * config.width + col
            if north_possible(index, obs.walls):
                actions[uid] = "NORTH"
        
    return actions