# Story Intro — Design

> **STATUS** (2026-10-30). Rebuilt to run inside the game, and it plays from
> START. It uses no story-only art: every frame is the real level. The barrier
> art (`art-src/STbarriers.webp`) is now part of the world, and the
> commander blinks (her blink edit is live; the talking one isn't used). The
> illustrated version and its six painted images are retired (§2, §8). Still
> optional: her thumbs-up (STORY_ART_PROMPTS.md §1c). Voice-over: a synthetic
> draft is installed and plays only with `?vo=draft` (STORY_VO.md).
> Preview any beat with `index.html#previewstory3` (beat 3), or
> `#previewstory3_150` (frozen 1.5 s in).

The opening story for **Tank vs Zombie — Angle Academy**, built from the LXD's
9-screen storyboard. It plays between **START ▶** and the learning section, and
it ends on the **NEXT ▶** hand-off to the lesson.

Companion files:
- [STORY_ART_PROMPTS.md](STORY_ART_PROMPTS.md): the optional commander
  expressions, and the record of the barrier art.
- [STORY_VO.md](STORY_VO.md): the voice-over script in all six languages, and
  the state of the draft recordings.

---

## 1. Where it sits

```
START ▶ ─► STORY (beats 1–9, ~36 s, plays in full) ─► NEXT ▶ ─► learning section
        ─► round 1 briefing ─► 5 rounds ─► safe-zone ending ─► Mission Complete ─► FINISH
```

It plays once per launch. **TRY AGAIN** after a lost round goes straight back
to that round.

## 2. Why it was rebuilt

The first version told beats 1–3 with painted story frames (a 2.5D parallax
of six GPT images) and beats 4–9 in the game. Reviewed against the game
itself, it failed in eight ways:

1. **It looked like a different game.** The frames were three-quarter
   perspective paintings with softer, busier rendering. The game is a flat
   side-on world with bold outlines and cel shading. Every cut from story to
   game was a jump in style, and no prompt reliably held GPT to the game's
   style across six images.
2. **It showed places the game doesn't have.** A road winding to the horizon
   doesn't exist in a side-on lane. The learner was shown a world they would
   never play in.
3. **It showed a different cast.** The three-quarter tank was GPT's redraw of
   ours, and its details drifted. Three of the six zombies are characters the
   player never meets.
4. **It promised barriers and never delivered them.** "We need to cross these
   barriers" was said over a painting, and then the game had none.
5. **Its safe zone wasn't the safe zone.** The compound in frame 3 was a
   different drawing from the one the tank drives into at the end.
6. **The goal had no shape.** "Reach the safe zone" didn't show how far away
   it is or what stands in the way: five outposts, five zombies, five rounds.
7. **It had a seam in the middle.** Two different-looking worlds were joined
   with a dive through black, and that join fell on "But first…", the turn
   the whole story leads up to.
8. **Beat 5 contradicted its line.** She climbed *out* of the tank while
   saying "Let's get into the tank!"

## 3. The idea

**Tell it in the game, not in front of it.** One world and one camera: the
story is a fly-over of the level the learner is about to play. It shows the
same tank, the same five ruins with their zombies, the same barriers and the
same safe zone that ends the game. The camera starts on the tank, travels to
the goal, whips back, and lands exactly where round 1 begins, so there is no
seam to hide. This is the 2D version of what Quartland and Sectorscape do in
3D: the intro happens in the game's own world.

The story does three jobs beyond setting the scene:

1. **It plants the goal.** The safe zone is seen in beat 3 and drawn on the
   mission strip, and the ending pays it off with the same compound.
2. **It previews the whole game.** The fly-over passes all five outposts, and
   the strip lays out the run: tank, five zombies, safe zone.
3. **It introduces the tools on the real objects.** Beats 6–9 happen on the
   actual tank, the actual first zombie and the actual triangle the learner is
   about to solve.

## 4. Beat sheet (as built)

Times are seconds into the beat. A beat moves on when its line has been heard
or read **and** its action has finished, whichever is later (§5).

| # | Caption (verbatim) | On screen | Camera | Sound |
|---|---|---|---|---|
| 1 | **Welcome to Zombie Land!** | The start of the world: the moonlit swamp and the tank parked at the far left, with no zombie in sight yet. The line arrives as a **big title** in the centre. | Opens pushed in (1.32×) on the sky and cranes back to the full view (0.2–2.8 s). | |
| 2 | **There are zombies everywhere!** | The camera glides over the first three outposts, each with its zombie already on its ruin. More zombies stand in the swamp between them, swaying, some further back in the mist. These are the game's own three zombie types. | Glides right over outposts 1–3 (0.15–4.55 s), eased at both ends. | A groan as each zombie comes on screen, pitched by type. |
| 3 | **We need to cross these barriers and reach the safe zone.** | The camera passes outposts 4 and 5, each with its barricades, hedgehogs, wire and sandbags, and the last line of barriers in front of the safe zone's gate. The **mission strip** springs in on the wall below the ground: tank → five zombies → safe zone, joined by a dotted route. The safe zone icon lights up when the camera arrives. | Glides on to the safe zone (0.1–4.9 s). | A rising blip per strip icon. |
| 4 | **But first, we need to clear the way!** | A whip back to the start through a dip to black (0.95 s). The strip fades out, the tank rolls up to the first outpost (the game's own intro drive), and the zombie spots it: arms up. | The whip, then the game's intro camera. | Whoosh, engine, the zombie's "uh-oh". |
| 5 | **Let's get into the tank!** | The hatch scene, with no caption yet: the latch knocks, steam hisses, the lid is flung open and she pops out on a spring. Once she has settled (1.9 s in), her line appears, and she blinks while it's up. When it's said, she **drops into the hatch** and the camera dives in after her. | Push in, punch in to her face, then the dive into black. | Latch, knocks, hiss, clang, pop; her line; duck and whoosh on the dive. |
| 6 | **We need to aim carefully.** | Fade up on the tank and the first outpost, with her at her post in the hatch. The barrel **searches**: up past the zombie (72°), down low (14°), back to rest. It never stops on the answer. | 1×, the round's own framing. | A servo whir per move. |
| 7 | **What angle will help us hit the target?** | The triangle draws itself: adjacent, opposite, hypotenuse, then the θ arc. **No measurements.** | Holds. | A rising blip per part. |
| 8 | **Trigonometric ratios connect the sides and angles.** | The sides light up one at a time in the storyboard's colours, each with its name on a tag: **Hypotenuse** (red), **Opposite** (yellow), **Adjacent** (blue). | Holds. | One note per side. |
| 9 | **Let's explore all six ratios to help us aim!** | The triangle holds with its named sides while she says the line, and **NEXT ▶** rises in the bottom-right corner 1.4 s in. The ratios themselves are left to the lesson. | Holds. | |

**NEXT ▶** clears the coloured sides and goes to the learning
section (the `openLesson` hook). When the learner comes back, she ducks in,
the hatch shuts, and round 1's normal briefing begins, this time with the
measurements.

Without voice-over, NEXT appears about **36 s** after START in English
(32.5 s with reduced motion, where the hatch is already open and she speaks
at once).

## 5. UX rules

- **One caption system** for the whole game. The story and the ending use the
  same parchment caption bar at the top. Beat 1 alone is a big centred title.
- **One narrator, with a face.** From beat 2 on, every caption carries the
  commander's portrait. The learner knows who is talking before she appears in
  beat 5. Once she's on screen she blinks every few seconds. Her mouth stays
  as drawn: a flapping mouth under the caption read as mumbling.
- **A line starts when its speaker can say it.** Every caption appears with
  its beat, except hers in beat 5, which waits until she is out of the hatch.
- **Pacing.** A line lasts as long as its voice-over plus 0.7 s. Without
  voice-over (no file, or sound muted) it lasts `max(3.2 s, 0.065 s ×
  characters)`, which is enough to read in any of the six languages. A beat
  also waits for its action: beats 1–3 for their camera moves (at least 3.8,
  4.8 and 5.6 s), beat 4 until 1.1 s after the tank arrives, beat 5 for her
  line and then the dive, and beats 6–8 for at least 2.8–3 s.
- **No skipping.** Every learner walks through all of it. There's no SKIP
  button, and tapping the screen or pressing Enter, Space or Esc doesn't
  advance a beat or cut one short. The same is true of the game's other
  scenes: the roll-in, the briefing, the hatch scene and the ending all play
  in full.
- **NEXT ▶ is the only way on.** It appears only on beat 9, bottom-right,
  where the storyboard and the commander scene put it. Enter or Space
  presses it.
- **Touch.** A held key doesn't repeat. After a tap that changes what's
  under the finger (a card rising, the hint table opening or closing),
  touches are ignored for 0.35 s, so a double-tap can't hit what appears in
  its place.
- **No text in any art.** Every word on screen is live text in the learner's
  language, including the SAFE ZONE sign.
- **Reduced motion:** no crane, glide, pan, push-in or dive zoom. Each beat
  cuts to its final framing, the dips to black stay as plain fades, and the
  zombies in the swamp don't sway. Everything else is the same.
- **Tone:** spooky-funny, never scary. The zombies are the game's goofy cast;
  there's nothing gory and no jump scares.

## 6. Barriers in the world

The story says "cross these barriers", so the barriers are now part of the
level, where the story shows them and where every round shows them again:

- **At every outpost:** two or three barriers (sandbags, hedgehogs, concrete
  blocks, barricades, barbed wire), each outpost a different mix.
- **At the gate:** a last line of three in front of the safe zone.

They stand on the ruins' ground line and always to a ruin's **right**. The
triangle, its measurement cards and the gun all live to the left, so a
barrier can never cover anything the learner needs. They are scenery: the
tank drives past them between rounds.

## 7. Decisions for the LXD to confirm

1. **"cosec" or "csc"?** Not shown in the story any more, but still in the
   game: its trig table says **csc θ**, while the NCERT Class 10 textbook
   writes **cosec θ**. We recommend switching the table and the lesson to
   **cosec θ**, so the game uses the learners' textbook notation.
2. **Side names in beat 8.** The storyboard only says "highlight the sides". We
   recommend naming them (Hypotenuse / Opposite / Adjacent) here, in the
   teaching moment. During gameplay the cards stay unnamed, so recognising the
   sides remains the learner's job.
3. **Night, not day.** The story is set at night to match the game. The
   storyboard frames are daytime.
4. **The game's own zombies.** Beat 2 shows only the cast the learner will
   actually fight, not the storyboard's realistic ones.
5. **One narrator.** We recommend that the commander voices all nine lines and
   both ending lines.
6. **Every launch, or first launch only?** As built, it plays in full on
   every launch, about 36 s, with no way to skip it. If the platform
   remembers learners, later launches could start on beat 9.
7. **The barrel in beat 6 searches but never settles on the answer**, so the
   story can't give the angle away.

## 8. Assets

**Everything the story shows is the game's own art.** That includes the swamp
and mist plates, ruins, tank sheet, the three zombie sheets, the commander, and
the safe zone compound and gate. The only new image it needed is the barrier
set:

| Asset | Status | File |
|---|---|---|
| Barrier set (five side-view props) | **live** | `art-src/STbarriers.webp` → `assets/world_barriers.webp` (`tools/fit_assets.py barriers`) |
| Commander: blink | **live** | `art-src/commander_blink.webp` → `assets/commander_face.webp` (`tools/fit_assets.py face`) |
| Commander: talking | made, **not used** (read as mumbling) | `art-src/commander_talk.webp` |
| Commander: thumbs-up | *optional*, not made | STORY_ART_PROMPTS.md §1c |
| Voice-over, 11 lines × 6 languages | draft installed, plays only with `?vo=draft` | STORY_VO.md |

**Retired:** `art-src/ST1.webp`, `ST2.webp`, `ST3.webp`, `STfg.webp`,
`STtank.webp` and `STzombies.webp`. Nothing loads them any more and their
`assets/story*.webp` cuts are deleted. They can be kept as concept art or
deleted.

**Not needed:** new zombie types. The story deliberately shows only the cast
the learner fights. A new type would have to join the rounds too, with a full
animated sprite sheet, or the story would be making a promise the game
doesn't keep.

## 9. How it's built

- A **STORY** state between the title and round 1, run from one data table,
  `STORY_BEATS` in `index.html`. Each row holds the caption key, the camera
  move or action, and a minimum length, so retuning the story means editing
  that table.
- **One clock per beat.** Every cue fires when the clock steps over its time,
  so a jump of the clock (a preview starting mid-beat) drops the cues it
  passes instead of playing them all at once. `settleBeat` puts a beat at its
  final frame as the next one begins, and it's also what
  `#previewstory3`-style previews start from.
- **Reused, not rebuilt:** beat 4 is the game's intro drive, beat 5 is the
  hatch scene with a dive added, and beats 7–8 are the briefing's triangle
  with a colour-and-name pass. The zombies standing between the outposts
  are drawn by the game's own zombie code.
- **Analytics:** the story reports `screen: story` when it starts, and
  `screen: intro` while the tank rolls up (XAPI_EVENTS.md).
- **Her blink** is an overlay on her bust (`CMDR_FACE`): the shut eyes, cut
  by `tools/fit_assets.py face` from the blink edit. `commanderBlinking()`
  decides when it shows.
- **Checked:** a scripted run from START to the first AIM (NEXT at 35.65 s, 0
  errors), and the reduced-motion run (NEXT at 32.45 s, 0 errors). A run that
  taps the screen and presses Enter, Space and Esc every quarter-second
  through the story, the briefing, the drive to round 2 and the ending gives
  exactly the same timings as a run with no input. Earlier builds also had
  screenshots of every beat in English and of her blinking in the close-up,
  and the title and the longest captions in the other five languages.
