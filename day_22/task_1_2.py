from collections import defaultdict
from dataclasses import dataclass
from re import compile

RE_BRICKS = compile(r"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)")


@dataclass
class Brick:
    p1: tuple[int, int, int]
    p2: tuple[int, int, int]


@dataclass
class Cube:
    x: int
    y: int
    z: int


def get_bricks() -> list[Brick]:
    # Extract bricks from input file
    bricks = []
    for line in open("input.txt", "r"):
        (x1, y1, z1, x2, y2, z2) = map(int, RE_BRICKS.match(line).groups())
        bricks.append(Brick((x1, y1, z1), (x2, y2, z2)))

    # Sort bricks by their first z coordinate
    # Looking at the example and real input it is guaranteed that
    # the first z coordinate of a brick is always smaller than the second one
    bricks.sort(key=lambda brick: brick.p1[2])

    return bricks


def stack_falling_bricks(
    bricks: list[Brick],
) -> tuple[dict[tuple[int, int], tuple[str | None, int]], dict[int, set[int]],]:
    z_max_lkp = defaultdict(lambda: (None, 0))
    bricks_support = {e: set() for e in range(len(bricks))}

    # Use the counter "i" as the brick identifier
    for i, brick in enumerate(bricks):
        # First split the brick into individual cubes
        # e.g. ((0,0,10), (2,0,10)) -> [(0,0,10), (1,0,10), (2,0,10)]
        cubes = []
        (x1, y1, z1), (x2, y2, z2) = brick.p1, brick.p2
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    cubes.append(Cube(x, y, z))

        # Find the highest z coordinate for each x,y coordinate in the z_max_lkp
        # All the cubes will be placed above the highest z coordinate
        z_max_xy = max([z_max_lkp[(c.x, c.y)] for c in cubes], key=lambda e: e[1])[1]

        # Calculate the difference between the z coordinates of the two points of the brick
        z_diff = z2 - z1

        for j, cube in enumerate(cubes):
            # Calculate the new z coordinate
            nz = z_max_xy + 1 if z_diff == 0 else z_max_xy + 1 + j

            # Update the highest z coordinate for each x,y coordinate
            # and save which bricks are supporting the current cube (or brick)
            z_max_brick, z_max = z_max_lkp[(cube.x, cube.y)]
            if z_max_brick is not None and z_max == z_max_xy:
                bricks_support[z_max_brick].add(i)

            # Update highest z coordinate
            if nz > z_max_xy:
                z_max_lkp[(cube.x, cube.y)] = (i, nz)

    return z_max_lkp, bricks_support


bricks = get_bricks()
z_max_lkp, bricks_support = stack_falling_bricks(bricks)

# Part 1:
# Find which bricks can be removed without breaking the structure
# A brick can be removed if it is not supporting any other brick
# or if there is another brick that can support the bricks that are currently supported
# by the brick that we want to remove
removable_bricks = 0
for brick, s_bricks in bricks_support.items():
    if len(s_bricks) == 0:
        removable_bricks += 1
        continue

    remaining_supports = set().union(
        *[s for b, s in bricks_support.items() if b != brick]
    )

    if len(s_bricks - remaining_supports) == 0:
        removable_bricks += 1

print(f"Number of removable bricks: {removable_bricks}")

# Part 2:
falling_bricks_sum = 0
for brick, s_bricks in bricks_support.items():
    # Removing a brick that is not supporting any other brick
    # has no effect on the structure
    if len(s_bricks) == 0:
        continue

    # Work with a copy of the bricks_support dictionary as we modify it
    # for each brick that we want to remove
    sbc = bricks_support.copy()
    sbc.pop(brick)

    # Bricks that are supported by the brick that we want to remove
    # e.g. they might fall if we remove the brick
    remove_candidates = s_bricks.copy()

    removed_bricks = 0
    while remove_candidates:
        c = remove_candidates.pop()

        # Join all remaining support sets to check if the brick that we want to remove
        # is still being supported by another brick
        remaining_supports = set().union(*sbc.values())

        if c not in remaining_supports:
            removed_bricks += 1
            # c is not supported by any other brick so it will fall
            # we need to check what will happen to the bricks that are supported by c
            remove_candidates.update(sbc.pop(c))

    falling_bricks_sum += removed_bricks

print(f"Sum of bricks that would fall: {falling_bricks_sum}")
