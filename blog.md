---
layout: default
title: Blog
permalink: /blog/
---

{% for post in site.posts %}
  {% if post.path contains "_posts/blog/" %}
    <div style="margin-bottom: 1.5rem;">
      <span style="color: #666; font-family: monospace;">{{ post.date | date: "%Y-%m-%d" }}</span> &nbsp;
      <a href="{{ post.url | relative_url }}"><strong>{{ post.title }}</strong></a>
    </div>
  {% endif %}
{% endfor %}
