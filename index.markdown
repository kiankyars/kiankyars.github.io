---
layout: home
title: Home
---

{% for post in site.posts %}
  <div class="post">
    <h2><a href="{{ post.url }}">{{ post.title }}</a></h2>
    <small>{{ post.date | date: "%b %-d, %Y" }}</small>
  </div>
{% endfor %}

