#!/usr/bin/env python3
"""Download the font weights the site actually uses and switch to self-hosting.

Run once, on your own machine (needs internet access to Google Fonts):

    python3 tools/selfhost-fonts.py

It downloads 9 woff2 files into assets/fonts/, writes assets/fonts/fonts.css,
and replaces the Google Fonts <link> in index.html with local tags.

All three families are SIL Open Font License, so self-hosting is allowed.

Weights kept — these are the only ones index.html actually uses (400/600/700/800):
    El Messiri        400, 700          (family has no 800; browser fakes it)
    Cairo             400, 600, 700
    Plus Jakarta Sans 400, 600, 700, 800
Dropped: every 300 and 500 you were requesting and never applying.

Subsets kept: arabic + latin. Google also ships latin-ext, cyrillic and
vietnamese blocks for these families — none of your copy needs them.
"""
import io, os, re, sys, pathlib, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONTDIR = ROOT / 'assets' / 'fonts'
KEEP_SUBSETS = {'arabic', 'latin'}

FAMILIES = [
    ('El Messiri',        [400, 700]),
    ('Cairo',             [400, 600, 700]),
    ('Plus Jakarta Sans', [400, 600, 700, 800]),
]

# Google serves woff2 only to browsers that advertise support.
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/120.0 Safari/537.36')


def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    return urllib.request.urlopen(req, timeout=30).read()


def main():
    FONTDIR.mkdir(parents=True, exist_ok=True)
    css_out, total = [], 0

    for family, weights in FAMILIES:
        q = family.replace(' ', '+')
        url = (f'https://fonts.googleapis.com/css2?family={q}:wght@'
               + ';'.join(str(w) for w in weights) + '&display=swap')
        try:
            css = get(url).decode('utf-8')
        except Exception as e:
            sys.exit(f"could not reach Google Fonts: {e}\n"
                     f"Check your connection, or download the families manually "
                     f"from fonts.google.com and drop the woff2 files in {FONTDIR}")

        # Google emits one @font-face per weight per unicode subset, each
        # preceded by a /* subset */ comment. Keep only the subsets we need.
        blocks = re.findall(r'/\*\s*([\w\-\[\]]+)\s*\*/\s*(@font-face\s*\{[^}]*\})', css)
        for subset, block in blocks:
            # Match the subset name exactly. Splitting on '-' would fold
            # latin-ext into latin, so both would fight over one filename.
            base = subset
            if base not in KEEP_SUBSETS:
                continue
            m = re.search(r'src:\s*url\((https://[^)]+\.woff2)\)', block)
            w = re.search(r'font-weight:\s*(\d+)', block)
            if not (m and w):
                continue

            name = f"{family.lower().replace(' ', '-')}-{w.group(1)}-{base}.woff2"
            path = FONTDIR / name
            if not path.exists():
                path.write_bytes(get(m.group(1)))
            total += path.stat().st_size

            local = block.replace(m.group(1), f'../fonts/{name}')
            local = re.sub(r'\)\s*format\([^)]*\)', ") format('woff2')", local)
            if 'font-display' not in local:
                local = local.replace('{', '{font-display:swap;', 1)
            css_out.append(local)

    (FONTDIR / 'fonts.css').write_text('\n'.join(css_out) + '\n', encoding='utf-8')
    print(f"{len(css_out)} face(s), {total/1024:.0f} KB -> assets/fonts/")

    # Swap the Google <link> tags for local ones, and preload the two faces
    # that paint first: Cairo 400 (body copy) and El Messiri 700 (headings).
    idx = ROOT / 'index.html'
    s = io.open(idx, encoding='utf-8').read()

    old = re.search(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">.*?'
                    r'<link href="https://fonts\.googleapis\.com/css2\?[^>]*>', s, re.S)
    if not old:
        print("index.html already switched — skipping")
        return

    pre = []
    for f in ('cairo-400-arabic.woff2', 'el-messiri-700-arabic.woff2'):
        if (FONTDIR / f).exists():
            pre.append(f'<link rel="preload" as="font" type="font/woff2" '
                       f'href="assets/fonts/{f}" crossorigin>')
    new = '\n'.join(pre + ['<link rel="stylesheet" href="assets/fonts/fonts.css">'])

    io.open(idx, 'w', encoding='utf-8').write(s.replace(old.group(0), new))
    print("index.html: Google Fonts link replaced with local stylesheet")


if __name__ == '__main__':
    main()
