"""Logic for factory movements with manhattan distance of 4"""
from collections import deque
from config import directionMap

def deploy_scouts(obs, config):
    pass

# Used BFS algorithm to pridict most optimized path
# Did not take south boundary shrinking condition
def move(row, col, southBound, width, walls):
    currIndex = (row - southBound) * width + col

    # For handling vis out of bound
    minCol = min(0, col - 4)
    minRow = southBound
    
    dirWts = [0] * 4
    vis = [[0] * 9] * 9
    q = deque()

    vis[row][col] = 1

    if col - 1 >= 0 and (walls[currIndex] & 8):
        q.append([3, row, col-1])

    if col + 1 < width and (walls[currIndex] & 2):
        q.append([1, row, col+1])

    if (walls[currIndex] & 1):
        q.append([0, row+1, col])

    while q:
        dir, r, c = q.popleft()

        if vis[r-minRow][c-minCol]: continue
        vis[r-minRow][c-minCol] = 1

        dirWts[dir] = abs(r - row)

        if c-1 >= 0 and (walls[r][c] & 8):
            q.append([dir, r, c-1])

        if c+1 < width and (walls[r][c] & 2):
            q.append([dir, r, c+1])

        if (walls[r][c] & 1):
            q.append([dir, r, c+1])

    result, wt = "", 0.5
    for i in range(4):
        if dirWts[i] > wt:
            wt = dirWts
            result = directionMap[i]

    return result