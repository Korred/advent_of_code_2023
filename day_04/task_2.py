from collections import defaultdict
from re import compile

CARD_PATTERN = compile(r"Card.*: ([\d ]+) \| ([\d ]+)")
NUM_PATTERN = compile(r"(\d+)")

entries = [line.strip() for line in open("input.txt", "r")]

scratch_cards = defaultdict(int)

for i, e in enumerate(entries):
    list_w, list_c = CARD_PATTERN.match(e).groups()

    winning_set = set(NUM_PATTERN.findall(list_w))
    card_set = set(NUM_PATTERN.findall(list_c))

    hits = len(winning_set.intersection(card_set))

    scratch_cards[i] += 1
    for num in range(i + 1, i + 1 + hits):
        scratch_cards[num] += 1 * scratch_cards[i]


print(f"Total number of scratch cards: {sum(scratch_cards.values())}")
