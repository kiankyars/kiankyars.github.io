import os
from datetime import datetime

# Directory for posts
POSTS_DIR = "_posts"

# Get today's date
now = datetime.now()

# Only proceed if today is Wednesday
if now.weekday() == 2:  # Monday=0, Wednesday=2
    date_str = now.strftime("%Y-%m-%d")
    filename = f"{date_str}-wednesday-victories.markdown"
    filepath = os.path.join(POSTS_DIR, filename)

    # Avoid overwriting if already exists
    if not os.path.exists(filepath):
        with open(filepath, "w") as f:
            f.write(f"""---
layout: post
title:  \"Wednesday Victories\"
date:   {date_str}
categories: reflection
---

## Wednesday Victories

1. Victory #1:
   
2. Victory #2:
   
3. Victory #3:
   
""")
        print(f"Created: {filepath}")
    else:
        print(f"Post already exists: {filepath}")
else:
    print("Today is not Wednesday. No post created.") 