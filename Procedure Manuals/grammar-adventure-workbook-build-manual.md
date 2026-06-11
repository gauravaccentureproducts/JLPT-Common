# JLPT Grammar "Adventure" Workbook — Cross-Level Build Manual

A reusable, **level-agnostic** procedure for producing a print-ready, child-friendly JLPT
grammar workbook for any level (N5 → N1). The first edition — *My N4 Grammar Adventure*
(128 gems, 18 chapters, 204 A5 pages) — is the **reference implementation**; every
level-specific number below is a parameter, not a constant.

> Scope: this manual covers only the printable grammar **workbook**. The web-app build is a
> separate document (`procedure-manual-build-next-jlpt-level.md`). Per-build issues are logged
> in `<Level>_Grammar_Patterns_BUGS.csv`; the publication review checklist is
> `<Level> grammar Book review Prompt.txt` (keep one per level, seeded from the N4 prompt).

---

## 0. Quickstart (the whole build in one screen)

```
# 0. Start from the N4 assets — copy, don't reinvent (see §3).
# 1. Author/curate the level's grammar corpus  -> _<lvl>_grammar_merged.json
# 2. Build the editor docx (applies CORPUS_FIX)
python _<lvl>_build_docx.py            # -> <Level>_Grammar_Patterns_<N>_<stamp>.docx
# 3. Extract entries from the NEWEST docx (verbatim, validated)
python _wb_extract.py                  # -> _wb_entries.json
# 4. Build the workbook HTML (taxonomy + layout)
python _wb_build.py                    # -> N<lvl>_Workbook/my-...-complete.html  (+ prints page count)
# 5. Render A5 PDF (Edge headless, see §11 for the exact flags)
# 6. Run the gates (MUST all pass — §10)
python _wb_verify.py ; python _wb_fidelity.py ; python _wb_practice_check.py
# 7. Impose the 2-up A4 print edition
python _wb_impose_2up.py               # -> my-...-2up-A4_<stamp>.pdf
# 8. Run the review loop until zero defects (§12), then ship both PDFs + the docx (§15)
```

Golden rules (each earned through a real defect — see §13):
1. **Content is corrected at the DOCX layer only** (via `CORPUS_FIX`), never in the HTML or PDF. The DOCX is the fidelity anchor.
2. **Every gate must pass before you call it done.** A failing gate is a blocker.
3. **A chapter name must describe *all* its gems**, not a minority or contradicted topic.
4. **Verify every instance** (montage all review/practice pages) — never fix one and assume the rest.
5. **Keep the total page count even** so the 2-up has no blank half-sheet.

---

## 1. The product

One body of grammar content, shipped as **two artifacts** plus a print edition:

- **Editor/reference DOCX** — `<Level>_Grammar_Patterns_<N>_<stamp>.docx`. Source-of-truth for
  content: for each pattern, the **4 fields** = pattern title, English meaning, usage formula
  ("Grammar Recipe"), and **3 example sentences** (JA + EN). Plain and reviewable.
- **Student workbook PDF** — `my-<level>-grammar-adventure-complete_<stamp>.pdf`. The polished,
  learner-facing A5 book.
- **2-up A4 print edition** — `my-<level>-grammar-adventure-2up-A4_<stamp>.pdf`.

Each grammar point is a **"gem."** Gems are grouped into themed **chapters** ("worlds" with
playful adventure names). Book spine:

- **Front matter:** cover · copyright/credits · How to Use This Book · Table of Contents (printed,
  gem-granular) · Adventure Map (illustrated).
- **Per chapter:** chapter intro → one **gem page** per gem → **Practice Time** → **Chapter Review**.
- **Back matter:** Progress Tracker · Answer Key · Grammar-Patterns reference list · back cover(s).

Tone: friendly but not babyish, age-appropriate to the level's typical learner (N4 reference
target = a 12-year-old; adjust per level — see §14). A mascot ("Bunpo-chan") gives encouragement.

---

## 2. Architecture & pipeline

Content flows one direction; each stage has a single responsibility. (Reference filenames shown;
the `_wb_*` stages are level-agnostic and reused as-is — only the `_<lvl>_*` source stages and
`_wb_cats.py` taxonomy change per level.)

