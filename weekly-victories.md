---
layout: default
title: Weekly Victories
permalink: /weekly-victories/
---

{% for post in site.posts %}
  {% if post.title == "Weekly Victories" %}
    <div style="margin-bottom: 1rem;">
      <small>{{ post.date | date: "%Y-%m-%d" }}</small> — 
      <a href="{{ post.url }}"><strong>Victory Log</strong></a>
    </div>
  {% endif %}
{% endfor %}
