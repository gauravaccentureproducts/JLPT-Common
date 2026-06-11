# JLPT N4 Vocabulary "Adventure" Workbook — Build Manual

Companion to **`grammar-adventure-workbook-build-manual.md`**. This builds the **N4 vocabulary**
edition of the kid-friendly "adventure" workbook: same look, same toolchain, same QA discipline —
but the content unit is a **word** (not a grammar gem), the pages are **word-card grids** (not
one-item-per-page), and the exercises and content risks are vocabulary-specific.

**Scope (locked for this edition):** full **~600-word N4 corpus** (the "N4-additional" set, i.e.
words beyond N5) · **one example sentence per word** · **N4-specific** · **reuse the grammar
workbook's look + pipeline**. The grammar manual stays the reference for any shared mechanics.

---

## 0. Quickstart + golden rules

```
# 0. Copy the grammar workbook's _wb_* toolchain; make vocab variants of the source stages.
# 1. Assemble the full ~600-word corpus            -> _n4_vocab_merged.json
# 2. Author one example sentence per word          (the big new content task)
# 3. Build the editor docx (applies VOCAB CORPUS_FIX)
python _n4_vocab_build_docx.py        # -> N4_Vocabulary_<N>_<stamp>.docx
# 4. Extract entries from the NEWEST docx (verbatim, validated)
python _wb_extract.py                 # -> _wb_vocab_entries.json
# 5. Build the workbook HTML (vocab taxonomy + card-grid layout)
python _wb_vocab_build.py             # -> N4_Vocab_Workbook/my-n4-vocabulary-adventure-complete.html
# 6. Render A5 PDF (Edge headless — identical flags to the grammar workbook, see grammar manual §11)
# 7. Gates (all must pass)
python _wb_vocab_verify.py ; python _wb_vocab_fidelity.py ; python _wb_vocab_practice_check.py
# 8. Impose 2-up A4   (python _wb_impose_2up.py, reused as-is)
# 9. Review loop to zero defects, then ship the bundle (PDF + 2-up + docx + BUGS)
```

Golden rules (the grammar rules carry over, plus two vocab-specific ones):
1. **Content is corrected at the DOCX layer only** (via `CORPUS_FIX`); the DOCX is the fidelity anchor.
2. **Every gate must pass before done.**
3. **The #1 vocabulary risk is a wrong reading (furigana).** Every kanji word's reading must be verified.
4. **The #2 risk is a wrong part of speech** (Noun vs suru-verb, godan vs ichidan, transitive vs intransitive).
5. **Keep the total page count even** (2-up has no blank half-sheet); **clip-risk must be 0** (dense card grids overflow easily).

---

## 1. What's reused vs what's new

| Reused from the grammar workbook (see its manual) | New / different for vocabulary (this manual) |
|---|---|
| Pipeline shape: source JSON → docx (+CORPUS_FIX) → extract → builder(+template+cats) → Edge render → 2-up (§2) | The **corpus** (~600 words) + its source/assembly (§2) |
| A5 geometry 148.5×210 mm, even page count, fonts, colour themes, full-bleed (§5) | The **word record** content model (§3) |
| Exact Edge render command + flags (§11) | The **vocab chapter taxonomy** (themes) (§4) |
| `_wb_impose_2up.py` (2-up A4), print guidance (§11) | **Word-card grid** page layout — the big change (§5) |
| Gate *concepts* (fidelity / clip-risk / answer-in-bank / even count) (§10) | **Example-sentence authoring** for ~600 words (§6) |
| Review-loop method + the dot-matching review component (§8, §12) | **Vocab exercises** + **word index** appendix (§7, §8) |
| Environment/Windows pitfalls — cp932, file locks, verify-don't-assume (§16) | **Vocab content rules** — readings, POS, kanji policy (§11) |
| Datetime-stamping, deliverable-bundle conventions (§15) | **Vocab-specific gates** — reading/POS sanity (§10) |

> The DOCX-as-fidelity-anchor contract and "corrections only at the docx layer" rule are **identical**
> — do not edit `_wb_vocab_entries.json`, the HTML, or the PDF directly.

---

## 2. The corpus (~600 N4 words)

