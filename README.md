# Interactive localization dashboards

GitHub Pages site for the UnitMatch / SLN↔DREDge Post-NeurIPS interactive
localization dashboards (self-contained Plotly HTML).

`public/index.html` is the landing page: per-session dashboards grouped by animal
(AL032, AL036, Misi, Steinmetz), each session linking the **localization-method ladder**

| label | localization |
|-------|--------------|
| `cnn` / `transformer` | SLN + DREDge (the two SLN architectures) |
| `MP` | monopolar TPCA, **no** drift correction |
| `MP+Dredge` | monopolar TPCA + one-shot DREDge drift correction |

Up to 4 dashboards per session. Each is a single self-contained HTML; the embedded
data (full background cloud + 1000 click-to-inspect spikes, exact precision) is stored
**gzip-compressed and base64-encoded**, decoded in the browser with `pako`, so each file
is ~5 MB instead of ~12 MB and all four methods fit under the GitHub Pages **1 GB limit**.
Dashboards pull Plotly and pako from CDNs, so viewers need internet.

## Layout

```
public/            # everything deployed to Pages
├── index.html     # landing page (4 links per session)
└── *.html         # per-session dashboards: <animal>_<session>_<cnn|transformer|mp_raw|mp_dredge>.html
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

The `public/` content is generated from the reruns dashboards by
`Post_Neurips/mp_ladder/code/build_website.py`, which compresses each source HTML
(`compress_html.py` — gzip+base64+pako, lossless) and rebuilds `index.html`. To add or
refresh sessions, rerun that script (`--force` to recompress existing) and push.
Keep the naming the index expects:
`<animal>_<session>_<cnn|transformer|mp_raw|mp_dredge>.html`.

Mind the 1 GB Pages limit (`du -sh public`); compression keeps ~150 dashboards near
~0.8 GB. The `mp_raw`→`MP` and `mp_dredge`→`MP+Dredge` labels are set in the index.

## Local preview

```bash
python -m http.server -d public 8000   # open http://localhost:8000
```
