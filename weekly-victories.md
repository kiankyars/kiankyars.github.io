---
layout: default
title: Weekly Victories
permalink: /weekly-victories/
---

{% assign victory_posts = site.posts | where_exp: "post", "post.path contains '_posts/weekly-victories/'" %}

{% for post in victory_posts %}

- [`{{ post.date | date: "%Y-%m-%d" }}`]({{ post.url | relative_url }})
  {% endfor %}
