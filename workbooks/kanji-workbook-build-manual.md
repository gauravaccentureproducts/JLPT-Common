# JLPT Kanji "Adventure" Workbook — Build Manual (Level-Agnostic)

How to build the **kanji** edition for any level (N5 → N1). Read
**`00-common-workbook-pipeline.md`** first (shared 6"×9" KDP pipeline, render, openers, typography,
extraction-artifact discipline, QA, environment). This manual covers what is **kanji-specific**.

> ✅ **Build #1 shipped: *My N4 Kanji Adventure* (143 kanji, 12 worlds, 53 pages, 2026-06).** Values it
> confirmed are tagged **[v1-confirmed]** below, and the v0 open questions (§8) are now resolved. The
> data + assets came entirely from the existing N4 app (no network). The grammar and vocabulary editions
> remain the references for shared mechanics.

---

## 1. The content unit — a kanji card

One record per kanji in `_<lvl>_kanji_full.json`, keyed by `char`:

```json
{
  "id": "...", "char": "持", "categoryOrder": 4,
  "meaning": "hold; have",                       // English keyword(s), keyword first
  "on":  ["ジ"],                                  // on'yomi in KATAKANA
  "kun": ["も.つ"],                                // kun'yomi in HIRAGANA, '.' marks the okurigana split
  "strokes": 9,
  "radical": "扌 (て・hand)",                       // radical + its name/meaning
  "components": ["扌", "寺"],                       // optional: mnemonic component breakdown
  "examples": [                                   // 2–3 compound words, at/under level
    { "word": "持つ",   "reading": "もつ",   "en": "to hold" },
    { "word": "気持ち", "reading": "きもち", "en": "feeling" }
  ],
  "strokeOrderSvg": "kanjivg/06301.svg"            // path to the numbered stroke-order asset (§3)
}
```

**Card anatomy:** the **kanji** (very large) · **on'yomi** (katakana) and **kun'yomi** (hiragana, with
okurigana shown after `・` or a dot) · **English keyword(s)** · **radical + components** · **stroke
count** · a **stroke-order diagram** (numbered) · **2–3 example compounds** (word + reading + EN) · a
**writing-practice grid**.

**Density [v1-confirmed]: 6 kanji per 6×9 page (2×3).** Build #1 first tried 4/page and each card had a
large empty middle; the fix was to let the **writing-practice grid fill the card body**
(`justify-content:space-evenly` over multiple rows) and pack 6/page. A kanji book is mostly writing
practice — don't leave a void. (143 kanji → 53 pages incl. front/back matter.)

