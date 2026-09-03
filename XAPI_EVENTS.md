# SwiftPAL games — outbound event spec (xAPI style)

Every analytics event is one statement `{ verb, object, result, context }`, dispatched through the
**platform bridge** (`swiftpal-bridge.js`, shipped in every game):

```js
SwiftPAL.sendEvent(statement)   // routes to Android / iOS / web / electron automatically
```

On web the bridge delivers it as `postMessage({ source:"swiftpal", fn:"sendEvent", args:[jsonString] })`.
If the bridge is absent (standalone dev), the game falls back to
`postMessage({ type:"swiftpal:xapi", statement })`. The game's internal bus is named `GameBus`
(`window.GameBus`) so the global `SwiftPAL` name belongs to the bridge.

`verb` is the event name. `object` = what was acted on. `result` / `context` are optional-by-verb.
**Every game (book) emits the same 7 verbs** — the per-template variety lives inside `context.template`, never in new event names.

## Verbs

| verb | when | object | result |
|---|---|---|---|
| `activity_launched` | child taps शुरू करें on the start screen | `{type:"activity", id:<skill_code>}` | — |
| `screen_viewed` | a passive screen mounts (tutorial demo, meet, celebration) | `{type:"screen", id:<slide_id>}` | — |
| `question_started` | an answerable screen mounts | `{type:"question", id:<slide_id>}` | — |
| `question_answered` | every answer tap, right or wrong | option detail (below) | `{score:1\|0, attempt:n, is_correct:bool}` |
| `hint_used` | hint bulb tapped | `{type:"hint", id:"bulb"}` | — |
| `audio_replayed` | any replay chip tapped | `{type:"audio", id:<chip>}` | — |
| `activity_completed` | **only** when the child taps आगे बढ़ें on the celebration screen | `{type:"activity", id:<skill_code>}` | see below |

## `question_answered` object

```json
{ "type": "text" | "image", "id": "opt_2", "text": "क्या", "mediaUrl": "assets/Images/obj_x.png" | null,
  "ui_index": 2, "original_index": 0 }
```
`ui_index` = position shown after shuffle; `original_index` = position authored in the card.
`result.score` is 1 only on a first-attempt correct; `attempt` counts taps on this question.

## `activity_completed` result — answers to the open questions

```json
{ "completed": true, "progress": 100, "score": 0.78, "duration_ms": 184032 }
```
- `completed` is **always `true`** and `progress` is **always `100`** — the event exists only at the
  end and only on the button tap. There is no partial-completion variant of this event.
- It **no longer fires when the celebration screen appears** — a host that redirects on
  `activity_completed` will always let the child see the celebration and choose to move on.
- `score` = first-try accuracy across all answered questions (0–1, 2dp). It is **not** always 1.

## context (on every statement)

```json
{ "skill_code": "HI01H04_L02_S02", "lo_code": "HI01H04_L02", "medium": "hi", "session_ms": 9249,
  "question_id": "P2", "question_index": 10, "template": "ODD_ONE_OUT", "question_format": "mcq",
  "phase": "practice", "context_id": "...", "journey_id": "..." }
```
- `skill_code` is the **stable content id** of the book — it never changes per journey, so reusing the
  book elsewhere cannot conflict. The journey binding is the **host's**: launch the game with
  `?context_id=...&journey_id=...` (and optionally `&medium=`) and those values are echoed into every
  statement's context.
- `question_format` values: `mcq`, `timed_mcq`, `build`, `drag`, `tap_count`. `template` is the exact
  screen template (e.g. `TAP_LETTER_BY_SOUND`) for finer analysis.

## Noise control

The old raw `swiftpal:signal` firehose (30+ internal signal names) is now **dev-only** (`?dev=1`).
Production hosts receive only the 7 verbs above, identically shaped from every book.
`swiftpal:proceed` (existing next-module message) still fires after `activity_completed` for backward
compatibility; `swiftpal:lesson_complete` (validator report) also moved to the button tap.

---

# How **Tank vs Zombie — Angle Academy** binds to the spec

The seven verbs are emitted from `index.html` by `window.GameBus`. `SwiftPAL.sendEvent` is used
whenever the bridge is present; the `swiftpal:xapi` postMessage is the standalone-dev fallback.

| verb | this book's trigger | object |
|---|---|---|
| `activity_launched` | **PLAY GAME** on the title plate (and **PLAY AGAIN**, which is a second run) | `{type:"activity", id:"MA10T01_L01_S01"}` |
| `screen_viewed` | title plate (`start`), the tank's roll-in (`intro`), the win card (`celebration`), the out-of-shells card (`game_over`) | `{type:"screen", id:…}` |
| `question_started` | a round's briefing begins — the triangle starts drawing itself | `{type:"question", id:"L1"…"L5"}` |
| `question_answered` | every shell resolves, hit or miss | the angle the dial was holding (below) |
| `hint_used` | the bulb opens the trig sheet (`bulb`), **SHOW ME THE ANGLE** lights the cell (`bulb_reveal`) | `{type:"hint", id:…}` |
| `audio_replayed` | the restart key replays the round's briefing and its cue track | `{type:"audio", id:"briefing"}` |
| `activity_completed` | **CONTINUE** on the win card — nothing else | `{type:"activity", id:"MA10T01_L01_S01"}` |

**`question_answered` object.** The dial is a five-option MCQ over `[0, 30, 45, 60, 90]` and is never
shuffled, so `ui_index` and `original_index` are always the same index:

```json
{ "type":"text", "id":"opt_1", "text":"30°", "mediaUrl":null, "ui_index":1, "original_index":1 }
```

`result.attempt` is the shell count on this round; `result.score` is 1 only when a first shell hits.

**context.** `template` is `SOLVE_ANGLE_SIN` / `_COS` / `_TAN` — the ratio the round asks for, which is
what separates the five rounds; `question_format` is always `mcq` and `phase` is `practice` on every
question-bearing statement (`intro` on the launch and the roll-in, `outro` on the two end cards).
`question_id` is `L1`…`L5` and `question_index` is the round's 0-based position.

**`skill_code`** defaults to `MA10T01_L01_S01` (`lo_code` `MA10T01_L01`) and is overridable with
`?skill_code=` / `?lo_code=`. `?context_id=` and `?journey_id=` are echoed into every statement.

**Completion.** `result.score` is first-try accuracy across the rounds actually answered — a round
replayed after an out-of-shells card is counted once, on its latest run. A child who never taps
CONTINUE never reports completion, by design. `swiftpal:lesson_complete` (a per-question report) and
`swiftpal:proceed` follow the verb, in that order, on the same tap.

**Noise control.** `GameBus.signal()` posts `swiftpal:signal` only under `?dev=1`. A production host
sees the seven verbs and nothing else.

## Language

Screen text lives in [`i18n/strings.json`](i18n/strings.json), keyed by its English source line, in
**en, hi, mr, te, or, gu**. `?lan=gu` picks the language (`?lang=` is accepted too, and `?medium=` is
honoured last, so a host that only sets the medium still gets the right script). An unknown code
falls back to English, as does a failure to fetch the file — the keys are the English lines.
`context.medium` follows `?medium=` when the host sets it, and the display language otherwise.

Two strings are painted into the artwork rather than drawn as text and so stay English in every
language: the **TANK VS ZOMBIE** wordmark on the title plate and the **FIRE** label on the fire key.
Both need new art to localise. `sin`/`cos`/`tan`, θ, the degree sign and the trig table's own values
are mathematical notation and are deliberately left alone.
