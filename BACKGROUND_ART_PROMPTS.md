# Night-Swamp Reskin — GPT Image Asset Prompt Pack

Prompts for **GPT (gpt-image-1 / ChatGPT image tool)** to generate a replacement
background set for TANK vs ZOMBIE in the style of the supplied reference
(moonlit swamp graveyard, teal fog, mossy stone-brick platforms).

**How to use:** attach the reference image to every request and paste the
prompt. Each prompt already contains the "match the reference" clause — do not
drop it, it is what keeps 20 separate generations in one world.

---

## STATUS — what has been wired in

**Delivered and live** (2026-09-03). `index.html` now draws the night swamp:

| Asset | From | In code as |
|---|---|---|
| `nbTrees.webp` | SBgm1 | `scene` — drowned dead-tree cluster |
| `nbMoon.webp` | SBgm5 | `scene2` — the only plate with the moon |
| `nbGraves.webp` | SBgm4 | `scene3` — leaning graveyard |
| `nbManor.webp` | SBgm3 | `scene4` — distant candlelit manor |
| `nbArch.webp` | SBgm2 | `scene5` — collapsed brick archway |
| `nbMist.webp` | SBgm6 | `cloud`, `CLOUD_SRC = [38,465,1191,312]` |
| `ruinCrypt.webp` | SBgm8 | `BUILDINGS[0]` |
| `ruinTower.webp` | SBgm9 | `BUILDINGS[1]` |
| `ruinColumn.webp` | SBgm10 | `BUILDINGS[2]` |

All five plates measured a grass line at y 811–813 rather than the 800 asked
for, so `tools/fit_assets.py plates` now finds each plate's own line and
derives the crop from it — all five land on stage y=600.0. Verified in Chrome:
no console errors, all five rounds stage, and the 4,600px composite shows no
seam.

### Still needed

1. **A title key-art plate (section 5).** Never generated. `preLBD.webp` is
   still the old daytime farm art, so the attract screen no longer matches the
   game it opens. This is the most visible remaining gap.
2. **Two or three more structures.** Three shapes cover five rounds, so two
   repeat. See the corrected specs in 4b.
3. **`ruinPlinth.webp` (SBgm7) is unusable as drawn** and is not registered.
   At 2.55:1 its slab reaches 1.25 of its own height left of its deck; a shape
   is positioned by its deck, so it stands on the tank in every round and
   `stagingFits()` rejects it 5/5. The fix is proportional, not stylistic —
   see 4b.
4. **`ruinCrypt` carries a skull** on its door, which the shared style block
   ruled out. It reads as cartoon Halloween rather than horror, so it was kept
   — worth a second look for a school audience.

Old daytime assets (`bgm*.webp`, `building*.webp`, `cloud.webp`, ~2.6 MB) are
now unreferenced but left on disk.

---

## 0. What the engine actually needs

The background is **not** one big image. `index.html` composites it from four
asset families, and each one has hard pixel contracts:

| Family | Files | Native size | Alpha | Code hook |
|---|---|---|---|---|
| **A. Scene plates** | 5 (`bgm.webp`, `bgm1…4.webp`) | 1672 × 941 | no | `MANIFEST.scene…scene5`, `buildLayers()` |
| **B. Mist sprite** | 1 (`cloud.webp`) | 1254 × 1254 | **yes** | `CLOUD_SRC`, `bakeCloud()` |
| **C. Structures** | 8 (`building.webp`, `building2…8.webp`) | 1122 × 1402 | **yes** | `BUILDINGS[]` |
| **D. Title key-art** | 1 (`preLBD.webp`) | 1672 × 941 | no | `TITLE_LOGO_RECT`, `TITLE_HEDGE_RECT` |

### The one conversion you need
The stage is **1280 × 720**. Plates are drawn with `drawCover`, so:

```
stage px = file px × 0.7656        file px = stage px × 1.3062
```

### The horizontal-tiling contract (this is the big one)
`buildLayers()` lays the five plates end to end with a **360 stage px
(470 file px) cross-fade** and a stride of 920 stage px (1202 file px), then
**cycles the five forever** across a ~8,700 px world.

Consequences the art must obey:

