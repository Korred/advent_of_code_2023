from dataclasses import dataclass
from itertools import pairwise
from re import compile

PLAN_PATTERN = compile(r"(D|U|L|R) (\d+) \((#\w{6})\)")


@dataclass(frozen=True)
class Vertex:
    x: int
    y: int


# https://en.wikipedia.org/wiki/Shoelace_formula
def shoelace_formula(vertices: list[Vertex]) -> int:
    area = 0
    for v1, v2 in pairwise(vertices):
        area += (v1.x * v2.y) - (v1.y * v2.x)
    return abs(area) // 2


# https://en.wikipedia.org/wiki/Pick%27s_theorem
def picks_theorem(number_of_vertices: int, area: int) -> int:
    return area + 1 - (number_of_vertices // 2)


def parse_plan(lines: list[tuple[str, str, str]]) -> list[Vertex]:
    DIR_OFFSET = {"D": (0, 1), "U": (0, -1), "L": (-1, 0), "R": (1, 0)}
    DIR_LKP = {"0": "R", "1": "D", "2": "L", "3": "U"}

    current_pos = Vertex(0, 0)
    corners = []

    for line in lines:
        _, _, code = line
        direction = DIR_LKP[code[-1]]
        distance = int(code[1:-1], 16)

        # Calculate new position
        new_pos = Vertex(
            current_pos.x + DIR_OFFSET[direction][0] * distance,
            current_pos.y + DIR_OFFSET[direction][1] * distance,
        )

        corners.append(current_pos)
        current_pos = new_pos

    # Add last corner
    corners.append(current_pos)

    return corners


lines = [
    tuple(PLAN_PATTERN.match(line.strip()).groups()) for line in open("input.txt", "r")
]

corner_vertices = parse_plan(lines)
trench = sum(
    [abs(v1.x - v2.x) or abs(v1.y - v2.y) for v1, v2 in pairwise(corner_vertices)]
)


# calculate the area using shoelace formula
area = shoelace_formula(corner_vertices)
# calculate the number of interior points using Pick's theorem
interior_points = picks_theorem(trench, area)
# total points = trench + interior points
total_points = trench + interior_points

print(total_points)
