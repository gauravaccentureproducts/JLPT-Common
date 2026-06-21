# JLPT Vocabulary "Adventure" Workbook — Build Manual (Level-Agnostic)

How to build the **vocabulary** edition for any level (N5 → N1). Read
**`00-common-workbook-pipeline.md`** first (shared 6"×9" KDP pipeline, render, openers, typography,
extraction-artifact discipline, QA, environment). This manual covers only what is **vocab-specific**:
the word-card model, the all-important **readings** and **part-of-speech** discipline, the
**collocation** row, register tagging, and the word index.

> Reference edition: *My N4 Vocabulary Adventure* — 682 words, 19 worlds, 225 pages. Counts are
> parameters (common §10).

---

## 1. The content unit — a word card

One record per word in the source JSON (`_<lvl>_vocab_full.json`), keyed by `form`:

```json
{
  "id": "...", "form": "上がる", "reading": "あがる",
  "gloss": "to rise; (of rain) to stop",          // English; primary sense first, register tags inline
  "pos": "verb-1", "section": "13. Verbs (general)",
  "ex":  [ { "ja": "雨が 上がりました。", "en": "The rain has stopped." } ],   // ONE example
  "use": { "label": "PHRASE", "ja": "雨が 上がる", "en": "the rain stops" }    // the collocation row
}
```

**Card anatomy (6-up grid, 2 cols × 3 rows):** `form` (large, kanji prominent) · `reading` (kana
furigana — **always shown**; a vocab book teaches it) · a coloured **POS chip** · `gloss` (English) ·
a **`use`/collocation row** (label + JA collocation + EN) · one `ex` example (JA + small EN).

**The collocation (`use`) row is a key teaching element** — it shows the word in a natural set phrase
(`PHRASE: 髪を 切る / to cut one's hair`). For grammar/interjection words use `label:"USE"` with a usage
note instead (`USE: casual 'you'; avoid with teachers`).

The grid is **height-constrained**: `.vcard{overflow:hidden}` is the backstop, and type is sized to the
**longest** card (a 3-line meaning, a 4-sense gloss). Adding senses/notes is fine but verify the
densest pages don't clip (common §9). Glosses up to ~50 chars render in ≤3 lines.

---

## 2. Build procedure

