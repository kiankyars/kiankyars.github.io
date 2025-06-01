---
layout: home
title: Home
---

# Blog

<ul>
  {% for post in site.posts %}
    <li><a href="{{ post.url }}">{{ post.title }}</a> <small>{{ post.date | date: "%b %-d, %Y" }}</small></li>
  {% endfor %}
</ul>

[Subscribe via RSS](/blog/feed.xml)

# Papers

<!-- Add your papers here, e.g.: -->
<ul>
  <li><a href="/blog/papers/your-paper.pdf">Your Paper Title</a></li>
</ul> 