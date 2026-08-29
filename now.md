---
layout: default
title: "Now"
permalink: /now/
---

- In SF.

## Currently reading

<ul>
{% for book in site.data.currently_reading %}
  <li><a href="{{ book.url }}"><em>{{ book.title | escape }}</em></a> by {{ book.author | escape }}</li>
{% else %}
  <li>Nothing at the moment.</li>
{% endfor %}
</ul>
