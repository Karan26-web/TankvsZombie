#!/usr/bin/env python3
"""Fit generated art into the pixel contracts index.html already expects.

  plates    — find each render's own grass line, crop it to 16:9 so that line
              lands on PLAY_SURFACE_Y, resize to 1672x941, write webp.
  mist      — measure the wisp's content box and print CLOUD_SRC.
  ruin      — measure a structure's alpha box, its flat deck row and that
              deck's centre column, and print its BUILDINGS[] entry.
  commander — trim the tank commander's bust, size it off her helmet, and
              print the CMDR numbers (helmet width, rim cut row, centre column).
  face      — line her expressions (editor re-renders of the bust) up with
              it, keep only what each one changed, and pack those as overlays
              on one sheet, with the CMDR_FACE numbers.
  safezone  — key the compound's magenta gate opening, scale the compound by
              it, fit the gate to it, and print the SZ numbers.
  barriers  — trim the side-view barrier props and print each one's box, for
              the outposts' and the safe zone's fortifications (BARRIER_BOX).

Nothing is force-fitted: the art keeps its own proportions and the measured
numbers go into the code, which is the only way a set of structures with
different silhouettes can all stand a zombie on a level surface.

The renders themselves live in art-src/, not assets/ — assets/ holds only
what index.html loads, and a 1536x1024 master is not that. They are lossless
webp, so re-cutting a plate starts from the same pixels the first cut did.

Usage:
  fit_assets.py plates art-src/SBgm1.webp:nbTrees  art-src/SBgm5.webp:nbMoon  ...
  fit_assets.py mist   art-src/SBgm6.webp:nbMist
  fit_assets.py ruin   art-src/SBgm7.webp:ruinPlinth [--check]
  fit_assets.py commander art-src/commander.webp:commander
  fit_assets.py face      art-src/commander_talk.webp:talk art-src/commander_blink.webp:blink
  fit_assets.py safezone  art-src/SZ1.webp:safeZone art-src/SZ2.webp:safeGate
  fit_assets.py barriers  (reads art-src/STbarriers.webp)
"""
import shutil, subprocess, sys
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
    if shutil.which("cwebp"):
        tmp = dest.with_suffix(".fit.png")
        img.save(tmp)
        subprocess.run(["cwebp", "-quiet", "-q", str(quality), "-alpha_q", "100",
                        str(tmp), "-o", str(dest)], check=True)
        tmp.unlink()
    else:                   # same settings through Pillow's own libwebp
        img.save(dest, "WEBP", quality=quality, alpha_quality=100, method=6)
    print(f"  -> assets/{dest.name}  {img.size[0]}x{img.size[1]}  "
          f"{dest.stat().st_size // 1024} KB")
    return dest


def split(arg):
    """'art-src/render.webp:outname' -> (Path, outname)"""
    if ":" not in arg:
        sys.exit(f"expected <render>:<outname>, got {arg!r}")
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


# ------------------------------------------------------------- commander
COMMANDER_HEAD_PX = 300     # helmet width in the shipped file — about 2.5x the
                            # most the zoomed cut-scene ever draws it at


def row_spans(al, thresh=128):
    """(left, right) of the opaque run on every row, None where empty."""
    spans = []
    for row in al:
        xs = np.where(row > thresh)[0]
        spans.append((int(xs.min()), int(xs.max())) if len(xs) else None)
    return spans