1. **Every plate's leftmost 470 px must be able to dissolve into every other
   plate's rightmost 470 px.** So both outer 470 px strips are "connective
   tissue": generic fog, generic reeds, generic wall — identical horizon
   height, identical value, identical hue. **No landmark, no tree trunk, no
   moon, no gravestone inside those strips.**
2. All five plates share **exactly** the same horizon line, water line, grass
   lip and wall band heights.
3. Anything unique (the moon, the haunted house, the big gnarled tree) lives
   in the **middle 730 px** of a plate only.
4. The moon appears in **exactly one plate** (recommended: plate 3). Five
   plates × 1202 px stride means it recurs every ~4,600 world px — twice in a
   full run, which reads as deliberate. A moon in two plates reads as broken.

### The horizontal bands (file px, 1672 × 941 plate)

| Band | file y | stage y | Rule |
|---|---|---|---|
| Open sky / mist band | 44 – 327 | 34 – 250 | Drifting mist sprites are drawn here at 38–82% alpha. Plate must be **painted clean of clouds** in this band. |
| Target airspace | 131 – 682 | 100 – 522 | Zombies, structures, the triangle and its labels all live here. **Keep contrast and detail LOW** — this is backdrop, it will be covered. |
| Gun line | ≈ 682 | ≈ 522 | The triangle's horizontal leg runs across here. Nothing busy. |
| Target lane foot line | 724 | 554 | Structures stand on this line. Needs a readable strip of open ground. |
| Tank band | 670 – 784 | 513 – 600 | The tank drives here, full width. **Dead flat, unobstructed.** |
| **Grass lip / play surface** | **784** | **600** | Hard contract. The top of the grass must land here on all five plates. |
| Dirt / wall band | 784 – 941 | 600 – 720 | Below the play surface. The control dock covers the middle from stage y 617 down, so the outer thirds are what shows. |

### The trap in the reference image
The reference's charm is the **floating brick ledges** — and they sit exactly
in the target airspace (stage y 100–522), where the game draws its zombie,
its right triangle and its metre labels. Baked into the plate they would:
fight the triangle for legibility, repeat every 1202 px, and read as
platforms the tank can reach when it cannot.

**So the ledges are not scenery — they are family C.** The plates get them
only as *distant, fog-veiled, very low contrast* silhouettes; the crisp,
readable brick platforms are delivered as the 8 transparent structure
sprites, each with a flat brick deck for a zombie to stand on.

---

## 1. Shared style block

Paste this **verbatim at the top of every prompt** in sections 2–5.

```
Reference image attached — match it exactly as a style target.

STYLE: 2D hand-painted side-scrolling platformer art, cartoon-realist
vector-painterly finish, clean confident shapes, soft airbrushed volume,
NO visible brush texture, NO canvas grain, NO photographic detail,
NO pixel art, NO 3D render, NO cel-shade outlines on background elements.
Atmospheric aerial perspective: everything further away is paler, cooler,
lower contrast and flatter, veiled in luminous teal ground fog.

PALETTE (hold these):
  night sky, zenith      #0d2c3d
  night sky, horizon     #2f8f80
  moonlit fog / haze     #7fd3c0
  moon disc + glow       #eef5d6
  stone brick, lit face  #7c8b84
  stone brick, shadow    #3f4f4d
  brick mortar line      #2b3a39
  moss / grass, light    #8fb63f
  moss / grass, deep     #2f5a2b
  dead tree bark         #1d2b2a  (near-silhouette)
  window candlelight     #f4b13c  (tiny accents only)

LIGHTING: single light source — a large full moon high and behind the scene.
Everything is rim-lit cool from behind and falls to near-black in the
foreground. Warm light exists only as pinprick window glows.

MOOD: spooky but friendly. A cartoon Halloween swamp for a children's
educational game. Not gore, not horror, not grimdark, no blood,
no skulls, no figures, no characters, no creatures, no text, no letters,
no watermark, no UI, no border, no vignette frame.
```

---

## 2. Family A — the five scene plates

### 2a. Generation settings & the crop step
`gpt-image-1` renders landscape at **1536 × 1024** (3:2), not 16:9. So every
plate prompt tells the model to place the grass lip at **78% height
(y ≈ 800 of 1024)**, and you then crop a centred 1536 × 864 window
(y 80 → 944) and resize to 1672 × 941. That crop puts the grass lip at
exactly 83.3% — the `PLAY_SURFACE_Y = 600` contract. The appendix script
does this for you.