```
[1] Source corpus (JSON)     _<lvl>_grammar_merged.json
       |                       one record/pattern: {id, pattern, meaning, usage, ex:[{ja,en}x3], categoryOrder}
       | + generated ex        _<lvl>_generated.py     (fills ex2/ex3 the corpus lacked)
       | + CORPUS_FIX           (a dict inside the docx builder — all hand corrections live here)
       v
[2] DOCX builder             _<lvl>_build_docx.py   ->  <Level>_Grammar_Patterns_<N>_<stamp>.docx
       v
[3] Extractor                _wb_extract.py         ->  _wb_entries.json
       |                       reads the NEWEST docx VERBATIM, strips provenance tags, validates 3 ex each
       v
[4] Workbook builder         _wb_build.py (+ _wb_template.html + _wb_cats.py)  ->  N<lvl>_Workbook/my-...-complete.html
       v
[5] Renderer                 Edge --headless --print-to-pdf  ->  my-...-complete_<stamp>.pdf  (A5)
       v
[6] Imposer                  _wb_impose_2up.py      ->  my-...-2up-A4_<stamp>.pdf

QA gates (run against [5]):  _wb_verify.py · _wb_fidelity.py · _wb_practice_check.py   (+ _wb_shots.py spot-renders)
```

**Key contracts**

- **The DOCX is the fidelity anchor.** `_wb_extract.py` reads the newest docx by timestamp;
  `_wb_fidelity.py` checks every docx field appears verbatim in the rendered PDF. Therefore any
  content correction is made in `CORPUS_FIX` (docx layer) → rebuild docx → re-extract → rebuild
  workbook. Never edit `_wb_entries.json`, the HTML, or the PDF directly.
- **The taxonomy (`_wb_cats.py`)** is shared by the extractor (stamps each pattern's
  `categoryOrder` + chapter title) and the builder (chapter names/colours/icons). It does **not**
  affect the DOCX, so renaming chapters never breaks fidelity.
- **Display-only condensations** (e.g., a shortened gloss for the cramped review-match column —
  `REVIEW_GLOSS`) live in the builder, never in the canonical meaning shown on the gem page,
  answer key, or grammar list.

---

## 3. Starting a new level (copy, don't reinvent)

1. Copy the reference assets into the level's working dir and rename the `_<lvl>_*` ones:
   - reused as-is: `_wb_extract.py`, `_wb_build.py`, `_wb_template.html`, `_wb_impose_2up.py`,
     `_wb_fidelity.py`, `_wb_verify.py`, `_wb_practice_check.py`, `_wb_shots.py`.
   - per-level: `_<lvl>_grammar_merged.json` (new corpus), `_<lvl>_build_docx.py` (new `OUT` name +
     fresh `CORPUS_FIX = {}`), `_wb_cats.py` (new `NEWCATS` taxonomy).
2. Point the path constants (DOCX glob, OUT paths, `N<lvl>_Workbook/`) at the new level.
3. Seed `<Level>_Grammar_Patterns_BUGS.csv` (empty) and copy the review prompt, swapping the level.
4. Work through §4.

---

## 4. Build procedure (step by step)

1. **Assemble the corpus.** Curate the level's official-ish grammar pattern list into
   `_<lvl>_grammar_merged.json` — one record per pattern with a stable `id`, the pattern title,
   a concise English `meaning`, a `usage` formula, and **3** example sentences (JA+EN). Generate
   missing examples programmatically (`_<lvl>_generated.py`) but hand-verify them.
2. **Build the DOCX:** `python _<lvl>_build_docx.py`. It applies `CORPUS_FIX` and emits a
   datetime-stamped docx. Corrections found later go into `CORPUS_FIX` keyed by id, e.g.
   `"<lvl>-066": {"ex1_ja": "...", "ex1_en": "...", "meaning": "..."}`.
3. **Extract:** `python _wb_extract.py` → `_wb_entries.json` (reads the newest docx, validates each
   pattern has exactly 3 examples + non-empty meaning/usage/title; fix any "bad" id it reports).
