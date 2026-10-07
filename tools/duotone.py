#!/usr/bin/env python3
"""Re-light a single-colour photo by mapping its brightness onto a colour ramp.

Used for the "No contact needed" card photo in visual-assets/. That photo is
lit in one colour (red), so rotating its hue with recolor.py just gives the
same picture in another flat colour and loses contrast. This instead reads
each pixel's brightness and looks it up on a ramp you choose: shadows get the
first colour, highlights the last, with any stops in between. Shadows and
highlights can therefore have different hues, which keeps the picture alive.

Requires:  pip install pillow numpy

Usage (PowerShell and bash, one line):

  python tools/duotone.py IN.webp OUT.webp --stops 0:0e0612,1:e65c84

Arguments
  --stops    the ramp, as POSITION:HEX pairs separated by commas. Position
             runs from 0 (darkest) to 1 (brightest); hex is RRGGBB with no #.
  --gain     brightness multiplier applied before the lookup (default 1;
             raise it for a dark source so highlights reach the top stop).
  --gamma    curve applied after the gain (default 1; above 1 deepens the
             midtones, below 1 lifts them).

Preset used on the site (run from the repo root):

  # No contact needed: darkroom red -> plum shadows, wine mids, rose highlights
  python tools/duotone.py visual-assets/why-no-contact.webp visual-assets/why-no-contact-wine.webp --stops 0:0e0612,0.38:340b24,0.74:8f1740,1:e65c84 --gain 1.45 --gamma 1.1
"""
import argparse

import numpy as np
from PIL import Image


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--stops", required=True)
    ap.add_argument("--gain", type=float, default=1.0)
    ap.add_argument("--gamma", type=float, default=1.0)
    ap.add_argument("--quality", type=int, default=90)
    a = ap.parse_args()

    stops = sorted((float(p), h) for p, h in (s.split(":") for s in a.stops.split(",")))
    pos = np.array([p for p, _ in stops])
    col = np.array([[int(h[i:i + 2], 16) for i in (0, 2, 4)] for _, h in stops]) / 255

    rgb = np.array(Image.open(a.src).convert("RGB")).astype(np.float32) / 255
    # brightest channel, not a weighted grey: a one-colour photo keeps the
    # most detail in the channel it was lit in
    lum = np.clip(rgb.max(-1) * a.gain, 0, 1) ** a.gamma

    out = np.stack([np.interp(lum, pos, col[:, c]) for c in range(3)], -1)
    Image.fromarray((out * 255 + 0.5).astype(np.uint8)).save(a.dst, quality=a.quality, method=6)
    print("wrote", a.dst)


if __name__ == "__main__":
    main()
