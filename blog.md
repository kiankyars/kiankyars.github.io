---
layout: default
title: Blog
permalink: /blog/
---

{% assign blog_posts = site.posts | where_exp: "post", "post.path contains '_posts/blog/'" %}

{% for post in blog_posts %}
- `{{ post.date | date: "%Y-%m-%d" }}` [{{ post.title }}]({{ post.url | relative_url }})
{% endfor %}
