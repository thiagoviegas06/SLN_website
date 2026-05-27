# Interactive Figures Site

Publishes the UnitMatch Post-NeurIPS interactive figures (self-contained
Plotly/Bokeh HTML) to GitHub Pages.

## Adding figures

Copy your `*.html` files into `figures/` (subfolders are fine — nesting is
preserved and shown in the index):

```bash
cp -r /path/to/Unitmatch/Post_Neurips/figures/interactive/* figures/
```

Commit and push to `main`. The workflow rebuilds the index and redeploys.

## How it works

- `build_index.py` scans `figures/**/*.html`, copies everything into `site/`,
  and writes a `site/index.html` landing page linking each figure.
- `.github/workflows/deploy.yml` runs the build and publishes `site/` to Pages
  on every push to `main` (or via the Actions "Run workflow" button).

## One-time GitHub setup

1. Create a repo and push this folder to it.
2. Repo **Settings → Pages → Build and deployment → Source: GitHub Actions**.
3. Push to `main`; the site URL appears in the workflow's `deploy` job output.

## Local preview

```bash
python build_index.py
python -m http.server -d site 8000   # then open http://localhost:8000
```
