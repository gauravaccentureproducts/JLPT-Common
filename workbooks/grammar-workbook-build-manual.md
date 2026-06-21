# JLPT Grammar "Adventure" Workbook — Build Manual (Level-Agnostic)

How to build the **grammar** edition for any level (N5 → N1). Read
**`00-common-workbook-pipeline.md`** first — it owns the shared mechanics (6"×9" KDP geometry, the
HTML→Edge→fitz 600-DPI render, design system, world openers, Japanese typography, extraction-artifact
discipline, QA method, environment). This manual covers only what is **grammar-specific**.

> Reference edition: *My N4 Grammar Adventure* — 128 gems, 18 worlds. Counts are parameters (common §10).

---

## 1. The content unit — a grammar "gem"

One record per pattern in the source JSON (`_wb_entries.json`), **4 canonical fields**:

```json
{
  "id": "n4-066", "num": 66, "categoryOrder": 7,
  "pattern": "～ことになる",                         // the pattern title
  "meaning": "it has been decided that; it turns out that",
  "usage":   "Verb(plain) + ことになる",             // the "Grammar Recipe" formula
  "ex": [ {"ja":"…","en":"…"}, {"ja":"…","en":"…"}, {"ja":"…","en":"…"} ]   // exactly 3
}
```

- **Exactly 3 example sentences** per gem (JA + EN). Validate this on load.
- **Each gem gets a full page** (grammar's defining layout choice — unlike vocab/kanji card-grids):
  pattern title → meaning → Grammar Recipe (usage) → 3 examples → a small handwriting/notes box.
- `categoryOrder` (world index) is stamped from the taxonomy (§3); a running `num` (1..N) drives the
  TOC and the back-matter Grammar-Patterns list.

---

## 2. Build procedure

1. **Assemble the corpus** → `_<lvl>_grammar_full.json`: the level's official-ish pattern list, one
   record per pattern with a stable id, title, concise meaning, usage formula, and 3 examples. Draft
   missing examples programmatically but **hand-verify every one**.
2. **Define the taxonomy** (§3) — the world tuples.
3. **Build the HTML:** `python _wb_build.py` (prints `worlds | gems | pages`). Confirm gem count =
   corpus size.
4. **Render** the 6×9 600-DPI PDF (common §4).
5. **Verify** (common §9): montage **all** Practice and **all** Review pages; spot-render front/back
   matter and the densest gem pages.
6. **Review loop** (§6) until zero defects; **stamp + keep-latest** (common §11).

Re-build the HTML on any content or taxonomy change, then re-render.

---

## 3. World taxonomy & naming rules

Define worlds as ordered tuples (one per world, in book order):
`(adventure_name, real_subtitle, ribbon_class, icon_id, colour_var, soft_var, [member pattern-ids])`.
Group **every** pattern into **exactly one** world; assert the union equals the full corpus.

**Naming rule (the most-corrected grammar lesson):** the adventure name must describe what is taught in
**all** of a world's gems — never a minority topic, never a contradicted one. Audit each world
gem-by-gem against its name. For a genuinely mixed world, name the two dominant buckets
(`A & B <Place>`) and fold the third into the subtitle; never let the name exclude a prominent gem.

> N4 renames that were forced: "Te-form Workshop" actually held compound verbs (出す); "Must-Do
> Mountain" held a *prohibition* (な — the opposite); "Change Den" excluded the *feelings* gems
> (がる/たがる); "How & Why Realm" excluded the focus/cleft gem (のは〜だ).

Names HTML-escape, so `&` renders correctly.

---

## 4. Grammar content rules

- **Correctness, naturalness, level-appropriateness** for every pattern, formula, and example. Watch
  the level's confusable sets — at N4: 間/間に · ば/たら/なら/と/ても · そうだ (hearsay vs appearance) ·
  みたいだ/ようだ/らしい · あげる/くれる/もらう/やる · にくい/づらい/やすい. Each level has its own set.
- **Compound-verb gems need a compound example in the primary slot** (the one that drives the gem page
  and the practice blank): V-stem + auxiliary (出す/始める/終わる/つづける/ていく/てくる) must show the host
  verb — `手紙を 書き終わりました`, not a standalone `コンサートが終わった`.
- **Meanings:** faithful, not over-broad, no nuance dropped; match the label to what the examples show.
  Apply the common no-added-gender and British-English rules.
- **Kanji policy is per-level** (common §10): outside the level's whitelist, use kana (N4: 速 was
  out-of-list → はやい).
