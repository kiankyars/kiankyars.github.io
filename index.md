---
layout: default
title: Home
---

## Blog

{% for post in site.posts %}
{% if post.title != "Weekly Victories" %}

<div class="post">
  <small>{{ post.date | date: "%b %-d, %Y" }}</small>
  <p><a href="{{ post.url }}">{{ post.title }}</a></p>
</div>
{% endif %}
{% endfor %}

## Weekly Victories

{% for post in site.posts %}
{% if post.title == "Weekly Victories" %}

<div class="post">
  <p>
    <a href="{{ post.url }}">
      {{ post.date | date: "%b %-d, %Y" }}
    </a>
  </p>
</div>
{% endif %}
{% endfor %}
