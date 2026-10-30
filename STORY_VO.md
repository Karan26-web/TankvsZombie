# Story Intro — Voice-Over Script

> **STATUS** (2026-10-30). A **synthetic draft** of all 60 files is installed
> in `assets/vo/<lang>/`. The original pack is kept at
> `art-src/vo/Tank_vs_Zombie_66_Story_VO_DRAFT.zip`; its six `story_05` files
> are left out of `assets/`, since beat 5's line is cut. It isn't good enough to
> ship (§5), so the game plays it only when the URL asks for it:
> `index.html?vo=draft`. Without that, every line holds for its reading time.
> When reviewed recordings replace the drafts at the same paths, switch them on
> in `index.html` (§5).

Ten lines: the story's eight (design in [STORY_INTRO.md](STORY_INTRO.md); beat 5
has no line any more) and the two the safe-zone ending already shows as
captions. Each line is spoken
exactly as it appears on screen, in all six of the game's languages.

The on-screen captions use these same texts, from `i18n/strings.json`, so the
voice and the caption can never disagree.

**Translations need a native speaker's review before recording.** They follow
the polite register the rest of the game uses.

---

## 1. The voice

**One narrator for everything: the commander** — the young woman in the tank
hatch. She is the learner's teammate, and she says "we" because she means it.

- Early twenties, warm, brave and encouraging, a little playful. A big sister
  on a mission, not a drill sergeant.
- Clear and unhurried, about 130–140 words a minute, for 10–15-year-olds.
- Energy by line:

