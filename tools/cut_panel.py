#!/usr/bin/env python3
"""Cut the mossy console kit out of its atlas into the sprites index.html loads.

art-src/controlPanel.png is one sheet of parts: a panel frame with four windows
cut clean through it, a red FIRE key, two arrow keys, a lit read-out plate, the
theta label, and a pile of moss, pipe and bolt decals the frame already wears.
This slices out the six pieces the dock is built from and writes them to
assets/ as webp, the way fit_assets.py does for the scenery.

TWO of them are repainted on the way out, and for the same reason: the artist
lettered them in English. "CONTROL PANEL" and "Fire" are baked pixels on the
sheet, and this game says both of those words in six languages — the CSS that
rebuilt the old FIRE key exists precisely because "FIRE" had been the last
string in the game that stayed English everywhere. Shipping the atlas as drawn
would put it straight back. So the lettering is taken off and index.html sets
real, translated text over the empty plate.

  python3 tools/cut_panel.py            # cut everything
  python3 tools/cut_panel.py --debug    # …and dump before/after previews
  python3 tools/cut_panel.py --measure  # re-derive PARTS/WINDOWS from the sheet
"""
import subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter

ROOT  = Path(__file__).resolve().parent.parent
# The master is LOSSLESS webp, the way art-src keeps every other master (see
# fit_assets.py): the sheet re-cuts from exactly the pixels the first cut saw,
# and the file is a third smaller than the PNG it came in as.
SRC   = ROOT / "art-src" / "controlPanel.webp"
OUT   = ROOT / "assets"                         # only what index.html loads
DEBUG = ROOT / "art-src" / "_cut_debug"

# ---- WHERE EACH PART SITS ON THE SHEET --------------------------------
# Measured, not eyeballed: every box is the alpha bounding box of one connected
# component of the atlas. --measure prints them again if the sheet is redrawn.
PARTS = {
    "cpPanel": (  10,  13, 1223, 467),   # the frame, windows already cut through it
    "cpFire":  (1306, 144,  322, 255),   # the red key
    "cpUp":    (1769, 139,  168, 166),
    "cpDown":  (1978, 139,  170, 166),
    "cpPlate": (1790, 370,  305, 192),   # the EMPTY read-out. The sheet's other plate
                                         # is lettered "30" as the artist's example,
                                         # and the number on it is live.
    "cpTheta": (1252, 435,  137, 122),   # theta and its equals sign, one glyph group
}
# The sheet also carries a brick course, a spare pipe elbow, and loose moss and
# bolt decals. None are cut: the scene paints its own wall, and the frame comes
# with its moss and its pipes already on it.

# ---- THE FOUR WINDOWS CUT THROUGH THE FRAME ---------------------------
# The holes in cpPanel that are not connected to the outside — panel-local px.
# index.html sets the read-out and the three keys over these, so cut() prints
# them as percentages of the panel, which is the form the CSS wants.
WINDOWS = {
    "readout": (315, 166, 221, 148),
    "up":      (608, 132,  97,  90),
    "down":    (608, 260,  97,  90),
    "fire":    (801, 135, 244, 207),
}

# ---- WHAT GETS UNLETTERED ---------------------------------------------
# FIELD is where the glyphs are, measured off the sheet's own row profile,
# which is the only way to place it: on the plaque, CONTROL PANEL runs y 62-91,
# then seven clean rows, then the lit bottom bevel at y 99-101 — and that bevel
# is BRIGHTER than the letters, so a brightness cut that reaches it erases the
# plaque's edge instead of its lettering. The field stops in the gap. Same
# story on the key, where the neon ring outshines the word.
#
# FACE is the surface the lettering sits on, and it is a separate thing: the
# repair is computed over the whole face (see unletter), not just around the
# glyphs, which is what keeps it seamless.
TITLE_FIELD = ( 460,  55, 268, 42)
TITLE_CUT   = 105                       # cream letters over mottled green-grey
TITLE_FACE  = ( 412,  54, 366, 45)      # the plaque's flat interior, inside its bevel
FIRE_FIELD  = (1400, 222, 165, 96)
FIRE_CUT    = 150                       # yellow letters over red

