# Publishing حفلتي on GitHub Pages

## One file or many?

Many. Publish **this folder**. Do not publish `haflati-standalone.html`.

The standalone file inlines every image as a base64 data URI. That has three
consequences that all hurt on a slow connection:

1. **Nothing can be lazy.** A data URI is part of the HTML, so the browser has
   to download all 81 captures before it can paint anything. The visitor waits
   for the vendor-app screens on a page that only shows the home screen.
2. **Nothing can be cached separately.** Change one word of copy and the whole
   5.8 MB is re-downloaded. In this folder, `index.html` is 347 KB and the
   images sit beside it untouched.
3. **base64 costs ~33% more bytes** than the same image as a file.

Keep the standalone build. It is useful for emailing, for a USB stick, and as
the source of truth you edit. It just should not be the thing on the web.

---

## What was already done to make it fast

| | before | after |
|---|---|---|
| images | 3.36 MB | 1.87 MB |
| whole site | 4.7 MB | 3.2 MB |

- **All 81 images converted to WebP.** Supported by every browser that matters
  since 2020, including Chrome and Samsung Internet on Android 5+.
- **Captures downscaled 600px → 500px.** The phone frame is `max-width:264px`
  with 9px of padding, so a capture paints at ~246 CSS pixels. 500px still
  covers a 2× retina screen. The extra 100px was bytes the browser decoded and
  then threw away. Text in the captures was checked at rendered size — no
  visible loss.
- **Preload hints added** for the hero poster and the dark-theme clip. Their
  `src` is assigned by JavaScript, so the browser's preload scanner could not
  see them and the hero started loading late. Now both fetches begin while the
  HTML is still parsing.
- **`og.jpg` share card added** (1200×630) so links pasted into WhatsApp or
  Facebook render properly instead of showing a bare URL. It stays JPEG on
  purpose — several scrapers still do not read WebP.
- Duplicate `og:type` tag removed; `canonical`, `twitter:card` and `og:locale`
  added.

The 32 `loading="lazy"` attributes were already right — a capture is only
fetched when its screen is actually shown, so opening the home page never
downloads the vendor screens.

---

## Publishing

Everything is static. No build step, no server, no database.

```bash
cd haflati-deploy
git init -b main
git add -A
git commit -m "Haflati site"
git remote add origin https://github.com/Moh-05/haflati.git
git push -u origin main
```

Then **Settings → Pages → Build and deployment → Deploy from a branch →
`main` / `/ (root)`**. First build takes a minute or two.

Your URL will be `https://moh-05.github.io/haflati/`.

Once you know it, stamp it into the share-card tags:

```bash
python3 tools/set-url.py https://moh-05.github.io/haflati
git commit -am "set canonical URL"; git push
```

Open Graph requires absolute URLs, so until you run this the WhatsApp preview
will not show the card.

### Two details that matter

- **`.nojekyll` is in this folder — keep it.** Without it GitHub runs the site
  through Jekyll, which skips any file or folder starting with `_` and adds
  build time for nothing.
- **Routing is hash-based** (`#/about`, `#/app`), so no rewrite rules are
  needed and no path 404s. `404.html` is only there for a mistyped URL.

---

## Adding the two APKs

Drop them into `downloads/`, named exactly:

```
downloads/haflati-user.apk
downloads/haflati-partners.apk
```

The buttons on `#/download` already point at those paths and already carry the
`download` attribute, so the file saves instead of trying to open. Nothing in
the HTML needs to change.

```bash
cp /path/to/user.apk     downloads/haflati-user.apk
cp /path/to/partners.apk downloads/haflati-partners.apk
git add downloads/*.apk
git commit -m "add APKs"
git push
```

**About the size.** 20 MB each is fine. Git's hard limit is 100 MB per file and
GitHub warns at 50 MB. You do **not** need Git LFS — and you should not use it,
because LFS files served through Pages do not download correctly. Plain `git
add` is right here.

`.gitattributes` already marks `*.apk` as binary so Git never tries to diff or
line-ending-convert them.

GitHub Pages serves unknown extensions as `application/octet-stream`, which is
exactly what you want for an APK — the browser saves it. Android will still
warn about installing from outside the Play Store; that is normal for sideload
and the note under the buttons already says so.

**One caveat worth knowing:** every time you replace an APK, the old 20 MB stays
in the repository's history forever. Replace them a dozen times and the clone
gets heavy. If you expect frequent rebuilds, put the APKs on a **GitHub
Release** instead and point the two buttons at the release asset URLs — the
files then live outside the Git history. For a launch with occasional updates,
committing them directly is simpler and fine.

---

## What you cannot fix on GitHub Pages

GitHub Pages sets `Cache-Control: max-age=600` on everything — a ten-minute
browser cache — and there is no setting to change it. For a returning visitor
that means re-validating the images after ten minutes rather than reading them
straight from disk for a year.

It is not a disaster: revalidation returns `304 Not Modified` with no body, so
it costs a round trip rather than 1.87 MB. But if repeat-visit speed matters to
you, **Netlify or Cloudflare Pages** let you set a real header and are the same
drag-and-drop effort:

```
/assets/*    Cache-Control: public, max-age=31536000, immutable
```

On the plus side, GitHub Pages gzips text assets automatically, so your 347 KB
`index.html` goes over the wire at roughly 60 KB without you doing anything.

---

## Optional, if you want it faster still

**Self-host the fonts.** This is the biggest remaining win, and it matters most
for exactly your audience. Right now the page blocks on a stylesheet from
`fonts.googleapis.com`, then on font files from `fonts.gstatic.com` — two extra
DNS lookups and TLS handshakes before any text renders, on connections in Syria
where that round trip is expensive and Google endpoints are not always quick.

You are also requesting far more than you use: 4 weights of El Messiri, 5 of
Cairo, 6 of Plus Jakarta Sans. Cutting to the weights actually used and serving
subset `.woff2` files from `assets/fonts/` would remove the third-party
dependency entirely. Say the word and I will do it.

**Minify `index.html`.** 347 KB → roughly 210 KB, so ~60 KB → ~45 KB gzipped.
Real but small, and it makes the file unreadable, which is a genuine cost for
something you are still editing. I would leave this until the site is frozen.

---

## Re-running the image pipeline

`haflati-standalone.html` stays the source of truth. If you re-export the
deploy folder from it, the new export will have `.jpg`/`.png` files again. Then:

```bash
pip install pillow
python3 tools/optimize-images.py
```

It downscales, converts to WebP, deletes the originals, and rewrites the paths
in the `IMG` map inside `index.html`. `--dry-run` reports without touching
anything. It leaves `og.jpg` alone on purpose.

---

## Local check before pushing

```bash
python3 -m http.server 8000
```

Open `http://localhost:8000`. Opening `index.html` as a `file://` path works too
but the videos may not autoplay.

---

## Self-hosting the fonts

Run this once, on your own machine (it needs to reach Google Fonts):

```bash
python3 tools/selfhost-fonts.py
git add assets/fonts index.html && git commit -m "self-host fonts" && git push
```

It downloads only the 9 weights the CSS actually uses, keeps only the Arabic and
Latin subsets, writes `assets/fonts/fonts.css`, replaces the Google `<link>` in
`index.html`, and preloads Cairo 400 and El Messiri 700 — the two faces that
paint first.

Check it worked: open DevTools → Network → filter `font`. Every request should
come from your own domain, and nothing from `fonts.gstatic.com`.

If the script can't reach Google, download the three families from
fonts.google.com manually, drop the `.woff2` files in `assets/fonts/`, and the
script will use what is already there instead of re-downloading.
