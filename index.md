---
layout: default
title: Kian Kyars
description: Kian Kyars is a Canadian builder and researcher in San Francisco working on AI systems and developer tools.
permalink: /
hide_title: true
---

<section class="hero">
  <p class="eyebrow">Builder, researcher, writer</p>
  <h1>I build systems and write down what I learn.</h1>
  <p class="lede">I’m a Canadian builder and researcher in San Francisco. I work on AI systems and developer tools. Recent projects include from-scratch versions of SQLite and a regex engine.</p>
  <div class="hero-actions">
    <a class="button button-primary" href="{{ '/build/' | relative_url }}">See what I’m building</a>
    <a class="button" href="{{ '/blog/' | relative_url }}">Read the blog</a>
  </div>
</section>
<section class="home-section" aria-labelledby="recent-writing">
  <div class="section-heading">
    <h2 id="recent-writing">Recent writing</h2>
    <a href="{{ '/blog/' | relative_url }}">All writing &rarr;</a>
  </div>

  {% assign recent_posts = site.posts | where_exp: "post", "post.path contains '_posts/blog/'" %}
  <ul class="post-list">
    {% for post in recent_posts limit: 6 %}
    <li>
      <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%Y-%m-%d" }}</time>
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    </li>
    {% endfor %}
  </ul>
</section>

<section class="home-section" aria-labelledby="selected-work">
  <div class="section-heading">
    <h2 id="selected-work">Selected work</h2>
    <a href="{{ '/build/' | relative_url }}">All projects &rarr;</a>
  </div>

  <div class="project-grid">
    <a class="project-card" href="https://github.com/kiankyars/sqlite">
      <small>Database</small>
      <strong>sqlite</strong>
      <span>An implementation of SQLite built from scratch with a small agent swarm.</span>
    </a>
    <a class="project-card" href="https://github.com/kiankyars/parallel-ralph">
      <small>Agent infrastructure</small>
      <strong>parallel-ralph</strong>
      <span>A distributed asynchronous harness for running coding agents.</span>
    </a>
    <a class="project-card" href="https://rlvrbook.com">
      <small>Textbook</small>
      <strong>RLVR</strong>
      <span>Reinforcement Learning from Verifiable Rewards.</span>
    </a>
  </div>
</section>

<section class="home-section" aria-labelledby="elsewhere">
  <h2 id="elsewhere">Elsewhere</h2>
  <ul class="link-row">
    <li><a href="https://github.com/kiankyars">GitHub</a></li>
    <li><a href="https://twitter.com/neuralkian">X</a></li>
    <li><a href="https://www.linkedin.com/in/kyars">LinkedIn</a></li>
    <li><a href="https://scholar.google.com/citations?user=tVqRWjoAAAAJ">Google Scholar</a></li>
    <li><a href="https://kiankyars.substack.com">Substack</a></li>
    <li><a href="https://www.youtube.com/@neuralkian">YouTube</a></li>
    <li><a href="https://www.strava.com/athletes/kyars">Strava</a></li>
    <li><a href="https://www.goodreads.com/user/show/108079212-kian">Goodreads</a></li>
  </ul>

  <p><a href="https://calendar.app.google/zCVm4G9X42sqKqfX8">Book a co-working session</a> or <a href="https://forms.gle/mgTM1h5fR4qzw5JR7">leave anonymous feedback</a>.</p>
</section>
