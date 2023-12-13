SYMBOLS_TO_NUM = str.maketrans(".#", "01")


def find_reflection_index(pattern: list[int], find_smudge: bool = False) -> int:
    for i in range(1, len(pattern)):
        left, right = pattern[:i][::-1], pattern[i:]

        length = min(len(left), len(right))
        # truncate the longer list to the length of the shorter one
        left, right = left[:length], right[:length]

        if find_smudge:
            diff = [a ^ b for a, b in zip(left, right) if a != b]
            if len(diff) == 1 and (diff[0] != 0 and diff[0] & (diff[0] - 1) == 0):
                return i
        else:
            if left == right:
                return i
    # if no reflection is found, return -1
    return -1


patterns = []
for entry in open("input.txt", "r").read().split("\n\n"):
    patterns.append(
        tuple(map(lambda x: x.translate(SYMBOLS_TO_NUM), entry.split("\n")))
    )

for e in range(2):
    summary = 0
    for pattern in patterns:
        # iterate over all rows of the pattern and change the binary string to an int
        rows = [int(row, 2) for row in pattern]

        # iterate over all columns of the pattern and change the binary string to an int
        columns = [int("".join(row), 2) for row in zip(*pattern)]

        rows_reflection_index = find_reflection_index(rows, find_smudge=bool(e))
        columns_reflection_index = find_reflection_index(columns, find_smudge=bool(e))

        if rows_reflection_index != -1:
            summary += rows_reflection_index * 100

        if columns_reflection_index != -1:
            summary += columns_reflection_index

    print(f"Task {e+1} summary value: {summary}")
