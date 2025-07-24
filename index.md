---
layout: default
title: Home
---

## Blog

{% for post in site.posts %}
  <div class="post">
    <h2><a href="{{ post.url }}">{{ post.title }}</a></h2>
    <small>{{ post.date | date: "%b %-d, %Y" }}</small>
  </div>
{% endfor %}

## Weekly Victories

{% for post in site.posts %}
  {% if post.title == "Weekly Victories" %}
    <div class="post">
      <h2>
        <a href="{{ post.url }}">
          {{ post.date | date: "%b %-d, %Y" }}
        </a>
      </h2>
    </div>
  {% endif %}
{% endfor %}