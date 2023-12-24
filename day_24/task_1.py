from dataclasses import dataclass
from itertools import combinations
from re import compile
from typing import Optional

NUMS_RE = compile(r"[-]*\d+")


@dataclass
class Hailstone:
    x: int
    y: int
    z: int

    vx: int
    vy: int
    vz: int

    def __str__(self):
        return f"pos=<x={self.x}, y={self.y}, z={self.z}>, vel=<x={self.vx}, y={self.vy}, z={self.vz}>"

    def __repr__(self):
        return self.__str__()


def hailstone_intersection_2d(
    h1: Hailstone, h2: Hailstone
) -> Optional[tuple[float, float]]:
    h1_slope = h1.vy / h1.vx
    h2_slope = h2.vy / h2.vx

    # parallel lines
    if h1_slope == h2_slope:
        return None

    h1_intercept = h1.y - h1_slope * h1.x
    h2_intercept = h2.y - h2_slope * h2.x

    x = (h2_intercept - h1_intercept) / (h1_slope - h2_slope)
    y = h1_slope * x + h1_intercept

    # check if the intersection is before or after the current position
    t1 = (x - h1.x) / h1.vx
    t2 = (x - h2.x) / h2.vx

    if t1 < 0 or t2 < 0:
        return None

    return x, y


# Read input and create Hailstone objects
hailstones = []
for line in open("input.txt"):
    nums = [int(num) for num in NUMS_RE.findall(line)]
    hailstones.append(Hailstone(*nums))

x_limits = [200000000000000, 400000000000000]
y_limits = [200000000000000, 400000000000000]

interesections = 0
# Compare each Hailstone with each other and see if they collide
for h1, h2 in combinations(hailstones, 2):
    intersection = hailstone_intersection_2d(h1, h2)

    if (
        intersection is not None
        and x_limits[0] <= intersection[0] <= x_limits[1]
        and y_limits[0] <= intersection[1] <= y_limits[1]
    ):
        interesections += 1

print(interesections)
