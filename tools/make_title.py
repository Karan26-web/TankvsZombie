#!/usr/bin/env python3
"""Compose the night title plate from assets that already exist.

An image model cannot letter a game title legibly, so the wordmark is not
regenerated — it is lifted off the old daytime plate and re-bedded on the moon
plate. Everything drawTitleScene() relies on keeps working because the wordmark
lands back inside TITLE_LOGO_RECT: the re-blit that throws the light burst
BEHIND the letters is a straight copy of that rectangle, so it does not care
what is underneath it.

  python3 tools/make_title.py
"""
from collections import deque
from pathlib import Path
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
A   = ROOT / "assets"      # what index.html loads, and what this script writes
SRC = ROOT / "art-src"     # masters the game never loads — the old daytime plate

LOGO = (439, 39, 807, 531)      # TITLE_LOGO_RECT, in the plate's own 1672x941 px
PAD = 18                        # sky to start the flood from, on every side
OUTLINE_LUM = 95               # below this is the wordmark's black keyline
# Daytime scenery the flood cannot reach because the wordmark's own outline
# fences it in. Measured off the crop; a nick into the black keyline costs
# nothing, because the plate behind it is darker than the line.
DEBRIS = [(0, 434, 118, 567), (100, 418, 140, 442)]


def lift_wordmark():
    """Key the wordmark out of the old plate. The letters are ringed by a
    near-black keyline and the sky and clouds are both light, so a flood that
    runs through everything EXCEPT that keyline stops dead at the glyphs and
    never leaks inside them. What survives is then reduced to its largest
    connected piece — the three words and their bolts are one shape — which
    drops the fence posts and scrub the flood could not enter."""
    src = Image.open(SRC / "preLBD.webp").convert("RGB")
    sx, sy, sw, sh = LOGO
    crop = src.crop((sx - PAD, sy - PAD, sx + sw + PAD, sy + sh + PAD))
    rgb = np.asarray(crop).astype(int)
    h, w, _ = rgb.shape
    lum = rgb.mean(axis=2)

    outside = np.zeros((h, w), bool)
    q = deque()
    border = [(y, x) for x in range(w) for y in (0, h - 1)]
    border += [(y, x) for y in range(h) for x in (0, w - 1)]
    for y, x in border:
        if lum[y, x] > OUTLINE_LUM and not outside[y, x]:
            outside[y, x] = True
            q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and not outside[ny, nx] and lum[ny, nx] > OUTLINE_LUM:
                outside[ny, nx] = True
                q.append((ny, nx))

    keep = ~outside
    for x0, y0, x1, y1 in DEBRIS:
        keep[y0:y1, x0:x1] = False

    # largest 8-connected piece = the wordmark
    seen = np.zeros((h, w), np.int32)
    best = (0, 0)
    nid = 0
    for y0 in range(h):
        for x0 in range(w):
            if keep[y0, x0] and not seen[y0, x0]:
                nid += 1
                q = deque([(y0, x0)])
                seen[y0, x0] = nid
                n = 0
                while q:
                    y, x = q.popleft()
                    n += 1
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = y + dy, x + dx
                            if 0 <= ny < h and 0 <= nx < w and keep[ny, nx] and not seen[ny, nx]:
                                seen[ny, nx] = nid
                                q.append((ny, nx))
                if n > best[0]:
                    best = (n, nid)
    alpha = np.where(seen == best[1], 255, 0).astype(np.uint8)
    word = Image.fromarray(np.dstack([rgb.astype(np.uint8), alpha]))
    print(f"  wordmark: {best[0]:,} px kept")
    return word


# WHICH PLATE CARRIES THE TITLE, and why it is not the obvious one.
#
# Two things have to be empty on an attract screen, and they are not the same
# place. The sky behind the wordmark, and the mid-ground behind the PLAY
# button — plate px x 613-1058, y 626-783. Every plate in the set puts its one
# distinctive motif in the central 600px on purpose, so nothing is empty in
# both by luck; it has to be chosen.
#
# The moon plate is out at once: its disc sits at (836,183), which is exactly
# where the wordmark goes. The ARCH plate reads well but stands its ruined
# gateway squarely behind the button, and a gate framing a button is a lot of
# scenery for a thing you want read as the one place to click.
#
# The MANOR plate is the one whose motif was specified DISTANT — small, pale
# and fog-washed. That puts its only landmark high, faint, and above the
# button rather than behind it, leaves open misty water where the button
# actually lands, and pushes its trees out to the frame edges. So the title is
# built on it, and the moon is transplanted into the corner the wordmark
# leaves free.
MOON_SRC = (606, 0, 1066, 420)      # a generous square of sky around the disc
MOON_AT  = (262, 212)               # where its centre lands on the title plate
GLOW_REACH   = 1.62                 # halo radius, in disc radii
GLOW_FALLOFF = 2.1                  # higher = tighter bloom hugging the rim
GLOW_PEAK    = 0.55                 # halo opacity just outside the disc