# The theta label is recoloured, not just cut. As drawn it is a dark grey
# glyph — rgb 49,52,46, luminance 49 — and the panel it is set on measures
# luminance 47, so on this frame it is very nearly invisible. (The sheet shows
# it over a lighter patch of plate than the frame actually has.) It is repainted
# in the cream the frame's own engraved lettering uses, which reads as the same
# paint applied to the same metal, and is legible. It has to be: theta is the
# quantity this game teaches, not decoration.
THETA_INK = (186, 174, 150)

GROW = 7        # px the glyph mask is dilated by, to take its anti-aliased rim
DILATE = 31     # …and how much wider the SUPPRESSION reaches — see unletter()
FEATHER = 18
BASE_R = 60     # radius of the smooth surface fitted under the lettering


def _blur(arr, r):
    return np.asarray(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
                      .filter(ImageFilter.GaussianBlur(r))).astype(float)


def _normconv(chan, keep, r):
    """A blur that only sees `keep` — make_title.py's trick for the moon.
    Dividing by the blurred mask is what stops colour bleeding in from the
    pixels being repaired, or from the transparent surround."""
    return _blur(chan * keep, r) / (_blur(keep * 255.0, r) / 255 + 1e-6)


def _mask(rgb, field, cut, grow):
    x, y, w, h = field
    lum = rgb[y:y + h, x:x + w].mean(axis=2)
    m = Image.fromarray(((lum > cut) * 255).astype(np.uint8)) \
             .filter(ImageFilter.MaxFilter(grow))
    full = np.zeros(rgb.shape[:2], bool)
    full[y:y + h, x:x + w] = np.asarray(m) > 128
    return full


def unletter(rgb, face, field, cut):
    """Take the word off a plate without leaving its shape behind.

    Cutting out the glyphs and filling the hole from its rim does NOT work
    here, and both plates say why: the word is drawn LIT, so it throws a broad
    bloom across the metal around it. Fill only the glyphs and the bloom stays,
    a bright cloud with a flat patch in the middle of it, and the word is still
    legible as a ghost. Widen the hole until it swallows the bloom and the fill
    now comes from the plate's dark outskirts, so the ghost comes back inverted
    — a dark slab the exact shape of the mask. Every radius is wrong because
    the premise is: there is no clean rim to fill from.

    So nothing is filled. The whole FACE is separated into a smooth base and
    its own texture:

        base   = the plate's gradient, fitted with a wide normalised blur
                 that cannot see the glyphs
        detail = plate - base, which carries the scratches, the grain AND the
                 word's bloom, all as local departures from that gradient

    and the plate is put back together as base + detail, with detail faded out
    across a feathered halo around the word. The word and its light go
    together, because the light IS detail; the scratches everywhere else are
    untouched; and there is no seam anywhere, because outside the halo
    base + detail is arithmetically the original pixel.

    What is lost is the texture inside the halo, which goes smooth. On a plaque
    that renders ~30 px tall on the stage, that is not a visible trade."""
    core = _mask(rgb, field, cut, GROW)
    halo = Image.fromarray((core * 255).astype(np.uint8)) \
                .filter(ImageFilter.MaxFilter(DILATE)) \
                .filter(ImageFilter.GaussianBlur(FEATHER))
    halo = np.clip(np.asarray(halo).astype(float) / 255 * 1.25, 0, 1)

    keep = (face & ~core).astype(float)
    out = rgb.copy()
    for c in range(3):
        base = _normconv(rgb[:, :, c], keep, BASE_R)
        out[:, :, c] = np.where(face, base + (rgb[:, :, c] - base) * (1 - halo),
                                rgb[:, :, c])
    return out, core


def fire_face(rgb, alpha):
    """The key's lit face, traced rather than boxed: it is an octagon, and a
    rectangle inside it either clips the corners or runs onto the neon ring —
    and the ring is the brightest thing on the sprite, so letting it into the
    fit would drag the whole fitted gradient up."""
    from scipy import ndimage
    x, y, w, h = PARTS["cpFire"]
    s = rgb[y:y + h, x:x + w]
    red = (s[:, :, 0] > 80) & (s[:, :, 0] - s[:, :, 1] > 45) & (alpha[y:y + h, x:x + w] > 200)
    red = ndimage.binary_fill_holes(red)                       # the yellow word is a hole
    red = ndimage.binary_erosion(red, np.ones((3, 3)), iterations=12)   # off the ring
    red = ndimage.binary_opening(red, np.ones((3, 3)), iterations=3)
    face = np.zeros(rgb.shape[:2], bool)
    face[y:y + h, x:x + w] = red
    return face


