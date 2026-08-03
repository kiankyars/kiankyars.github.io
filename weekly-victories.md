---
layout: default
title: Weekly Victories
description: A weekly record of wins, lessons, and moments worth remembering.
permalink: /weekly-victories/
---

<p class="page-intro">A weekly record of wins, lessons, and moments worth remembering.</p>

{% assign victory_posts = site.posts | where_exp: "post", "post.path contains '_posts/weekly-victories/'" %}
{% assign current_year = "" %}

{% for post in victory_posts %}
{% assign post_year = post.date | date: "%Y" %}
{% if post_year != current_year %}
{% unless forloop.first %}</ul>{% endunless %}
<h2 class="archive-year">{{ post_year }}</h2>
<ul class="post-list">
{% assign current_year = post_year %}
{% endif %}
<li>
  <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%Y-%m-%d" }}</time>
  <a href="{{ post.url | relative_url }}">Week ending {{ post.date | date: "%B %-d" }}</a>
</li>
{% if forloop.last %}</ul>{% endif %}
{% endfor %}
