from collections import deque
from math import lcm
from typing import Optional


def run_pulse(
    g: dict[str, list[str]],
    f: dict[str, bool],
    c: dict[str, dict[str, bool]],
    origin: str,
    target: str,
    pulse: bool,
) -> Optional[list[tuple[str, str, bool]]]:
    if target in f:
        if pulse:
            return None
        new_pulse = f[target] = not f[target]
    elif target in c:
        c[target][origin] = pulse
        new_pulse = not all(c[target].values())
    elif target in g:
        new_pulse = pulse
    else:
        return None

    return [(target, new_target, new_pulse) for new_target in g[target]]


def push_button(
    g: dict[str, list[str]], f: dict[str, bool], c: dict[str, dict[str, bool]]
) -> tuple[int, int]:
    # Queue of (origin module, target module, is_high_pulse) tuples
    q = deque([("button", "broadcaster", False)])

    low_pulses = 0
    high_pulses = 0

    while q:
        origin, target, pulse = q.popleft()

        if pulse:
            high_pulses += 1
        else:
            low_pulses += 1

        next_pulses = run_pulse(g, f, c, origin, target, pulse)

        if next_pulses:
            q.extend(next_pulses)

    return low_pulses, high_pulses


def find_cycles(
    g: dict[str, list[str]],
    f: dict[str, bool],
    c: dict[str, dict[str, bool]],
) -> list[int]:
    # Basically same approach as day_08/task_2.py
    # After analyzing the input graph:
    # &kh points to rx
    # &pv, &qh, &xm, &hz point to &kh
    # --> find when all of these are sending a high pulse e.g. lcm of their cycles

    rx_origin = [origin for origin, targets in g.items() if "rx" in targets][0]
    cyclic_conjunctions = {
        origin for origin, targets in g.items() if rx_origin in targets
    }

    counts = []

    i = 0
    while cyclic_conjunctions:
        i += 1

        q = deque([("button", "broadcaster", False)])
        while q:
            origin, target, pulse = q.popleft()

            # low pulse
            if not pulse and target in cyclic_conjunctions:
                counts.append(i)
                # use discard instead of remove to avoid KeyError
                cyclic_conjunctions.discard(target)

            next_pulses = run_pulse(g, f, c, origin, target, pulse)

            if next_pulses:
                q.extend(next_pulses)

    return counts


config = [line.strip().split(" -> ") for line in open("input.txt", "r")]

graph = {}
flipflops = {}
conjunctions = {}

for origin, targets in config:
    module, name = (origin[0], origin[1:]) if origin[0] in ["%", "&"] else ("", origin)

    # Flipflop module
    if module == "%":
        flipflops[name] = False
    # Conjunction module
    elif module == "&":
        conjunctions[name] = {}

    graph[name] = targets.split(", ")

for origin, targets in graph.items():
    for target in filter(conjunctions.__contains__, targets):
        conjunctions[target][origin] = False

lcm_cycles = lcm(*find_cycles(graph, flipflops, conjunctions))
print(f"LCM of module cycles: {lcm_cycles}")
