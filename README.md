# Nityabhyas website

Live at **https://neal786y.github.io/nityabhyas/** (GitHub Pages).

Product website for **Nityabhyas**, the daily aptitude-practice app (English and Hindi). Static HTML on GitHub Pages: no build step, no dependencies, no tracking.

## Pages
| English | Hindi | What |
|---|---|---|
| `index.html` | `hi/index.html` | Home: hero, features, how it works, exams, Free vs Pro, screenshots, FAQ, about |
| `support.html` | `hi/support.html` | Help & FAQ and contact (the app's support link) |
| `privacy.html` | `hi/privacy.html` | Privacy policy (Play and the app link here: never rename) |
| `terms.html` | `hi/terms.html` | Terms of use (the app links here: never rename) |
| `404.html` | – | One bilingual "not found" page for the whole site |

Public addresses drop `.html` (`/privacy`, `/hi/terms`); GitHub Pages serves the file at both.

## Design
The app's design system (Rozabhyas repo, `docs/DESIGN.md`): the *Jamun* palette in light and the designed dark set, Mukta (self-hosted in `fonts/`, Latin + Devanagari), flat cards with 1 px borders, purple for action, apricot only for rewards, green/red never decorative. All tokens are at the top of `styles.css`.

## Editing
- Edit any page directly. Shared parts (`<head>` basics, header, footer) live in `tools/partials/`; after changing one, run:
  ```
  python3 tools/sync.py          # updates every page's shared blocks and sitemap.xml
  python3 tools/sync.py --check  # fails if a page is out of date
  ```
  The site address (`SITE`) is set once at the top of `tools/sync.py`.
- Hindi text is marked `TODO-HI-REVIEW` until reviewed.
- Legal texts change only together with the app's Data safety answers (source drafts: Rozabhyas `docs/legal/`).
- No inline styles or scripts: the Content-Security-Policy allows only this site's own files.

## Check every link
```
python3 tools/linkcheck.py https://neal786y.github.io/nityabhyas    # after each push (exit 1 = broken links)
```

## Preview locally
```
python3 -m http.server 8765    # then open http://127.0.0.1:8765/  (add ?theme=dark to preview dark mode)
```

## Screenshots
From the app's Play kit (Rozabhyas `docs/play/screenshots/{en,hi}`):
```
for l in en hi; do for f in <rozabhyas>/docs/play/screenshots/$l/*.png; do n=$(basename $f .png); n=${n#*-}
  sips -s format jpeg -s formatOptions 82 --resampleWidth 540 $f --out images/shots/$l/$n.jpg; done; done
```

## Deploy
GitHub Pages from `main`, root folder (`.nojekyll` serves files as they are): every push to `main` is live in about a minute.

All links are relative (written by `tools/sync.py`), so the same files work at `github.io/nityabhyas/`, on a custom domain and in a local preview. The 404 page is the exception: its links are absolute from `BASE`.

**Never rename this repo or the GitHub account:** released app versions link to `https://neal786y.github.io/nityabhyas/privacy`, `/terms` and `/support`.

### Moving to a custom domain later
1. Buy the domain; at the registrar add `CNAME www → neal786y.github.io` and the four GitHub Pages `A`/`AAAA` records for the bare domain.
2. Set `SITE` in `tools/sync.py` to `https://www.<domain>`, run `python3 tools/sync.py`, add a `CNAME` file with `www.<domain>`, push.
3. Settings → Pages: set the custom domain, then **Enforce HTTPS**.
GitHub then redirects every old `github.io/nityabhyas/...` address (path included) to the domain, so old app versions keep working.
