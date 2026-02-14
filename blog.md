---
layout: default
title: Blog
permalink: /blog/
---

{% for post in site.posts %}
  {% unless post.title == "Weekly Victories" %}
    <div style="margin-bottom: 1rem;">
      <small>{{ post.date | date: "%Y-%m-%d" }}</small> — 
      <a href="{{ post.url }}"><strong>{{ post.title }}</strong></a>
    </div>
  {% endunless %}
{% endfor %}
