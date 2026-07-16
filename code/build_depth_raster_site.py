#!/usr/bin/env python3
"""Build the public site from the depth_raster_viz single-session explorers.

The updated explorers are one HTML per session and already contain the SLN
explore view plus the full-method compare raster. They are too large to publish
raw, so this applies the same gzip/base64 DATA wrapper used by the older site.
"""
from __future__ import annotations

import argparse
import base64
import gzip
import html
import re
from pathlib import Path

PAKO = '<script src="https://cdn.jsdelivr.net/npm/pako@2.1.0/dist/pako.min.js"></script>'
MARKER = "pako.ungzip"

# All AL032 and Steinmetz sessions are kept. AL031/AL036 are sampled across
# time so public/ stays comfortably below the GitHub Pages 1 GB published-site
# limit.
SCOPE = {
    "AL032": [
        "AL032_2019-11-21",
        "AL032_2019-11-22",
        "AL032_2019-12-03",
        "AL032_2019-12-13",
        "AL032_2020-01-07",
        "AL032_2020-01-16",
        "AL032_2020-02-04",
        "AL032_2020-02-19",
        "AL032_2020-03-06",
        "AL032_2020-03-19",
        "AL032_2020-03-31",
        "AL032_2020-06-03",
    ],
    "AL031": [
        "AL031_2019-12-02",
        "AL031_2020-08-05",
    ],
    "AL036": [
        "AL036_2020-02-14",
        "AL036_2020-05-15",
        "AL036_2020-08-05",
    ],
    "Steinmetz": [
        "dataset1_p1",
        "dataset1_p2",
        "dataset2_p1",
        "dataset2_p2",
        "dataset3_p1",
        "dataset3_p2",
    ],
}


def compress(text: str) -> str:
    if MARKER in text:
        return text
    lines = text.split("\n")
    data_idx = next(i for i, line in enumerate(lines) if line.lstrip().startswith("const DATA"))
    match = re.match(r"(\s*)const DATA = (.*);\s*$", lines[data_idx])
    if not match:
        raise ValueError("could not parse the `const DATA = ...;` line")
    indent, payload = match.group(1), match.group(2)
    b64 = base64.b64encode(gzip.compress(payload.encode("utf-8"), 9)).decode("ascii")
    lines[data_idx] = (
        f"{indent}const DATA = JSON.parse(pako.ungzip("
        f'Uint8Array.from(atob("{b64}"), c=>c.charCodeAt(0)), {{to:"string"}}));'
    )
    text = "\n".join(lines)
    if PAKO not in text:
        text = re.sub(
            r'(<script src="https://cdn\.plot\.ly/[^"]+"></script>)',
            r"\1\n" + PAKO,
            text,
            count=1,
        )
        if PAKO not in text:
            text = text.replace("</head>", PAKO + "\n</head>", 1)
    return text


def source_name(animal: str, session: str) -> str:
    return f"depth_raster_explorer_{animal}_{session}.html"


def build_index(public: Path, selected: dict[str, list[str]]) -> None:
    n_sessions = sum(len(sessions) for sessions in selected.values())
    rows: list[str] = []
    for animal, sessions in selected.items():
        rows.append(
            f'<h2>{html.escape(animal)} <span class="n">({len(sessions)} sessions)</span></h2><table>'
        )
        for session in sessions:
            fn = source_name(animal, session)
            rows.append(
                f'<tr><td class="sess">{html.escape(session)}</td>'
                f'<td><a href="{html.escape(fn)}">Open explorer</a></td></tr>'
            )
        rows.append("</table>")

    total_bytes = sum(path.stat().st_size for path in public.glob("*.html") if path.name != "index.html")
    page = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>SLN depth-raster explorers</title>
<style>
 body{{font-family:-apple-system,Segoe UI,Roboto,sans-serif;max-width:980px;margin:2rem auto;padding:0 1rem;color:#222}}
 h1{{font-size:1.45rem}} h2{{margin-top:1.6rem;border-bottom:1px solid #ddd;padding-bottom:.2rem}}
 .n{{color:#888;font-weight:normal;font-size:.9rem}}
 table{{border-collapse:collapse;width:100%}} td{{padding:.3rem .6rem;border-bottom:1px solid #f0f0f0}}
 td.sess{{font-family:ui-monospace,monospace;color:#555;width:18rem}}
 a{{text-decoration:none;color:#1a66cc}} a:hover{{text-decoration:underline}}
 .note{{color:#555;background:#f6f8fa;border:1px solid #eaecef;border-radius:6px;padding:.55rem .8rem;font-size:.9rem;margin:.7rem 0}}
</style></head><body>
<h1>SLN depth-raster explorers</h1>
<p>{n_sessions} compressed single-session explorers. Each page contains the SLN localization explorer, depth raster, waveform overlay, and full-method compare raster.</p>
<div class="note">AL032 and Steinmetz are complete. AL031 and AL036 are sampled across the recording timeline to keep the published GitHub Pages payload below 1 GB. Current dashboard payload: {total_bytes / 1e6:.0f} MB.</div>
{''.join(rows)}
</body></html>
"""
    (public / "index.html").write_text(page, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    repo = Path(__file__).resolve().parents[1]
    default_source = repo.parent / "ks_SLN_single_session" / "depth_raster_viz"
    parser.add_argument("--repo", type=Path, default=repo)
    parser.add_argument("--source", type=Path, default=default_source)
    args = parser.parse_args()

    public = args.repo / "public"
    public.mkdir(parents=True, exist_ok=True)

    for path in public.glob("*.html"):
        path.unlink()

    total = 0
    for animal, sessions in SCOPE.items():
        for session in sessions:
            name = source_name(animal, session)
            src = args.source / name
            if not src.exists():
                raise FileNotFoundError(src)
            dst = public / name
            before = src.stat().st_size
            dst.write_text(compress(src.read_text(encoding="utf-8")), encoding="utf-8")
            after = dst.stat().st_size
            total += after
            print(f"{name}: {before / 1e6:.2f}MB -> {after / 1e6:.2f}MB")

    build_index(public, SCOPE)
    print(f"public dashboard payload: {total / 1e6:.0f} MB ({total / 1e9:.2f} GB)")


if __name__ == "__main__":
    main()
