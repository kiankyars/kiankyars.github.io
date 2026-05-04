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

## Related Projects

### microddp (`/Users/kian/Developer/microddp`)

A course teaching Data Parallelism (DDP) from scratch using PyTorch distributed.

**Run commands** (always prefix with `PYTHONPATH=.`):
```bash
PYTHONPATH=. torchrun --nproc-per-node=N <script>
```

**Source files** (`src/`):
- `comms.py` — `init_distributed()`, `cleanup()`
- `model.py` — `FullMLP(dim, depth)`
- `allreduce.py` — 4 all-reduce implementations (`allreduce1`–`allreduce4`)
- `optimisations.py` — `register_hooks(model)`, `register_bucketed_hooks(model)`
- `manual.py` — reference single-process manual data parallel
- `main.py` — reference distributed DDP with hooks
- `examples.py` — performance comparison benchmarks

**Lab files** (`my_work/`):
- `step1_manual.py` — simulate 2 GPUs, average gradients by hand
- `step2_sandbox.py` — exercises with `dist.all_reduce`, broadcast, reduce
- `step3_allreduce.py` — implement naive all-reduce from scratch
- `step4_ddp.py` — full DDP training loop with gradient hooks

## Content Conventions

- **Posts:** Written in Markdown with YAML front matter.
- **Images:** Should be placed in a subdirectory within `imgs/` that matches the post's filename slug to keep the directory organized.
- **Links:** Use relative URLs where possible to ensure portability.
