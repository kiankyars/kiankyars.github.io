import os
from datetime import datetime
import sys

# Get today's date
date = datetime.now()
if not sys.argv[3]:
    date_str = date.strftime("%Y-%m-%d")
else:
    date_str = date.strftime(f"%Y-%m-%{sys.argv[3]}")

if sys.argv[1] == "w":
    filename = f"{date_str}-weekly-victories.md"
    POSTS_DIR = f"_posts/weekly-victories"
else:
    filename = f"{date_str}-{sys.argv[1]}.md"
    POSTS_DIR = f"_posts/blog"

filepath = os.path.join(POSTS_DIR, filename)

with open(filepath, "w") as f:
    f.write(f"""---
layout: post
title: {"Weekly Victories" if sys.argv[1] == "w" else sys.argv[1].replace("-", " ").title()}
date: {date_str}
categories: {f'''reflection
---

{'\n'.join([f'Victory #{n}:\n\n- \n' for n in range(int(sys.argv[2]))])}''' if sys.argv[1] == "w" else "\n---"}""")
print(f"Created: {filepath}")