**Reading discipline (kanji's #1 risk, mirrors vocab readings):** on'yomi in **katakana**, kun'yomi in
**hiragana**, okurigana split marked (`も.つ`, `あ.がる`). Show only the level-relevant readings; a kanji
can have many — curating to the readings the learner needs is an editorial decision, not a dump.

---

## 2. Writing-practice grid (the kanji-only component)

The feature a grammar/vocab book never has. Per kanji, a row of **square cells with a faint cross/quad
guide** (the 田-style grid that teaches proportion):
- **Cell 1–2:** the kanji **traced** in a pale grey (the learner traces over it).
- **Remaining cells:** empty guide squares for free writing.
- Optionally a first cell showing the **numbered stroke order** at writing size.

Build the grid in CSS (a flex/grid row of fixed-size bordered squares with a `::before` cross-hair) so
it scales cleanly and prints crisp — do **not** rasterise it. Keep the guide lines very light so they
don't dominate the printed page. Verify the grid doesn't overflow the page bottom (common §9,
`overflow:hidden` backstop).

---

## 3. Stroke-order diagrams — the main new production task

**[v1-confirmed] — KanjiVG gives three things for free; don't recompute any of them.** The level app
already ships KanjiVG SVGs at `<lvl>/svg/kanji/<glyph>.svg` (CC-BY-SA — credit on the copyright page):

- **The numbered diagram itself.** Each SVG already contains a `<g id="kvg:StrokeNumbers_…">` group of
  positioned `<text>` numbers, so you **inline the SVG verbatim** and get a numbered, vector, any-DPI
  diagram with **zero generation**. Only work: recolour the stroke paths (`stroke:#000000` → ink), size
  to fit the card. Internal IDs are per-glyph hex (`kvg:0540c…`), so inlining 100+ causes no ID clashes.
- **Stroke count** = `len(re.findall(r"<path[^>]*kvg:type", svg))` (one path per stroke) — derive it.
- **Radical** = the `<g>` carrying a `kvg:radical` attribute → its `kvg:element` (prefer `tradit` →
  `general` → `nelson`). E.g. 同 → 口.

So the v0 "build a numbered-diagram helper" task evaporates — KanjiVG is pre-numbered. Spot-check one
**high-stroke** page (11–13 strokes) to confirm legibility at print size. (No font-glyph or raster
"stroke order" hacks — they look poor at print size.)

---

## 4. World taxonomy (kanji)

~N kanji ÷ ~12–18 worlds. Two viable groupings (pick one, keep it uniform):
- **By radical / component family** (teaches the system: water 氵 world, hand 扌 world, person 亻 world…).
- **By theme / frequency tier** (Numbers & Time, Nature, People & Body, School, …), which aligns with
  the vocab worlds and lets a series share world names.
Same tuple structure as grammar/vocab; the world name must fit **all** its kanji. Stamp `categoryOrder`
from the taxonomy. Per-level **kanji list** comes from the official-ish source (Tanos/JLPT lists);
de-dupe against lower levels (a kanji is taught once, at its lowest level).

---

## 5. Kanji exercises

Per world, after its kanji cards:
- **Reading** — given the kanji/compound, write the **kana reading** (the core skill).
- **Writing** — given the meaning + reading (or an English keyword), write the **kanji**; a guide square
  is provided.
- **Compound building / matching** — match a kanji to a compound it forms, or assemble a compound from
  two taught kanji.
- **Radical/meaning matching ("draw a line")** — reuse the shared deranged dot-matching component
  (grammar manual §5): one line per item + its dot, uniquely matchable, deranged shuffle.
- **Answer key** per world (back matter). Build banks from the world's kanji so the "answer-in-bank"
  check holds.

---

## 6. Build procedure

1. **Assemble the level's kanji list** → `_<lvl>_kanji_full.json`; de-dupe against lower levels.
2. **Populate each record:** meaning keyword(s), curated on/kun readings, stroke count, radical +
   components, 2–3 at-level example compounds (with readings + EN), and the stroke-order asset path.
   Hand-verify readings, stroke counts, and that example compounds are at/under level.
3. **Wire stroke-order SVGs** (§3) + the writing grid (§2).
4. **Define the taxonomy** (§4).
5. **Build the HTML** (a `_<lvl>_kanji_build.py`, modelled on `_wbv_workbook.py`); confirm kanji count =
   list size.
6. **Render** the 6×9 600-DPI PDF (common §4) — verify stroke diagrams stay vector/crisp.
7. **Verify** (common §9): montage **all** card pages (stroke diagram present + correct count, grid not
   clipped) and **all** exercises; spot-check the densest pages.
8. **Review loop** (§7) to zero; **stamp + keep-latest** (common §11).

---

## 7. Review loop & recurring kanji defect classes

Keep an `<Level> kanji Book review Prompt.txt`. Pass order: programmatic scans (stroke-count vs diagram;
on=katakana / kun=hiragana; example readings present; level-scope of example compounds) → content read
of every kanji (readings, meaning, radical, examples) → layout montage of all card + exercise pages.

**Recurring kanji defect classes (re-check the whole book each pass):**
1. **Wrong/extra/missing reading**; on'yomi written in hiragana or kun'yomi in katakana; okurigana split
   wrong (も.つ).
2. **Stroke count ≠ diagram**, or wrong **stroke order** in the asset.
3. **Wrong radical / component** breakdown.
4. **Circular example** — the "example word" is just the bare kanji (a kun-fallback where the kun has no
   okurigana, e.g. 京→京, 心→心) — or a **missing example**; also a compound above level, wrong reading,
   or one that doesn't use the kanji. *(Build #1's dominant finding: 30 circular + 8 missing; the review
   scan flags `example.word == char`, fixed with hand-authored compounds — native-review those.)*
5. **Writing grid** overflow / guide lines too heavy / traced glyph misaligned in the square.
6. **Stroke-order numbering** illegible or overlapping the kanji at print size.
7. **Matching** not uniquely solvable.
8. **Licence/attribution** for stroke-order data missing on the copyright page.
9. **Extraction artifacts mistaken for defects** (common §8).
10. Process: fixed one kanji but not its siblings; declared done with a check failing.

---

## 8. Build-#1 decisions [v1-confirmed]

The v0 open questions, resolved by *My N4 Kanji Adventure*:
- **Cards-per-page: 6 (2×3).** Stroke diagram sits **inline on the card** (top-right); the writing grid
  fills the card body (§1–2).
- **Taxonomy axis: learning-order "journey" stages** for v1 — chunk `lesson_order`/`frequency_rank` into
  ~12 named worlds. Radical-family / semantic-theme grouping is a richer v2 axis but needs more
  authoring — deferred (§4).
- **Stroke-order source: KanjiVG** from the app repo; diagrams are pre-numbered (§3); credit CC-BY-SA.
- **Readings: the curated app `kanji.json` set** (on=katakana, kun=hiragana) — not a comprehensive dump.
- **Cross-link kanji ↔ vocabulary: YES** — examples mined from the reviewed vocab (~94% at N4); the gap
  filled with hand-authored compounds (native-review them) (§5).
- **Data pipeline:** `_kanji_assemble.py` merges app `kanji.json` + KanjiVG + vocab → `_kanji_full.json`;
  a `_kanji_review_scan.py` (objective flags) + `_kanji_review_export.py` (DOCX/CSV/MD for reviewers)
  complete the loop. Render with **absolute paths** (relative paths break `_print2x`'s file URI).

---

*Kanji-specific addendum to the common pipeline — extrapolated from the grammar/vocab editions and
standard kanji pedagogy. Replace the v0 assumptions with confirmed values after the first real build,
and add new kanji defect classes here as they surface.*
