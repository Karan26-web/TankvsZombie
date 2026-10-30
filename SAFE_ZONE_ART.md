# Safe Zone — GPT Image Asset Prompts

> **STATUS — delivered and live** (2026-10-30). `art-src/SZ1.webp` (compound)
> and `art-src/SZ2.webp` (gate) are fitted by
> `tools/fit_assets.py safezone art-src/SZ1.webp:safeZone art-src/SZ2.webp:safeGate`
> into `assets/safeZone.webp` (802×361) and `assets/safeGate.webp` (229×120),
> and the in-code stand-in is gone. The render's opening came out 1.91:1
> rather than 1.3:1; that is fine — the art is scaled by the opening's
> height (120 stage px), and the gate render matched it at 1.86:1. To
> regenerate either image, follow the prompts below and re-run the command.

Art for the game's new ending (LXD storyboard, end screens 2–3): after the last
zombie the tank drives up to the **SAFE ZONE**, the gates open, it drives in,
the gates close behind it, fireworks go up, and **Mission Complete!** comes up
with a **FINISH** key.

The ending already works in the game today with a **stand-in compound drawn in
code** (`bakeSafeZone()` in `index.html`). These two images replace it. Nothing
else in the ending needs art: the lit passage behind the gates, the light
spilling out, the blue beacon glow, the fireworks, the caption and the card are
all drawn by the game.