- **Display-only condensations** (a shortened gloss for the cramped review-match column) live in the
  builder as a `REVIEW_GLOSS` override — never in the canonical meaning on the gem page / answer key /
  grammar list. That divergence is intentional.

---

## 5. Exercise design (grammar)

Practice tests each world's **first 3 gems**; Review matches its **first ~6**. Build the word bank from
the **gem patterns** (not the conjugated answers), so changing what a blank covers never breaks the
"answer-in-bank" check.

**Practice cloze:**
- The blank must test the **gem**, not a leftover tail. Bad: bank `ことになる` but the sentence shows
  `ことに___` needing only `なりました`. Good: blank the whole `ことになりました`, or blank from a visible stem.
- Reject spurious ≤2-char answers (a stray `さ` inside `くださ-い`); fall back to a clean token.
- **The host verb must be present or cued.** Circumfix/wrapping gems (お〜ください / お〜になる, causative
  させてください) otherwise swallow the verb. Render a dictionary-verb cue before the blank:
  `こちらに （すわる）___。` → おすわりください.
- The English line is the learner's clue; the completed sentence must be natural.

**Review matching ("draw a line"):**
- **One line per meaning, each with its connector dot.** A meaning long enough to **wrap** orphans the
  wrapped line (no dot) and breaks the dot grid — keep meanings to one line (use `REVIEW_GLOSS` if
  needed; the full meaning still shows on the gem page / answer key / list).
- **Every meaning matches exactly one gem.** No two displayed meanings identical, contained, or
  near-identical in wording (the real trap: 出す "to begin to; start to" vs 始める "to start; to begin
  to" — sharpen one). Near-synonyms need a unique distinguisher: a register tag (ではないか formal /
  じゃないか casual), a grammatical position (みたいな +noun / みたいに +verb), or a form label.
- **Derange the right column** (no meaning sits on its own gem's row) so a partial shuffle never reads
  like an error.

**Answer Key** lists every world's Practice fill answers + Review `gem = meaning` pairs, kept in sync.

---

## 6. Review loop & recurring grammar defect classes

Keep a per-level review prompt (`<Level> grammar Book review Prompt.txt`, seeded from N4's); act as the
senior JLPT reviewer + children's-book editor, produce an evidence-based issue list (page/pattern,
current text, why, exact fix, severity), fix at the **JSON layer**, re-render, re-verify. Repeat to
zero. Log rounds in `<Level>_Grammar_Patterns_BUGS.csv`.

**Re-check every one across the WHOLE book each pass** (montage all Practice + Review pages):
1. Malformed kana / mixed notation (京と, 問だい) — kanji→kana scan.
2. Compound-verb example standalone instead of compound (§4).
3. Meaning over-broad / nuance dropped / **gender added** the JP doesn't specify.
4. World name describes only part of its world (§3).
5. Cloze tests a leftover tail; or host verb missing/uncued for circumfix/causative gems (§5).
6. Review meaning wraps → orphan bullet / broken dot grid (§5).
7. Two review meanings not uniquely matchable (identical / contained / near-identical) (§5).
8. Word-bank ≠ blank / answer not derivable.
9. **Extraction artifacts mistaken for defects** (common §8) — verify render-vs-extract before editing.
10. Provenance-tag leakage in the learner PDF (must be 0).
11. Cross-references (printed TOC page numbers vs real footers) after any front/mid change.
12. Process: fixed one instance but not its siblings; declared done with a check failing.

---

## 7. Back matter

- **Progress Tracker** — colour-in checklist of all gems by world.
- **Answer Key** — all Practice + Review answers (§5).
- **Grammar-Patterns list** — every gem with its meaning, running serial 1..N, under world headers
  (the printed TOC is already gem-granular, so this need not have its own TOC line).
- **Certificate + back cover.** A vocabulary glossary is optional and the largest hand-authoring task —
  decide scope per level before committing (`janome` can segment, but glosses are hand-authored).

---

*Grammar-specific addendum to the common pipeline. Add new grammar defect classes here in the same pass
that fixes them.*
