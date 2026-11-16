#!/usr/bin/env python3
"""Keeps the shared parts of every page in step. Standard library only; no build step.

Each page is a normal, hand-editable HTML file. Shared blocks sit between markers:

    <!-- @head -->   ...   <!-- /@head -->
    <!-- @header --> ...   <!-- /@header -->
    <!-- @footer --> ...   <!-- /@footer -->

Run `python3 tools/sync.py` after editing anything in tools/partials/. It rewrites only those blocks,
fills each page's canonical/hreflang URLs (English at /x/, Hindi at /hi/x/), marks the current menu
item, and writes sitemap.xml. `--check` fails (exit 1) if any page is out of date, without writing.
"""
import datetime
import pathlib
import re
import sys

# The final address. Change this one line when the domain is bought.
SITE = "https://www.nityabhyas.in"

ROOT = pathlib.Path(__file__).resolve().parent.parent
PARTIALS = ROOT / "tools" / "partials"
SKIP_DIRS = {"tools", "images", "fonts", ".git", ".github"}
BLOCKS = ("head", "header", "footer")


def pages():
    for path in sorted(ROOT.rglob("*.html")):
        parts = path.relative_to(ROOT).parts
        if not SKIP_DIRS.intersection(parts) and not any(p.startswith(".") for p in parts):
            yield path


def urls_for(path):
    """(lang, en_url, hi_url, en_link, hi_link): clean public URLs (/privacy, as Play and the app link them;
    GitHub Pages serves privacy.html there) and file links that also work in a local preview."""
    rel = path.relative_to(ROOT).as_posix()
    hindi = rel.startswith("hi/")
    base = rel[3:] if hindi else rel
    en_link, hi_link = "/" + base, "/hi/" + base
    if base == "index.html":
        en_link, hi_link = "/", "/hi/"
    clean = "" if base == "index.html" else base[: -len(".html")]
    return ("hi" if hindi else "en"), "/" + clean, "/hi/" + clean, en_link, hi_link


def render(name, lang, url, en, hi, link, en_link, hi_link):
    file = PARTIALS / (f"{name}.html" if name == "head" else f"{name}.{lang}.html")
    text = file.read_text(encoding="utf-8")
    values = {
        "site": SITE, "url": url, "en_url": en, "hi_url": hi, "en_link": en_link, "hi_link": hi_link,
        "og_locale": "hi_IN" if lang == "hi" else "en_IN",
        "year": str(datetime.date.today().year),
    }
    text = re.sub(r"\{\{(\w+)\}\}", lambda m: values[m.group(1)], text)
    if name == "header":
        # The current section is highlighted in the menu (and announced by screen readers).
        text = re.sub(
            r'<a href="([^"]+)">',
            lambda m: f'<a href="{m.group(1)}" aria-current="page">'
            if m.group(1) == link and link not in ("/", "/hi/") else m.group(0),
            text,
        )
    return text.strip("\n")


def sync(check=False):
    stale, entries = [], []
    for path in pages():
        lang, en, hi, en_link, hi_link = urls_for(path)
        url = hi if lang == "hi" else en
        link = hi_link if lang == "hi" else en_link
        original = path.read_text(encoding="utf-8")
        updated = original
        for name in BLOCKS:
            pattern = re.compile(rf"(<!-- @{name} -->)(.*?)(\s*<!-- /@{name} -->)", re.S)
            if not pattern.search(updated):
                sys.exit(f"{path.relative_to(ROOT)}: missing <!-- @{name} --> block")
            indent = re.search(rf"\n([ \t]*)<!-- @{name} -->", updated)
            pad = indent.group(1) if indent else ""
            body = "\n".join(pad + line if line else line for line in render(name, lang, url, en, hi, link, en_link, hi_link).split("\n"))
            updated = pattern.sub(lambda m: f"{m.group(1)}\n{body}\n{pad}<!-- /@{name} -->", updated, count=1)
        if updated != original:
            stale.append(path.relative_to(ROOT).as_posix())
            if not check:
                path.write_text(updated, encoding="utf-8")
        if not path.name == "404.html":
            entries.append((url, en, hi))
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for url, en, hi in entries:
        sitemap += [f"  <url><loc>{SITE}{url}</loc>",
                    f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE}{en}"/>',
                    f'    <xhtml:link rel="alternate" hreflang="hi" href="{SITE}{hi}"/>',
                    "  </url>"]
    sitemap.append("</urlset>")
    sitemap_text = "\n".join(sitemap) + "\n"
    sitemap_path = ROOT / "sitemap.xml"
    if not sitemap_path.exists() or sitemap_path.read_text(encoding="utf-8") != sitemap_text:
        stale.append("sitemap.xml")
        if not check:
            sitemap_path.write_text(sitemap_text, encoding="utf-8")
    return stale


if __name__ == "__main__":
    check = "--check" in sys.argv
    changed = sync(check)
    if check and changed:
        sys.exit("Out of date (run python3 tools/sync.py): " + ", ".join(changed))
    print(("Up to date" if not changed else "Updated: " + ", ".join(changed)) if not check else "Up to date")
