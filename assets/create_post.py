import os
from datetime import datetime
import sys

date_str = datetime.now().strftime("%Y-%m-%d")
is_weekly = sys.argv[1] == "w"

filename = f"{date_str}-{'weekly-victories' if is_weekly else sys.argv[1]}.md"
post_dir = f"_posts/{'weekly-victories' if is_weekly else 'blog'}"
filepath = os.path.join(post_dir, filename)

title = "Weekly Victories" if is_weekly else sys.argv[1].replace("-", " ").title()
categories = "reflection" if is_weekly else ""
content = '\n'.join([f'Victory #{n}:\n\n- \n' for n in range(int(sys.argv[2]))]) if is_weekly else ""

with open(filepath, "w") as f:
    f.write(f"""---
layout: post
title: {title}
date: {date_str}
categories: {categories}
---

{content}""")
print(f"Created: {filepath}")