4. **Define the taxonomy** in `_wb_cats.py` → `NEWCATS` (see §6).
5. **Build the workbook HTML:** `python _wb_build.py` (prints `chapters | gems | total pages`).
   Confirm gem count = corpus size and total pages is **even**.
6. **Render the A5 PDF** with Edge headless (§11).
7. **Run all gates** (§10). Fix failures at the correct layer, rebuild, re-render, re-gate.
8. **Impose** the 2-up: `python _wb_impose_2up.py`.
9. **Review loop** (§12) until zero defects.
10. **Ship** (§15): copy both PDFs + the docx + the BUGS log into the deliverable bundle.

Re-render whenever the HTML changes; re-build-docx → re-extract whenever content changes.

---

## 5. Page model & design system

**Geometry (invariant across levels):**
- Page size **148.5 mm × 210 mm** (= A4 ÷ 2). Set in `_wb_template.html`: `@page{ size:148.5mm 210mm; margin:0; }`
  and `.page{ width:148.5mm; height:210mm; ... padding:12mm 11mm; }`. The 148.5 (not 148) lets two
  pages tile an A4-landscape sheet **edge-to-edge** (2 × 148.5 = 297 = A4 width).
- Full-bleed page background (cream) so trimming/borderless printing leaves no white.
- **Total page count must be EVEN** (so the 2-up has no blank half-sheet). The builder prints the
  count; if odd, adjust a multi-page back-matter section's per-page packing (e.g. chapters-per-page)
  to add/remove one page.

**Typography (Google Fonts, embedded via `@import`):**
`--display: "Baloo 2"` (headings) · `--jp: "Zen Maru Gothic"` (Japanese) · `--en: "Nunito"` (English) ·
`--hand: "Klee One"` (handwritten notes/mascot). Keep these; they read as warm + child-friendly.

**Colour themes:** six ribbon palettes — `r-gold / r-matcha / r-coral / r-sky / r-lav / r-sakura`,
each with a `--<name>` and `--<name>-soft` colour var and an icon. Each chapter is assigned a theme
tuple in `_wb_cats.py`. Reuse the palette; assign themes so adjacent chapters differ.

**Page types** (the builder emits them in this order; `_wb_verify.py` mirrors the sequence to check
the page count): `cover, copyright, howto, tradtoc×T, map×ntoc, [intro, gem×k, practice, review]×chapters,
tracker×pc, answerkey×ceil(ch/5), grammar×ceil(ch/3), backcover, tradback`.

---

## 6. Chapter taxonomy & naming rules

Defined in `_wb_cats.py` as `NEWCATS` — a list of tuples, one per chapter, in book order:

```
(adventure_name, real_subtitle, ribbon_class, icon_id, colour_var, soft_var, [member pattern-ids])
```

Derived automatically: `RECAT` (id→chapter index), `THEME_NAME` (playful names, used only in the
PDF), `TITLE` (subtitles), `THEME` (colours/icons). The builder imports `THEME/THEME_NAME`; the
extractor imports `RECAT/TITLE`. **Group every pattern into exactly one chapter; assert the union
equals the full corpus.**

**Naming rule (gem-level accuracy — the most-corrected lesson):** the adventure name must describe
what is actually taught in **all** of a chapter's gems — never a minority topic, never a contradicted
one. Audit each chapter gem-by-gem against its name. For a genuinely mixed chapter, name the two
dominant buckets (`A & B <Place>`) and fold the third into the subtitle; never let the name exclude a
prominent gem.

> N4 mistakes that were renamed: "Te-form Workshop" actually held compound verbs (出す); "Must-Do
> Mountain" held a prohibition (な, the opposite of must-do); "Change Den" excluded the *feelings*
> gems (がり/がる/たがる); "How & Why Realm" excluded the *focus/cleft* gem (のは〜だ).

Names pass through HTML-escape, so `&` renders correctly as `&` in the PDF.

---

## 7. Content authoring rules

