---
layout: default
title: Weekly Victories
permalink: /weekly-victories/
---

{% for post in site.posts %}
  {% if post.path contains "_posts/weekly-victories/" %}
    <div style="margin-bottom: 1rem;">
      <a href="{{ post.url }}">
        <strong>{{ post.date | date: "%B %d, %Y" }}</strong>
      </a>
    </div>
  {% endif %}
{% endfor %}
