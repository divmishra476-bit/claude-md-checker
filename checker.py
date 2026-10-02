import re
import sys

MAX_LINES = 200
VAGUE = ["write good code", "be careful", "best practices", "clean code",
         "high quality", "make sure it works", "be smart"]
SECTIONS = {
    "commands (build/test/run)": ["npm ", "pytest", "make ", "pip ", "cargo ", "run "],
    "code style": ["style", "naming", "format", "convention"],
    "project structure": ["structure", "directory", "folder", "architecture"],
}

def check(text):
    lines = text.splitlines()
    low = text.lower()
    problems, penalty = [], 0

    if len(lines) > MAX_LINES:
        problems.append(f"Too long: {len(lines)} lines (limit {MAX_LINES}). Long files eat context.")
        penalty += 20

    for name, keys in SECTIONS.items():
        if not any(k in low for k in keys):
            problems.append(f"Missing section: {name}")
            penalty += 15

    for i, line in enumerate(lines, 1):
        for phrase in VAGUE:
            if phrase in line.lower():
                problems.append(f"Line {i}: vague instruction '{phrase}'. Say what exactly to do.")
                penalty += 10

    return max(0, 100 - penalty), problems

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "CLAUDE.md"
    score, problems = check(open(path, encoding="utf-8").read())
    print(f"Score: {score}/100")
    for p in problems:
        print(" -", p)
    sys.exit(0 if score >= 70 else 1)