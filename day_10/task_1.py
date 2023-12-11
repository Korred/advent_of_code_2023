from collections import deque

sketch = [list(line.strip()) for line in open("input.txt", "r")]


def find_starting_point(sketch: list[list[str]]) -> tuple[int, int]:
    for y, line in enumerate(sketch):
        for x, char in enumerate(line):
            if char == "S":
                return x, y


OFFSET_CONNECTIONS_LKP = {
    (0, -1): {"|", "7", "F"},
    (0, 1): {"|", "L", "J"},
    (1, 0): {"-", "J", "7"},
    (-1, 0): {"-", "L", "F"},
}
VALID_NEIGHBOUR_OFFSETS = {
    "|": [(0, -1), (0, 1)],
    "-": [(1, 0), (-1, 0)],
    "L": [(0, -1), (1, 0)],
    "F": [(0, 1), (1, 0)],
    "J": [(0, -1), (-1, 0)],
    "7": [(0, 1), (-1, 0)],
    "S": [(0, -1), (0, 1), (1, 0), (-1, 0)],
}


def bfs_sketch(sketch: list[list[str]], start: tuple[int, int]) -> int:
    """
    Breadth-first search for the provided sketch where we return
    the number of steps needed to reach the furthest point from the
    starting point.
    """

    # We use a deque to store the points we need to visit.
    # We start with the starting point.
    points_to_visit = deque([start])
    visited = set()

    # We use a dictionary to store the distance from the starting point
    # to the current point.
    distances = {start: 0}

    while points_to_visit:
        x, y = points_to_visit.popleft()

        # Check if we have already visited the point.
        # e.g. a shorter path to the point has already been found.
        if (x, y) in visited:
            continue

        # We mark the point as visited.
        visited.add((x, y))

        # Check the neighbors of the current point.
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nx, ny = x + dx, y + dy

            # Check if the new point is within the sketch.
            if nx < 0 or nx >= len(sketch[0]) or ny < 0 or ny >= len(sketch):
                continue

            # Ignore ground
            if sketch[ny][nx] == ".":
                continue

            # Ignore visited
            if (nx, ny) in visited:
                continue

            # Check if the neighbour is reachable from the current point
            current = sketch[y][x]
            neighbour = sketch[ny][nx]
            if (dx, dy) not in VALID_NEIGHBOUR_OFFSETS[
                current
            ] or neighbour not in OFFSET_CONNECTIONS_LKP[(dx, dy)]:
                continue

            # We add the new point to the queue.
            points_to_visit.append((nx, ny))

            # We update the distance to the new point.
            distances[(nx, ny)] = distances[(x, y)] + 1

    max_distance = max(distances.values())

    return max_distance


start = find_starting_point(sketch)
max_distance = bfs_sketch(sketch, start)
print(start, max_distance)