def commander_crop(im):
    """The box her bust is cut out with, and the size it is scaled to: the
    helmet (the widest row in the top two-thirds, the ear-cups) comes out
    COMMANDER_HEAD_PX wide. Her expressions (`face`) are cut with the same
    two, so they land on exactly the pixels they are drawn over."""
    x0, y0, w, h = content_box(im, thresh=40)
    pad = 6
    box = (x0 - pad, y0 - pad, x0 + w + pad, y0 + h + pad)
    spans = row_spans(np.asarray(im.crop(box))[:, :, 3])
    widths = [s[1] - s[0] if s else 0 for s in spans]
    head_row = max(range(len(spans) * 2 // 3), key=lambda y: widths[y])
    sc = COMMANDER_HEAD_PX / widths[head_row]
    return box, (round((box[2] - box[0]) * sc), round((box[3] - box[1]) * sc))


def do_commander(arg):
    """A head-and-shoulders bust that climbs out of the turret hatch. The game
    only needs three numbers off it: how wide the helmet is (that sets her
    scale against the hatch), and where the shoulders begin and on which
    column — that row is the one the hatch rim cuts her off at."""
    src, name = split(arg)
    im = Image.open(src).convert("RGBA")
    box, size = commander_crop(im)
    im = im.crop(box).resize(size, Image.LANCZOS)
    spans = row_spans(np.asarray(im)[:, :, 3])
    widths = [s[1] - s[0] if s else 0 for s in spans]
    rows = len(spans)
    head_row = max(range(rows * 2 // 3), key=lambda y: widths[y])
    # the neck: the narrowest row between the helmet and the chest
    band = range(head_row + 1, rows * 9 // 10)
    neck = min((y for y in band if widths[y]), key=lambda y: widths[y])
    # the cut: where the shoulders have opened 30% past the neck
    cut = next(y for y in range(neck, rows) if widths[y] >= widths[neck] * 1.3)
    cx = round((spans[cut][0] + spans[cut][1]) / 2)
    top = next(y for y in range(rows) if spans[y])
    to_webp(im, name, quality=90)
    print(f"\n  paste into index.html:\n"
          f"  const CMDR = {{w:{im.width}, h:{im.height}, headW:{widths[head_row]}, "
          f"top:{top}, cut:{cut}, cx:{cx}}};")
    print(f"  neck {widths[neck]}px at y={neck}, shoulders {widths[cut]}px at the cut; "
          f"{cut - top}px of her shows above the rim")


# ------------------------------------------------------------------ face
# Her expressions (STORY_ART_PROMPTS.md §1) are edits of art-src/commander.webp
# made in an image editor, which hands back a whole fresh render: re-framed,
# rescaled, and a pixel or two out here and there. Swapping whole frames would
# make every line of her shimmer, so only what the edit changed — the open
# mouth, the closed eyes — is kept, cut with the bust's own crop and scale,
# and drawn over the bust as an overlay.
FACE_SHEET_GAP = 4


def _gray(im):
    """luminance over the swamp's teal, so her dark outline reads against it"""
    bg = Image.new("RGBA", im.size, (40, 90, 80, 255))
    bg.alpha_composite(im)
    return np.asarray(bg.convert("L"), dtype=np.float32)


def _outline(g):
    from scipy import ndimage
    e = np.hypot(ndimage.sobel(g, 1), ndimage.sobel(g, 0))
    return e / (e.max() + 1e-6)


def _xcorr(a, b):
    """how well a lies over b at its best offset, and that offset (dy, dx)"""
    hh, ww = a.shape[0] + b.shape[0], a.shape[1] + b.shape[1]
    a, b = a - a.mean(), b - b.mean()
    c = np.fft.irfft2(np.conj(np.fft.rfft2(a, (hh, ww))) * np.fft.rfft2(b, (hh, ww)), (hh, ww))
    y, x = np.unravel_index(np.argmax(c), c.shape)
    dy, dx = (y if y < hh // 2 else y - hh), (x if x < ww // 2 else x - ww)
    return c[y, x] / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9), dy, dx


def _warp(edit, size, T):
    """the edit resampled onto the master's canvas; T takes a master pixel
    to the edit pixel showing the same spot: (a, b, c, d, e, f)"""
    return edit.transform(size, Image.AFFINE, T, Image.BICUBIC)


def _patch_pairs(m, r, ok, T, win=56, step=40, reach=6):
    """Slide each textured patch of the warped edit over the master; every
    patch that finds its place gives a (master point, edit point) pair. Those
    that can't — the area the edit changed — are left out by their error."""
    found = []
    for y in range(reach, m.shape[0] - win - reach, step):
        for x in range(reach, m.shape[1] - win - reach, step):
            if not ok[y - reach:y + win + reach, x - reach:x + win + reach].all():
                continue
            pa = m[y:y + win, x:x + win]
            if pa.std() < 10:
                continue
            err, dy, dx = min((float(np.mean((pa - r[y + j:y + j + win, x + i:x + i + win]) ** 2)), j, i)
                              for j in range(-reach, reach + 1) for i in range(-reach, reach + 1))
            found.append((x + win / 2, y + win / 2, dx, dy, err ** .5))
    errs = np.array([f[4] for f in found])
    good = [f for f in found if f[4] <= 2 * np.median(errs)]
    a, b, c, d, e, f = T
    pairs = [((px, py), (a * (px + dx) + b * (py + dy) + c, d * (px + dx) + e * (py + dy) + f))
             for px, py, dx, dy, _ in good]
    return pairs, [np.hypot(g[2], g[3]) for g in good]


def register(master, edit):
    """The affine taking a master pixel to the same spot in the edit: a
    search over scale (the outlines cross-correlated at each), then patch by
    patch over her whole bust, solved for an affine, twice."""
    def search(scales, k):
        """the best scale at 1/k size, and its offset in full-size px"""
        target = _outline(_gray(edit.resize((edit.width // k, edit.height // k), Image.LANCZOS)))
        best = None
        for s in scales:
            m = master.resize((round(master.width * s / k), round(master.height * s / k)), Image.LANCZOS)
            q, dy, dx = _xcorr(_outline(_gray(m)), target)
            if best is None or q > best[0]:
                best = (q, s, dx * k, dy * k)
        return best[1:]
    s, _, _ = search(np.exp(np.arange(np.log(.5), np.log(2.0), .02)), 4)
    s, tx, ty = search(s * np.exp(np.arange(-.025, .0251, .0025)), 2)
    T = (s, 0, tx, 0, s, ty)
    mg, ma = _gray(master), np.asarray(master)[:, :, 3]
    for _ in range(2):
        r = _warp(edit, master.size, T)
        ok = (ma > 250) & (np.asarray(r)[:, :, 3] > 250)
        pairs, _ = _patch_pairs(mg, _gray(r), ok, T)
        P = np.array([[x, y, 1] for (x, y), _ in pairs])
        Q = np.array([q for _, q in pairs])
        (a, b, c), (d, e, f) = np.linalg.lstsq(P, Q[:, 0], rcond=None)[0], np.linalg.lstsq(P, Q[:, 1], rcond=None)[0]
        T = (a, b, c, d, e, f)
    r = _warp(edit, master.size, T)
    _, left = _patch_pairs(mg, _gray(r), (ma > 250) & (np.asarray(r)[:, :, 3] > 250), T)
    print(f"  scale {np.hypot(T[0], T[3]):.4f} x {np.hypot(T[1], T[4]):.4f}, "
          f"{len(left)} patches, worst {max(left):.1f}px / mean {np.mean(left):.2f}px out after fitting")
    return r


def changed_area(master, r):
    """Where the edit changed her: strong colour differences, cleared of the
    one-pixel outline jitter a re-render leaves everywhere, and kept only
    where they make real shapes (a mouth, a pair of eyes)."""
    from scipy import ndimage
    m = np.asarray(master).astype(np.int16)
    e = np.asarray(r).astype(np.int16)
    hit = (np.abs(m[:, :, :3] - e[:, :, :3]).max(axis=2) > 56) & (m[:, :, 3] > 250) & (e[:, :, 3] > 250)
    hit = ndimage.binary_opening(hit, iterations=3)
    lab, n = ndimage.label(hit)
    if not n:
        sys.exit("  the edit changed nothing that shows")
    sizes = ndimage.sum(hit, lab, range(1, n + 1))
    keep = [i + 1 for i, s in enumerate(sizes) if s >= max(400, .15 * sizes.max())]
    return ndimage.binary_fill_holes(ndimage.binary_closing(np.isin(lab, keep), iterations=6))


def do_face(args):
    """art-src/commander_talk.webp:talk ... -> assets/commander_face.webp,
    one overlay per expression, and CMDR_FACE: each overlay's box on the
    sheet and where it sits on commander.webp."""
    from scipy import ndimage
    master = Image.open(ROOT / "art-src" / "commander.webp").convert("RGBA")
    box, size = commander_crop(master)
    fit = lambda im: im.crop(box).resize(size, Image.LANCZOS)
    alpha = np.asarray(master)[:, :, 3].astype(np.float32) / 255
    parts = []
    for arg in args:
        src, name = split(arg)
        print(f"{src.name}:")
        r = register(master, Image.open(src).convert("RGBA"))
        area = changed_area(master, r)
        # blend the edit in over the change and a margin round it; the
        # overlay runs a little wider again, over the bust's own pixels,
        # so the resampling of the blend's edge is covered too
        blend = np.clip(ndimage.gaussian_filter(ndimage.binary_dilation(area, iterations=8).astype(np.float32), 3), 0, 1)
        cover = np.clip(ndimage.gaussian_filter(ndimage.binary_dilation(area, iterations=18).astype(np.float32), 3), 0, 1)
        m, e = np.asarray(master).astype(np.float32), np.asarray(r).astype(np.float32)
        # a fresh render can drift in tint: match the skin just outside the change
        ring = ndimage.binary_dilation(area, iterations=24) & ~ndimage.binary_dilation(area, iterations=10) & (alpha > .98)
        tint = np.median(e[ring][:, :3] - m[ring][:, :3], axis=0)
        e[:, :, :3] -= tint
        out = m.copy()
        out[:, :, :3] = m[:, :, :3] * (1 - blend[..., None]) + e[:, :, :3] * blend[..., None]
        comp = fit(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)))
        a = np.asarray(fit(Image.fromarray((cover * alpha * 255).astype(np.uint8)))).astype(np.float32) / 255
        ys, xs = np.where(a > .004)
        x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
        part = np.asarray(comp)[y0:y1, x0:x1].copy()
        part[:, :, 3] = np.round(a[y0:y1, x0:x1] * 255)
        parts.append((name, Image.fromarray(part), int(x0), int(y0)))
        print(f"  changed {int(area.sum())} px of the master, tint {np.round(tint, 1).tolist()}; "
              f"overlay {x1 - x0}x{y1 - y0} at ({x0},{y0}) on the bust")
    sheet = Image.new("RGBA", (sum(p.width for _, p, _, _ in parts) + FACE_SHEET_GAP * (len(parts) - 1),
                               max(p.height for _, p, _, _ in parts)), (0, 0, 0, 0))
    entries, x = [], 0
    for name, p, dx, dy in parts:
        sheet.paste(p, (x, 0))
        entries.append(f"{name}:[{x},0,{p.width},{p.height},{dx},{dy}]")
        x += p.width + FACE_SHEET_GAP
    to_webp(sheet, "commander_face", quality=90)
    print("\n  paste into index.html ([sx, sy, w, h] on the sheet, [x, y] on commander.webp):\n"
          f"  const CMDR_FACE = {{{', '.join(entries)}}};")


# ------------------------------------------------------------ safe zone
SZ_DOOR_H = 120   # the gate opening's height on the stage: the tank stands ~97 px,
                  # so it rolls in with headroom rather than scraping the lintel


def do_safezone(zone_arg, gate_arg):
    """The ending's compound and its gate (SAFE_ZONE_ART.md). The compound's
    gate opening comes painted in flat magenta: that is keyed out, and its box
    is the one number everything else is placed by — the art is scaled so the
    opening stands SZ_DOOR_H tall, and the gate is fitted to exactly that box.
    The sign plate, the beacon glass and the two floodlamp faces are found by
    colour, so the game can letter the sign and light the lamps itself."""
    from scipy import ndimage
    src, name = split(zone_arg)
    im = Image.open(src).convert("RGBA")
    a = np.asarray(im).astype(int)
    r, g, b, al = a[:, :, 0], a[:, :, 1], a[:, :, 2], a[:, :, 3]
    key = (r > 200) & (g < 80) & (b > 200) & (al > 128)
    ys, xs = np.where(key)
    dx0, dy0, dx1, dy1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    fill = key[dy0:dy1, dx0:dx1].mean()
    if fill < .97:
        sys.exit(f"the magenta covers only {fill:.0%} of its box — the opening must be a filled rectangle")
    x0, y0, w, h = content_box(im, thresh=24)
    sc = SZ_DOOR_H / (dy1 - dy0)

    # the hole goes, and so does the magenta the frame's outline was blended with
    # — and off every half-transparent edge pixel too: the render's own cut-out
    # left its background tinted magenta under the alpha, and the resize blends
    # transparent pixels' RGB into their neighbours, so it would bleed back pink
    out = a.copy()
    out[key, 3] = 0
    rim = ndimage.binary_dilation(key, iterations=4) & ~key
    pink = (rim | (al < 250)) & (r - g > 40) & (b - g > 40)
    out[pink | key, :3] = (14, 19, 16)

    def found(mask, what):
        lab, n = ndimage.label(mask)
        if not n:
            sys.exit(f"could not find the {what}")
        sizes = ndimage.sum(mask, lab, range(1, n + 1))
        sl = ndimage.find_objects(lab)[int(np.argmax(sizes))]
        return sl[1].start, sl[0].start, sl[1].stop, sl[0].stop
    above = np.zeros(key.shape, bool)
    above[y0:dy0, dx0:dx1] = True
    plate = found(above & (g > b + 15) & (g > r) & (r > 45) & (r < 120) & (g < 140), "sign plate")
    beacon = found((b > 160) & (b - g > 60) & (r < 90) & (al > 128), "beacon glass")
    lamp_zone = np.zeros(key.shape, bool)
    lamp_zone[y0:plate[1], :] = True
    bright = lamp_zone & (r > 150) & (g > 150) & (b > 130) & (abs(r - b) < 50) & (al > 128)
    mid = (dx0 + dx1) / 2
    left, right = bright.copy(), bright.copy()
    left[:, int(mid):] = False
    right[:, :int(mid)] = False
    lamps = [found(m, "floodlamp") for m in (left, right)]

    zone = Image.fromarray(out.astype(np.uint8)).crop((x0, y0, x0 + w, y0 + h))
    zone = zone.resize((round(w * sc), round(h * sc)), Image.LANCZOS)
    to_webp(zone, name, quality=90)

    S = lambda v, o: round((v - o) * sc)
    box = lambda q: f"{{x:{S(q[0], x0)}, y:{S(q[1], y0)}, w:{round((q[2]-q[0])*sc)}, h:{round((q[3]-q[1])*sc)}}}"
    centre = lambda q: f"[{S((q[0]+q[2])/2, x0)},{S((q[1]+q[3])/2, y0)}]"
    door = (dx0, dy0, dx1, dy1)
    dw, dh = round((dx1 - dx0) * sc), round((dy1 - dy0) * sc)

    gsrc, gname = split(gate_arg)
    gim = Image.open(gsrc).convert("RGBA")
    gx, gy, gw, gh = content_box(gim, thresh=24)
    gate = gim.crop((gx, gy, gx + gw, gy + gh))
    ga = np.asarray(gate)[:, :, :3].astype(int).sum(axis=2)
    band = range(int(gw * .45), int(gw * .55))
    seam = min(band, key=lambda c: ga[:, c].mean())     # the darkest column near the middle
    to_webp(gate.resize((dw, dh), Image.LANCZOS), gname, quality=90)

    print(f"\n  opening {fill:.1%} filled; scale {sc:.4f}; gate aspect {gw/gh:.2f} "
          f"against the opening's {(dx1-dx0)/(dy1-dy0):.2f}; gate seam at {seam/gw:.1%}")
    print(f"\n  paste into index.html:\n"
          f"  const SZ = {{w:{zone.width}, h:{zone.height}, door:{box(door)}, sign:{box(plate)},\n"
          f"              beacon:{centre(beacon)}, lamps:[{centre(lamps[0])},{centre(lamps[1])}]}};")


# -------------------------------------------------------------- barriers
def do_barriers():
    """The side-view barrier props (STORY_ART_PROMPTS.md §2) that fortify the
    zombie outposts and the safe zone's approach. The sheet is trimmed to its
    props and shipped whole; each prop's box on it is printed for
    BARRIER_BOX, so the game draws them straight off the sheet."""
    from scipy import ndimage
    sheet = Image.open(ROOT / "art-src" / "STbarriers.webp").convert("RGBA")
    al = np.asarray(sheet)[:, :, 3] > 40
    lab, n = ndimage.label(ndimage.binary_dilation(al, iterations=4))
    boxes = []
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        ys, xs = np.where((lab[sl] == i) & al[sl])
        if len(xs) < 3000:
            continue
        boxes.append((sl[1].start + xs.min(), sl[0].start + ys.min(),
                      xs.max() - xs.min() + 1, ys.max() - ys.min() + 1))
    boxes.sort()
    x0 = min(b[0] for b in boxes) - 4
    y0 = min(b[1] for b in boxes) - 4
    x1 = max(b[0] + b[2] for b in boxes) + 4
    y1 = max(b[1] + b[3] for b in boxes) + 4
    to_webp(sheet.crop((x0, y0, x1, y1)), "world_barriers", quality=88)
    names = ["hedgehog", "barricade", "concrete", "sandbags", "wire"]
    print("\n  paste into index.html (boxes on world_barriers.webp, left to right):")
    for name, (bx, by, bw, bh) in zip(names + ["?"] * 9, boxes):
        print(f"    {name}:[{bx - x0},{by - y0},{bw},{bh}],")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if sys.argv[1] == "barriers":
        return do_barriers()
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
    elif mode == "commander":
        do_commander(args[0])
    elif mode == "face":
        do_face(args)
    elif mode == "safezone":
        do_safezone(args[0], args[1])
    else:
        sys.exit(f"unknown mode {mode!r}")


if __name__ == "__main__":
    main()
