from functools import cache


@cache
def get_arrangements(springs: str, groups: tuple[int, ...]) -> int:
    # Remove operational springs
    springs = springs.lstrip(".")

    # No springs left
    if not springs:
        return 1 if not groups else 0

    # No groups left
    if not groups:
        return 1 if springs.find("#") == -1 else 0

    # Damaged spring
    if springs[0] == "#":
        # Operational spring breaking up group or not enough springs left
        if "." in springs[: groups[0]] or len(springs) < groups[0]:
            return 0
        # Current group size matches remaining springs (but other groups might be left)
        elif len(springs) == groups[0]:
            return 1 if len(groups) == 1 else 0
        # Two groups must be seperated by an operational spring
        elif springs[groups[0]] == "#":
            return 0
        # Spring match group size - continue with next group
        else:
            return get_arrangements(springs[groups[0] + 1 :], groups[1:])

    # unknown spring (dot or hash)
    dot_arrangements = get_arrangements("." + springs[1:], groups)
    hash_arrangements = get_arrangements("#" + springs[1:], groups)

    return dot_arrangements + hash_arrangements


entries = [line.strip().split() for line in open("input.txt", "r")]


valid_arrangements = 0
for springs, groups in entries:
    groups = tuple(map(int, groups.split(",")))
    valid_arrangements += get_arrangements(springs, groups)

print("Sum of valid arrangements in Task 1:", valid_arrangements)

valid_arrangements = 0
for springs, groups in entries:
    unfolded_springs = "?".join([springs] * 5)
    unfolded_groups = tuple(map(int, ",".join([groups] * 5).split(",")))
    valid_arrangements += get_arrangements(unfolded_springs, unfolded_groups)

print("Sum of valid arrangements in Task 2:", valid_arrangements)