Request: `size: 1536x1024`, `quality: high`, `background: opaque`,
`format: png`.

In practice GPT put the line at y 811–813, not 800. That is fine and needs no
reroll — `fit_assets.py plates` finds each plate's own grass line and derives
the crop from it, so the instruction only has to get the line roughly right
and keep all five plates agreeing with each other.

### 2b. The per-plate common clause

Paste the shared style block, then this:

```
Produce ONE seamless 3:2 landscape background plate for a 2D side-scrolling
game. No characters, no vehicles, no text.

STRICT LAYOUT (image is 1536 wide × 1024 tall, y measured from the top):

1. SKY, y 0–330: open night sky, smooth vertical gradient from #0d2c3d at
   the very top to #2f8f80 near the horizon. A scatter of tiny faint stars
   in the upper third only. THIS BAND MUST BE PAINTED COMPLETELY CLEAN OF
   CLOUDS — no clouds, no cloud wisps, no cloud banks anywhere above y=330.
   (Drifting clouds are a separate animated layer.)

2. FAR BACKGROUND, y 250–620: layered silhouette ranges of misty mountains
   and a dense drowned forest of bare, twisted dead trees, each layer paler,
   cooler and lower contrast than the one in front. Luminous teal fog
   pooling between the layers. Very low contrast — this band gets covered by
   gameplay art, so it must read as soft atmospheric backdrop, never as
   detail that competes.

3. MIDGROUND, y 560–800: still black swamp water with soft horizontal
   mirror reflections, low mossy rocks, clumps of reeds and cattails,
   gnarled exposed roots. Fog sitting on the water surface.

4. GROUND, y 800: the GRASS LIP. A single dead-straight horizontal line of
   mossy grass tufts running the FULL width of the image, unbroken from edge
   to edge, at exactly y=800. This line must not rise, dip, or be
   interrupted by anything.

5. FOUNDATION, y 800–1024: directly beneath the grass lip, a continuous
   horizontal wall of large mossy grey stone bricks in a regular running-bond
   course pattern — same brick style as the platforms in the reference.
   Bricks are cool grey #7c8b84 lit from above, mortar lines dark #2b3a39,
   moss creeping over the top course. Full width, unbroken, dead level.
   A fringe of tall dark grass at the very bottom edge.

6. EDGE STRIPS — CRITICAL: the leftmost 470 px and the rightmost 470 px of
   the image must be deliberately GENERIC and INTERCHANGEABLE: only fog,
   distant reeds, plain water and the plain brick wall. No landmark, no
   large tree trunk, no moon, no structure, no gravestone, nothing visually
   distinctive within 470 px of either the left or the right edge. The two
   edge strips must be the same brightness, hue and horizon height as each
   other, and must be able to cross-dissolve into the equivalent strip of a
   DIFFERENT plate of the same set without a visible seam.

7. All distinctive content sits in the CENTRAL 600 px of the image only.

8. Do NOT paint any floating or hovering brick platform in the air anywhere
   in this image. Any elevated brick ledge may only appear as an extremely
   faint, fog-washed, far-distance silhouette below 12% contrast.
```

### 2c. The five unique centres

Append **one** of these to the common clause. This is the only thing that
differs between the five plates.

**Plate 1 → `nbTrees.webp`** (`MANIFEST.scene`) — delivered as SBgm1
```
CENTRE MOTIF: a cluster of three enormous bare gnarled dead trees with
curling tendril branches and hanging moss, standing in the shallow water,
their trunks near-silhouette #1d2b2a against the teal haze. No moon in this
plate.
```

**Plate 2 → `nbGraves.webp`** (`MANIFEST.scene3`) — delivered as SBgm4
```
CENTRE MOTIF: a small overgrown graveyard on a low mossy island — five or
six leaning weathered stone gravestones and one broken cross, wrapped in
knee-high fog, with a single dead tree behind them. No moon in this plate.
```

