---
layout: default
title: Home
---


{% for post in site.posts %}
    <div class="post">
      <h2>
        <a href="{{ post.url }}">
          {{ post.date | date: "%b %-d, %Y" }}
        </a>
      </h2>
    </div>
{% endfor %}