# Interactive localization dashboards

GitHub Pages site for the UnitMatch / SLN↔DREDge Post-NeurIPS interactive
localization dashboards (self-contained Plotly/Bokeh HTML).

`public/index.html` is the curated landing page: per-session `cnn` / `transformer`
dashboards grouped by animal (AL032, AL036, Misi), plus a **Combined** section for the
all-session-per-animal dashboards (AL032, AL036, Steinmetz). 69 HTML files,
~872 MB total. Each dashboard pulls Plotly from a CDN, so viewers need internet.

## Layout

```
public/            # everything deployed to Pages
├── index.html     # landing page
└── *.html         # 68 dashboards
.github/workflows/deploy.yml   # publishes public/ to Pages on push to main
```

## One-time GitHub setup

1. Create the repo and push this folder.
2. Repo **Settings → Pages → Build and deployment → Source: GitHub Actions**.
3. Push to `main` (or run the workflow manually); the live URL appears in the
   `deploy` job output.

> **Note:** GitHub Pages is publicly accessible even on a private repo (unless
> you're on GitHub Enterprise with access control). Don't publish here if the
> dashboards shouldn't be world-readable.

## Updating figures

Replace files in `public/`, keeping the naming the index expects
(`<animal>_<session>_<cnn|transformer>.html`, `<animal>_<cnn|transformer>_combined.html`),
then commit and push. Edit `public/index.html` if you add/remove sessions.

## Local preview

```bash
python -m http.server -d public 8000   # open http://localhost:8000
```
