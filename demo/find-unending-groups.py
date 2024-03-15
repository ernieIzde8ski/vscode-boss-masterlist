#!/usr/bin/env python3

"""
This script is shoddily written and probably not likely to become
relevant again, but I stash it just in case. 2024 MIT licensed by
Ernie Izdebski or no rights preserved, whatever you prefer.
"""

from dataclasses import dataclass
import re
import sys


@dataclass
class Delimiter:
    begins: bool
    name: str
    line: int


delimiters: list[Delimiter] = []
lines: list[str]

# --- parse masterlist.txt into group delimiters

with open("masterlist.txt", "r") as file:
    lines = file.readlines()

pattern = re.compile(r"^(BEGIN|END)GROUP:\s*(.+)")
for i, text in enumerate(lines):
    match = re.match(pattern, text)
    if match is None:
        continue
    begins = match[1] == "BEGIN"
    delimiter = Delimiter(begins, name=match[2], line=i+1)
    delimiters.append(delimiter)

delimiters.reverse()
stack: list[Delimiter] = []

# --- check if delimiters are either OK or broken

while delimiters:
    delimiter = delimiters.pop()
    if delimiter.begins:
        stack.append(delimiter)
    elif not stack:
        print(
            "unknown group termination:",
            f"`{delimiter.name}` at masterlist.txt#{delimiter.line}",
            file=sys.stderr,
        )
        exit(1)
    elif stack[-1].name == delimiter.name:
        stack.pop()
    else:
        print(
            "group delimiter mismatch:",
            f"group began: `{stack[-1].name}` at masterlist.txt#{stack[-1].line}",
            f"group ended: `{delimiter.name}` at masterlist.txt#{delimiter.line}",
            sep="\n",
            file=sys.stderr,
        )
        exit(2)
