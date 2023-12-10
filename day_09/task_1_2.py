from itertools import pairwise

entries = [line.strip() for line in open("input.txt", "r")]


def predict_next_number(numbers: list[int]) -> int:
    if set(numbers) == {0}:
        return 0

    new_numbers = [b - a for a, b in pairwise(numbers)]
    lv = predict_next_number(new_numbers)

    return numbers[-1] + lv


extrapolated_numbers = [[], []]

for line in entries:
    numbers = [int(n) for n in line.split(" ")]

    next_number = predict_next_number(numbers)
    prev_number = predict_next_number(numbers[::-1])

    extrapolated_numbers[0].append(next_number)
    extrapolated_numbers[1].append(prev_number)

print(f"Sum of all extrapolated (next) numbers is: {extrapolated_numbers[0]}")
print(f"Sum of all extrapolated (prev) numbers is: {extrapolated_numbers[1]}")
