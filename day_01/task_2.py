from re import findall


def spelled_to_digit_str(digit: str) -> str:
    """Converts spelled digit to digit string.
    If the digit is already a digit string, it is returned unchanged."""

    STR_TO_DIGIT = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    return STR_TO_DIGIT.get(digit, digit)


# (?=...) is a lookahead assertion
DIGITS_REGEXP = r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))"

entries = [line.strip() for line in open("input.txt", "r")]

digits_sum = 0

for e in entries:
    digits = list(map(spelled_to_digit_str, findall(DIGITS_REGEXP, e)))
    digits_sum += int(f"{digits[0]}{digits[-1]}")

print(f"The sum of all calibration values is: {digits_sum}")
