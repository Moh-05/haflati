#!/usr/bin/env python3
"""Re-run the image pipeline after re-exporting captures from the standalone build.

    pip install pillow
    python3 tools/optimize-images.py            # convert, then rewrite index.html
    python3 tools/optimize-images.py --dry-run  # report only

Drops any new .jpg/.png into assets/img/, downscales it to the size it is
actually painted at on a 2x screen, encodes WebP, deletes the original, and
points the IMG map in index.html at the .webp.

Why the cap: the phone frame is max-width 264px with 9px padding, so a capture
is painted at ~246 CSS px. 500px covers a 2x display with room to spare;
anything wider is bytes the visitor downloads and the browser throws away.
"""
import io, os, re, sys, glob, pathlib
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
DRY = '--dry-run' in sys.argv

# filename prefix -> max width in device pixels
CAP = {'sh_': 500, 'poster': 540}
QUALITY_PHOTO = 80    # captures, cards
QUALITY_ALPHA = 88    # logos, marks — alpha channel, flat colour, less forgiving

os.chdir(ROOT)
originals = [f for f in sorted(glob.glob('assets/img/*.jpg') + glob.glob('assets/img/*.png'))
             if os.path.basename(f) != 'og.jpg']   # social card must stay JPEG
if not originals:
    print("nothing to convert — assets/img/ is already all WebP")
    sys.exit(0)

before = after = 0
for f in originals:
    name = os.path.basename(f)
    im = Image.open(f)
    target = next((w for pre, w in CAP.items() if name.startswith(pre)), None)
    if target and im.size[0] > target:
        im = im.resize((target, round(im.size[1] * target / im.size[0])), Image.LANCZOS)

    out = os.path.splitext(f)[0] + '.webp'
    if not DRY:
        if im.mode in ('RGBA', 'LA', 'P'):
            im.convert('RGBA').save(out, 'WEBP', quality=QUALITY_ALPHA, method=6)
        else:
            im.convert('RGB').save(out, 'WEBP', quality=QUALITY_PHOTO, method=6)
        after += os.path.getsize(out)
        os.remove(f)
    before += os.path.getsize(f) if os.path.exists(f) else 0

if DRY:
    print(f"would convert {len(originals)} file(s)")
    sys.exit(0)

s = io.open('index.html', encoding='utf-8').read()
s, n = re.subn(r'(assets/img/[A-Za-z0-9_]+)\.(?:jpg|png)(?!")', r'\1.webp', s)
s = s.replace('assets/img/og.webp', 'assets/img/og.jpg')   # never rewrite the card
io.open('index.html', 'w', encoding='utf-8').write(s)

print(f"{len(originals)} image(s): {before/1024/1024:.2f} MB -> {after/1024/1024:.2f} MB")
print(f"index.html: {n} path(s) rewritten")
