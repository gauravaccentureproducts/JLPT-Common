"""Restructure procedure-manual-build-next-jlpt-level.md into 5 chapters.

Run from JLPT Common/ root:
    python restructure_to_5_chapters_2026_05_13.py

Produces procedure-manual-build-next-jlpt-level.NEW.md alongside the
original (does NOT overwrite — manual swap step at the end).

Chapters (matching the 5-step summary):
    1. Foundation  — bootstrap, scope, schema, permissions, migration
    2. Safety nets — build pipeline, CI invariants, tooling
    3. Content     — authoring strategy, anti-patterns, KB rules
    4. Interface   — UI / front-end, audio, mobile, PWA
    5. Review      — audits, native review, process discipline, anti-pattern lists

The script preserves the internal sub-section structure of each block,
so existing cross-references like "see §3.2.27" or "§B.8" still resolve
because the §3.2.27 anchor stays inside its block; the block just moves
to a different chapter.
"""

import re
from pathlib import Path

SRC = Path("procedure-manual-build-next-jlpt-level.md")
DST = Path("procedure-manual-build-next-jlpt-level.NEW.md")


# Map of "block-start heading text" -> chapter number.
# Order in the file is preserved within each chapter.
# Headings that start with "## " (top-level) OR with "# §" / "# Native" / "# Appendix"
# (mid-document re-h1-injections) are treated as section starts.
ASSIGN = {
    # ---- Preamble (lives before Chapter 1, untouched) ----
    "## How to read this manual: level placeholders": 0,  # 0 = preamble

    # ---- Chapter 1: Foundation ----
    "## 0.A One-instruction autonomous-build contract": 1,
    "## ⚠ Operating modes — read this first": 1,
    '## 0. Scope of "next level"': 1,
    "## 1. Day 0 — Repo bootstrap (1-2 hours)": 1,
    "## 11. Migration considerations from level <P> to level <L>": 1,
    "## 13. Estimated total effort": 1,

    # ---- Chapter 2: Safety nets ----
    "## 2. Phase 1 — Foundation (week 1)": 2,
    "## 6. Phase 5 — Quality gates (continuous)": 2,
    "## 7. Tooling that paid off — port these scripts": 2,

    # ---- Chapter 3: Content ----
    "## 3. Phase 2 — Content authoring strategy (weeks 2-8)": 3,
    "## 10. N5-specific wins to keep": 3,
    "# §20 Vocab.json structural rules + dedup tooling pattern (added 2026-05-09)": 3,

    # ---- Chapter 4: Interface ----
    "## 4. Phase 3 — UI / Front-end (weeks 4-9, parallel with content)": 4,

    # ---- Chapter 5: Review ----
    "## 5. Phase 4 — Audit cadence (continuous, weeks 6+)": 5,
    "## 8. Process discipline": 5,
    "## 9. External-blocked items — anticipate up front": 5,
    "## 12. What we learned about working with Claude Code": 5,
    "## 14. Anti-patterns from N5 — the bumper-sticker list": 5,
    "## 15. Open questions / decisions to make for N<L>": 5,
    "## 16. References": 5,
    "## 17. Appendix A — One-Shot Mode supplements": 5,
    "## 18. Pass-20 review findings — disposition": 5,
    "# §19 Native-teacher audit playbook (added 2026-05-09)": 5,

    # ---- Appendices (remain after Chapter 5, untouched) ----
    "# §B Appendix B — Schemas & rules extracted from N5 (merged 2026-05-04)": 6,  # 6 = appendix
    "# Procedure Manual Appendix B — Extracted from N5 Codebase": 6,
    "# §C Appendix C — JLPT-N5 audit-pass closure summary (merged 2026-05-08)": 6,
    "# Procedure Manual Appendix C — closure notes from N5 audit Passes 20–24": 6,
    "# §D TASKS.md canonical template (merged 2026-05-04)": 6,
    "# TASKS.md — Canonical Template": 6,
    "# Appendix C — Session learnings 2026-05-10/11 (UI-audit + content-enrichment cycle)": 6,
    "# Appendix D — 2026-05-12 / 2026-05-13 Audit Cycle Learnings": 6,
}

CHAPTER_TITLES = {
    1: "# Chapter 1: Foundation",
    2: "# Chapter 2: Safety Nets",
    3: "# Chapter 3: Content",
    4: "# Chapter 4: Interface",
    5: "# Chapter 5: Review",
    6: "# Appendices",
}

