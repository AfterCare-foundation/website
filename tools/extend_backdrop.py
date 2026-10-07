#!/usr/bin/env python3
"""Recompose a portrait studio photo onto a wider canvas.

Used for the desktop version of the "Stay informed" card photo in
visual-assets/. The desktop panel is roughly square-to-landscape, so the
portrait photo either gets cropped to a sliver or sits as a strip. This
scales the photo, places the subject where asked, and continues the plain
backdrop out to the canvas edges. No subject pixels are invented: each row
of the backdrop is carried on from the photo's edge, relaxing into a smooth
vertical gradient further out so no row leaves a horizontal streak.

Only works for photos whose backdrop is plain at the left and right edges.

Requires:  pip install pillow numpy

Usage (PowerShell and bash, one line):

  python tools/extend_backdrop.py IN.webp OUT.webp --bbox 67,287,631,1091

Arguments
  --bbox     subject bounding box in the source, x0,y0,x1,y1 in pixels.
  --size     output canvas, WxH (default 1160x1036, the desktop panel's
             shape at 2x).
  --height   subject height as a fraction of the canvas (default 0.66).
  --left     subject's left edge as a fraction of canvas width (default 0.16).
  --cy       subject's vertical centre as a fraction of canvas height
             (default 0.52).

Preset used on the site (run from the repo root):

  # Stay informed, desktop: banana left of centre, room on the right for
  # the notification bubble (.why-notif sits 10% in from the right edge)
  python tools/extend_backdrop.py visual-assets/why-stay-informed-remap.webp visual-assets/why-stay-informed-remap-wide.webp --bbox 67,287,631,1091

The panel is narrower than the canvas at small desktop widths and crops up
to ~8% off each side, so keep the subject clear of the outer edges.
"""
import argparse
import numpy as np
from PIL import Image, ImageFilter

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("dst")
ap.add_argument("--size", default="1160x1036")
ap.add_argument("--bbox", required=True, help="subject x0,y0,x1,y1 in the source")
ap.add_argument("--height", type=float, default=0.66, help="subject height as a fraction of the canvas")
ap.add_argument("--left", type=float, default=0.16, help="subject left edge as a fraction of canvas width")
ap.add_argument("--cy", type=float, default=0.52, help="subject vertical centre as a fraction of canvas height")
a = ap.parse_args()

W, H = (int(v) for v in a.size.split("x"))
bx0, by0, bx1, by1 = (int(v) for v in a.bbox.split(","))
img = Image.open(a.src).convert("RGB")
k = a.height * H / (by1 - by0)
img = img.resize((round(img.width * k), round(img.height * k)), Image.LANCZOS)
x0 = round(a.left * W - bx0 * k)
y0 = round(a.cy * H - (by0 + by1) / 2 * k)
assert y0 <= 0 and y0 + img.height >= H, "source does not cover the canvas height"
src = np.asarray(img).astype(np.float32)[-y0:-y0 + H]
sw = src.shape[1]
assert x0 >= 0 and x0 + sw <= W, "subject placement pushes the source off the canvas"

def vsmooth(col, sigma):
    # blur a (H,3) column of colours along the vertical only
    im = Image.fromarray(np.clip(col, 0, 255).astype(np.uint8)[:, None, :].repeat(3, 1))
    return np.asarray(im.filter(ImageFilter.GaussianBlur(sigma))).astype(np.float32)[:, 1, :]

def extend(edge, n, toward_left):
    """n columns continuing `edge` (H,3): row-accurate at the seam, relaxing to a
    smooth vertical gradient further out so no row leaves a horizontal streak."""
    near, far = vsmooth(edge, 8), vsmooth(edge, 70)
    t = np.clip(np.arange(n) / 110.0, 0, 1); t = t * t * (3 - 2 * t)
    out = near[:, None, :] * (1 - t)[None, :, None] + far[:, None, :] * t[None, :, None]
    return out[:, ::-1] if toward_left else out

canvas = np.zeros((H, W, 3), np.float32)
canvas[:, x0:x0 + sw] = src
if x0 > 0:
    canvas[:, :x0] = extend(src[:, :8].mean(1), x0, True)
if x0 + sw < W:
    canvas[:, x0 + sw:] = extend(src[:, -8:].mean(1), W - x0 - sw, False)
Image.fromarray(np.clip(canvas + 0.5, 0, 255).astype(np.uint8)).save(a.dst, quality=90, method=6)
print("wrote", a.dst, "source placed at x", x0, "to", x0 + sw)
