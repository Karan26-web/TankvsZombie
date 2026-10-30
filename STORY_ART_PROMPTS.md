# Story Intro — Art

> **STATUS** (2026-10-30). The story now runs inside the game and is drawn
> with the game's own art (STORY_INTRO.md §2–3), so the painted story frames
> are retired (§3). It needed one new image, the barrier set, which is
> delivered and live (§2). The commander's **blink** edit is live (§1): she
> blinks while she's up. Her **talking** edit was made but is not used, since
> the flapping mouth read as mumbling. The **thumbs-up** (§1c) is still open,
> and it's optional.

**The rule the first version taught us:** new art for this game is drawn in
the game's own view and style (flat side-on, bold dark outlines, the moonlit
teal palette) and placed into the existing world. GPT can match the game's
style for a single prop or a small edit to a character. It couldn't hold that
style across a set of full painted scenes, so the story isn't built from them.

---

## 1. The commander's three expressions

Beat 5 is the one moment the camera is close on her: punched in at 3.4× for
about three seconds while she says "Let's get into the tank!". Three small
edits bring that shot to life:

| Edit | What the game does with it | Status |
|---|---|---|
| **a. Talking** | Tried as a mouth opening and shutting on a syllable beat while her line played. Taken out: under a caption it read as mumbling. Her mouth stays as drawn. | Made, **not used** (kept in `art-src/`) |
| **b. Blink** | A 0.12 s blink 0.7 s after she settles, then every 2.2–3.8 s while she's up. It can land mid-word. | **Live** |
| **c. Thumbs-up** | Held for the last moment before she drops into the hatch: "Let's go!" | Optional, not made |

**How they're used:** `python3 tools/fit_assets.py face
art-src/commander_blink.webp:blink` lines the edit up with
`art-src/commander.webp`, keeps only what it changed (the closed eyes), and
packs that into `assets/commander_face.webp` (142×77, 4 KB). The game draws
it as an overlay on her normal bust, so nothing else about her ever shifts
between frames. The step takes several edits at once (`…:talk …:blink`) if
the talking one is ever wanted back. The editor handed both renders back
re-framed (1138×1382, about 1.3× larger, cut off at the shoulders), which is
fine: the tool finds the scale and position by itself.

**Why a thumbs-up**, not the pointing pose planned before or a beckon:
pointing was for beat 6, where she is now small on screen and it wouldn't
read. A beckon only reads when it moves, and a still frame of it looks like a
wave. A thumbs-up reads in one frame, at any size, and it's what you'd do
right before ducking in.

### How to make them: edits, not new drawings

1. In a new ChatGPT conversation, upload **`art-src/commander.webp`**
   (1254×1254, transparent).
2. Click the image, choose **Select**, brush **only** the area named below,
   and paste the prompt.
3. Download the result with its transparency and save it to `art-src/` under
   the name given (PNG or WebP).
4. Start each of the three edits from the original image, not from a previous
   edit.

Only the edited area of each result is used, so a small drift elsewhere in
the picture doesn't matter, and neither does a change of size or framing.
What matters is that the edited area matches the rest of her, and that the
rest of the picture stays recognisably the same image so the tool can line it
up.

The thumbs-up adds a hand **outside** her outline, where today's `face` step
takes nothing. When it arrives, the step needs one addition: carry the edit's
own transparency there.

**a. Talking → `art-src/commander_talk.webp`** (select the mouth and chin)
```
Change only her mouth: open mid-word in a friendly, confident speaking shape,
upper teeth just visible. Keep everything else exactly the same — face, eyes,
helmet, outline, colours, size and position — and keep the background
transparent.
```

**b. Blink → `art-src/commander_blink.webp`** (select both eyes)
```
Change only her eyes: closed in a relaxed, natural blink, lashes showing.
Keep everything else exactly the same and the background transparent.
```

**c. Thumbs-up → `art-src/commander_thumbs.webp`** (select her left shoulder,
on the RIGHT of the picture, and the empty space above it beside her helmet)
```
Raise her left hand (the one on the RIGHT side of the picture) beside her
helmet in a confident thumbs-up: forearm rising from her shoulder, fist at the
height of her ear-cup, thumb pointing straight up, in the same green jacket
sleeve with the same bold dark outline. Keep the whole hand inside the picture
and to the right of her helmet, without covering her face, the headset or the
microphone. Keep her face, helmet, body, size and position exactly the same,
keep the straight cut across the bottom, and keep the background transparent.
```

The hand has to be at ear-cup height because the hatch rim cuts her off at the
shoulders, so anything lower would be hidden inside the tank.

**What I check:** the edit looks like the same character in the same style;
the rest of the picture still matches the original (the tool reports how well
it lined up); the thumbs-up hand is a simple cartoon fist (four fingers curled,
one thumb) entirely above her shoulders; the background is transparent.

---

## 2. Barrier set — delivered and live → `art-src/STbarriers.webp`

Fitted by `python3 tools/fit_assets.py barriers` into
`assets/world_barriers.webp` (1503×225). The game places the five props at every
outpost and in front of the safe zone's gate (STORY_INTRO.md §6).

To regenerate it, attach `assets/ruinTower.webp` and `assets/tankSheet.webp`,
paste the prompt below, save the result over `art-src/STbarriers.webp`, re-run
the command, and paste the five boxes it prints into `BARRIER_BOX` in
`index.html`. Keep the props in this order: the tool names them left to right.

```
Draw a set of FIVE separate barrier props in the game's SIDE-ON view (flat
side view, like the attached ruin), same style:
1. a steel anti-tank hedgehog (three crossed beams),
2. a red-and-white striped road barricade on legs,
3. a grey concrete road barrier block,
4. a waist-high stack of sandbags,
5. a coil of barbed wire strung between two wooden posts.
Each standing on its own flat base, completely separate with at least 80 px
of clear space around it, in one row along a level line.

