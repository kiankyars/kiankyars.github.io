---
title: "Weekly Victories"
permalink: /weekly-victories/
---

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
