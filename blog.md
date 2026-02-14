---
layout: default
title: Blog
permalink: /blog/
---

{% for post in site.posts %}
  {% unless post.title == "Weekly Victories" %}
    <div style="margin-bottom: 2rem;">
      <small>{{ post.date | date: "%B %d, %Y" }}</small><br>
      <a href="{{ post.url }}"><strong>{{ post.title }}</strong></a>
      <p>{{ post.excerpt | strip_html | truncatewords: 25 }}</p>
    </div>
  {% endunless %}
{% endfor %}