- **Grammar correctness & naturalness:** every pattern, usage formula and example must be
  grammatically correct, natural, and **level-appropriate**. Watch the classic confusable sets for
  the level (e.g. at N4: 間/間に · ば/たら/なら/と/ても · そうだ hearsay vs appearance · みたいだ/ようだ/らしい ·
  あげる/くれる/もらう/やる · にくい/づらい/やすい).
- **Kanji policy is per-level.** Maintain a kanji whitelist matching the level; outside it, use kana
  (N4 example: 速 was out-of-list → use はやい). Lower levels lean more on kana.
- **English meanings:** faithful, not over-broad, no nuance dropped. **Do not add gender** the
  Japanese doesn't specify (`he/she` for あの人/omitted subject is a defect; おばあさん→"her" / 弟→"him"
  are fine because the JP specifies). Match the meaning label to what the examples actually show.
- **Compound-verb gems need a compound example** in the **primary** slot (the one that drives the gem
  page and the practice blank): V-stem+auxiliary (出す, 始める, 終わる, つづける, ていく, てくる, …) must show
  the host verb, e.g. 「手紙を 書き終わりました」 — not a standalone 「コンサートが終わった」.
- **Spelling/style consistency:** pick UK or US and hold it (N4 reference is UK: colour/favour/realise).
  Keep punctuation ASCII-clean in learner text (no stray em-dash/smart-quote/ellipsis) for uniformity.
- **No malformed notation:** never mix kanji+kana inside a word (e.g. 京と, 問だい); a general
  kanji→kana scan catches these.
- **All corrections go in `CORPUS_FIX`**, keyed by id, overriding only the fields that change
  (`meaning`, `usage`, `ex<n>_ja`, `ex<n>_en`). The raw corpus stays pristine.

---

## 8. Exercise design rules

Practice pages test each chapter's **first 3 gems**; Review pages match its **first 6**. The
**word bank is built from the gem patterns** (not the conjugated answers), so changing what the blank
covers never breaks the word-bank gate.

**Practice cloze (`_practice_blank`):**
- The blank must test the **gem**, not a leftover tail. Bad: word bank `ことになる` but the sentence
  shows `ことに___` and the blank only needs `なりました`. Good: blank the whole `ことになりました`, or
  blank from a visible stem so the learner writes the gem-bearing form.
- Reject spurious ≤2-char answers (e.g. a stray さ inside くださ-い); fall back to a clean token.
- **The host verb must be present or cued.** Gems that *fuse/wrap* the verb — circumfix
  お〜ください / お〜になる, causative させてください — otherwise swallow the verb, leaving nothing to attach
  the pattern to. Render a dictionary-verb cue before the blank, e.g. 「こちらに （すわる）___。」 → おすわりください,
  parallel to a literal cloze where the stem is already visible (早く ね___ → なさい).
- The English line is the learner's clue; the completed sentence must be natural.

**Chapter Review matching ("draw a line"):**
- **One line per meaning, each with its connector dot.** A meaning long enough to **wrap** leaves the
  wrapped line with no dot (an orphan bullet) and breaks the aligned dot grid. Keep meanings short
  enough to fit one line; for an over-long meaning use a display-only `REVIEW_GLOSS` (the full meaning
  still shows on the gem page / answer key / grammar list — that difference is intentional).
- **Every meaning must match exactly one gem.** No two displayed meanings identical or one contained
  in another. Near-synonyms are OK only with a unique distinguisher: a register tag
  (ではないか formal / じゃないか casual), grammatical position (みたいな +noun / みたいに +verb), a form label
  (なさる = honorific of する / お〜になる), or a unique sense word. The real trap is near-**identical
  wording** (e.g. 出す "to begin to; start to" vs 始める "to start; to begin to") — sharpen one.
