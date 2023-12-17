from collections import defaultdict
from heapq import heappop, heappush
from math import inf


def crucible_dijkstra(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])

    dirs = {"N": (-1, 0), "S": (1, 0), "W": (0, -1), "E": (0, 1)}

    # Usually we would just store the (x,y) pos of the nodes in order to lookup
    # the shortest distance. However, in this case we also need to store the direction
    # the crucible came from and the amount of straight steps it took. This will help
    # us decide which direction to go next (we cannot go straight more than 3 times)
    distances = defaultdict(lambda: inf)
    distances[(0, 0, None, 0)] = 0

    # We use a priority queue to store the nodes we need to visit next.
    # cost, x, y, prev_x, prev_y, prev_dir, straight_steps
    pq = [(0, 0, 0, -1, -1, None, 0)]

    while pq:
        cost, x, y, prev_x, prev_y, prev_dir, straight_steps = heappop(pq)
        # print(cost, x, y, prev_x, prev_y, prev_dir, straight_steps)

        if (x, y) == (cols - 1, rows - 1) and straight_steps == 4:
            return cost

        for direction, (dx, dy) in dirs.items():
            nx, ny = x + dx, y + dy

            # Ensure we cannot move backwards
            if (nx, ny) == (prev_x, prev_y):
                continue

            # Ensure we do not go out of bounds
            if not (0 <= nx < cols and 0 <= ny < rows):
                continue

            if straight_steps < 4 and direction != prev_dir and prev_dir is not None:
                continue

            if straight_steps == 10 and direction == prev_dir:
                continue

            new_straight_steps = straight_steps + 1 if prev_dir == direction else 1
            new_cost = cost + grid[ny][nx]
            # print("NSS", new_straight_steps, new_cost)

            if new_cost < distances[(nx, ny, direction, new_straight_steps)]:
                distances[(nx, ny, direction, new_straight_steps)] = new_cost
                heappush(pq, (new_cost, nx, ny, x, y, direction, new_straight_steps))


grid = [list(map(int, list(line.strip()))) for line in open("input.txt", "r")]

cost = crucible_dijkstra(grid)
print("Least amount of heat loss that can be achieved:", cost)