| # | Line | Read it… |
|---|---|---|
| 1 | Welcome to Zombie Land! | with wonder, a storyteller opening the book (on screen it's the big title) |
| 2 | There are zombies everywhere! | alarmed but fun, a half-laugh |
| 3 | We need to cross these barriers and reach the safe zone. | determined, laying out the plan |
| 4 | But first, we need to clear the way! | urgent, rising |
| 6 | We need to aim carefully. | calm, focused, a little quieter |
| 7 | What angle will help us hit the target? | a real question, curious, inviting an answer |
| 8 | Trigonometric ratios connect the sides and angles. | explaining, clear on every word |
| 9 | Let's explore all six ratios to help us aim! | inviting, bright, the hand-off |
| E1 | The path is clear. Let's head in! | relieved, upbeat |
| E2 | We made it to the safe zone! | triumphant, celebrating |

## 2. Audio specs

- **Files:** `assets/vo/<lang>/story_01.mp3` … `story_09.mp3` (no `story_05`:
  the files keep their beat's number), `end_01.mp3` and `end_02.mp3`, with
  `<lang>` one of `en hi mr te or gu`. That's 60 files.
- **Format:** mono, 44.1 kHz, MP3 at 128 kbps.
- **Level:** −16 LUFS integrated, peaks no higher than −1 dBTP, matched across
  all lines and languages.
- **Edit:** trim to 80 ms of silence at the head and tail; no music or effects
  (the game adds those).
- **Length:** ideally under 5 s per line. The beat waits for the line (plus
  0.7 s), so a long read slows the story down. Beats 1–3 hold for at least
  3.8, 4.8 and 5.6 s anyway for their camera moves, so lines up to about that
  length cost nothing there.
- **Same voice in every language** if your TTS has one multilingual voice. If
  not, or if you record people, cast one voice per language matched to the
  character.

Whatever is missing still plays: a line with no file, or with sound muted,
holds for its reading time instead.

---

## 3. The lines

### story_01 — Welcome to Zombie Land!

| lang | text |
|---|---|
| en | Welcome to Zombie Land! |
| hi | ज़ॉम्बी लैंड में आपका स्वागत है! |
| mr | झोंबी लँडमध्ये तुमचे स्वागत आहे! |
| te | జాంబీ ల్యాండ్‌కు స్వాగతం! |
| or | ଜୋମ୍ବି ଲ୍ୟାଣ୍ଡକୁ ସ୍ୱାଗତ! |
| gu | ઝોમ્બી લેન્ડમાં તમારું સ્વાગત છે! |

### story_02 — There are zombies everywhere!

| lang | text |
|---|---|
| en | There are zombies everywhere! |
| hi | हर तरफ़ ज़ॉम्बी ही ज़ॉम्बी हैं! |
| mr | सगळीकडे झोंबीच झोंबी आहेत! |
| te | ఎక్కడ చూసినా జాంబీలే! |
| or | ସବୁଆଡ଼େ ଜୋମ୍ବି ହିଁ ଜୋମ୍ବି! |
| gu | બધે જ ઝોમ્બી જ ઝોમ્બી છે! |

### story_03 — We need to cross these barriers and reach the safe zone.

| lang | text |
|---|---|
| en | We need to cross these barriers and reach the safe zone. |
| hi | हमें ये रुकावटें पार करके सुरक्षित क्षेत्र तक पहुँचना है। |
| mr | आपल्याला हे अडथळे पार करून सुरक्षित क्षेत्रापर्यंत पोहोचायचे आहे. |
| te | మనం ఈ అడ్డంకులను దాటి సురక్షిత ప్రాంతానికి చేరుకోవాలి. |
| or | ଆମକୁ ଏହି ବାଧାଗୁଡ଼ିକ ପାର କରି ସୁରକ୍ଷିତ ଅଞ୍ଚଳରେ ପହଞ୍ଚିବାକୁ ହେବ। |
| gu | આપણે આ અવરોધો પાર કરીને સુરક્ષિત વિસ્તાર સુધી પહોંચવાનું છે. |

### story_04 — But first, we need to clear the way!

| lang | text |
|---|---|
| en | But first, we need to clear the way! |
| hi | लेकिन पहले, हमें रास्ता साफ़ करना होगा! |
| mr | पण आधी, आपल्याला रस्ता मोकळा करावा लागेल! |
| te | కానీ ముందు, మనం దారిని సుగమం చేయాలి! |
| or | କିନ୍ତୁ ପ୍ରଥମେ, ଆମକୁ ରାସ୍ତା ସଫା କରିବାକୁ ହେବ! |
| gu | પણ પહેલાં, આપણે રસ્તો સાફ કરવો પડશે! |

### story_06 — We need to aim carefully.

| lang | text |
|---|---|
| en | We need to aim carefully. |
| hi | हमें ध्यान से निशाना लगाना होगा। |
| mr | आपल्याला काळजीपूर्वक नेम धरावा लागेल. |
| te | మనం జాగ్రత్తగా గురి పెట్టాలి. |
| or | ଆମକୁ ସାବଧାନତାର ସହ ଲକ୍ଷ୍ୟ କରିବାକୁ ହେବ। |
| gu | આપણે ધ્યાનથી નિશાન તાકવું પડશે. |

### story_07 — What angle will help us hit the target?

| lang | text |
|---|---|
| en | What angle will help us hit the target? |
| hi | कौन-सा कोण हमें निशाने पर वार करने में मदद करेगा? |
| mr | कोणता कोन आपल्याला लक्ष्यावर नेम साधायला मदत करेल? |
| te | ఏ కోణం మనకు లక్ష్యాన్ని తాకడానికి సహాయపడుతుంది? |
| or | କେଉଁ କୋଣ ଆମକୁ ଲକ୍ଷ୍ୟ ଭେଦ କରିବାରେ ସାହାଯ୍ୟ କରିବ? |
| gu | કયો ખૂણો આપણને નિશાન પર વાર કરવામાં મદદ કરશે? |

### story_08 — Trigonometric ratios connect the sides and angles.

| lang | text |
|---|---|
| en | Trigonometric ratios connect the sides and angles. |
| hi | त्रिकोणमितीय अनुपात भुजाओं और कोणों को जोड़ते हैं। |
| mr | त्रिकोणमितीय गुणोत्तरे बाजू आणि कोन यांना जोडतात. |
| te | త్రికోణమితి నిష్పత్తులు భుజాలను, కోణాలను కలుపుతాయి. |
| or | ତ୍ରିକୋଣମିତି ଅନୁପାତ ବାହୁ ଓ କୋଣକୁ ଯୋଡ଼େ। |
| gu | ત્રિકોણમિતીય ગુણોત્તરો બાજુઓ અને ખૂણાઓને જોડે છે. |

### story_09 — Let's explore all six ratios to help us aim!

| lang | text |
|---|---|
| en | Let's explore all six ratios to help us aim! |
| hi | चलिए, निशाना लगाने के लिए सभी छह अनुपातों को समझते हैं! |
| mr | चला, नेम धरण्यासाठी सहाही गुणोत्तरे समजून घेऊया! |
| te | గురి పెట్టడానికి ఆరు నిష్పత్తులనూ తెలుసుకుందాం! |
| or | ଚାଲନ୍ତୁ, ଲକ୍ଷ୍ୟ କରିବା ପାଇଁ ସବୁ ଛଅଟି ଅନୁପାତ ଜାଣିବା! |
| gu | ચાલો, નિશાન તાકવા માટે છએ છ ગુણોત્તરો શીખીએ! |

### end_01 — The path is clear. Let's head in! *(already in the game as a caption)*

| lang | text |
|---|---|
| en | The path is clear. Let's head in! |
| hi | रास्ता साफ़ है। चलिए, अंदर चलते हैं! |
| mr | रस्ता मोकळा आहे. चला, आत जाऊया! |
| te | దారి స్పష్టంగా ఉంది. పదండి, లోపలికి వెళ్దాం! |
| or | ରାସ୍ତା ସଫା ଅଛି। ଚାଲନ୍ତୁ, ଭିତରକୁ ଯିବା! |
| gu | રસ્તો સાફ છે. ચાલો, અંદર જઈએ! |

### end_02 — We made it to the safe zone! *(already in the game as a caption)*

| lang | text |
|---|---|
| en | We made it to the safe zone! |
| hi | हम सुरक्षित क्षेत्र में पहुँच गए! |
| mr | आपण सुरक्षित क्षेत्रात पोहोचलो! |
| te | మనం సురక్షిత ప్రాంతానికి చేరుకున్నాం! |
| or | ଆମେ ସୁରକ୍ଷିତ ଅଞ୍ଚଳରେ ପହଞ୍ଚିଗଲୁ! |
| gu | આપણે સુરક્ષિત વિસ્તારમાં પહોંચી ગયા! |

---

## 4. Not spoken, only shown

Beat 8 labels the sides. These are on-screen labels, not lines.

- **Side names:** Hypotenuse, Opposite, Adjacent. These reuse the game's existing
  translations of these words.

---

## 5. The installed draft, and replacing it

The draft pack's own README says it is a set of preview tracks, not a
finished recording:

- The voices are synthetic and robotic. None of them is the warm, confident
  commander described in §1.
- **Marathi** is read by a Hindi voice.
- **Odia** was transliterated into Bengali script and read by a Bengali voice.
- **Telugu** and **Gujarati** use experimental voices.

The files are mono, 44.1 kHz, 128 kbps MP3, as §2 asks, and the pack says
they're normalised to −16 LUFS. They're useful for checking timing. In the
draft, every line is under 5 s except `story_03` (5.2–6.2 s in the five Indian
languages) and the Odia `story_01` (5.7 s). Both are acceptable: they stretch
beat 3 to at most 6.9 s (its minimum is 5.6 s) and the Odia beat 1 to 6.4 s
(from 3.8 s).

**To replace them:** have each language's lines reviewed by a native speaker
(§3), record them, and save them over the drafts at the same paths. Then, in
`index.html`, change

```js
const VO_LANGS = QS.get('vo')==='draft' ? LANGS : [];
```

to list the languages that now have real recordings, e.g.
`const VO_LANGS = ['en', 'hi'];`, or `LANGS` once all six are done. A language
left off the list keeps its timed captions.
