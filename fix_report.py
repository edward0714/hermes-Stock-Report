
import re

with open("news/2026/07/2026-07-25.html","r") as f:
    html = f.read()

# Read replacement data
with open("/tmp/hermes-Stock-Report/data/replacements.txt","r") as f:
    lines = f.readlines()

i = 0
while i < len(lines):
    old = lines[i].rstrip("\n")
    new = lines[i+1].rstrip("\n")
    if old and new and old != "---":
        html = html.replace(old, new)
    i += 2

with open("news/2026/07/2026-07-25.html","w") as f:
    f.write(html)
print("Replacements done")
