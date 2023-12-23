from collections import defaultdict, deque


def collapse_grid_into_junction_graph(
    grid: list[list[str]], start: tuple[int, int], end: tuple[int, int]
) -> dict[tuple[int, int], dict[tuple[int, int], int]]:
    dir_offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    dists = defaultdict(dict)
    seen_nodes = set()

    # cell pos, distance traveled so far, previous cell pos, previous junction node
    q = deque([(start, 0, (-1, -1), start)])
    while q:
        (x, y), d, (px, py), j = q.popleft()

        neighbours = []
        for dx, dy in dir_offsets:
            nx, ny = x + dx, y + dy
            # ensure we don't go backwards
            if (nx, ny) == (px, py):
                continue

            # ensure we don't go off the grid
            if not (0 <= nx < len(grid[0]) and 0 <= ny < len(grid)):
                continue

            # ensure we only move on valid cells
            if grid[ny][nx] in ".<^>v":
                neighbours.append((nx, ny))

        # check if we are at a junction node
        if len(neighbours) > 1 or (x, y) == end:
            dists[j][(x, y)] = d
            dists[(x, y)][j] = d

            j = (x, y)
            d = 0

            if (x, y) in seen_nodes:
                continue
            else:
                seen_nodes.add((x, y))

        for nx, ny in neighbours:
            q.append(((nx, ny), d + 1, (x, y), j))

    return dists


def get_longest_path_dfs(
    start: tuple[int, int],
    end: tuple[int, int],
    graph: dict[tuple[int, int], dict[tuple[int, int], int]],
) -> int:
    seen = set([start])
    stack = [(start, 0, seen)]
    mx = 0
    while stack:
        pos, dist, seen = stack.pop()
        if pos == end:
            mx = max(mx, dist)
        for next, d in graph[pos].items():
            if next not in seen:
                stack.append((next, dist + d, seen | set([next])))
    return mx


grid = [list(line.strip()) for line in open("input.txt")]

start = (1, 0)
end = (len(grid[0]) - 2, len(grid) - 1)

graph = collapse_grid_into_junction_graph(grid, start, end)
longest_path = get_longest_path_dfs(start, end, graph)

print(longest_path)
