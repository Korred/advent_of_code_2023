from collections import defaultdict
from dataclasses import dataclass

SYMBOL_SET = {"-", "=", "&", "*", "@", "%", "+", "$", "/", "#"}


@dataclass
class GearCandidate:
    hits: int = 0
    ratio: int = 1


def get_border_positions(x, y):
    return {
        (x - 1, y),
        (x + 1, y),
        (x, y - 1),
        (x, y + 1),
        (x - 1, y - 1),
        (x + 1, y - 1),
        (x - 1, y + 1),
        (x + 1, y + 1),
    }


# Parse input file
entries = [line.strip() for line in open("input.txt", "r")]

# Prepare data structures
gear_candidates = defaultdict(GearCandidate)
part_numbers = list()

x_len, y_len = len(entries[0]), len(entries)

# Part 1: Iterate over the grid and find part numbers
for y, e in enumerate(entries):
    current_number = ""
    border_set = set()
    for x, c in enumerate(e):
        if c.isdigit():
            current_number += c

            # This will include positions that are part of the number itself
            # but since we are only looking for symbols this is not a problem
            border_set.update(get_border_positions(x, y))

            # Save current number if we reached the end of the line or the next
            # character is not a digit
            if x + 1 == x_len or not entries[y][x + 1].isdigit():
                symbol_found = False

                # Check if any of the border positions contain a symbol
                # If so, we have found a part number
                for bx, by in border_set:
                    # Skip positions outside of the grid
                    if bx < 0 or bx >= x_len or by < 0 or by >= y_len:
                        continue

                    if entries[by][bx] in SYMBOL_SET:
                        symbol_found = True

                        # For Part 2: If we just found a gear candidate,
                        # ensure we increment the hits counter and recalculate the ratio
                        if entries[by][bx] == "*":
                            gear_candidates[(bx, by)].hits += 1
                            gear_candidates[(bx, by)].ratio *= int(current_number)

                # Save part number
                if symbol_found:
                    part_numbers.append(int(current_number))

                # Reset current number and border set for the next iteration
                current_number = ""
                border_set = set()


print(f"Part 1: The sum of all part numbers is {sum(part_numbers)}")

gears = dict(filter(lambda x: x[1].hits == 2, gear_candidates.items()))
gear_ratio_sum = sum(x.ratio for x in gears.values())

print(f"Part 2: The sum of all gear ratios is {gear_ratio_sum}")
