from re import findall

entries = [line.strip() for line in open("input.txt", "r")]

digits_sum = 0

for e in entries:
    digits = findall(r"\d", e)
    digits_sum += int(f"{digits[0]}{digits[-1]}")

print(f"The sum of all calibration values is: {digits_sum}")
