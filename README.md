# Kian Kyars

Source for [kiankyars.github.io](https://kiankyars.github.io), a personal site built with Jekyll and published through GitHub Pages.

## Run locally

Install Ruby 3.3.4, then run:

```bash
bundle install
bundle exec jekyll serve
```

Open `http://127.0.0.1:4000`.

## Add content

Create a blog post from the repository root:

```bash
python3 misc/create_post.py my-post-slug
```

Create the next Weekly Victories post:

```bash
python3 misc/create_post.py w
```

Posts live in `_posts/blog/` and `_posts/weekly-victories/`. Put post images in `imgs/YYYY-MM-DD-slug/`.

## Check changes

```bash
bundle exec jekyll build --strict_front_matter
bundle exec ruby scripts/check_site.rb _site
```

GitHub runs the same build for pushes and pull requests. Publishing remains managed by the repository's GitHub Pages configuration.
