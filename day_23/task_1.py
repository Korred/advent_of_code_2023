from collections import deque

grid = [list(line.strip()) for line in open("input.txt")]
dir_offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
valid_slope = {">": (1, 0), "<": (-1, 0), "v": (0, 1), "^": (0, -1)}


start = (1, 0)
end = (len(grid[0]) - 2, len(grid) - 1)
dist = {}
q = deque([(start, 0, (-1, -1))])

while q:
    (x, y), d, (px, py) = q.popleft()

    for dx, dy in dir_offsets:
        nx, ny = x + dx, y + dy
        # ensure we don't go backwards
        if (nx, ny) == (px, py):
            continue

        # ensure we don't go off the grid
        if not (0 <= nx < len(grid[0]) and 0 <= ny < len(grid)):
            continue

        if grid[ny][nx] == "." or (
            grid[ny][nx] in valid_slope and valid_slope[grid[ny][nx]] == (dx, dy)
        ):
            q.append(((nx, ny), d + 1, (x, y)))
            dist[(nx, ny)] = max(d + 1, dist.get((nx, ny), 0))

print(dist[end])
