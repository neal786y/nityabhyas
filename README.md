# nityabhyas.in

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
GitHub Pages from `main`, root folder (`.nojekyll` serves files as they are). Custom domain via `CNAME` and the registrar's DNS; enforce HTTPS in Settings → Pages.