**Plate 3 → `nbMoon.webp`** (`MANIFEST.scene2`) — the moon plate, delivered as SBgm5
```
CENTRE MOTIF: an enormous full moon, pale #eef5d6 with soft visible craters
and a wide luminous halo, sitting high in the sky centred horizontally,
its lower edge no lower than y=340. Its glow silhouettes a single vast
gnarled dead tree that leans in from centre-right. The moon must sit fully
inside the central 600 px of the image and must not touch either edge strip.
```

**Plate 4 → `nbManor.webp`** (`MANIFEST.scene4`) — delivered as SBgm3
```
CENTRE MOTIF: a tall derelict haunted manor house far back in the mist,
near-silhouette, steep gables and a crooked chimney, with four tiny warm
#f4b13c candlelit windows. It is DISTANT and fog-washed — small, pale and
low contrast, not a foreground building. No moon in this plate.
```

**Plate 5 → `nbArch.webp`** (`MANIFEST.scene5`) — delivered as SBgm2
```
CENTRE MOTIF: a collapsed stone ruin on the near bank — a crumbling mossy
brick archway and a tumbled heap of the same grey bricks, half sunk in the
water, with dead reeds growing through it. Its highest point must stay
below y=640 so it never rises into the gameplay airspace. No moon in this
plate.
```

> **Consistency trick:** generate Plate 1 first, then attach *both* the
> reference **and** finished Plate 1 to the next four requests, adding:
> *"Second image attached is plate 1 of this same set. Match its horizon
> height, fog density, water line, grass lip position, brick wall and overall
> brightness exactly; only the central motif changes."*

---

## 3. Family B — the mist sprite (`nbMist.webp`)

One transparent wisp, cloned 5× at 85–200 stage px wide, 38–82% alpha,
drifting through stage y 34–250. Because the plates are painted clean, this
single sprite is *every* cloud in the sky.

Request: `size: 1024x1024`, `background: transparent`, `format: png`.

```
[shared style block]

Produce ONE isolated cloud on a FULLY TRANSPARENT background. Nothing else
in the image — no sky, no gradient, no ground, no frame, no second cloud.

A single soft horizontal wisp of moonlit night mist, wider than it is tall
(roughly 2.1 : 1). Pale luminous teal-white #cfe9e0 catching moonlight along
its upper edge, fading to translucent #4a7d78 underneath. Torn, feathery,
wind-stretched silhouette with a few trailing tendrils on the left and right
so it does not read as a symmetrical blob. Edges soft and semi-transparent,
dissolving completely into transparency — no hard rim, no outline, no drop
shadow.

It will be tinted and faded by code and drawn at small sizes, so keep the
internal value range narrow and the silhouette interesting.
```

**After generating:** `fit_assets.py mist` measures the content box and
prints the `CLOUD_SRC` line to paste in. The delivered wisp came out at
3.82:1 against the old cloud's 2.12:1, so the unchanged size table now draws
threads of ground fog rather than puffs — which suits a night swamp, and is
why the sizes were left alone.

---

## 4. Family C — the structures (the brick platforms)

This is where the reference's floating ledges actually land. Each file is a
**complete standalone structure** on transparency, scaled by the engine as
one piece, with a **flat level deck on top** that a zombie stands on and
that the round's right triangle is pinned to.

Request: `size: 1024x1536`, `background: transparent`, `format: png`.

### 4a. The common clause

```
[shared style block]

Produce ONE complete standalone structure on a FULLY TRANSPARENT background,
in tall portrait orientation. Nothing else in the image: no ground, no sky,
no grass, no water, no fog bank, no cast shadow on the floor, no second
object, no text. The structure must be fully contained with a small margin
of empty transparency on all four sides.

MATERIAL: exactly the mossy grey stone brickwork of the platforms in the
reference image — large regular bricks in running-bond courses, cool grey
#7c8b84 lit faces, #3f4f4d shadowed faces, dark #2b3a39 mortar lines,
chipped and weathered corners, clumps of bright #8fb63f moss and hanging
vines on the top course and drooping over the edges, a few dangling roots.
Lit cool from above and behind, moonlit rim on the top edges, deep shadow
underneath every overhang.

THE DECK — hard requirement: the top of the structure must present ONE flat,
perfectly horizontal brick surface, wide enough to stand a figure on and
level to within a couple of pixels. It must read unmistakably as a walkable
brick platform surface, viewed dead-on from the side (no perspective, no
top-face foreshortening). Nothing may protrude above that surface anywhere
near its centre — no spire, no railing, no chimney, no tall vine.

VIEW: flat side elevation, orthographic, camera exactly level with the
structure's mid-height. Same viewing angle as the reference's platforms.
```