def to_webp(img, name, quality=92):
    dest = OUT / f"{name}.webp"
    tmp = dest.with_suffix(".cut.png")
    img.save(tmp)
    subprocess.run(["cwebp", "-quiet", "-q", str(quality), "-alpha_q", "100",
                    str(tmp), "-o", str(dest)], check=True)
    tmp.unlink()
    print(f"  -> assets/{dest.name}  {img.size[0]}x{img.size[1]}  "
          f"{dest.stat().st_size // 1024} KB")


def measure():
    """Re-derive PARTS and WINDOWS from the sheet itself."""
    from scipy import ndimage
    a = np.asarray(Image.open(SRC).convert("RGBA"))
    m = a[:, :, 3] > 24
    lab, _ = ndimage.label(m, structure=np.ones((3, 3)))
    print("components (area >= 400), as (x, y, w, h):")
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        area = (lab[sl] == i).sum()
        if area < 400:
            continue
        ys, xs = sl
        print(f"  ({xs.start:5d},{ys.start:4d},{xs.stop-xs.start:5d},{ys.stop-ys.start:4d})"
              f"   area {area}")
    px, py, pw, ph = PARTS["cpPanel"]
    hole = np.ones(a.shape[:2], bool)
    hole[py:py + ph, px:px + pw] = ~m[py:py + ph, px:px + pw]
    lab, _ = ndimage.label(hole, structure=np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]))
    edge = set(lab[0]) | set(lab[-1]) | set(lab[:, 0]) | set(lab[:, -1])
    print("windows cut through cpPanel, panel-local:")
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        if i in edge or (lab[sl] == i).sum() < 2000:
            continue
        ys, xs = sl
        print(f"  ({xs.start-px:4d},{ys.start-py:4d},{xs.stop-xs.start:4d},{ys.stop-ys.start:4d})")


def cut(debug=False):
    atlas = np.asarray(Image.open(SRC).convert("RGBA")).astype(float)
    rgb, alpha = atlas[:, :, :3], atlas[:, :, 3]

    tx, ty, tw, th = TITLE_FACE
    plaque = np.zeros(rgb.shape[:2], bool)
    plaque[ty:ty + th, tx:tx + tw] = True

    rgb, title_core = unletter(rgb, plaque, TITLE_FIELD, TITLE_CUT)
    rgb, fire_core = unletter(rgb, fire_face(rgb, alpha), FIRE_FIELD, FIRE_CUT)

    sheet = Image.fromarray(np.clip(np.dstack([rgb, alpha]), 0, 255).astype(np.uint8))

    if debug:
        DEBUG.mkdir(exist_ok=True)
        was = Image.open(SRC).convert("RGB")
        for who, (x, y, w, h) in (("title", TITLE_FIELD), ("fire", FIRE_FIELD)):
            box = (x - 55, y - 45, x + w + 55, y + h + 45)
            strip = Image.new("RGB", (box[2] - box[0], (box[3] - box[1]) * 2 + 8), (30, 30, 30))
            strip.paste(was.crop(box), (0, 0))
            strip.paste(sheet.convert("RGB").crop(box), (0, box[3] - box[1] + 8))
            strip.save(DEBUG / f"{who}.png")
        print(f"  before/after previews in {DEBUG}/")

    for name, (x, y, w, h) in PARTS.items():
        part = sheet.crop((x, y, x + w, y + h))
        if name == "cpTheta":
            flat = np.asarray(part).astype(float)
            flat[:, :, :3] = THETA_INK          # alpha, and only alpha, is the glyph
            part = Image.fromarray(np.clip(flat, 0, 255).astype(np.uint8))
        to_webp(part, name)

    pw, ph = PARTS["cpPanel"][2], PARTS["cpPanel"][3]
    print(f"\n  cpPanel {pw}x{ph}, aspect {pw/ph:.4f}")
    print("  windows as % of the panel — left / top / width / height:")
    for k, (x, y, w, h) in WINDOWS.items():
        print(f"    {k:8s} {x/pw*100:7.3f} {y/ph*100:7.3f} {w/pw*100:7.3f} {h/ph*100:7.3f}")


if __name__ == "__main__":
    if "--measure" in sys.argv:
        measure()
    else:
        cut("--debug" in sys.argv)
