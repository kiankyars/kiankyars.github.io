---
layout: default
title: Writing
description: Essays and notes on AI, software, investing, books, and personal experiments.
permalink: /blog/
---

<p class="page-intro">Essays and notes on AI, software, investing, books, and personal experiments. Follow new posts through <a href="{{ '/feed.xml' | relative_url }}">RSS</a>.</p>

{% assign blog_posts = site.posts | where_exp: "post", "post.path contains '_posts/blog/'" %}
{% assign current_year = "" %}

{% for post in blog_posts %}
{% assign post_year = post.date | date: "%Y" %}
{% if post_year != current_year %}
{% unless forloop.first %}</ul>{% endunless %}
<h2 class="archive-year">{{ post_year }}</h2>
<ul class="post-list">
{% assign current_year = post_year %}
{% endif %}
<li>
  <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%Y-%m-%d" }}</time>
  <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
</li>
{% if forloop.last %}</ul>{% endif %}
{% endfor %}
