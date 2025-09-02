import os
from datetime import datetime
import sys

# Get today's date
now = datetime.now()

date_str = now.strftime("%Y-%m-%d")
arg = sys.argv[1]
if arg == "w":
    filename = f"{date_str}-weekly-victories.md"
    POSTS_DIR = f"_posts/weekly-victories"
else:
    filename = f"{date_str}-{arg}.md"
    POSTS_DIR = f"_posts/blog"

filepath = os.path.join(POSTS_DIR, filename)

with open(filepath, "w") as f:
    f.write(f"""---
layout: post
title:  {"Weekly Victories" if arg == "w" else arg.replace("-", " ").title()}
date:   {date_str}
categories: {'''reflection
---

Victory #1:
             
- 

Victory #2:
             
- 

Victory #3:
             
- ''' if arg == "w" else "\n---"}""")
print(f"Created: {filepath}")