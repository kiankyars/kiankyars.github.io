import os
from datetime import datetime, timedelta
import sys
import calendar

# Run from repo root so _posts/ paths work whether script is run from misc/ or repo root
_script_dir = os.path.dirname(os.path.abspath(__file__))
_repo_root = os.path.dirname(_script_dir) if os.path.basename(_script_dir) == "misc" else _script_dir
os.chdir(_repo_root)

date = datetime.now()

if len(sys.argv) < 2:
    print("Usage: python3 create_post.py <title|w>")
    sys.exit(1)

mode = sys.argv[1]

if mode == "w":
    # Calculate next Friday (or today if it's Friday)
    # weekday(): Monday=0, Sunday=6. Friday=4.
    days_until_friday = (4 - date.weekday()) % 7
    target_date = date + timedelta(days=days_until_friday)
    date_str = target_date.strftime("%Y-%m-%d")
    
    filename = f"{date_str}-weekly-victories.md"
    POSTS_DIR = "_posts/weekly-victories"
    
    title = "Weekly Victories"
    categories = "reflection"
    calendar.setfirstweekday(5)
    days = list(calendar.day_name)[5:] + list(calendar.day_name)[:5]
    content = "\n".join([f"### {day}\n\n- \n" for day in days])
else:
    # Blog post mode
    date_str = date.strftime("%Y-%m-%d")
    filename = f"{date_str}-{mode}.md"
    POSTS_DIR = "_posts/blog"
    
    title = mode.replace("-", " ").title()
    categories = ""
    content = ""

filepath = os.path.join(POSTS_DIR, filename)

with open(filepath, "w") as f:
    f.write(f"""---
layout: post
title: {title}
date: {date_str}
categories: {categories}
---

{content}""")

print(f"Created: {filepath}")
