"""Crawl starter agent: build a worker, march north, knock down walls."""
from bots.factory import move

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
            direction = move(row, col, obs.southBoud, config.width, obs.walls)
            if len(direction) > 0:
                actions[uid] = direction
            else:
                # Deploy Worker
                pass
        
    return actions