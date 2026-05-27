#!/usr/bin/env python3
"""Generate a static index.html linking every interactive figure under figures/.

Self-contained Plotly/Bokeh HTML files need no build step themselves; this just
produces a browsable landing page. Run from the repo root: `python build_index.py`.
The generated site is written to site/ (figures are copied in alongside index.html).
"""
import html
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIGURES = ROOT / "figures"
SITE = ROOT / "site"
TITLE = "UnitMatch — Post-NeurIPS Interactive Figures"


def collect():
    """Return sorted (relative_path, display_name) for every .html under figures/."""
    items = []
    for p in sorted(FIGURES.rglob("*.html")):
        rel = p.relative_to(FIGURES)
        items.append((rel.as_posix(), rel.as_posix()))
    return items


def render(items):
    rows = "\n".join(
        f'      <li><a href="figures/{html.escape(href)}">{html.escape(name)}</a></li>'
        for href, name in items
    ) or '      <li><em>No figures found. Copy *.html files into figures/.</em></li>'
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(TITLE)}</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 820px; margin: 3rem auto; padding: 0 1rem; line-height: 1.5; }}
    h1 {{ font-size: 1.4rem; }}
    ul {{ list-style: none; padding: 0; }}
    li {{ padding: .35rem 0; border-bottom: 1px solid #eee; }}
    a {{ text-decoration: none; color: #1a56db; }}
    a:hover {{ text-decoration: underline; }}
    .count {{ color: #666; font-size: .9rem; }}
  </style>
</head>
<body>
  <h1>{html.escape(TITLE)}</h1>
  <p class="count">{len(items)} figure(s)</p>
  <ul>
{rows}
  </ul>
</body>
</html>
"""


def main():
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)
    items = collect()
    if FIGURES.exists():
        shutil.copytree(FIGURES, SITE / "figures")
    else:
        (SITE / "figures").mkdir()
    (SITE / "index.html").write_text(render(items), encoding="utf-8")
    print(f"Wrote {SITE/'index.html'} with {len(items)} figure link(s).")


if __name__ == "__main__":
    main()
