from collections import deque
from dataclasses import dataclass


@dataclass
class Vertex:
    _id: str
    position: tuple[int, int]
    direction: tuple[int, int] = None

    def __hash__(self):
        hashed = hash((self._id, self.position))
        return hashed

    def __eq__(self, other):
        return self._id == other._id and self.position == other.position


@dataclass(frozen=True)
class Edge:
    start: Vertex
    end: Vertex


class Sketch:
    NEIGHBOUR_OFFSETS = {
        "|": [(0, -1), (0, 1)],
        "-": [(1, 0), (-1, 0)],
        "L": [(0, -1), (1, 0)],
        "F": [(0, 1), (1, 0)],
        "J": [(0, -1), (-1, 0)],
        "7": [(0, 1), (-1, 0)],
        "S": [(0, -1), (0, 1), (1, 0), (-1, 0)],
    }

    OFFSET_CONNECTIONS = {
        (0, -1): {"|", "7", "F"},
        (0, 1): {"|", "L", "J"},
        (1, 0): {"-", "J", "7"},
        (-1, 0): {"-", "L", "F"},
    }

    CORNERS = {"L", "F", "J", "7"}

    def __init__(self, sketch: list[list[str]]) -> None:
        self.sketch = sketch
        self.width = len(sketch[0])
        self.height = len(sketch)

    def get_neighbours(self, v: Vertex, skip: set[Vertex] = None) -> list[Vertex]:
        neighbours = []

        x, y = v.position

        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nx, ny = x + dx, y + dy

            if nx < 0 or nx >= self.width or ny < 0 or ny >= self.height:
                continue

            nv = Vertex(self.sketch[ny][nx], (nx, ny), (dx, dy))
            if not skip or nv not in skip:
                neighbours.append(nv)

        return neighbours

    def get_valid_neighbours(self, v: Vertex) -> list[Vertex]:
        # Use this to find neighbours that are valid pipes
        neighbours = filter(
            lambda n: self.is_matching_pipe(v._id, n._id, n.direction),
            self.get_neighbours(v),
        )
        return list(neighbours)

    def is_matching_pipe(
        self, source_pipe: str, target_pipe: str, direction: tuple[int, int]
    ) -> bool:
        return (
            direction in self.NEIGHBOUR_OFFSETS[source_pipe]
            and target_pipe in self.OFFSET_CONNECTIONS[direction]
        )

    def is_corner(self, v: Vertex) -> bool:
        if v._id in self.CORNERS:
            return True

        elif v._id == "S":
            neighbours = self.get_valid_neighbours(v)

            x_diff = neighbours[0].direction[0] + neighbours[1].direction[0]
            y_diff = neighbours[0].direction[1] + neighbours[1].direction[1]

            return x_diff != 0 or y_diff != 0

        return False

    def get_starting_point(self) -> Vertex:
        # Return the starting point

        for y, line in enumerate(self.sketch):
            for x, char in enumerate(line):
                if char == "S":
                    # This will always return 2 valid neighbours.
                    return Vertex(char, (x, y))

    def __bfs_connected(self, start: Vertex, skip: set[Vertex] = None) -> set[Vertex]:
        points_to_visit = deque([start])
        visited = set()

        while points_to_visit:
            v = points_to_visit.popleft()

            if v in visited:
                continue

            visited.add(v)

            neighbours = self.get_neighbours(v, skip=skip)

            for n in neighbours:
                if n not in visited:
                    points_to_visit.append(n)

        return visited

    def get_connected_areas(
        self, skip: set[Vertex] = None
    ) -> tuple[list[set[Vertex]], set[Vertex]]:
        connected_areas = []
        tiles_seen = set()

        for y, line in enumerate(self.sketch):
            for x, char in enumerate(line):
                v = Vertex(char, (x, y))
                if (not skip or v not in skip) and (v not in tiles_seen):
                    area = self.__bfs_connected(v, skip)
                    connected_areas.append(area)
                    tiles_seen.update(area)

        return connected_areas, tiles_seen

    def find_cycle(self, start: Vertex) -> tuple[set[Vertex], set[Edge]]:
        # Basically do a BFS but instead of following all the possible paths,
        # we just follow the first one we find. We know that the path is a circle,
        # so eventually we will find the starting point again.
        next_to_visit = start
        visited = set()
        corners = []

        while next_to_visit:
            v = next_to_visit

            if v in visited:
                break

            visited.add(v)

            if self.is_corner(v):
                corners.append(v)

            neighbours = self.get_valid_neighbours(v)
            next_to_visit = None
            for n in neighbours:
                if n not in visited:
                    next_to_visit = n
                    break

        # Ensure we have a closed cycle/path
        corners.append(corners[0])

        # Create the edges
        edges = set()
        for i in range(len(corners) - 1):
            edges.add(Edge(corners[i], corners[i + 1]))

        return visited, edges


def is_inside(v: Vertex, edges: set[Edge]) -> bool:
    # We use a simple ray casting algorithm to check if the vertex is inside the
    # polygon defined by the edges.
    # https://en.wikipedia.org/wiki/Point_in_polygon#Ray_casting_algorithm

    # If we cast a ray from the vertex to a point outside the polygon and count
    # the number of intersections with the edges, we can determine if the vertex
    # is inside the polygon.
    # odd number of intersections -> inside
    # even number of intersections -> outside
    count = 0

    x, y = v.position

    for edge in edges:
        (x1, y1), (x2, y2) = edge.start.position, edge.end.position

        # If the edge is horizontal, skip it
        if y1 == y2:
            continue

        # If the edge is vertical, check for intersections
        if x1 == x2:
            # Check if the ray intersects with the edge
            if x < x1 and (y1 <= y < y2 or y2 <= y < y1):
                count += 1

    return count % 2 == 1


# Read the input and create a sketch object
sketch = Sketch([list(line.strip()) for line in open("input.txt", "r")])

# Find the starting point that is needed to find the pipe cycle
start = sketch.get_starting_point()

# Find the cycle of pipes
# Returns all vertices that are part of the cycle and the edges of the cycle
# Edge = segment between two corner pipes
vertices, edges = sketch.find_cycle(start)

# Find all the connected areas that are not part of the cycle
areas, tiles_seen = sketch.get_connected_areas(skip=vertices)

# We now have all connected areas (with vertices that are not part of the cycle)
# Find all areas that are enclosed by the cycle.
tiles_sum = 0
for area in areas:
    # Select a random point from the area
    for v in area:
        # Check if the point is inside the cycle using the ray casting algorithm
        if is_inside(v, edges):
            tiles_sum += len(area)
        break

print(f"Number of tiles enclosed by the pipe cycle: {tiles_sum}")
