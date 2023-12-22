from collections import deque
from math import ceil


def grid_bfs(
    grid: list[list[str]],
    origin: tuple[int, int],
    max_steps: int,
    ignore_oob: bool = False,
) -> int:
    queue = deque([(0, origin)])
    visited = set()
    tot = 0
    parity = max_steps % 2

    height, width = len(grid), len(grid[0])

    while queue:
        steps, (x, y) = queue.popleft()
        if steps > max_steps:
            break

        if (x, y) in visited:
            continue

        if steps % 2 == parity:
            tot += 1

        visited.add((x, y))

        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nx, ny = x + dx, y + dy

            # Check if the new point is within the sketch.
            # OOB = Out of bounds only needed for part 2
            if not ignore_oob and (
                nx < 0 or nx >= len(grid[0]) or ny < 0 or ny >= len(grid)
            ):
                continue

            cond = (
                grid[ny % height][nx % width] != "#"
                if ignore_oob
                else grid[ny][nx] != "#"
            )
            if cond:
                queue.append((steps + 1, (nx, ny)))

    return tot


grid = [line.strip() for line in open("input.txt", "r")]

# Find starting point
origin = None
for y, row in enumerate(grid):
    for x, c in enumerate(row):
        if c == "S":
            origin = (x, y)
            break
    if origin:
        break

reachable_cells_part_1 = grid_bfs(grid, origin, 64)
print(f"Reachable garden plots in 65 steps:{reachable_cells_part_1}")


# Part 2 is actually a quadratic sequence problem (VS Code code minimap helped me to spot it)
# We can use the first 3 values to find the coefficients
# and then calculate the reachable cells at n*H steps (26501365 / H)
# https://math.libretexts.org/Bookshelves/Precalculus/Corequisite_Companion_to_Precalculus_%28Freidenreich%29/8%3A_Problem_Solving/8.04%3A_Quadratic_Sequences


def f(n, a, b, c):
    # A*n**2 + B*n + C
    A = ((c - b) - (b - a)) // 2
    B = (b - a) - 3 * A
    C = a - B - A

    return A * n**2 + B * n + C


height, width = len(grid), len(grid[0])
mod = 26501365 % height
distances = [mod, mod + height, mod + 2 * height]
vals = [grid_bfs(grid, origin, d, ignore_oob=True) for d in distances]

reachable_cells_part_2 = f(ceil(26501365 / height), *vals)
print(f"Reachable garden plots in 26501365 steps:{reachable_cells_part_2}")
