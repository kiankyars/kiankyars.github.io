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
- Root Markdown files: Main site pages (`index.md`, `about.md`, `blog.md`, `build.md`, `now.md`, `publications.md`, `weekly-victories.md`).
- `misc/`: CV/resume and scripts — `CV.tex` (build with `make` in `misc/` → `CV.pdf`), `create_post.py`, and other PDFs (e.g. `main.pdf`).

## Development Workflows

### Creating New Content

Use the `misc/create_post.py` script to generate new post files with the correct front matter (run from repo root).

- **Blog Post:**

    ```bash
    python3 misc/create_post.py my-post-slug
    ```

    Creates `_posts/blog/YYYY-MM-DD-my-post-slug.md`.

- **Weekly Victory Post:**
    ```bash
    python3 misc/create_post.py w
    ```
    Creates `_posts/weekly-victories/YYYY-MM-DD-weekly-victories.md`.

### Updating the biomaxing L-theanine trial table

`_posts/blog/2026-02-04-biomaxing.md` has a daily table of Polar sleep score/charge and cardio-load status. To auto-fill empty cells from Polar AccessLink:

```bash
python3 misc/update_biomaxing.py
```

Idempotent: only writes empty cells. Reads `POLAR_ACCESS_TOKEN` from `~/.env`. Date conventions and token-refresh instructions are documented in the script's docstring. The general-purpose Polar OAuth helper lives at `misc/polar_accesslink.py`.
