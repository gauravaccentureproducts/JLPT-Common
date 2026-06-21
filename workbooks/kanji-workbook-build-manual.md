# JLPT Kanji "Adventure" Workbook — Build Manual (Level-Agnostic)

How to build the **kanji** edition for any level (N5 → N1). Read
**`00-common-workbook-pipeline.md`** first (shared 6"×9" KDP pipeline, render, openers, typography,
extraction-artifact discipline, QA, environment). This manual covers what is **kanji-specific**.

> ⚠️ **No kanji edition has shipped yet.** This manual extrapolates the *proven* shared infrastructure
> (which transfers directly) plus standard kanji-workbook pedagogy. Treat the content-model and asset
> sections as a v0 to validate on the first build; promote a parameter to a constant only once a real
> edition confirms it. The grammar and vocabulary editions are the proven references for everything
> shared.

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

**Density:** kanji cards are far richer than vocab cards (stroke diagram + practice grid), so plan
**1–2 kanji per page** (e.g. info block on top, a full practice row beneath), not a 6-up grid. Expect
more pages per word than vocab — size the per-page packing to land a sensible page count for the level.

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

This is the genuinely new asset (vocab/grammar had only the mascot raster). Options, best first:
- **KanjiVG** (`kanjivg` project, CC-BY-SA) — per-kanji SVGs with stroke paths in order; render each
  with **numbered strokes** (number each `<path>` by its document order, place the index near the
  stroke's start point). SVG ⇒ **vector, crisp at any DPI** and small. **Check the licence/attribution**
  and add the required credit to the copyright page.
- Generate the numbered diagram **at build time** from the SVG (a helper that reads the stroke paths and
  emits a labelled SVG inline into the HTML) so it stays vector through the 600-DPI render.
- Avoid font-glyph "stroke order" hacks and low-res raster diagrams — they look poor at print size.

**Gate stroke data:** the diagram's stroke count must equal the card's `strokes` field; mismatch = a
data or asset error. Spot-check a sample of rendered diagrams visually (stroke numbering legible, no
overlap with the kanji).

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
4. **Example compound above level**, wrong reading, or doesn't actually use the headword kanji.
5. **Writing grid** overflow / guide lines too heavy / traced glyph misaligned in the square.
6. **Stroke-order numbering** illegible or overlapping the kanji at print size.
7. **Matching** not uniquely solvable.
8. **Licence/attribution** for stroke-order data missing on the copyright page.
9. **Extraction artifacts mistaken for defects** (common §8).
10. Process: fixed one kanji but not its siblings; declared done with a check failing.

---

## 8. Open questions to settle on the first kanji edition

- Final **cards-per-page** and whether the stroke diagram sits inline on the card or in a dedicated
  practice strip.
- **Taxonomy axis** (radical-family vs theme) — theme aligns the series; radical teaches the system.
- Stroke-order **source + licence** (KanjiVG vs alternative) and the build-time numbering helper.
- How many **readings per kanji** to show at each level (curated vs comprehensive).
- Whether to cross-link kanji ↔ the vocabulary edition (shared example words).

Resolve these on build #1, then record the decisions here and promote the confirmed values into the
per-level parameter table (common §10).

---

*Kanji-specific addendum to the common pipeline — extrapolated from the grammar/vocab editions and
standard kanji pedagogy. Replace the v0 assumptions with confirmed values after the first real build,
and add new kanji defect classes here as they surface.*