1. **Assemble + de-dupe** the corpus → `_<lvl>_vocab_full.json` (drop words already taught at lower
   levels; de-dupe against the lower-level app's `data/vocab.json`).
2. **Author one example + one collocation per word** — the largest content task; hand-verify every one.
3. **Define the world taxonomy** (§5).
4. **Build the HTML:** `python _wbv_workbook.py` (prints `chapters | words | pages | index start`).
5. **Render** the 6×9 600-DPI PDF (common §4).
6. **Verify** (common §9): montage **all** card pages + **all** exercise pages; spot-check the longest
   glosses and densest worlds for clipping.
7. **Review loop** (§7) + **native QA** (§8) to zero; **stamp + keep-latest** (common §11).

Content edits go in the JSON, **keyed by `form`** via a small script (duplicate gloss strings like
"baby; infant" make raw find-replace unsafe), with a `.bak_<reason>` backup first.

---

## 3. The two dominant vocab risks (gate these)

1. **Reading / furigana (#1 risk).** Every kanji word's kana reading must be correct. Watch
   multi-reading kanji (音/訓), special readings (今日=きょう, 上手=じょうず), rendaku (何時→なんじ), and
   counter sound-changes (一杯/一匹). **Gate:** every kanji word has a reading and the reading contains
   **no kanji**.
2. **Part of speech (#2 risk).** Use a **fixed controlled set** so it can be validated: `noun`,
   `noun (suru)`, `verb-1` (godan), `verb-2` (ichidan), `verb-3` (suru/irregular), with transitivity
   noted; `i-adj`, `na-adj`, `adverb`, `pre-noun`, `pronoun`, `conjunction`, `counter`, `katakana
   noun`. **Get transitive/intransitive pairs right** — 上がる/上げる, 開く/開ける, 変わる/変える are classic
   traps. **Gate:** flag any free-text POS.

---

## 4. Gloss & example content rules (this edition's lessons)

- **Primary sense first; don't over-list.** Match the example to the listed sense. (上がる glossed "to
  rise" but exemplified with rain → fix the gloss to "to rise; (of rain) to stop" *and* the example.)
- **Register tags inline in the gloss**, consistently:
  - Pronouns/relations: `君 → "you (casual, male; avoid with superiors)"`, `僕 → "I (casual, male)"`,
    `ご主人 → "(polite) someone else's husband"`, `家内 → "(humble, old-fashioned) one's own wife"`,
    `お宅 → "(polite) someone else's home"`.
  - **Formal/uncommon する-verbs:** flag them so learners don't produce unnatural Japanese —
    `水泳する → "to swim (formal; everyday 泳ぐ)"`, `暖房する → "to heat a room (formal; daily
    暖房をつける)"`, `試験する → "to test something (formal; everyday テストする)"`. (Pairing the noun's
    natural collocation, e.g. `暖房をつける`, on the noun card reinforces the daily form.)
- **Transitive/intransitive accuracy in the English.** An intransitive verb must read intransitive:
  `無くなる (intransitive) → "My wallet is gone."` **not** "I lost my wallet" (that maps to the transitive
  無くす and blurs the pair). Tag the pair `変える "to change something (transitive)"` / `変わる "to
  change; become different (intransitive)"`.
- **Distinguish near-duplicate glosses** so two words aren't both "industry"/"baby": `工業 "(manufacturing)
  industry"` vs `産業 "industry (in general)"`; `赤ちゃん "baby"` vs `赤ん坊 "baby (formal/older word)"`;
  `誕生 "birth (the event)"` vs `生まれ "birth; one's origin"`; `毛 "hair; fur (animal/body)"` vs `髪
  "hair (on the head)"`.
- **British English**, ASCII punctuation, no added gender (common §1). Examples use only at-or-below
  level grammar+vocab, short, with the headword in obvious context.

---

## 5. Noun + する pair differentiation (systemic — ~50 pairs at N4)

When the corpus has both a noun `X` and a verb `Xする` (紹介/紹介する, 準備/準備する, 暖房/暖房する…), their
cards must **not** show the identical collocation. Rule:
- **Noun card** `use` = the noun phrase: `紹介を する / to introduce`, or a more natural set phrase where
  one exists (`暖房を つける`, `約束を まもる`).
- **Verb card** `use` = a **contextual collocation** (object + verb), derived from the verb's example's
  first `〜を` object: `紹介する → 友だちを 紹介する / to introduce a friend`; `準備する → パーティーを 準備
  する`; `教育する → 子どもを 教育する`. For self-object suru-verbs with no distinct object, vary the
  modifier or use a destination/partner particle (`案内する → 駅まで 案内する`, `会議する → みんなで 会議する`).
- Pairs that already differ (拝見/拝見する, 関係/関係する, 計画/計画する, 故障/故障する) need no change.
- **Newly generated collocations are the only non-native-reviewed Japanese** in an otherwise
  native-reviewed book — list them for a native spot-check (particles に/を/と/で, naturalness, avoid
  over-literal reuse of the example's object).

---

## 6. World taxonomy & word index

- **Taxonomy:** ~35–40 words/world. Group **nouns by semantic theme** (Family, Food, Home, School,
  Work, Travel, Time, Body/Health, Nature/Weather, Town, Shopping…) and put function words in
  **POS-based worlds** (Everyday Verbs, Adjectives, Adverbs, Little Words). Same tuple structure as
  grammar; the world name must fit **all** its words (don't drop 食べる into a "nouns" world).
- **Kanji→kana read-scope (per level):** a headword whose standard kanji is in the level's read-scope
  may show kanji; otherwise kana. Be consistent across card, example, collocation, and index.
- **Word index (essential, back matter):** a あいうえお-ordered, dictionary-style list `word · reading ·
  page`. Lets a learner look up any word. **For the index, association beats alignment** — page numbers
  sit **right after the word** (ragged), with the gutter visibly wider than the word→number gap; a
  rigidly right-aligned column detaches the number from short CJK words (the deliberate opposite choice
  from the aligned opener checklists — common §6).

---

## 7. Vocab exercises

Per world, after its word cards:
- **Word ↔ meaning matching ("draw a line")** — one line per meaning + its dot, every meaning uniquely
  matchable, deranged shuffle (grammar manual §5). The scramble is **intentional**; if a reviewer's
  extraction shows it interleaved/garbled, that is an extraction artifact (common §8), not a defect.
- **Fill-in-the-blank** — word in a sentence; bank = the world's words; the answer is the word in its
  correct form.
- **Reading practice** — show a kanji word, learner writes the **kana reading** (the core vocab skill a
  grammar book never tests).
- **Answer key** per world section (back matter).

---

## 8. Review loop, native QA & recurring vocab defect classes

Keep an `<Level> vocabulary Book review Prompt.txt`. Pass order: programmatic scans (common §9) →
content read of every word (reading + POS + gloss + collocation + example) → layout montage of **all**
card + exercise pages. Fix in the JSON, re-render, re-verify. A **native QA pass** specifically checks
particle choice, naturalness, and over-literal example reuse on the §5 collocations.

**Recurring vocab defect classes (re-check the whole book each pass):**
1. **Wrong reading / missing furigana** (the dominant defect).
2. Wrong or free-text **POS**; transitive/intransitive mix-ups.
3. **Gloss** over-listed, wrong sense, mismatched to the example, or **not distinguished** from a
   near-duplicate (§4).
4. **Example** unnatural, above-level, or doesn't use the headword; voice mismatch (intransitive verb
   given a transitive English) (§4).
5. **Noun/する collocation duplication** (§5).
6. **Missing register / formal-usage tag** where a learner could produce unnatural Japanese (§4).
7. **Card-grid overflow** / reading collides with form (verify densest pages — clip-risk + visual).
8. **Matching** not uniquely solvable (two glosses too close).
9. **Index** incomplete, mis-ordered, page numbers stale; number detached from word (§6).
10. **Kanji-policy** inconsistency; katakana long-vowel (ー) errors; romaji leaking onto learning pages.
11. **Extraction artifacts mistaken for defects** (common §8) — e.g. `コンピュータcomputer`,
    `USE**_**…`, header merges.
12. Process: fixed one card but not its siblings; declared done with a check failing.

---

*Vocabulary-specific addendum to the common pipeline. Add new vocab defect classes here in the same
pass that fixes them.*