- **Source:** the `JLPTSuccess/N4/n4-vocab-inventory-*.md` files document it — the ~100-entry *sample*
  exists; the full **~600 "N4-additional" words** are fetched from the **Tanos N4 vocab CSV**
  (tanos.co.uk/jlpt/jlpt4/vocab) cross-checked with the JLPT Sensei N4 list. ("N4-additional" = N4
  words that are not already in the N5 set; the N5 app's `data/vocab.json` is the de-dupe reference.)
- **Assembly target:** `_n4_vocab_merged.json` — one record per word (model in §3). De-dupe against
  N5; drop anything already taught at N5.
- Each word then needs **one authored example sentence** (§6) — this is the largest new task and the
  main quality risk after readings.

---

## 3. Content model (the word record)

```json
{
  "id": "n4v-001",
  "form": "上がる",                  // headword as written: kanji if it has one, else kana/katakana
  "reading": "あがる",                // kana reading (furigana); for kana/katakana words = the word itself
  "meaning": "to rise; to go up",    // English; primary sense first, don't over-list
  "pos": "Verb (godan, intransitive)", // controlled vocabulary (see §11)
  "example": { "ja": "ねだんが 上がりました。", "en": "The price went up." },
  "categoryOrder": 7                 // chapter index, stamped from the taxonomy (§4)
}
```

Notes: `reading` is **mandatory for every kanji word** and is what the card shows as furigana.
`romaji` is **not** stored for the learning pages (it's a crutch); if wanted, generate it only for the
back-of-book index. POS comes from a fixed controlled set so it can be validated (§10).

---

## 4. Chapter taxonomy (vocab "worlds")

~600 words ÷ ~16–18 chapters ≈ 35–40 words/chapter. Group **nouns by semantic theme** and put the
function words in **POS-based chapters**. Define in a vocab `_wb_cats.py`
(`(adventure_name, subtitle, ribbon, icon, colour, soft, [word-ids])`), same structure as grammar.

Suggested N4 starting taxonomy (refine to the real word distribution):

| # | Adventure name | Real theme |
|---|----------------|-----------|
| 1 | Family Town | People & family |
| 2 | Kitchen Garden | Food & drink |
| 3 | Cozy House | Home & daily life |
| 4 | Market Street | Shopping & clothing |
| 5 | School Gate | School & study |
| 6 | Work Plaza | Jobs & workplace |
| 7 | Travel Station | Transport, town & directions |
| 8 | Holiday Shore | Travel & leisure |
| 9 | Clock Tower | Time, dates & frequency |
| 10 | Health Spring | Body, health & feelings |
| 11 | Weather Hill | Nature, weather & animals |
| 12 | Action Dojo | Everyday verbs |
| 13 | Describe Meadow | Adjectives (い & な) |
| 14 | Express Avenue | Adverbs & set expressions |
| 15 | Number Vault | Numbers, counters & quantity |
| 16 | Katakana Cove | Loanwords (katakana) |
| 17 | Mind & Words | Communication & abstract nouns |

Naming rule carries over: the world name must fit **all** its words (don't put 食べる in a "nouns"
world). Verbs/adjectives/adverbs that belong to a theme can stay in the theme; the POS chapters
(12–14) catch the rest.

---

## 5. Page layout — word-card grids (the big difference)

Grammar gives each gem a full page; vocabulary cannot (600 pages). Instead use **word-card grids**.

**Card anatomy** (one per word):
- **Form** — the headword, large (kanji prominent).
- **Reading** — kana, shown small above/beside the form (**always shown** — a vocab book teaches the
  reading; this is the opposite of the grammar book, which omitted furigana on purpose).
- **POS tag** — a small coloured chip (Noun / Verb / い-adj / な-adj / Adverb / Expression …).
- **Meaning** — English.
- **Example** — the one sentence (JA + small EN), inside the card or as a sub-row.

**Density:** ~**6–10 words per A5 page** (fewer if the example sits inside each card, more if examples
are a compact sub-line). Tune so the full book lands ~**120–160 pages** (≈ even). A 2-column card grid
or single-column word rows both work — pick one and keep it uniform.

**Spine per chapter:** chapter intro → word-card pages → exercises (§7). Reuse the A5 template,
colour themes, mascot, cover/copyright/back-matter from grammar.

**Watch overflow:** dense grids are the most likely place to clip — the clip-risk gate (§10) must stay
0, and (per the grammar TOC lesson) clip-risk does **not** catch overlap with decorative bands, so
**eyeball the fullest card pages**.

---

## 6. Example-sentence authoring (~600 sentences)

Each word gets one example. Rules:
- **N4-readable:** the example may use only N5–N4 grammar and N5–N4 vocabulary, so a learner at this
  level can read it. Don't introduce a harder word to explain an easier one.
- Show the **headword in a natural, typical context**; the sentence should make the meaning obvious.
- Correct **kanji/kana policy** (§11); keep examples short (a card is small).
- No added gender the Japanese doesn't specify; UK/US spelling consistent in the EN (match the grammar
  book's UK choice for one house style).
- Generate drafts programmatically if helpful, but **hand-verify every one** — fabricated or unnatural
  examples are the second-biggest review burden after readings.

---

## 7. Exercise design (vocabulary)

Per chapter, after its word cards (reuse grammar's exercise components where possible):
- **Word ↔ meaning matching** ("draw a line") — reuse the grammar review-match component verbatim
  (one line per meaning + its dot, every meaning uniquely matchable, deranged shuffle; see grammar
  manual §8). Right-column = English meanings; left = the words.
- **Fill-in-the-blank** — the word used in a sentence; word bank = the chapter's words. The blank must
  test the **target word**, and the answer must be the word in its correct form.
- **Reading practice** — show a kanji word, learner writes the **kana reading** (vocab-specific; this
  is the core skill a grammar book never tests).
- **Recall (optional)** — English → write the Japanese word.
- **Answer key** per chapter section (back matter).

Keep the word bank built from the chapter's words (so the "answer in bank" gate works), and ensure
each item is answerable from what the page taught.

---

## 8. Appendices

- **Word index (essential for vocab)** — a kana/あいうえお-ordered, dictionary-style list:
  `word · reading · meaning · page`. Lets a learner look up any word. (Optionally a second index by
  English meaning.)
- **Kanji list** — the kanji used across the book, with readings, grouped or by stroke/level.
- **Answer key** — all exercise answers (matching pairs, cloze answers, readings).

The printed Table of Contents lists chapters (and can list the index/answer key); it need not list
every one of 600 words (unlike the grammar TOC) — the **word index** is the per-word lookup.

---

## 9. Build procedure (steps)

1. **Assemble + de-dupe** the ~600-word corpus → `_n4_vocab_merged.json` (§2).
2. **Author examples** (§6) and fold into the corpus (or a `_n4_vocab_generated.py` for drafts).
3. **Build the editor DOCX:** `python _n4_vocab_build_docx.py` → `N4_Vocabulary_<N>_<stamp>.docx`
   (applies the vocab `CORPUS_FIX`; emits per word: form, reading, meaning, POS, example).
4. **Extract:** `python _wb_extract.py` (vocab variant) → `_wb_vocab_entries.json`; validate every word
   has form+reading+meaning+pos+example.
5. **Taxonomy:** define the vocab `_wb_cats.py` (§4).
6. **Build HTML:** `python _wb_vocab_build.py` (card-grid layout) — confirm word count = corpus size and
   page count is **even**.
7. **Render A5 PDF** (Edge, grammar manual §11).
8. **Gates** (§10) — fix at the correct layer, rebuild, re-render, re-gate.
9. **Impose 2-up:** `python _wb_impose_2up.py` (reused).
10. **Review loop** (§12) to zero defects.
11. **Ship** the bundle (§14).

---

## 10. QA gates (adapted) + vocab-specific gates

Reused gate *concepts* (grammar manual §10), with vocab fields:

| Gate | Checks |
|------|--------|
| `_wb_vocab_verify.py` | page_count == expected page-type sequence; **clip-risk 0** (no card/grid overflow) |
| `_wb_vocab_fidelity.py` | every word's **form + reading + meaning + POS + example (ja/en)** appears VERBATIM in the PDF vs the docx (count = words × fields) |
| `_wb_vocab_practice_check.py` | every exercise answer (matching pair / cloze / reading) is present in its word bank / answer key |

**New vocab-specific checks (add to verify):**
- **Reading present + kana-only** for every kanji word (no missing furigana; reading contains no kanji).
- **POS in the controlled set** (flag any free-text POS).
- **No romaji on learning pages** (romaji, if any, only in the index).
- **Katakana long-vowel marks** present where expected; **no kanji above N4 policy** on a card without
  a kana fallback.

Plus the invariants: **even page count**, and **regenerate the 2-up after any change**.

---

## 11. Vocabulary content rules (the critical risks)

1. **Readings (#1).** Every kanji word's kana reading must be correct. Verify against a dictionary;
   watch multi-reading kanji (音/訓), special/irregular readings (今日=きょう, 上手=じょうず), rendaku
   (e.g. 時 → どき in 何時), and counter readings (一杯/一匹 sound changes).
2. **Part of speech (#2).** Use a fixed controlled set: Noun, Noun (suru-verb), Verb (godan / ichidan,
   transitive / intransitive), い-adjective, な-adjective, Adverb, Pre-noun adjectival, Expression,
   Conjunction, Counter, Katakana noun. Get transitive/intransitive pairs right (上がる/上げる,
   開く/開ける) — these are classic N4 traps.
3. **Meanings.** Primary sense first; include only the senses an N4 learner needs; don't over-list.
   Match the example to the listed sense. No gender the JP doesn't specify.
4. **Kanji policy.** Show N4-level kanji with reading; words whose kanji are above N4 appear in kana.
   Be consistent across cards, examples and index.
5. **Katakana / loanwords.** Correct long-vowel marks (ー), standard katakana orthography.
6. **No romaji crutch** on the learning pages.
7. **Corrections go in the vocab `CORPUS_FIX`** (docx layer), keyed by word id.

---

## 12. Review loop (vocab review prompt)

Keep an `N4 vocabulary Book review Prompt.txt` (seed from the grammar review prompt, swap the focus).
The reviewer checks, per word and per page:
- **Reading** correct (spot the furigana errors — the highest-yield check).
- **POS** correct + from the controlled set.
- **Meaning** faithful, matches the example.
- **Example** natural, N4-readable, shows the word in typical use.
- **Exercises** answerable; matching is uniquely solvable (no two meanings collide); reading-practice
  items have a single correct kana answer.
- **Layout** — no card/grid overflow; reading legibly placed; index complete and correctly kana-ordered.
- **Hygiene** — no romaji leakage on learning pages, no provenance tags, UK/US spelling consistent.

Pass order, fixes, and the BUGS log work exactly as in the grammar manual §12. Verify **every** card
page and **every** exercise (montage them), not a sample.

---

## 13. Recurring defect classes (vocab checklist)

1. **Wrong reading / missing furigana** (the dominant vocab defect).
2. **Wrong or free-text POS**; transitive/intransitive mix-ups.
3. **Meaning** over-listed, wrong sense, or mismatched to the example.
4. **Example** unnatural, above-level, or doesn't actually use the headword.
5. **Kanji-policy** inconsistency (kanji on one card, kana for the same word elsewhere).
6. **Card-grid overflow** / reading collides with form (clip-risk + visual).
7. **Matching exercise** not uniquely solvable (two meanings too close — see grammar §8).
8. **Index** incomplete, mis-ordered, or page numbers stale.
9. **Romaji leakage** onto learning pages; **katakana** long-vowel errors.
10. **Even page count / 2-up** broken; stale 2-up after a content change.
11. **Process:** fixed one card but not its siblings; declared done with a gate failing.

---

## 14. Print + deliverables

- **Print + 2-up:** identical to the grammar workbook — render A5, impose with `_wb_impose_2up.py`,
  print the 2-up at Actual-size + Landscape + duplex, borderless if available (grammar manual §11).
- **Deliverable bundle** (e.g. `JLPTSuccess/N4/vocab-workbook/`): newest
  `my-n4-vocabulary-adventure-complete_<stamp>.pdf`, `...-2up-A4_<stamp>.pdf`,
  `N4_Vocabulary_<N>_<stamp>.docx`, and `N4_Vocabulary_BUGS.csv`. Datetime-stamp every output; keep one
  current copy of each; remove superseded stamps.

---

## 15. Environment & tooling pitfalls

Identical to the grammar workbook — **see `grammar-adventure-workbook-build-manual.md` §16**
(cp932 console mangles Japanese in `python -c` → write to UTF-8 files and read back; open PDF viewers
lock files; the extractor/fidelity pick the newest docx by mtime; verify by rendering, not by assuming).
One vocab addition: when scanning/validating readings programmatically, do the kana/kanji checks on
file data (never via Japanese literals in `python -c`).

---

*This manual encodes the N4 vocabulary edition's plan; it inherits the grammar workbook's build
machinery and QA discipline. When the build surfaces a new vocab defect class or invariant, add it
here in the same pass that fixes it.*
