# Kian Kyars Personal Website

This project is a personal website and blog for Kian Kyars, hosted on GitHub Pages. It serves as a portfolio, blog, and repository of personal reflections.

## Project Structure

- `_posts/`: Contains all blog content, subdivided by type.
  - `blog/`: General articles and technical posts.
  - `weekly-victories/`: Weekly reflection posts.
- `_layouts/`: Jekyll templates.
  - `default.html`: The main wrapper for all pages.
  - `post.html`: Template specifically for blog posts.
- `imgs/`: Post-specific images, typically organized into subdirectories named after the post date and slug (e.g., `imgs/2026-02-12-sqlite/`).
- `assets/`:
  - `create_post.py`: A utility script to automate the creation of new posts with proper front matter.
  - `CV.pdf`, `main.pdf`: Static documents.
- Root Markdown files: Main site pages (`index.md`, `about.md`, `blog.md`, `build.md`, `now.md`, `publications.md`, `weekly-victories.md`).

## Development Workflows

### Creating New Content

Use the `assets/create_post.py` script to generate new post files with the correct front matter.

- **Blog Post:**
  ```bash
  python3 assets/create_post.py my-post-slug
  ```
  Creates `_posts/blog/YYYY-MM-DD-my-post-slug.md`.

- **Weekly Victory Post:**
  ```bash
  python3 assets/create_post.py w
  ```
  Creates `_posts/weekly-victories/YYYY-MM-DD-weekly-victories.md`.

## Content Conventions

- **Posts:** Written in Markdown with YAML front matter.
- **Images:** Should be placed in a subdirectory within `imgs/` that matches the post's filename slug to keep the directory organized.
- **Links:** Use relative URLs where possible to ensure portability.
