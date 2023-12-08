import os
import pdb
import re
from dataclasses import dataclass, field
from enum import Enum
from math import lcm
from typing import TypedDict

FILE = os.path.join(os.path.dirname(__file__), "input.txt")


@dataclass
class Node:
    name: str
    left: str
    right: str
    node_map: dict[str, "Node"]

    def __getitem__(self, key):
        if key == "R":
            return self.node_map[self.right]
        elif key == "L":
            return self.node_map[self.left]
        raise KeyError(f"Invalid key {key}")

    @classmethod
    def from_line(cls, line: str, node_map: dict[str, "Node"]):
        name, left, right = re.findall(r"(\w+)", line)
        return cls(name=name, left=left, right=right, node_map=node_map)


@dataclass
class Instructions:
    steps: list[str]
    count: int = 0

    @classmethod
    def create(cls, line: str):
        return cls(steps=list(line.strip()))

    def next(self):
        step = self.steps.pop(0)
        self.steps.append(step)
        self.count += 1
        return step


def do_solution(lines: list[str]):
    node_map = {}
    for line in lines:
        if "=" not in line:
            continue
        node = Node.from_line(line, node_map)
        assert node.name not in node_map, f"Node {node.name} already exists"
        node_map[node.name] = node

    cursor = node_map["AAA"]
    instructions = Instructions.create(lines[0])
    while cursor.name != "ZZZ":
        cursor = cursor[instructions.next()]

    return instructions.count


def do_solution_2(lines: list[str]):
    cursors: list[Node] = []
    node_map = {}
    for line in lines:
        if "=" not in line:
            continue
        node = Node.from_line(line, node_map)
        assert node.name not in node_map, f"Node {node.name} already exists"
        node_map[node.name] = node
        if node.name[-1] == "A":
            cursors.append(node)

    counts = []
    for cursor in cursors:
        instructions = Instructions.create(lines[0])
        while cursor.name[-1] != "Z":
            cursor = cursor[instructions.next()]
        counts.append(instructions.count)

    return lcm(*counts)



if __name__ == "__main__":
    with open(FILE, "r") as file:
        lines = list(file.readlines())

        total = do_solution(lines)
        print("TOTAL: ", total)

        total2 = do_solution_2(lines)
        print("TOTAL2: ", total2)
