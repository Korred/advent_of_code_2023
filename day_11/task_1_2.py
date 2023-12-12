from itertools import combinations

entries = [list(line.strip()) for line in open("input.txt", "r")]


def find_galaxies(entries: list[list[str]]) -> list[tuple[int, int]]:
    galaxies = []
    for y, row in enumerate(entries):
        for x, col in enumerate(row):
            if col == "#":
                galaxies.append([x, y])
    return galaxies


def manhattan_distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def find_empty_rows_cols(entries: list[list[str]]) -> tuple[list[int]]:
    empty_rows = [y for y, row in enumerate(entries) if row.count(".") == len(row)]

    empty_cols = [
        x
        for x in range(len(entries[0]))
        if [row[x] for row in entries].count(".") == len(entries)
    ]

    return empty_rows, empty_cols


galaxies = find_galaxies(entries)
empty_rows, empty_cols = find_empty_rows_cols(entries)


for e, multiplier in enumerate([2, 1000000]):
    dist_sum = 0
    for g1, g2 in combinations(galaxies, 2):
        dist = manhattan_distance(g1, g2)

        x_coords = sorted([g1[0], g2[0]])
        y_coords = sorted([g1[1], g2[1]])

        # empty rows between two galaxies generator count
        empty_cols_count = sum(
            1 for col in empty_cols if x_coords[0] < col < x_coords[1]
        )
        empty_rows_count = sum(
            1 for row in empty_rows if y_coords[0] < row < y_coords[1]
        )

        dist -= empty_cols_count
        dist -= empty_rows_count

        # add empty rows and cols count to distance
        dist += (empty_rows_count * multiplier) + (empty_cols_count * multiplier)

        dist_sum += dist

    print(f"Sum of all distances in Task {e+1} is: {dist_sum}")
