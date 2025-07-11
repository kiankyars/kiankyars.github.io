import os
from datetime import datetime

# Directory for posts
POSTS_DIR = "_posts"

# Get today's date
now = datetime.now()

date_str = now.strftime("%Y-%m-%d")
filename = f"{date_str}-weekly-victories.markdown"
filepath = os.path.join(POSTS_DIR, filename)

# Avoid overwriting if already exists
if not os.path.exists(filepath):
    with open(filepath, "w") as f:
        f.write(f"""---
layout: post
title:  \"Weekly Victories\"
date:   {date_str}
categories: reflection
---

Victory #1:
- 

Victory #2:
- 

Victory #3:
- 
""")
    print(f"Created: {filepath}")
else:
    print(f"Post already exists: {filepath}")