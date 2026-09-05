#!/usr/bin/env python3
"""Stamp the live site URL into the OG and canonical tags.

    python3 tools/set-url.py https://amerzybq-hue.github.io/haflati

Open Graph needs absolute URLs, so WhatsApp/Facebook/X can only render the
share card once this has been run. Re-run it if the address ever changes.
"""
import io, re, sys, pathlib

if len(sys.argv) != 2:
    sys.exit(__doc__)

url = sys.argv[1].rstrip('/')
if not url.startswith('http'):
    sys.exit("URL must start with http:// or https://")

p = pathlib.Path(__file__).resolve().parent.parent / 'index.html'
s = io.open(p, encoding='utf-8').read()

# replace the placeholder, or an already-stamped URL, in og:image + canonical
s, n = re.subn(r'(?<=content=")SITE_URL(?=/assets/img/og\.jpg")', url, s)
s, m = re.subn(r'(?<=<link rel="canonical" href=")SITE_URL(?=/">)', url, s)
if n + m == 0:
    s, n = re.subn(r'(https?://[^"]*?)(/assets/img/og\.jpg")', url + r'\2', s)
    s, m = re.subn(r'(<link rel="canonical" href=")https?://[^"]*?(/">)', r'\g<1>' + url + r'\2', s)

io.open(p, 'w', encoding='utf-8').write(s)
print(f"stamped {n + m} tag(s) with {url}")
