from re import compile

CARD_PATTERN = compile(r"Card.*: ([\d ]+) \| ([\d ]+)")
NUM_PATTERN = compile(r"(\d+)")

entries = [line.strip() for line in open("input.txt", "r")]


scratch_cards_points = 0

for e in entries:
    list_w, list_c = CARD_PATTERN.match(e).groups()

    winning_set = set(NUM_PATTERN.findall(list_w))
    card_set = set(NUM_PATTERN.findall(list_c))

    hits = len(winning_set.intersection(card_set))
    if hits > 0:
        scratch_cards_points += 2 ** (hits - 1)

print(f"Total scratch cards points: {scratch_cards_points}")
