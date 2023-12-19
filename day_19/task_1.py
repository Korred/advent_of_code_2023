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


# Read input
workflows, parts = open("input.txt", "r").read().split("\n\n")
workflows = workflows.split("\n")
parts = parts.split("\n")


workflow_lkp = {}

for workflow in workflows:
    name, rules, default = RE_WORKFLOW.match(workflow).groups()
    rules = RE_RULES.findall(rules)
    workflow_lkp[name] = Workflow(name, rules, default)


rating_numbers_sum = 0
for part in parts:
    x, m, a, s = list(map(int, RE_PARTS.match(part).groups()))

    current_workflow = workflow_lkp["in"]
    while True:
        next_workflow = current_workflow.apply(x, m, a, s)

        if next_workflow == "R":
            break

        if next_workflow == "A":
            rating_numbers_sum += sum([x, m, a, s])
            break

        current_workflow = workflow_lkp[next_workflow]


print(f"Task 1 summary value: {rating_numbers_sum}")
