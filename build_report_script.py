
import os
path = "/tmp/hermes-Stock-Report/news/2026/07/2026-07-11.html"
content = open(path, "r").read() if os.path.exists(path) else ""
# Now we have the start, need to add more
print(f"File has {len(content)} chars")