def clean_moon(patch):
    """Take the tree off the moon.

    The moon was painted with a gnarled limb silhouetted across it, and that
    limb is what a straight transplant carries along: the branch is DARKER
    than the sky it lands on, so a lighten composite leaves it as a hole
    punched in the disc, and the tree it belonged to is nowhere in frame. A
    severed branch floating on the moon.

    Painting it out by diffusion would smear a 40px mossy limb across a flat
    field and show. What works instead is the moon's own geometry: the disc is
    a disc, the damage is all on one side, and the far side is untouched. So
    every wounded pixel is filled from the pixel diametrically opposite it —
    a 180 degree turn about the centre, which lands the clean upper-left onto
    the ruined lower-right.

    A ROTATION, not a mirror, and that is the whole point. Reflection would
    make the craters bilaterally symmetric, which the eye picks up
    immediately; point symmetry through the centre is invisible unless you go
    looking for it, and only the branch's own footprint is resampled, so every
    crater around it is still the one the painter put there.

    The radius reaches past the disc to take the glow with it. The branch
    crossed that too, and a repair that stopped at the rim would leave a
    notch bitten out of the halo."""
    a = np.asarray(patch).astype(float)
    h, w, _ = a.shape
    lum = a.mean(axis=2)

    disc = lum > 170                       # the lit field, branch excluded by luminance
    ys, xs = np.where(disc)
    cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
    r = max(xs.max() - xs.min(), ys.max() - ys.min()) / 2
    yy, xx = np.mgrid[0:h, 0:w]
    rad = np.hypot(xx - cx, yy - cy)
    reach = r * 1.16                       # far enough out to take the glow too

    # WHAT BELONGS AT EACH RADIUS. A flat luminance threshold cannot find this
    # branch: the disc is bright, its glow falls off into a sky darker than
    # the branch itself, so any single cut either misses the limb or condemns
    # the whole sky as damage — which is what a first attempt did, handing
    # 23,000 sky pixels to the repair. What IS true at every radius is that
    # the branch is a MINORITY of that ring, so the ring's own upper quartile
    # estimates the clean level there and anything well under it is the tree.
    ring = np.clip((rad / 2).astype(int), 0, int(reach / 2))
    nrings = ring.max() + 1
    clean = np.zeros(nrings)
    for i in range(nrings):
        vals = lum[(ring == i) & (rad <= reach)]
        clean[i] = np.percentile(vals, 75) if vals.size else 0
    expected = clean[np.clip(ring, 0, nrings - 1)]
    wound = (rad <= reach) & (lum < expected * 0.74)

    # grow it a little: the limb is anti-aliased and mossy at its edges, and a
    # fill that stops on the last fully dark pixel leaves a dark rind behind
    m = Image.fromarray((wound * 255).astype(np.uint8))
    m = m.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(2))
    soft = (np.asarray(m).astype(float) / 255)[:, :, None]

    src_y = np.clip((2 * cy - yy).round().astype(int), 0, h - 1)
    src_x = np.clip((2 * cx - xx).round().astype(int), 0, w - 1)
    out = a * (1 - soft) + a[src_y, src_x] * soft

    # Safety net: wherever a wounded pixel's opposite number was ALSO wounded,
    # the turn had nothing clean to offer. Those few are diffused instead of
    # left dark — normalised convolution, so only valid pixels contribute.
    still = (out.mean(axis=2) < expected * 0.74) & (rad <= reach)
    if still.any():
        # 8-bit blurs, because ImageFilter will not touch a float buffer. The
        # denominator only has to normalise a weighted average, so a byte of
        # precision is plenty.
        blur = lambda arr, rd: np.asarray(
            Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
                 .filter(ImageFilter.GaussianBlur(rd))).astype(float)
        valid = (~still).astype(float)
        den = blur(valid * 255, 18) / 255 + 1e-6
        for c in range(3):
            num = blur(out[:, :, c] * valid, 18)
            out[:, :, c] = np.where(still, num / den, out[:, :, c])
        print(f"  moon: {int(still.sum())} px needed the diffusion fallback")

    print(f"  moon: disc centre ({cx:.0f},{cy:.0f}) r {r:.0f}, "
          f"{int(wound.sum())} px of tree turned out")
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)), cx, cy, r


