# JLPT "Adventure" Workbooks — Common Build Pipeline (Level- & Type-Agnostic)

The shared foundation for every printable JLPT **Adventure** workbook — **grammar**, **vocabulary**,
and **kanji** — at **any level (N5 → N1)**. The three content-type manuals in this folder
(`grammar-workbook-build-manual.md`, `vocabulary-workbook-build-manual.md`,
`kanji-workbook-build-manual.md`) cover only what is *unique* to their content unit; everything
common — page geometry, design system, render pipeline, QA method, environment gotchas — lives here.

> Reference implementations: *My N4 Grammar Adventure* (128 gems / 18 worlds) and *My N4 Vocabulary
> Adventure* (682 words / 19 worlds). Every level- or count-specific number is a **parameter**, not a
> constant — see §10.

---

## 1. The product & house style

A single body of content, shipped as a **print-ready PDF** plus its build sources. Tone: warm,
child-friendly but not babyish (pitch to the level's typical reader — see §10); a **Shiba mascot
("Bunpo-chan")** gives encouragement. Each learning unit is a collectible **"gem."** Gems are grouped
into themed **"worlds"** with playful adventure names.

**Book spine (same order for all three types):**
- **Front matter:** cover · copyright/credits · How to Use This Book · Table of Contents · Adventure Map.
- **Per world:** world opener (a "collect the gems" checklist) → content pages (one-per-page for grammar,
  card-grids for vocab/kanji) → Practice → Review.
- **Back matter:** Progress Tracker · Answer Key · reference list/index · certificate · back cover.

**House style (hold these across the whole series):**
- **British English** (colour/favour/realise/programme/holidays) — pick once, never drift.
- **ASCII-clean punctuation** in learner text (no smart-quotes, em-dashes, ellipses) for uniformity.
- **No added gender** the Japanese doesn't specify. `あの人`/omitted subject → "they"/neutral, never
  "he/she"; `おばあさん→her`, `弟→him` are fine because the JP specifies.
- **Co-authors / branding** are constants set once in the builder.

---

## 2. Format & page geometry (CURRENT: 6"×9" KDP)

The series ships as **Amazon KDP trade paperback, 6" × 9" (152.4 × 228.6 mm)**.

- `@page{ size:6in 9in; margin:0; }` and `.page{ width:6in; height:9in; overflow:hidden;
  padding:13mm 12mm 15mm; display:flex; flex-direction:column; }`
- **Full-bleed cream background** so trimming leaves no white edge.
- **`overflow:hidden` on every `.page`** is the backstop against any element overflowing the trim.
- `print-color-adjust:exact` on `html` so background tints/chips print.

> **History (do not reintroduce):** the first drafts were A5 with a 2-up A4 imposition step
> (`_wb_impose_2up.py`) and an even-page-count rule. The series was re-trimmed to **6"×9" KDP**; the
> user rejected A5. **KDP prints single pages — there is no 2-up step and no even-count requirement.**
> If you find references to A5 / 2-up / `impose`, they are superseded.

---

## 3. Content source = one canonical JSON (the source of truth)

Each workbook's content lives in **one JSON file**, one record per gem, keyed by a stable headword/id.
The builder loads it directly and is the *only* place content is authored or corrected.

- Grammar: `_wb_entries.json` · Vocabulary: `_n4_vocab_full.json` · Kanji: `_<lvl>_kanji_full.json`.
- **Edit content in the JSON only** — never in the generated HTML or the PDF (they are derived and
  overwritten on every build). Edit **keyed by headword/id** via a tiny script (avoids the ambiguity
  of duplicate gloss strings), and **back up first** (`cp file.json file.json.bak_<reason>`).
- **Reviewer-facing DOCX (optional).** Early editions used a DOCX as a "fidelity anchor" (content
  corrected only in the docx, extracted verbatim, then a gate proved every field appeared in the PDF).
  That discipline is sound for a heavy external-review cycle, but the series has since moved to
  **JSON-direct** for agility. If you run a formal external review, generate a read-only DOCX *from*
  the JSON for the reviewer — but the JSON stays canonical; fold their fixes back into the JSON.

---

## 4. Render pipeline — HTML → Edge → fitz (600 DPI)

```
[1] JSON source        _<type>_full.json / _wb_entries.json
       v   (python _<builder>.py  — emits one big self-contained HTML; re-embeds mascot art as base64)
[2] HTML               N<lvl>_<Type>_Workbook/<book>.html
       v   (python _print2x.py <html> <out_hq.pdf> <edge-profile>)
[3] 600-DPI PDF        _hq2_<type>.pdf
       v   (stamp: copy to a datetime-stamped deliverable; keep only the latest)
[4] Deliverable        <book>_<YYYYMMDD_HHMMSS>_screen.pdf
```

**The 600-DPI technique (`_print2x.py`) — the core print-quality trick:**
1. Take the built HTML, rewrite the `@page` rule to **double size (12in × 18in)** and add `html{zoom:2}`.
2. Render that 2× page with **Edge headless** to PDF (so Edge rasterises embedded images — the mascot
   PNGs — at 300 DPI *of the doubled page* = **~600 DPI of the real 6×9**, while text stays vector).
3. **Downscale back to 6×9** with **PyMuPDF (`fitz`)**: `new_page(width=432,height=648)` (6×9 in points)
   + `show_pdf_page(rect, src, i)`; save with `garbage=4, deflate=True, deflate_images=True, clean=True`.

**Edge headless flags (exact):**
```
msedge --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=120000 \
  --run-all-compositor-stages-before-draw --user-data-dir="<temp-profile>" \
  "--print-to-pdf=<out>.pdf" "file:///<html, spaces as %20>"
```
Edge path (Windows): `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`. Use a **fresh temp
`--user-data-dir` per run** to avoid profile locks. Google Fonts load via `@import` (network) — keep a
generous `virtual-time-budget`. `fallback_task_provider`/SmartScreen lines in stderr are benign noise.

---

## 5. Design system

- **Fonts (Google, embedded via `@import`):** `--display:"Baloo 2"` (headings) · `--jp:"Zen Maru
  Gothic"` (Japanese) · `--en:"Nunito"` (English) · `--hand:"Klee One"` (mascot/handwritten).
- **Palette:** a fixed set of ribbon themes (`matcha / coral / sky / lav / sakura / gold` + each
  `-soft`), one `--var` per. Each world is assigned a theme tuple; assign so adjacent worlds differ.
  Per-world page tints are pale versions of the theme applied as the section background.
- **Charm layer:** washi-tape strips, a dotted-paper background (`.page.dot`), the Shiba mascot in
  speech-bubble callouts, gem/star/blossom SVG symbols. Defined once, reused everywhere.
- **Mascot art** is embedded as **base64** in the HTML (so the file is self-contained for Edge);
  source PNGs live in `mascot_assets/`. Keep raster art ≤ ~800 px native — the 2× render already
  doubles it; oversized embeds make Edge's print pass time out.

---

## 6. The world opener (the "treasure board") — shared component

Each world starts with a single-column checklist of its gems ("Tick each gem as you collect it!").
**Single column on purpose:** a 2-column layout fuses adjacent items in content-order PDF extractors.

- Layout is a 3-column **CSS grid**: `grid-template-columns:auto max-content 1fr` =
  **[checkbox] [Japanese] [English]**. `max-content` locks the English column to a fixed start per page;
  the English is left-aligned right after it.
- **Balance the vertical rhythm:** the gap *above* the white checklist box (pill→box) should ≈ the gap
  *below* it (box→callout). These are set by the box's top/bottom margin + the callout's top margin.
- **English column readability:** keep the English a notch darker than a mid-grey (≈ `#5e5e76`) so the
  right side doesn't read as empty; keep the JP→EN column-gap tight (~`.2–.3em`).
- **Inherent trade-off:** a *fixed* (aligned) English column means short headwords have visible lead-in
  space before the English. That is the cost of alignment; do not "fix" it by right-aligning the JP
  (that flings the checkbox far from short words). If you want zero gap, you must drop alignment
  (ragged) — that was the deliberate choice for the back-of-book index, not the openers.

---

## 7. Japanese typography rules (critical)

- **Deliberate word-spacing:** author Japanese example/phrase text with **spaces between bunsetsu**
  (`へやに 入って ください。`). It aids the young reader and gives the line clean break opportunities.
- **`word-break:keep-all` on every Japanese sentence element** (`.exj` example, `.uc` use-phrase, etc.).
  Without it, CJK wraps between *any* two characters and orphans a trailing kana on the next line
  (`…教えて もらいま` / `す。`). With `keep-all`, lines break **only at the inter-bunsetsu spaces**, so
  conjugations (`もらいます。`, `しました。`) stay whole. This is mandatory for print polish.
- **Furigana/readings:** a vocab/kanji book *shows* the reading (it teaches it); a grammar book omits
  furigana on purpose. Never mix kanji+kana inside one word (`京と`, `問だい`) — run a kanji→kana scan.

---

## 8. ⚠️ PDF text-EXTRACTION artifacts vs visual defects (the #1 review trap)

A reviewer who **copies/extracts text** from the PDF (or uses a screen reader / automated text check)
will see "bugs" that **are not on the printed page**. Before changing source for any reported text
defect, **verify visually** (render the page to PNG) *and* with extraction (`page.get_text()`) side by
side. **Never edit source to fix an extraction artifact — it damages the visual or is a no-op.**

Known artifact classes (all confirmed on this series):
| Extraction shows | Reality on the page | Cause |
|---|---|---|
| `People & Relationshipsch.1` | "People & Relationships … ch.1" (chip far right) | two adjacent flex `<span>`s, no text node between |
| `V O C A B U L A R Y`, `S R I VAS TAVA` | clean tracked display type | CSS `letter-spacing`; extractor inserts spaces between glyphs |
| `挨拶 section managerちゃん…` | clean two-column "draw a line" exercise | extractor reads across the two columns row-wise |
| `お見舞いvisiting`, `コンピュータcomputer` | form and gloss in separate grid/block cells | no space node between separate elements |
| `USE**_**…_**` | bold label + italic text | bold/italic styling rendered as markdown-ish markers |
| `しまし た`, `もらいま す` | a sentence that *wrapped* mid-bunsetsu | line-wrap (fix with §7 `keep-all`), **not** a source space |

**Real** text defects (incomplete sentences, wrong meaning, mismatched phrase↔example) are fixed in the
JSON. **Artifacts** are left alone. Forcing spaces into the opener grid would break its
`auto/max-content/1fr` columns; removing letter-spacing would degrade the headers.

---

## 9. QA & verification method (verify, don't assume)

File edits are invisible until rendered. **Always render → read the PNG/PDF → only then report.**

- **Rasterise specific pages** with fitz: `doc[p].get_pixmap(matrix=fitz.Matrix(200/72,200/72))` (~200
  DPI) → save PNG → look at it. To find a gem's card page, `page.search_for(term)` and skip the opener
  (contains "Gems to collect") and the back-matter index (`page_index >= index_start`).
- **Check the worst cases, not a sample:** the **densest** content page (most items) for clipping, the
  **sparsest** for emptiness, plus the longest gloss/example. The card grid is **height-constrained**;
  long content clips silently behind `overflow:hidden`.
- **Measure when "pixel-perfect" matters** (opener gap balance, callout-vs-box alignment): scan pixel
  rows/columns for the white-box and callout bands; treat soft drop-shadows as ±2–3 px noise.
- **Programmatic scans** (cheap, run every review pass): kanji→kana mixing; provenance-tag leakage
  (must be 0); British/US spelling drift; gendered-pronoun candidates (verify each against the JP);
  polite-form consistency (examples end です/ます…); for vocab, reading-present + POS-in-controlled-set.

---

## 10. Per-level parameters (what changes between N5…N1)

| Parameter | N5 | N4 (ref) | N3 | N2 | N1 |
|-----------|----|----------|----|----|----|
| Typical reader | younger child | ~12 yr | teen | teen/adult | adult |
| Tone | most playful | playful | playful-lite | neutral-warm | neutral |
| Kanji policy | mostly kana | N5–N4 whitelist | + N3 | + N2 | + N1 |
| Example complexity | very simple | simple | moderate | longer | nuanced |
| Grammar gems | ~80 | **128** | ~180 | ~210 | ~250 |
| Vocab words | ~650 | **682** | ~1.5k | ~1.8k | ~2k+ |
| Kanji | ~80 | ~170 | ~370 | ~1k | ~2k |

**Level-invariant (leave alone):** the 6×9 geometry, the render flags, the `_print2x` technique, the
design system, the QA method, the environment workarounds. **Per-level (change):** the source corpus
JSON, the world taxonomy (`_wb_cats.py`-style tuples), the kanji whitelist, the `N<lvl>_…/` paths,
co-author/branding constants, and the per-level review prompt.

---

## 11. Deliverables & cleanup discipline

- **Datetime-stamp every generated deliverable:** `<book>_<YYYYMMDD_HHMMSS>_screen.pdf`. Working files
  (scripts, template, taxonomy, the source JSON) keep stable names.
- **Keep only the latest** stamped PDF in the deliverable folder; delete superseded stamps. The
  intermediate `_hq2_*.pdf` is a duplicate of the latest deliverable — remove it after stamping.
- **Keep content backups** (`*.json.bak_<reason>`) so any single edit is revertible.
- **Remove scratch** (one-shot verify/dump scripts, `_verify/`, `_diag/` PNG folders) when done.
- Point the user at the newest stamped file; flag older copies as superseded.

---

## 12. Environment & tooling pitfalls (Windows)

- **cp932 console mangles Japanese** in `python -c "…日本語…"` (throws / corrupts). **Write Japanese to
  UTF-8 files and read them back; print only ASCII** summaries/counts. Source `.py/.html/.json` are
  UTF-8 — Japanese inside files is fine.
- **Open PDF viewers lock the file** ("being used by another process" on delete/overwrite). The new
  stamped render is unaffected; ask the user to close the old one, then delete it.
- **`fitz` (PyMuPDF)** does both the downscale and all verification rasterisation — it is the one
  hard dependency beyond Edge.
- **EFS-encrypted working tree (env-specific):** on some corporate machines the workbook folder is
  EFS-encrypted; if the user's EFS key is unavailable, file reads fail with "Access denied" even though
  they own the files. That is an environment issue, not a build bug.
- **Verify by rendering, never by assuming.** "It should work" is not evidence.

---

*This common manual + the three type manuals encode the lessons of the N4 grammar and vocabulary first
editions (build + dozens of review/correction rounds). When a build surfaces a new defect class or
invariant, add it to the right manual in the same pass that fixes it.*
