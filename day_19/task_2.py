from collections import deque
from math import prod
from re import compile

RE_RULES = compile(r"(?>(\w+)(<|>)(\d+):(\w+))")
RE_WORKFLOW = compile(r"(\w+){(.*),(\w+)}")
RE_PARTS = compile(r"\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}")


class Workflow:
    def __init__(self, name: str, rules: list[str], default: str):
        self.name = name
        self.rules = self.__parse_rules(rules)
        self.default_rule = default

    def __parse_rules(self, rules: list[str]) -> list[dict[str, str]]:
        rules = [
            dict(zip(["name", "operator", "value", "next"], rule)) for rule in rules
        ]
        return rules

    def apply(self, x: str, m: str, a: str, s: str) -> str:
        variables = {"x": x, "m": m, "a": a, "s": s}
        for rule in self.rules:
            variable, operator, value, workflow = rule.values()
            if (operator == ">" and variables[variable] > int(value)) or (
                operator == "<" and variables[variable] < int(value)
            ):
                return workflow
        return self.default_rule

    def apply_ranges(self, ranges: list[tuple[int, int]]) -> list[tuple[str, list]]:
        next_ranges = []
        index_lkp = {"x": 0, "m": 1, "a": 2, "s": 3}

        current_ranges = ranges.copy()
        for rule in self.rules:
            variable, operator, value, workflow = rule.values()

            r_min, r_max = current_ranges[index_lkp[variable]]
            new_ranges = current_ranges.copy()

            if operator == ">":
                new_ranges[index_lkp[variable]] = (int(value) + 1, r_max)
                next_ranges.append((workflow, new_ranges))
                current_ranges[index_lkp[variable]] = (r_min, int(value) + 1)

            elif operator == "<":
                new_ranges[index_lkp[variable]] = (r_min, int(value))
                next_ranges.append((workflow, new_ranges))
                current_ranges[index_lkp[variable]] = (int(value), r_max)

        # apply default rule
        next_ranges.append((self.default_rule, current_ranges))

        return next_ranges


# Read input
workflows, parts = open("input.txt", "r").read().split("\n\n")
workflows = workflows.split("\n")
parts = parts.split("\n")


workflow_lkp = {}

for workflow in workflows:
    name, rules, default = RE_WORKFLOW.match(workflow).groups()
    rules = RE_RULES.findall(rules)
    workflow_lkp[name] = Workflow(name, rules, default)


ranges_queue = deque([("in", [(1, 4001), (1, 4001), (1, 4001), (1, 4001)])])

valid_combinations = 0
while ranges_queue:
    workflow_name, ranges = ranges_queue.popleft()
    workflow = workflow_lkp[workflow_name]

    new_workflow_ranges = workflow.apply_ranges(ranges)

    for name, new_range in new_workflow_ranges:
        if name == "A":
            prod_val = prod([max - min for min, max in new_range])

            valid_combinations += prod_val
        elif name == "R":
            continue
        else:
            ranges_queue.append((name, new_range))


print(f"Task 2 summary value: {valid_combinations}")
