from dataclasses import dataclass
from re import compile
from typing import Optional
import z3


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

# Create Z3 solver
solver = z3.Solver()
x, y, z, vx, vy, vz = z3.Reals("x y z vx vy vz")

# Add constraints
for i, h in enumerate(hailstones[:3]):
    ti = z3.Reals(f"t{i}")[0]
    solver.add(ti > 0)
    solver.add(x + ti * vx == h.x + ti * h.vx)
    solver.add(y + ti * vy == h.y + ti * h.vy)
    solver.add(z + ti * vz == h.z + ti * h.vz)

solver.check()
model = solver.model()
sx, sy, sz = [model[v].as_long() for v in [x, y, z]]
print(sum([sx, sy, sz]))