**How to use:** generate in ChatGPT (gpt-image-1 or newer). Attach the two
reference files to every request — `assets/ruinTower.webp` (the world's style)
and `assets/tankSheet.webp` (outline weight and palette) — and paste the prompt
as-is. Save the raw renders to `art-src/` as `SZ1.webp` (compound) and
`SZ2.webp` (gate), then hand them back to me: I fit them, cut them into the
game's layers and swap out the stand-in.

---

## 0. What the game needs, and why each rule exists

The game is a side-on 2D scroller. The tank (288 px long, ~100 px tall on a
1280×720 stage) drives left-to-right along the grass line and **into** the
compound through a gate in its front wall. That is staged with layers, and the
layers are why the rules below are strict:

| Layer | What it is | Drawn |
|---|---|---|
| back | the whole compound, with the lit passage showing through the opening | behind the tank |
| front | only the wall **right of the opening** | in front of the tank — this is the wall it disappears behind |
| gates | two steel leaves that slide apart into the wall | in front of the tank, clipped to the opening |

So:

1. **The gate opening is filled with flat pure magenta `#FF00FF`.** No shading,
   no gradient, no texture, hard edges. I key it out to get the exact hole.
2. **The opening is a plain rectangle** at ground level, flat top (a lintel),
   no arch. The gate leaves are rectangles and have to cover it exactly.
3. **The opening sits on the LEFT of the facade.** Left of it: only a narrow
   pillar (no wider than a third of the opening). Right of it: at least
   **twice the opening's width** of solid wall, at full height down to the
   ground — the tank (and its long gun) has to vanish completely behind it.
4. **Nothing sticks out to the left at ground level** — no sandbags, crates or
   barriers left of the opening. The tank stops right in front of the pillar.
5. **The opening must be tall enough for the tank**: opening height ≈ 0.75× its
   width, and the whole compound's height ≈ 2.6× the opening's height.
6. **Blank sign, no letters.** The game says "SAFE ZONE" in six languages, so the
   plaque over the gate must be empty. (Any baked English word gets painted
   over or rejected.)
7. **No glows or light beams.** Windows may be lit warm, but no bloom, no
   searchlight cones, no beacon glow — the game animates the beacon and the
   light from the gate, and a baked glow would fight them.
8. **Transparent background, flat ground line.** The compound stands on a
   straight, level base — it is placed on the game's grass line.

The game's own stand-in uses these proportions; matching them means the art
drops straight in:

```
canvas 600 × 360 (stage px)   opening x 80, y 224, 176 × 136   beacon x 495, y 56
```

---

## 1. The compound — `SZ1`

```
Use the attached images as a strict style reference: the ruined stone tower
for the world's painting style and moonlit palette, the tank sprite sheet for
outline weight and colours. Draw a SAFE ZONE compound for a 2D side-scrolling
game: the fortified military outpost at the end of a zombie-infested road,
where the heroes are safe for the night.

VIEW
- Pure side-on view, like a 2D platformer: we see the compound's front wall
  flat-on, standing on a perfectly level ground line along the bottom edge.
- No perspective tilt, no top surfaces visible except thin caps and ledges.

LAYOUT – follow exactly, left to right
- LEFT: a heavy gatehouse block of reinforced concrete with steel corner posts.
  In its lower part, a large RECTANGULAR gate opening at ground level, set in
  a thick steel frame, with a lintel striped in yellow-and-black hazard paint.
  The opening sits near the left end of the gatehouse: only a narrow concrete
  pillar (about a third of the opening's width) stands to its left.
- Fill the gate opening COMPLETELY with flat pure magenta #FF00FF — one solid
  colour, no shading, no texture, sharp straight edges. It will be keyed out.
- Opening proportions: about 1.3 wide to 1 tall. Its height is about 38% of
  the compound's total height.
- Above the opening: a mounted sign board, rectangular with rounded corners,
  dark green metal with a bright brass rim and four bolts. The sign is
  COMPLETELY BLANK — no letters, no symbols.
- RIGHT of the gatehouse: a long, lower fortified wall (concrete blocks, a
  steel cap along its top, coils of barbed wire along the cap), at least twice
  as wide as the gate opening, solid all the way to the ground. Two small
  barred windows in it, lit warm orange from inside.
- On the long wall, near its right end: a steel watchtower on four angled legs
  with cross-braces, a small cabin with a warm-lit window, a pitched roof, and
  on the roof a small beacon lamp with clear blue glass (NOT glowing).
- Two small floodlight housings on the gatehouse's top corners (unlit).
- A short stack of sandbags at the foot of the long wall, on the RIGHT only.
  Nothing at all in front of or to the left of the gate opening.

STYLE – match the references
- Same painted cartoon game-art look as the ruined tower: chunky readable
  shapes, bold dark outlines (#0E1310) of the same weight as the tank sheet,
  cel shading in 2–3 tones, a little moss and grime at the base only.
- Palette: cool blue-grey concrete (#617574 to #3F4E4F), dark gunmetal steel
  (#434C47, #2E373C), hazard yellow (#F2B632), warm window light (#FFCF6B).
  Moonlit from the upper left, teal ambient light, like the rest of the world.
- It must read as SAFE: solid, repaired, lived-in — not ruined.

CANVAS
- 1536×1024, fully transparent background (real PNG alpha).
- The compound fills most of the width, its ground line flat along the
  bottom, nothing cropped by the canvas edges.
- No ground, no road, no grass, no sky, no shadow on the ground, no glow,
  no light beams, no text, no letters, no people, no zombies.
```

**What I check before fitting it:** the magenta is one flat colour with hard
edges; the opening is a rectangle at ground level; nothing left of it; the wall
right of it is at least twice its width; the sign is blank; no baked glow.

---

## 2. The gate — `SZ2`

```
Use the attached images as a strict style reference (same painting style,
outline weight and palette as before). Draw a heavy steel DOUBLE GATE for the
safe zone compound, seen flat-on from the front, closed.

- Two identical steel leaves side by side, meeting in a vertical seam exactly
  in the middle, together forming one rectangle about 1.3 wide to 1 tall.
- Each leaf: riveted dark gunmetal plate (#5F6E6B to #3A4644), a raised frame
  around its edge, three horizontal reinforcing ribs with rivets, and a band of
  yellow-and-black hazard stripes (#F2B632 / #1C1F1D) along the bottom.
- The two leaves are mirror images of each other; a slight dark gap at the
  seam.
- Bold dark outline (#0E1310) around each leaf, same weight as the reference.
- Flat-on, no perspective, no frame or wall around it — only the two leaves.

CANVAS
- 1536×1024, fully transparent background (real PNG alpha).
- The gate centred, as large as fits with a margin, edges perfectly straight
  and axis-aligned.
- No glow, no shadow, no text, no logo.
```

**What I check:** two equal leaves, a straight vertical seam in the exact
middle, straight edges (I trim to the rectangle and split it at the seam).

---

## 3. What happens after you hand them over

1. I add a `safezone` step to `tools/fit_assets.py` that keys the magenta,
   measures the opening, the sign plate and the beacon, scales the compound so
   its opening matches the stage contract (176×136 px), and writes
   `assets/safeZone.webp` — then trims and splits `SZ2` into the two leaves.
2. `bakeSafeZone()` stops drawing the stand-in and builds the same three layers
   (back / front / gates) from the art. The sign gets its "SAFE ZONE" in the
   player's language set over the blank plate, exactly as the stand-in does now.
3. I check the whole ending in the browser: approach, gates, the drive in, the
   gates shutting with the tank fully hidden, fireworks, Mission Complete.

## 4. If a render comes back wrong

| Problem | Ask GPT |
|---|---|
| Opening is arched or shaded | "Make the gate opening a plain rectangle filled with one flat colour, pure magenta #FF00FF, no shading." |
| Something stands left of the gate | "Remove everything in front of and to the left of the gate opening; only a narrow pillar may stand left of it." |
| Sign has text | "Make the sign board completely blank — no letters or symbols." |
| Beacon or windows glow | "Remove all glow and light effects; keep the beacon glass plain blue." |
| Ground or sky drawn in | "Transparent background only — remove the ground, road and sky." |
