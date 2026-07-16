# SLN depth-raster explorer website

GitHub Pages site for the updated UnitMatch / SLN single-session depth-raster
explorers from:

`../ks_SLN_single_session/depth_raster_viz`

Each published dashboard is one self-contained HTML page containing the SLN
localization explorer, depth raster, waveform overlay, and full-method compare
raster. The source HTML files are about 69 MB each, so the site build rewrites
the embedded `const DATA = ...` payload as gzip + base64 and decodes it in the
browser with `pako`.

## Current published scope

All 41 AL031/AL032/AL036 sessions plus Steinmetz do not fit under the GitHub
Pages 1 GB published-site limit after compression. The current scope keeps all
AL032 and Steinmetz sessions, then samples AL031/AL036 across time:

- AL032: all 12 sessions
- Steinmetz: all 6 sessions
- AL031: 2019-12-02, 2020-08-05
- AL036: 2020-02-14, 2020-05-15, 2020-08-05

That gives 23 dashboards and leaves margin below the 1 GB Pages limit.

## Rebuild

From this directory:

```bash
python code/build_depth_raster_site.py
du -sh public
```

The script clears old generated HTML from `public/`, compresses the selected
`depth_raster_explorer_*.html` source files, and rebuilds `public/index.html`.

## Deploy

`.github/workflows/deploy.yml` publishes `public/` to GitHub Pages on pushes to
`main` or manual workflow dispatch.

GitHub Pages publishes the current `public/` tree, but the repository history can
still be much larger than the published site if older dashboard blobs remain in
git. To actually shrink the remote repository, rewrite history or recreate the
repo from the current tree, then force-push intentionally.

## Local preview

```bash
python -m http.server -d public 8000
```
