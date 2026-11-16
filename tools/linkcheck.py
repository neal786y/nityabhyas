#!/usr/bin/env python3
"""Crawls the site from its English and Hindi home pages and checks every href/src on every page,
including #fragments (the section must exist on the target page). Standard library only.

    python3 tools/linkcheck.py https://neal786y.github.io/nityabhyas      # the live site
    python3 tools/linkcheck.py http://127.0.0.1:8766/nityabhyas            # a local copy served from a sub-folder

Exits 1 when anything is broken. Links to Google Play are skipped (the listing is private until release)."""
import re, sys, urllib.request, urllib.parse, html
base = sys.argv[1].rstrip('/') + '/'
start = [base, base + 'hi/']
pages, cache, bad, todo = set(), {}, [], list(start)
def fetch(u):
    if u not in cache:
        try:
            r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'linkcheck'}))
            cache[u] = (r.status, r.read().decode('utf-8', 'replace') if 'html' in r.headers.get('Content-Type', '') else '')
        except urllib.error.HTTPError as e: cache[u] = (e.code, '')
        except Exception as e: cache[u] = (str(e), '')
    return cache[u]
def ids(body): return set(re.findall(r'\bid="([^"]+)"', body))
while todo:
    page = todo.pop()
    if page in pages: continue
    pages.add(page)
    status, body = fetch(page)
    for attr, ref in re.findall(r'\b(href|src)="([^"]*)"', body):
        ref = html.unescape(ref)
        if ref.startswith(('mailto:', 'data:')) or 'play.google.com' in ref: continue
        full = urllib.parse.urljoin(page, ref)
        if not full.startswith(base):  # external: just check it answers
            continue
        url, _, frag = full.partition('#')
        st, b = fetch(url)
        if st != 200: bad.append(f'{page[len(base)-1:] or "/"}: {ref} -> {url[len(base)-1:]} [{st}]'); continue
        if frag and frag not in ids(b): bad.append(f'{page[len(base)-1:] or "/"}: {ref} -> missing #{frag} on {url[len(base)-1:]}')
        if b and url not in pages and url.startswith(base): todo.append(url)
print(f'pages crawled: {len(pages)}')
for p in sorted(pages): print('  ', p[len(base)-1:])
print(f'problems: {len(bad)}')
for b in sorted(set(bad)): print('  ', b)
sys.exit(1 if bad else 0)