- Shuffle the right column with a **derangement** (no meaning sits on its own gem's row), else a
  partial shuffle reads like an error.

**Answer Key:** lists every chapter's Practice fill answers and Review-match `gem = meaning` pairs,
matching the current questions.

---

## 9. Appendices & back-matter

- **Progress Tracker** — a colour-in checklist of all gems by chapter.
- **Answer Key** — exercise answers (above). Already covers "all exercise answers"; don't duplicate.
- **Grammar-Patterns list** — a consolidated reference: every gem with its English meaning, a running
  serial 1..N, grouped under chapter headers (TOC-style numbered list). The printed TOC is already
  gem-granular (it indexes every gem with a page), so this back-matter reference need not have its own
  TOC line if the TOC is full — placing it right after the Answer Key is sufficient.
- **Vocabulary glossary (optional, deferred on N4)** — a JP-EN list of content words used in the book.
  There is no bundled JP-EN dictionary; `janome` can tokenize (segment + base form) but glosses are
  hand-authored. Decide scope per level (core recurring words vs every word) before committing — it is
  the largest hand-authoring task.

---

## 10. QA gates (automated, non-negotiable)

Run all three against the freshly-rendered PDF. **Any failure is a blocker.**

| Gate | Command | Pass condition |
|------|---------|----------------|
| Page structure | `python _wb_verify.py` | `page_count == expected` (built from the page-type sequence) **and** all-page clip-risk **0** (no content within 3.5 mm of the footer) |
| Fidelity | `python _wb_fidelity.py` | `VERBATIM-IN-PDF: K×9 / K×9` — every docx field (title+meaning+usage + 3 ex × ja/en) appears verbatim in the PDF (K = pattern count) |
| Word bank | `python _wb_practice_check.py` | "every answer is in its word bank" (count / 0 missing) |

Spot-render any page to PNG with `_wb_shots.py` (0-indexed page input) for visual checks.

**Gate caveats (learned):**
- clip-risk checks only the **footer band**, not decorative bands (e.g. a TOC's centre divider or the
  mascot strip). A column can clear the footer yet still overlap a divider — **verify dense pages
  visually**, don't trust clip-risk alone there.
- The fidelity count `K×9` means **DOCX↔PDF consistency is gated**; you don't need to re-diff meanings
  manually once it's green.
- After any content change, **regenerate the 2-up** too (it's built from the rendered PDF).

---

## 11. Print production (A5 + 2-up A4)

**Render (Edge headless, exact flags):**
```
msedge --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=50000 \
  --run-all-compositor-stages-before-draw --user-data-dir="<temp-profile>" \
  "--print-to-pdf=<out>.pdf" "<file-uri-of-the-built-html>"
```
(`fallback_task_provider` and SmartScreen-DNS lines in the output are benign noise.)

**Two-up:** `_wb_impose_2up.py` places two consecutive A5 pages, full-bleed, on each
**A4-landscape (297×210 mm)** sheet — no gutter. Output sheets = pages ÷ 2 (hence the even-count rule).

**Printing the 2-up correctly (tell the end user):**
- Print the **pre-imposed 2-up PDF** at **"Actual size / 100%"** with **Landscape** + duplex
  (flip on long edge). Do **not** use Acrobat's "Multiple / pages-per-sheet" — its N-up always shrinks
  pages and adds a margin, and it has no borderless option.
- The remaining thin white edge is the printer's **non-printable margin** (~4–6 mm on office lasers) —
  not a document defect. True edge-to-edge needs a **borderless** device or print-on-oversize + trim;
  the cream background already bleeds to the edge to support trimming.

---

## 12. The review loop (run → fix → repeat until zero)

Keep a per-level review prompt (`<Level> grammar Book review Prompt.txt`, seeded from N4's). Each
pass: act as the senior JLPT reviewer + children's-book editor it describes, produce a precise,
evidence-based issue list (document, page/pattern, current text, why, exact fix, severity), then fix
each at the correct layer and re-run the gates. Repeat until zero defects.

Efficient pass order:
1. **Objective battery** (programmatic, cheap): gates; PDF scan for provenance-tag leakage (must be 0);
   grammar-list serial complete (1..N, no gaps/dups); punctuation + UK/US spelling consistency;
   gendered-pronoun candidates (verify each against the JP).
2. **Content read:** all K gems × (meaning + usage + 3 examples).
3. **Layout:** montage **all** review pages and **all** practice pages (not a sample) to catch
   orphan bullets / missing host verbs / overflow; spot-render front/back matter.

Log every round in `<Level>_Grammar_Patterns_BUGS.csv` (`RNN-xx, round, area, field, severity,
provenance, issue, fix, status`).

---

## 13. Recurring defect classes (the checklist)

Re-check every one across the WHOLE book each review pass:

1. **Malformed kana / mixed notation** (京と, 問だい) — general kanji→kana scan.
2. **Compound-verb examples** standalone instead of compound (§7).
3. **Meaning glosses** over-broad, nuance dropped, or **gender added** the JP doesn't specify (§7).
4. **Chapter name** describes only part of its chapter (§6).
5. **Cloze tests a leftover tail** instead of the gem; or the **host verb is missing/uncued** for
   circumfix/causative gems (§8).
6. **Review meaning wraps** → orphan bullet / broken dot grid (§8).
7. **Two review meanings not uniquely matchable** (identical / contained / near-identical wording) (§8).
8. **Word-bank ≠ blank** / answer not derivable from the bank.
9. **Print/format:** wrong page size, odd page count, broken 2-up tiling (§5, §11).
10. **Provenance-tag leakage** in the learner-facing PDF (must be 0).
11. **Cross-references** (printed TOC page numbers vs real footers) — adding back-matter after the
    answer key doesn't shift earlier refs, but verify after any front/mid change.
12. **Process:** fixed one instance but not its siblings; or declared done with a gate failing.

---

## 14. Per-level parameters (what changes)

Approximate; the authoritative pattern set comes from the level's grammar list.

| Parameter | N5 | N4 (ref) | N3 | N2 | N1 |
|-----------|----|----------|----|----|----|
| Gems (patterns) | ~80 | **128** | ~180 | ~210 | ~250 |
| Chapters | ~12 | **18** | ~22 | ~26 | ~30 |
| Typical reader | younger child | ~12 yr | teen | teen/adult | adult |
| Kanji policy | mostly kana | N5–N4 whitelist | + N3 | + N2 | + N1 |
| Example complexity | very simple | simple | moderate | longer | nuanced |
| Tone | most playful | playful | playful-lite | neutral-warm | neutral |

Code touch-points per level: the source corpus JSON; `_wb_cats.py` `NEWCATS` (new taxonomy + names);
the docx builder `OUT` name + `CORPUS_FIX`; the kanji whitelist; the `N<lvl>_Workbook/` path. The
layout geometry, gates, render flags and imposer are **level-invariant** — leave them alone.

---

## 15. Deliverables & file conventions

- **Always datetime-stamp generated outputs**: `_YYYYMMDD_HHMMSS` before the extension. Source/working
  files (scripts, template, taxonomy) keep stable names.
- **Deliverable bundle** (e.g. `JLPTSuccess/N<lvl>/grammar-workbook/`): the newest
  `...-complete_<stamp>.pdf`, `...-2up-A4_<stamp>.pdf`, `<Level>_Grammar_Patterns_<N>_<stamp>.docx`,
  and `<Level>_Grammar_Patterns_BUGS.csv`. Keep exactly one current copy of each; remove superseded
  stamps.
- Point users to the newest stamped file; flag older copies as superseded.

---

## 16. Environment & tooling pitfalls (Windows)

- **cp932 console mangles Japanese** in `python -c "...日本語..."` (can throw / corrupt). Write Japanese
  to UTF-8 files and read them back; print only ASCII summaries/counts to the console.
- **Source files are UTF-8** even though the console isn't — Japanese in `.py`/`.html`/`.json` is fine.
- **Open PDF viewers lock files** ("Device or resource busy" on delete/overwrite). Close the viewer or
  retry; the new stamped render is unaffected.
- **`_wb_extract.py` / `_wb_fidelity.py` pick the newest docx by mtime** — after rebuilding the docx the
  whole chain uses it automatically; clean out stale dated docx to avoid confusion.
- **Verify, don't assume**: render → read the PNG/PDF → only then report. File edits are invisible until
  rendered; "it should work" is not evidence.

---

*This manual encodes the lessons of the N4 first edition (build + 36 correction/review rounds).
When a new level surfaces a new defect class or invariant, add it here in the same pass that fixes it.*