CHAPTER_INTROS = {
    1: ("> **Foundation** — start by copying what already works from the previous "
        "level. Decide ground rules (scope, schema, permissions, level-to-level "
        "migration) before any content is authored. Time-budget the build."),
    2: ("> **Safety nets** — set up automatic quality checks before writing any "
        "content. Build pipeline, CI invariants, integrity gates, and the tooling "
        "that catches regressions before they ship."),
    3: ("> **Content** — write the lessons: grammar, vocabulary, kanji, reading, "
        "listening. KB-first markdown → derive JSON. Apply the anti-patterns at "
        "§3.2.x to avoid repeating N5 mistakes."),
    4: ("> **Interface** — build the app screens so learners can use the content. "
        "Vanilla static + PWA + audio pipeline + mobile contract + cache discipline."),
    5: ("> **Review** — keep reviewing for errors; a native Japanese teacher gives "
        "final approval. Audits, process discipline, AI-assistant lessons, and the "
        "bumper-sticker anti-pattern list live here."),
    6: ("> **Appendices** — schemas, templates, and dated session-learning notes. "
        "Reference material; not part of the linear procedure."),
}


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    lines = text.split("\n")

    # --- Parse top-level blocks ---
    # A block starts at a heading line that matches one of:
    #   ^## [0-9⚠A]                — primary structure (## 0., ## 0.A, ## ⚠, ## 1., etc.)
    #   ^# §                       — re-injected h1 like # §19 Native-teacher
    #   ^# Appendix                — re-injected h1 like # Appendix C
    #   ^# Procedure Manual Appendix — appendix re-heading
    #   ^# TASKS.md                — Tasks template re-heading
    #   ^# Native Japanese JLPT    — sub-template (kept inside its parent)
    # The doc title "# Procedure Manual — Building..." (line 1) is special.
    boundary_re = re.compile(
        r"^(##\s+(?:[0-9]|⚠|A\.|B\.|C\.|D\.)|#\s+§|#\s+Appendix|#\s+Procedure Manual Appendix|#\s+TASKS\.md)"
    )

    blocks = []  # list of dicts: {start, heading, lines}
    current = None
    preamble_lines = []
    in_preamble = True
    title_line = lines[0] if lines else ""

    for i, line in enumerate(lines):
        if i == 0:
            continue  # keep doc title for the final emit, skip here
        if boundary_re.match(line):
            # close any in-flight block
            if current is not None:
                blocks.append(current)
            current = {"start": i, "heading": line.strip(), "lines": [line]}
            in_preamble = False
        else:
            if in_preamble:
                preamble_lines.append(line)
            elif current is not None:
                current["lines"].append(line)
    if current is not None:
        blocks.append(current)

    # --- Classify each block ---
    unmapped = []
    chapter_blocks = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
    preamble_blocks = []
    for b in blocks:
        h = b["heading"]
        # Match against ASSIGN keys: prefer exact match
        ch = ASSIGN.get(h)
        if ch is None:
            # Fuzzy: try matching by leading prefix up to first significant punct
            for key, val in ASSIGN.items():
                if h.startswith(key.split("(")[0].rstrip()):
                    ch = val
                    break
        if ch is None:
            unmapped.append(h)
            # Default fallback: put unrecognized blocks in appendices
            ch = 6
        if ch == 0:
            preamble_blocks.append(b)
        else:
            chapter_blocks[ch].append(b)

    # --- Emit new file ---
    out = []
    out.append(title_line)
    out.append("")
    out.append(
        "**Source project:** JLPT N5 Tutor (this repo)  "
        "\n**Target audience:** any future JLPT level app (N4, N3, N2, N1) using the same architecture  "
        "\n**Prepared:** 2026-05-01 from accumulated N5 build experience (Phases 1-5 + Passes 1-19)  "
        "\n**Restructured:** 2026-05-13 into 5 chapters (Foundation / Safety Nets / Content / Interface / Review) for readability  "
        "\n**Status:** Living document — update as each next-level build adds new lessons"
    )
    out.append("")
    out.append(
        "This manual is written prescriptively. Where N5 hit a problem, the manual tells the next level how to avoid it. Generic best-practice advice has been omitted; only N5-specific learnings are included."
    )
    out.append("")
    out.append("---")
    out.append("")

    # TOC
    out.append("## Table of Contents")
    out.append("")
    for ch in range(1, 7):
        out.append(f"- **{CHAPTER_TITLES[ch].lstrip('# ')}**")
        for b in chapter_blocks[ch]:
            h = b["heading"]
            # Strip leading # markers for TOC display
            display = re.sub(r"^#+\s+", "", h)
            out.append(f"  - {display}")
    out.append("")
    out.append("---")
    out.append("")

    # Preamble lines (e.g. "How to read this manual: level placeholders"
    # — the section after the doc title but before the first boundary heading).
    if preamble_lines:
        for line in preamble_lines:
            out.append(line)
        out.append("")
    # Preamble blocks (explicitly chapter=0 assignments — currently none, but kept
    # for future expansion).
    for b in preamble_blocks:
        out.extend(b["lines"])
        out.append("")

    # Chapters 1-5
    for ch in range(1, 6):
        out.append("")
        out.append("---")
        out.append("")
        out.append(CHAPTER_TITLES[ch])
        out.append("")
        out.append(CHAPTER_INTROS[ch])
        out.append("")
        for b in chapter_blocks[ch]:
            out.extend(b["lines"])
            out.append("")

    # Appendices
    out.append("")
    out.append("---")
    out.append("")
    out.append(CHAPTER_TITLES[6])
    out.append("")
    out.append(CHAPTER_INTROS[6])
    out.append("")
    for b in chapter_blocks[6]:
        out.extend(b["lines"])
        out.append("")

    new_text = "\n".join(out)
    DST.write_text(new_text, encoding="utf-8")

    # --- Report ---
    print(f"Source: {SRC} ({len(text)} chars, {len(lines)} lines)")
    print(f"Dest:   {DST} ({len(new_text)} chars, {new_text.count(chr(10))} lines)")
    print()
    print(f"Blocks parsed: {len(blocks)}")
    print(f"Preamble blocks: {len(preamble_blocks)}")
    for ch in range(1, 7):
        print(f"  Chapter {ch} ({CHAPTER_TITLES[ch].split(': ')[-1] if ':' in CHAPTER_TITLES[ch] else 'Appendices'}): {len(chapter_blocks[ch])} blocks")
    if unmapped:
        print(f"\nUNMAPPED blocks (fell into appendix):")
        for h in unmapped:
            print(f"  {h}")
    else:
        print("\nAll blocks were explicitly mapped — clean restructure.")


if __name__ == "__main__":
    main()