def moon_sprite():
    """The moon as its own sprite: repaired disc, generated glow.

    The first version transplanted a RECTANGLE of the moon plate and let a
    lighten composite sort it out, on the reasoning that both plates share a
    sky so the sky would cancel. It does — but the tree in that rectangle does
    not. The limb is mossy, and moss is BRIGHTER than a night sky, so lighten
    kept it: a severed branch hanging beside the moon. Repairing only the disc
    left it there, and worse, the repair's own 180 degree turn had started
    pasting that moss into the halo on the opposite side.

    The lesson is what to harvest. The only thing on that plate worth having
    is the painted disc — its craters are art. The halo is a radial gradient,
    and a radial gradient is something to GENERATE, not to cut out of a
    painting and hope nothing else came with it. So the disc is masked to its
    own circle, the glow is built from the disc's own rim colour, and the tree
    is not in the sprite at all — there is nothing left for it to survive in."""
    patch, cx, cy, r = clean_moon(
        Image.open(A / "nbMoon.webp").convert("RGB").crop(MOON_SRC))
    a = np.asarray(patch).astype(float)
    R = int(round(r * GLOW_REACH))
    yy, xx = np.mgrid[0:2 * R, 0:2 * R]
    rad = np.hypot(xx - R, yy - R)

    # the disc, lifted whole, with a hairline feather so its rim is not stepped
    src_y = np.clip((yy - R + cy).round().astype(int), 0, a.shape[0] - 1)
    src_x = np.clip((xx - R + cx).round().astype(int), 0, a.shape[1] - 1)
    rgb = a[src_y, src_x]
    disc_a = np.clip((r - rad) / 2 + .5, 0, 1)

    # the glow, tinted with the colour the disc actually ends on, so the bloom
    # belongs to this moon rather than to a colour picked by hand
    ring = (rad > r * .86) & (rad < r)
    tint = a[src_y, src_x][ring].mean(axis=0) if ring.any() else np.array([238., 245., 214.])
    t = np.clip((R - rad) / max(R - r, 1), 0, 1) ** GLOW_FALLOFF
    glow_a = np.where(rad > r, t * GLOW_PEAK, 0)

    alpha = np.clip(disc_a + glow_a * (1 - disc_a), 0, 1)
    colour = rgb * disc_a[:, :, None] + tint * (1 - disc_a[:, :, None])
    sprite = np.dstack([colour, alpha * 255])
    print(f"  moon: sprite {2*R}x{2*R}, disc r {r:.0f}, glow to {R}, "
          f"tint rgb({tint[0]:.0f},{tint[1]:.0f},{tint[2]:.0f})")
    return Image.fromarray(np.clip(sprite, 0, 255).astype(np.uint8)), R


def transplant_moon(plate):
    """Drop the moon sprite into the corner the wordmark leaves free."""
    sprite, R = moon_sprite()
    out = plate.convert("RGBA")
    out.alpha_composite(sprite, (MOON_AT[0] - R, MOON_AT[1] - R))
    return out.convert("RGB")


def compose():
    """Two assets, not one.

    The wordmark used to be baked INTO the title plate, and drawTitleScene()
    put it back on top of the light burst by re-blitting its rectangle out of
    the plate. That worked, but it made the rectangle a hole in time: anything
    drawn between the plate and the re-blit was erased inside it. Drifting
    clouds are exactly that, and they cross that rectangle.

    So the wordmark ships as its own transparent sprite, at plate resolution
    and in plate position, and everything that used to fight the rectangle
    simply draws underneath it. No rect, no feather, no re-blit."""
    plate = transplant_moon(Image.open(A / "nbManor.webp").convert("RGB"))
    W, H = plate.size
    word = lift_wordmark()
    sx, sy, sw, sh = LOGO

    # Separate the letters from the moon WITHOUT touching the moon. Darkening
    # the plate was the obvious move and the wrong one: the wordmark sits right
    # on the moon, so a scrim big enough to help turned the brightest thing in
    # the frame to mud, and the moon is the hero of this composition.
    # So the shadow is cast by the wordmark instead of onto the plate — its own
    # alpha, spread and blurred, laid down underneath it. The letters gain a
    # halo that reads as them floating in front of the moon, and every pixel
    # the letters do not cover stays exactly as painted.
    # The halo travels WITH the wordmark rather than being burnt into the
    # plate, so the letters carry their own separation wherever they are drawn
    # and whatever ends up behind them — moon, rays, or a passing cloud.
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.paste(word, (sx - PAD, sy - PAD))
    halo = layer.getchannel("A").filter(ImageFilter.MaxFilter(5)) \
                                .filter(ImageFilter.GaussianBlur(11))
    halo = halo.point(lambda v: int(v * .58))
    sprite = Image.merge("RGBA", (
        Image.new("L", (W, H), 4), Image.new("L", (W, H), 20),
        Image.new("L", (W, H), 28), halo))
    sprite.alpha_composite(layer)

    for img, name, args in ((plate, "nbTitle", ["-q", "90"]),
                            (sprite, "nbWord", ["-q", "94", "-alpha_q", "100"])):
        tmp = A / f"{name}.fit.png"
        img.save(tmp)
        dest = A / f"{name}.webp"
        subprocess.run(["cwebp", "-quiet", *args, str(tmp), "-o", str(dest)], check=True)
        tmp.unlink()
        print(f"  -> assets/{dest.name}  {W}x{H}  {dest.stat().st_size // 1024} KB")


if __name__ == "__main__":
    compose()