### 4b. What is in the set, and what a new shape must satisfy

Each slot's proportions and deck position are **fixed by `BUILDINGS[]` in
`index.html`**. Match the aspect and deck rule and the appendix script will
place the art into the exact box the code expects — no code edit needed.

Three are in. The engine reads `box` / `deck` / `deckCx` in each file's own
pixels and scales the shape as one piece, so **nothing needs to match a fixed
canvas or a fixed box** — `tools/fit_assets.py ruin` measures the art and
prints the `BUILDINGS[]` entry. What art direction still has to hit is one
ratio, below.

| In the set | Aspect | Deck | Left reach | Stages in |
|---|---|---|---|---|
| `ruinCrypt` — mausoleum, flat slab lid | 0.839 | 47% across, 4.9% down | 0.40 | rounds 1, 3 |
| `ruinTower` — snapped bell tower | 0.562 | 40% across, 1.9% down | 0.23 | rounds 1–5 |
| `ruinColumn` — vine-wrapped column | 0.272 | 56% across, 2.0% down | 0.15 | rounds 1–5 |
| ~~`ruinPlinth`~~ — slab on two stubby piers | 2.551 | 49% across, 10.5% down | **1.25** | **none — rejected** |

### The one number that decides whether a shape can be used

**Left reach** = how far the shape spills left of its deck, as a fraction of
its own height. The engine pins the deck under the zombie and scales the shape
to reach its foot line, so left reach is what closes on the tank:

- **≤ 0.29** — stages in every round, the steep 60° one included. `ruinColumn`
  and `ruinTower` are here, which is why they carry rounds 2, 4 and 5.
- **0.3 – 0.6** — the shallow 30° rounds only. `ruinCrypt` is here.
- **> 0.6** — stages nowhere. `ruinPlinth` is here.

With a roughly centred deck, left reach ≈ half the width over the height, so
the rule of thumb for a new shape is **aspect ≤ 1.2**, and **≤ 0.6 to be
usable in every round**. A wide platform is not forbidden — it just needs a
tall footing under the slab instead of two stubby piers, so the height carries
the width.

### The three shapes still worth generating

Use the 4a common clause, then:

| Want | Aspect to aim for | Deck | Design |
|---|---|---|---|
| An asymmetric ruin | ~0.80 | 62% across, at the top | Tall flat-topped brick pier on the RIGHT, a lower crumbled wall spilling LEFT. Deck is the right pier's top. |
| A two-tier ruin | ~1.0 | 62% across, **25% down** | Taller broken brick wall LEFT and BEHIND; the deck is a wide mid-height brick ledge to the RIGHT and IN FRONT of it. |
| A wide platform, done right | **≤ 1.2** | ~50% across, at the top | The plinth reattempted: one thick brick slab, but carried on a single tall solid brick base that runs to the ground — not on short legs. |

### 4c. Per-slot prompt template

```
[common clause from 4a]

THIS STRUCTURE: <paste the Design cell>

PROPORTIONS: the structure's silhouette must be <ASPECT> times as wide as it
is tall, measured on its own bounding box. Hold that proportion.

DECK POSITION: the centre of the flat brick standing surface must sit
<ACROSS>% of the way across the structure's width from its left edge, and
<DOWN>% of the way down from its highest point. Nothing may stand above that
surface within 20% of the width either side of it.
```

Then place it into the exact box the code reads:

```bash
python3 tools/fit_assets.py building b5 ~/Downloads/b5.png
# override if the render's flat top didn't land where you asked:
python3 tools/fit_assets.py building b5 ~/Downloads/b5.png 0.58
```

---

## 5. Family D — the title key-art plate (`preLBD.webp`)

The attract screen. This one plate carries the wordmark, and the code
re-blits two rectangles of it back over live effects, so its **layout is
locked**:

