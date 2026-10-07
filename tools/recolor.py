#!/usr/bin/env python3
"""Recolor a photo's background by remapping a hue range, keeping texture.

Used for the "Why AfterCare" card photos in visual-assets/. Instead of
filling the background with a flat color (which looks cut out), this
rotates every pixel whose hue is close to the background's hue toward a
new hue and scales its brightness. Grain, gradients and shadows survive,
and skin / subject colors outside the hue window are left alone.

Near the old background (a few pixels around it) the hue window is
widened, so anti-aliased edge pixels and colored shadow "spill" get
recolored too instead of leaving a fringe of the old color.

Requires:  pip install pillow numpy

Usage (PowerShell and bash, one line):

  python tools/recolor.py IN.webp OUT.webp --from-hue 344 --to-hue 258 --value 0.85

Arguments
  --from-hue   hue of the old background in degrees (0-360). Find it by
               sampling a background pixel; the script prints it with --probe.
  --to-hue     hue you want instead (e.g. blue 224, violet 262, teal 176).
  --value      brightness multiplier for the recolored area (<1 darker).
  --sat        saturation multiplier for the recolored area (default 1).
  --width      half-width of the hue window in degrees (default 40, how far
               from --from-hue still counts as background).
  --edge       pixels of widened matching around the background (default 6,
               use 0 to turn the edge widening off).
  --probe X,Y  just print the hue/saturation/value at pixel X,Y and exit.

Presets used on the site (run from the repo root):

  # Healthier scene: crimson -> purple
  python tools/recolor.py visual-assets/why-healthier-scene.webp out.webp --from-hue 344 --to-hue 262 --value 0.85 --sat 0.8 --width 30

Tip: always zoom into the edges of the result (200-400%) and check for
leftover fringes before shipping. If a thin line of the old color remains,
raise --edge or --width a little.
"""
import argparse

import numpy as np
from PIL import Image, ImageFilter


def smoothstep(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


def rgb_to_hsv(rgb):
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mx = rgb.max(-1)
    d = mx - rgb.min(-1)
    sat = np.where(mx > 0, d / np.maximum(mx, 1e-6), 0)
    dd = np.maximum(d, 1e-6)
    hue = np.where(
        mx == r,
        ((g - b) / dd) % 6,
        np.where(mx == g, (b - r) / dd + 2, (r - g) / dd + 4),
    ) * 60
    return hue, sat, mx


def hsv_to_rgb(hue, sat, val):
    c = val * sat
    hp = (hue % 360) / 60
    x = c * (1 - np.abs(hp % 2 - 1))
    m = val - c
    z = np.zeros_like(c)
    i = np.floor(hp).astype(int) % 6
    r = np.choose(i, [c, x, z, z, x, c])
    g = np.choose(i, [x, c, c, x, z, z])
    b = np.choose(i, [z, z, x, c, c, x])
    return np.stack([r + m, g + m, b + m], -1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("dst", nargs="?")
    ap.add_argument("--from-hue", type=float)
    ap.add_argument("--to-hue", type=float)
    ap.add_argument("--value", type=float, default=1.0)
    ap.add_argument("--sat", type=float, default=1.0)
    ap.add_argument("--width", type=float, default=40.0)
    ap.add_argument("--edge", type=int, default=6)
    ap.add_argument("--quality", type=int, default=90)
    ap.add_argument("--probe", help="X,Y: print hue/sat/value at this pixel and exit")
    a = ap.parse_args()

    img = Image.open(a.src).convert("RGB")
    rgb = np.array(img).astype(np.float32) / 255
    hue, sat, val = rgb_to_hsv(rgb)

    if a.probe:
        x, y = (int(v) for v in a.probe.split(","))
        print("hue %.0f  sat %.2f  value %.2f" % (hue[y, x], sat[y, x], val[y, x]))
        return
    if a.from_hue is None or a.to_hue is None or not a.dst:
        ap.error("need DST, --from-hue and --to-hue (or use --probe)")

    # signed hue distance from the old background hue, in degrees
    dh = ((hue - a.from_hue + 180) % 360) - 180

    # core weight: 1 for clearly-background pixels, fading to 0 at the window edge
    fade = max(a.width * 0.4, 1)
    core = smoothstep((a.width - np.abs(dh)) / fade) * smoothstep((sat - 0.25) / 0.3)

    weight = core
    if a.edge > 0:
        # Only near pure background: a wider hue window and lower saturation gate,
        # so blended edge pixels and colored spill are caught too.
        pure = core > 0.97
        mask = Image.fromarray((pure * 255).astype("uint8"))
        near = np.array(mask.filter(ImageFilter.MaxFilter(2 * a.edge + 1))) > 0
        zone = np.array(Image.fromarray((near * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(2))).astype(np.float32) / 255
        wide = smoothstep((a.width * 1.7 - np.abs(dh)) / (fade * 1.2)) * smoothstep((sat - 0.12) / 0.2)
        weight = np.maximum(core, wide * zone)

    new_hue = (hue + (a.to_hue - a.from_hue) * weight) % 360
    new_sat = np.clip(sat * (1 - weight + weight * a.sat), 0, 1)
    new_val = val * (1 - weight + weight * a.value)

    out = np.clip(hsv_to_rgb(new_hue, new_sat, new_val), 0, 1)
    Image.fromarray((out * 255 + 0.5).astype(np.uint8)).save(a.dst, quality=a.quality, method=6)
    print("wrote", a.dst)


if __name__ == "__main__":
    main()
