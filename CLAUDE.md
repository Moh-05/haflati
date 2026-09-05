# CLAUDE.md — working notes for this repo

## What this is

The marketing/demo site for **حفلتي (Haflati)**, a two-sided events marketplace
for the Syrian market. Bilingual Arabic (RTL, default) / English (LTR).

It is a **static site with no build step**. No npm, no bundler, no framework, no
server code. One `index.html` (~347 KB) that contains all the markup, all the
CSS, and all the JavaScript inline, plus an `assets/` folder.

Do not introduce a build system, a package manager, a framework, or a CSS
preprocessor. If a task seems to need one, stop and ask first.

## Layout

```
index.html            everything — markup, CSS, JS, i18n strings
assets/img/           81 screen captures + logos + qr, all .webp
                      (except og.jpg — the social card, must stay JPEG)
assets/video/         4 hero clips (webm + mp4, light + dark theme)
downloads/            the two APKs go here — not yet present
tools/                maintenance scripts, see below
404.html              redirect shim for mistyped paths
.nojekyll             keep this — stops GitHub running Jekyll
DEPLOY.md             full deployment + optimisation notes. Read it.
```

`haflati-standalone.html` may sit one directory above this folder. It is a
self-contained build with every image inlined as base64 (5.8 MB). It is the
source of truth for edits, but **it must never be committed or published** —
inlined images cannot be lazy-loaded or cached, which is the whole reason the
split build exists.

## How the page works

- **Routing is hash-based**: `#/`, `#/about`, `#/app`, `#/partners`, `#/admin`,
  `#/tech`, `#/download`. No server rewrites needed and no path 404s.
- **All images go through one JS object** called `IMG`, roughly at line 3704.
  It maps a key to a file path. Nothing references an image file directly in
  markup — the `<img>` tags carry `data-pair` / `data-img` attributes and the JS
  fills in `src`. If you change an image filename you must update `IMG`.
- **All user-facing copy goes through an i18n object** (`ar` first, `en`
  second, as a two-element array per key). Elements carry `data-i18n="key"`.
  Static markup and the i18n entry must say the same thing — if you edit copy in
  one place, edit the other, or the text silently changes when the user toggles
  language.
- **Theme** is light/dark. Most screen captures exist as a `L`/`D` pair and the
  JS picks the right one.

## Tasks, in order

### 1. Self-host the fonts

Currently the page blocks on `fonts.googleapis.com` and `fonts.gstatic.com` —
two extra DNS lookups and TLS handshakes before any text renders in the right
face. That is the single biggest remaining slowdown, and it hits hardest on the
Syrian mobile connections that are the actual audience.

```bash
python3 tools/selfhost-fonts.py
```

Needs `pillow`-free stdlib only, but does need internet. It downloads the 9
weights the CSS actually uses (400/600/700/800 — the requested 300 and 500 are
unused), keeps only the Arabic and Latin subsets, writes
`assets/fonts/fonts.css`, replaces the Google `<link>` block in `index.html`,
and adds `preload` tags for Cairo 400 and El Messiri 700.

This script has **not been run or verified end to end** — only its
find-and-replace regex was tested against the real `index.html`. If the download
fails, report what happened rather than working around it silently. Manual
fallback: download El Messiri, Cairo and Plus Jakarta Sans from fonts.google.com,
put the `.woff2` files in `assets/fonts/`, re-run.

Verify: DevTools → Network → filter `font`. Every font request should come from
localhost. Zero requests to `fonts.gstatic.com`.

Then check both languages and both themes still render correctly — Arabic
headings use El Messiri, Arabic body uses Cairo, English uses Plus Jakarta Sans.
El Messiri has no 800 weight, so `font-weight:800` on Arabic headings is
synthesised by the browser. That is expected, not a bug to fix.

### 2. Test locally

```bash
python3 -m http.server 8000
```

Open `http://localhost:8000`. Check:

- All six routes load and the nav highlights correctly
- Language toggle AR ↔ EN, both directions, on every route
- Theme toggle light ↔ dark — captures swap, hero video swaps
- The phone simulator advances through its screens
- Below 1000px the nav becomes a horizontal section strip
- No 404s in the Network tab (except the two APKs, see below)
- No console errors

`downloads/haflati-user.apk` and `downloads/haflati-partners.apk` will 404.
That is expected — the files are being supplied separately and are not here yet.
Do not stub them, do not remove the buttons, do not change their paths.

### 3. Publish to GitHub Pages

```bash
git init -b main
git add -A
git commit -m "Haflati site"
git remote add origin https://github.com/Moh-05/<repo>.git
git push -u origin main
```

Then Settings → Pages → Deploy from a branch → `main` / `/ (root)`.

After the URL is known:

```bash
python3 tools/set-url.py https://moh-05.github.io/<repo>
```

This stamps the absolute URL into the `og:image` and `canonical` tags. Open
Graph requires absolute URLs, so until this runs the WhatsApp/Facebook link
preview will not render the share card. Commit and push the change.

### 4. APKs (later, when the files arrive)

Drop them into `downloads/` named exactly `haflati-user.apk` and
`haflati-partners.apk`. The buttons already point there and already carry the
`download` attribute. Nothing in the HTML changes.

~20 MB each. Commit them with plain `git add`. **Do not use Git LFS** — LFS
files served through GitHub Pages do not download correctly. `.gitattributes`
already marks `*.apk` binary.

## Guardrails

- **Do not reformat, minify, or prettify `index.html`.** It is hand-maintained
  and still being edited. A reformat makes every future diff unreadable.
- **Do not touch the Arabic copy** unless explicitly asked. Watch for RTL
  characters and Arabic-Indic numerals (`١`, `٧`) — the site uses them
  deliberately, do not "normalise" them to Latin digits.
- **Do not convert `og.jpg` to WebP.** Several social scrapers still don't read
  WebP. `tools/optimize-images.py` already skips it.
- **Do not re-optimise the images.** They are already WebP, already downscaled
  from 600px to 500px to match the ~246 CSS px the phone frame paints them at.
  `tools/optimize-images.py` is only for after a fresh export from the
  standalone build, when `.jpg`/`.png` files reappear.
- **Do not add analytics, tracking, cookie banners, or third-party embeds**
  without asking. The point of the recent work was removing third-party
  dependencies, not adding them.
- GitHub Pages forces `Cache-Control: max-age=600` on everything and there is no
  setting to change it. Don't spend time trying — if long caching becomes
  important, the answer is moving to Netlify or Cloudflare Pages, not a
  workaround.

## Done when

- [ ] Fonts served from `assets/fonts/`, zero requests to Google
- [ ] All six routes work in both languages and both themes
- [ ] No console errors, no unexpected 404s
- [ ] Pushed to GitHub, Pages build green, live URL loads
- [ ] `tools/set-url.py` run with the real URL and committed
- [ ] APKs added and both download buttons tested (later)