| Region | file px rect (in 1672 × 941) | Must contain |
|---|---|---|
| Wordmark | x 439–1246, y 39–570 | The game title art, and nothing that continues below y 570 |
| Open band | centred on stage (640, 548) ≈ file (836, 716), radius ≈ 360 file px | Must be **quiet and uncluttered** — a light burst is drawn here and CTA buttons sit on top |
| Bottom-right fringe | x 1071–1672, y 896–941 | Continuous foliage/grass, uniform above and below y 896 — the zombie line-up's feet are veiled by re-blitting this strip |

Request: `size: 1536x1024`, `quality: high`, `format: png`, then crop as in 2a.

```
[shared style block]

Produce ONE finished 3:2 title-screen key-art illustration for a children's
educational game, in the moonlit swamp-graveyard world of the reference.

COMPOSITION (image 1536 wide × 1024 tall, y from the top):
- Upper half: an enormous pale full moon low-centre behind the scene, its
  halo blowing out the sky, framed by two towering gnarled dead trees that
  arch in from the left and right edges like a proscenium.
- Leave the rectangle from x 400 to x 1145, y 40 to y 620 as CLEAR OPEN SKY
  and moon glow — a title logo will be placed there. Nothing may cross into
  it: no branch, no bird, no gravestone, no platform.
- Middle: layered mossy stone-brick ruins and leaning gravestones receding
  into teal fog on both sides, with a still black reflecting pool between
  them.
- The horizontal band from y 620 to y 860, centred on x 768, must be OPEN
  and QUIET — a soft empty patch of moonlit mossy ground with no detail,
  no object and no strong value contrast. Interface elements go there.
- Bottom edge, y 860 to 1024: a dense continuous band of dark overgrown
  grass, ferns and swamp reeds running the FULL width, uniform in density
  and colour, so any horizontal slice of it looks like any other.
- No characters, no vehicles, no figures, no text, no letters, no logo
  lettering, no numbers, no watermark.
```

Generate the wordmark separately (or letter it in Figma) and composite it
into the x 439–1246 / y 39–570 rect — asking an image model for legible
game-title lettering is the one part of this pack that reliably fails.

---

## 6. What changed in `index.html`

Three places, all data:

- **`MANIFEST`** — the five `scene*` keys and `cloud` now name the `nb*`
  plates; the eight `b1…b8` keys are replaced by three `ruin*` keys.
- **`CLOUD_SRC`** — re-measured to `[38,465,1191,312]`.
- **`BUILDINGS[]`** — three measured entries, with a note recording why the
  plinth is not among them.

Not touched, and not needing to be: `buildLayers()`, `drawBG()`,
`fitBuilding()`, `stagingFits()`, `drawTower()`, the cloud size table.
Family D would need nothing either — `TITLE_LOGO_RECT` /
`TITLE_HEDGE_RECT` are respected by the layout spec in section 5.
- **Worth a look:** `spawnDriveDust()` throws warm dust, and
  `bakeBoomLayers()` builds a warm orange blast. Both still read fine against
  teal — warm-on-cool is the strongest contrast pair here — but the drive
  dust may want a cooler, paler tint on a night ground.
- **Also worth a look:** the UI (`board.svg`, the warm timber palette,
  `--plate-c`) stays warm and readable over teal, so leave it. Only
  `#msg` / `#objBanner` need a legibility pass.

---

## 7. Appendix — the fitter script

Drops generated PNGs into the exact boxes the code expects and writes WEBP.

```bash
python3 tools/fit_assets.py plates SBgm1.png:nbTrees SBgm5.png:nbMoon ...
python3 tools/fit_assets.py mist   SBgm6.png:nbMist
python3 tools/fit_assets.py ruin   SBgm9.png:ruinTower --check
```

`plates` finds each render's own grass line and crops from it. `ruin`
measures the alpha box, finds the widest level run along the silhouette's top
profile — the deck a zombie can actually stand on, which on a ruin is often
*not* the highest thing in the file — and prints the `BUILDINGS[]` entry plus
the shape's left reach. `--check` writes an overlay to `/tmp` showing the
detected box, deck row and deck centre, so the measurement can be eyeballed
before it goes into the code.

See `tools/fit_assets.py`.