CANVAS: 1536×1024, fully transparent background (real PNG alpha). No ground,
no shadow, no glow, no text.
```

---

## 3. Retired: the painted story frames

Nothing loads these any more, and their `assets/story*.webp` cuts are deleted.
Keep them as concept art or delete them.

| File | Was | Why it's retired |
|---|---|---|
| `art-src/ST1.webp` | Frame 1, Zombie Land | A three-quarter painted scene, not the game's side-on world |
| `art-src/ST2.webp` | Frame 2, the ruined road | A road the game doesn't have |
| `art-src/ST3.webp` | Frame 3, barriers and the safe zone | A different safe zone from the one in the ending |
| `art-src/STfg.webp` | Foreground framing layer | Only needed for the parallax frames |
| `art-src/STtank.webp` | The tank, three-quarter rear view | A redraw of the tank that drifted from the sprite |
| `art-src/STzombies.webp` | Six zombies, facing us | Three of them never appear in the game |

---

## 4. If a render comes back wrong

| Problem | Ask GPT |
|---|---|
| More than the selected area changed | "Change only the selected area; keep her face, eyes, helmet and colours exactly as in the original." |
| Size or position changed | "Keep the image 1254×1254 with her in exactly the same place and size." |
| The hand covers her face or headset | "Move the hand further right, beside the helmet, clear of her face, headset and microphone." |
| Odd fingers or thumb | "Draw a simple cartoon fist with four fingers curled and one thumb up, in the same bold outline style." |
| The hand sits low, at chest height | "Raise the fist to the height of her ear-cup; the forearm rises from her shoulder." |
| The background came back solid | "Keep the background fully transparent." |

## 5. Hand-over checklist

```
art-src/commander_talk.webp     (1a, delivered, not used)
art-src/commander_blink.webp    (1b, delivered, live)
art-src/commander_thumbs.webp   (1c, optional, not made)
art-src/STbarriers.webp         (§2, delivered, live)
```
