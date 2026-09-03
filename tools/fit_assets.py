#!/usr/bin/env python3
"""Fit generated art into the pixel contracts index.html already expects.

  plates    — find each render's own grass line, crop it to 16:9 so that line
              lands on PLAY_SURFACE_Y, resize to 1672x941, write webp.
  mist      — measure the wisp's content box and print CLOUD_SRC.
  ruin      — measure a structure's alpha box, its flat deck row and that
              deck's centre column, and print its BUILDINGS[] entry.

Nothing is force-fitted: the art keeps its own proportions and the measured
numbers go into the code, which is the only way a set of structures with
different silhouettes can all stand a zombie on a level surface.

Usage:
  fit_assets.py plates SBgm1.png:nbTrees  SBgm5.png:nbMoon  ...
  fit_assets.py mist   SBgm6.png:nbMist
  fit_assets.py ruin   SBgm7.png:ruinPlinth [--check]
"""
import subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
OUT  = ROOT / "assets"

W, H = 1280, 720            # the stage
PLAY_SURFACE_Y = 600        # index.html — the row the tank's tracks rest on
PLATE = (1672, 941)         # every scene plate's native size
DECK_TOL = 5                # px of unevenness still counted as one flat deck


def to_webp(img, name, quality=88):
    dest = OUT / f"{name}.webp"
    tmp = dest.with_suffix(".fit.png")
    img.save(tmp)
    subprocess.run(["cwebp", "-quiet", "-q", str(quality), "-alpha_q", "100",
                    str(tmp), "-o", str(dest)], check=True)
    tmp.unlink()
    print(f"  -> assets/{dest.name}  {img.size[0]}x{img.size[1]}  "
          f"{dest.stat().st_size // 1024} KB")
    return dest


def split(arg):
    """'render.png:outname' -> (Path, outname)"""
    if ":" not in arg:
        sys.exit(f"expected <render.png>:<outname>, got {arg!r}")
    src, name = arg.rsplit(":", 1)
    return Path(src), name


# ---------------------------------------------------------------- plates
def surface_row(rgb):
    """The row the tank stands on: the crest of the mossy lip that caps the
    brick wall. Moss is the one thing in this palette where green runs well
    ahead of blue — the sky, fog and water are all teal, where the two track
    each other — so the greenness peak finds the lip without being told where
    to look, and finds it in the same place on every plate."""
    a = np.asarray(rgb).astype(int)
    greenness = (a[:, :, 1] - a[:, :, 2]).mean(axis=1)
    lower = slice(int(a.shape[0] * 0.6), a.shape[0])
    return lower.start + int(np.argmax(greenness[lower]))


def do_plates(args):
    for arg in args:
        src, name = split(arg)
        im = Image.open(src).convert("RGB")
        w, h = im.size
        crop_h = round(w * H / W)
        if crop_h > h:
            sys.exit(f"{src}: {w}x{h} is already taller-cropped than 16:9")
        # Put the plate's own grass line exactly where the engine's play
        # surface is, rather than cropping centred and hoping.
        row = surface_row(im)
        top = row - round(crop_h * PLAY_SURFACE_Y / H)
        clamped = max(0, min(top, h - crop_h))
        plate = im.crop((0, clamped, w, clamped + crop_h)).resize(PLATE, Image.LANCZOS)
        landed = (row - clamped) * PLATE[1] / crop_h * (H / PLATE[1])
        note = "" if clamped == top else f"  [clamped from {top}]"
        print(f"{src.name}: grass line y={row} -> crop top {clamped}, "
              f"lands on stage y={landed:.1f} (want {PLAY_SURFACE_Y}){note}")
        to_webp(plate, name, quality=86)


# ------------------------------------------------------------------ mist
def content_box(rgba, thresh=8):
    a = np.asarray(rgba)[:, :, 3]
    ys, xs = np.where(a > thresh)
    if not len(xs):
        sys.exit("fully transparent")
    return int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)


def do_mist(arg):
    src, name = split(arg)
    im = Image.open(src).convert("RGBA")
    sx, sy, sw, sh = content_box(im)
    to_webp(im, name)
    print(f"\n  paste into index.html:\n"
          f"  const CLOUD_SRC = [{sx},{sy},{sw},{sh}];"
          f"      // measured content box in {name}.webp\n"
          f"  aspect {sw/sh:.2f} — a wisp this flat draws "
          f"{round(200/(sw/sh))}px tall at the widest cloud size")


# ------------------------------------------------------------------ ruin
def measure_ruin(im):
    """Alpha box, plus the widest level run along the silhouette's top
    profile — which is the deck a zombie can actually stand on."""
    al = np.asarray(im)[:, :, 3]
    x0, y0, w, h = content_box(im, thresh=40)
    x1 = x0 + w - 1
    top = {}
    for x in range(x0, x1 + 1):
        col = np.where(al[:, x] > 120)[0]
        if len(col):
            top[x] = int(col[0])
    if not top:
        sys.exit("no opaque columns")
    best = (0, 0, 0)                       # (run, start x, deck row)
    for band in range(min(top.values()), min(top.values()) + 120):
        run = 0
        start = None
        for x in range(x0, x1 + 2):
            if abs(top.get(x, 10**6) - band) <= DECK_TOL:
                if start is None:
                    start = x
                run += 1
            else:
                if run > best[0]:
                    best = (run, start, band)
                run = 0
                start = None
        if run > best[0]:
            best = (run, start, band)
    run, dstart, deck = best
    return (x0, y0, w, h), deck, round(dstart + run / 2), run


def do_ruin(arg, check=False):
    src, name = split(arg)
    im = Image.open(src).convert("RGBA")
    (sx, sy, sw, sh), deck, dcx, run = measure_ruin(im)
    to_webp(im, name)
    reach = (dcx - sx) / sh                # left spill, as a fraction of height
    print(f"  {{img:'{name}', box:[{sx},{sy},{sw},{sh}], "
          f"deck:{deck}, deckCx:{dcx}}},")
    print(f"  aspect {sw/sh:.3f}   deck {run}px wide "
          f"({run/sw:.0%} of the shape), {(dcx-sx)/sw:.0%} across, "
          f"{(deck-sy)/sh:.1%} down")
    print(f"  left reach {reach:.2f} of its height"
          + ("  <-- wide: only the shallow rounds will stage it" if reach > .6 else
             "  <-- slim: this is the one that fits the steep round" if reach < .2 else ""))
    if check:
        vis = im.copy().convert("RGBA")
        chk = Image.new("RGB", im.size, (255, 255, 255))
        d = ImageDraw.Draw(chk)
        for y in range(0, im.size[1], 28):
            for x in range(0, im.size[0], 28):
                if (x // 28 + y // 28) % 2:
                    d.rectangle([x, y, x + 28, y + 28], fill=(190, 190, 190))
        chk.paste(vis, (0, 0), vis)
        d = ImageDraw.Draw(chk)
        d.rectangle([sx, sy, sx + sw - 1, sy + sh - 1], outline=(255, 0, 0), width=3)
        d.line([(sx, deck), (sx + sw, deck)], fill=(255, 0, 255), width=4)
        d.line([(dcx, deck - 90), (dcx, deck + 90)], fill=(0, 120, 255), width=4)
        p = Path(f"/tmp/{name}_check.png")
        chk.save(p)
        print(f"  check image: {p}")


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    mode, args = sys.argv[1], [a for a in sys.argv[2:] if not a.startswith("--")]
    check = "--check" in sys.argv
    if mode == "plates":
        do_plates(args)
    elif mode == "mist":
        do_mist(args[0])
    elif mode == "ruin":
        for a in args:
            do_ruin(a, check)
    else:
        sys.exit(f"unknown mode {mode!r}")


if __name__ == "__main__":
    main()
