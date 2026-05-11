# Procedure Manual Review - Issues

**Source document:** `procedure-manual-build-next-jlpt-level.md` (584 lines, prepared 2026-05-01)
**Lens applied:** zero-interaction one-shot agent execution. The analysis treats the manual as if it must produce a complete N4/N3/N2 application without further clarification, with no human supplying missing inputs.

---

## Issue 1
- **Location (section / step):** §0 "Scope of next level" + §11.2 "Kanji policy escalation"
- **Issue description:** The manual gives kanji/vocab/grammar count *targets* (~280 kanji, ~1500 vocab, ~210 grammar patterns for N4) but does not provide the *content* of those lists. There is no embedded N4 kanji inventory, no N4 vocabulary inventory, no N4 grammar pattern catalog, and no source list URL the agent must fetch from. The agent is told the size of the deliverable but not its identity.
- **Severity:** Critical
- **Impact on one-shot app generation:** The agent cannot author KnowledgeBank markdown files for N4 grammar, kanji, or vocab without first independently determining what those items are. This will either force the agent to invent content (untrustworthy and likely wrong) or to halt and ask. Multiplies across N3/N2/N1 since the same gap applies to all higher levels.

## Issue 2
- **Location (section / step):** §3.3 "Authoring cadence" + §11.3 "Borderline grammar promotion"
- **Issue description:** No procedural definition of *how* an authoring step works for content. The cadence table says "Week 2-3: Grammar catalog" producing "grammar.json with N4 patterns" but does not specify: which sources to consult, how to verify pattern is N4 (vs N3 or N5), how many examples per pattern, what fields the entry must populate, or how to derive the meaning_en / meaning_ja text.
- **Severity:** Critical
- **Impact on one-shot app generation:** The "what to do" is described at the level of weekly milestones, not at the level of an executable instruction. An agent trying to execute "author the grammar catalog" has no defined inputs, no defined process, no defined output schema, and no defined acceptance test for an individual entry.

## Issue 3
- **Location (section / step):** §1.3 "Schema decisions to lock in NOW" - JSON schemas
- **Issue description:** The manual references field names (`schema_version`, `entity_count`, `id_range`, `id_gap_policy`, `history`, `auto`, `tier`) without providing the full JSON schema for any data file (grammar.json, vocab.json, kanji.json, reading.json, listening.json, questions.json). There is no indication of required vs optional fields, types, value enumerations, or nesting structure. The "copy from N5" instruction assumes the agent has access to the N5 repo; the manual itself does not contain the schema.
- **Severity:** Critical
- **Impact on one-shot app generation:** The agent cannot generate well-formed JSON without the schema. References to fields like `examples`, `form_rules`, `meaning_en`, `meaning_ja`, `furigana`, `vocab_ids`, `audio`, `format_type`, `tier`, `level`, `topic` appear scattered across §2.2 invariants and §3 cadence but are never collected into a canonical contract.

## Issue 4
- **Location (section / step):** §1 "Day 0" + §16 "References"
- **Issue description:** The manual repeatedly says "copy from N5" / "port verbatim" / "see N5 spec" but the N5 source files (`KnowledgeBank/*.md`, `data/*.json`, `tools/*.py`, `specifications/jlpt-n5-design-system-zen-modern.md`, `.claude/CLAUDE.md`, `js/*`, `index.html`) are not bundled with the manual nor declared as required inputs.
- **Severity:** Critical
- **Impact on one-shot app generation:** A coding agent operating against this manual alone (without the N5 repo at hand) cannot satisfy any "copy from N5" instruction. The dependency is implicit. If the directive is "you also have access to the N5 repo," this needs to be stated explicitly as a precondition with a path or URL.

## Issue 5
- **Location (section / step):** §4 "Phase 3 - UI / Front-end" (entire section)
- **Issue description:** §4.1 says "no framework, vanilla static, ~3000 lines of JS across ~25 modules" but does not enumerate which modules, their responsibilities, their API contracts, or their interactions. §4.2 lists Day-1 features as bullets ("5-card Learn hub", "TOC collapsible by super-category", "SM-2 SRS in Review tab") with no design specs, no component breakdowns, no state-management contract, and no routing table.
- **Severity:** Critical
- **Impact on one-shot app generation:** The agent has feature names but no UI specifications. "Pattern detail page with prev/next nav at top corners (small font, peripheral)" is stylistic prose, not implementable. There is no wireframe, no DOM contract, no event-handler list, no localStorage schema, no CSS architecture beyond pointing at the design-system spec.

## Issue 6
- **Location (section / step):** §4.4 "Audio" + §1.1 directory structure
- **Issue description:** `data/audio_manifest.json` is referenced and `build_audio.py` is mentioned but the manifest's structure is not defined, the audio item naming convention is not specified, the relationship between `audio` paths in `listening.json` / `reading.json` / `grammar.json` and the manifest is not specified, and the per-item voice metadata (e.g., the VOICEVOX speaker-tag field documented in N5) is absent. §10 mentions "audio refs resolve" as invariant JA-15 but doesn't define what a resolvable ref looks like.
- **Severity:** Major
- **Impact on one-shot app generation:** The agent cannot produce a runnable audio pipeline without the manifest schema. Audio is integral to listening drills; missing this blocks the listening module entirely.

## Issue 7
- **Location (section / step):** §3.2 "Anti-patterns from N5" + §6 "Phase 5 quality gates"
- **Issue description:** The manual provides 14 anti-patterns and 24 invariants (X-6.1 through JA-24) as descriptive prose but no executable specifications. For example, JA-2 says "Particle MCQs have valid particle distractors" without defining what makes a particle distractor "valid" (which particles count? which combinations are forbidden?). JA-23's "known-interchangeable particle pairs" lists `に`/`へ`, `から`/`ので`, `は`/`が` but doesn't say whether `を`/`が` (with stative predicates) or `に`/`と` (recipient vs companion) are also blocked.
- **Severity:** Major
- **Impact on one-shot app generation:** The agent cannot implement `tools/check_content_integrity.py` without each invariant being a precise, testable rule. "Comparable density" or "manageable false-positive rate" (used in §5.4) are subjective. An invariant that cannot be unit-tested will not be enforced.

## Issue 8
- **Location (section / step):** §1.3 "tier taxonomy" + §11.1
- **Issue description:** The tier taxonomy `core_n4`/`late_n4`/`n3_borderline` is named but the rule for assigning a tier to a specific pattern is not given. There is no list of which N4 patterns belong in which tier, no decision tree, and no source authority (Bunpro? Genki? Minna no Nihongo? Imabi?). §11.3 says "plan ~30-40 such promotions" but does not list the patterns being promoted, only points at "the N5 pattern catalog `late_n5` tier" as a source.
- **Severity:** Major
- **Impact on one-shot app generation:** Tier classification is a per-pattern judgement requiring source authority. Without a defined mapping, the agent will assign tiers inconsistently or have to skip the field, breaking JA-21 (and the new N4-equivalent JA invariant referenced in §2.2).

## Issue 9
- **Location (section / step):** §0 + §11 (cross-level scaling)
- **Issue description:** The manual's claim that "N3+ is mostly content scaling" is asserted without evidence and the level transitions N3→N2→N1 are described only via the count table in §0. There is no specific content for: kanji whitelist beyond ~280 (no list for N3, N2, or N1), reading-passage authentic-style guidance, listening-pace targets, JLPT exam structure differences (e.g., N1 has no "Mondai 4 短文" in the same form), or scoring breakdown changes.
- **Severity:** Major
- **Impact on one-shot app generation:** A user generating an N3, N2, or N1 app from this manual gets the same gaps multiplied. The manual is N4-specific despite presenting itself as a generic template. An agent attempting N2/N1 would face larger, undocumented content jumps.

## Issue 10
- **Location (section / step):** §3.4 "External corpus extraction"
- **Issue description:** The manual instructs "do NOT copy verbatim into your bank - copyright" and prescribes triangulation only. But it does not provide: the URL list to extract from, fair-use boundaries, attribution requirements, or what triangulation output looks like. `tools/coverage_compare.py` is referenced as a tool to port; its inputs and outputs are not specified.
- **Severity:** Major
- **Impact on one-shot app generation:** The agent cannot execute "extract questions from a third-party N4 site" without the source list. WebFetch operates on URLs that must be supplied. A coding agent running zero-interaction will skip this step or web-search arbitrarily.

## Issue 11
- **Location (section / step):** §2.2 "Content integrity invariants" - invariant naming
- **Issue description:** Invariants are stated under "X-6.x" and "JA-x" naming with cross-references to N5 "Pass-N" cycles ("Pass-7", "Pass-13", etc.). The Pass-N history is not contained in the manual; it's referenced as if the reader already knows what each Pass cycle did. JA-21 says "rename for N4" without specifying the new name.
- **Severity:** Major
- **Impact on one-shot app generation:** The invariant names are opaque without context, and the rename instruction is ambiguous (rename `JA-21` to `JA-21'`? to `JA-21-n4`? leave the ID and update the rule?). An agent implementing the integrity checker will produce a tool with N5-specific names baked in, contradicting "reusable across levels."

## Issue 12
- **Location (section / step):** §3.2.1 "Don't auto-generate filler MCQs"
- **Issue description:** The manual prohibits agent-generated filler MCQs but does not define what counts as filler vs. legitimate MCQ. "If you find yourself wanting to generate filler MCQs because the bank looks small: the bank is small for a reason - author real questions, or accept fewer." This is human-directed advice; an automated agent has no introspection about whether it is "wanting" to generate filler. A purely instruction-following agent might generate any number of MCQs as long as none of them match the specific failed-pattern stem.
- **Severity:** Major
- **Impact on one-shot app generation:** The agent has no clear stop-condition for question generation. Without a target count + "stop when running out of authentic templates," the agent will overgenerate or undergenerate. The N5 number (100 per question file = 400 total) is buried in §3.3's cadence table but not declared as an authoritative target for N4.

## Issue 13
- **Location (section / step):** §3.2.3 "Don't ship 'see pattern detail' as a distractor explanation"
- **Issue description:** The manual prescribes "author all distractor explanations by hand (or LLM-author then native-review)" and provides ONE example. There is no template, no explanation-quality rubric, no length range, no language register guidance, and no enumeration of the contrasts the explanation must make.
- **Severity:** Major
- **Impact on one-shot app generation:** The agent cannot reliably produce ~1500-2400 distractor explanations (4 per question × 400 questions, minus the correct answers) at consistent quality. Each will be ad-hoc. The manual's only quality guard is "or native review", which presumes a human in the loop and contradicts the one-shot premise.

## Issue 14
- **Location (section / step):** §1.1 directory structure - i18n / locales
- **Issue description:** The directory structure shows `locales/` and §10 references "5-locale i18n shell (en/vi/id/ne/zh)" but the manual provides no translation source files, no message catalog format, no string-extraction pipeline, no fallback policy, and no rule for handling new strings authored at N4. Translations of N4 grammar explanations into Vietnamese / Indonesian / Nepali / Simplified Chinese are not addressed at all.
- **Severity:** Major
- **Impact on one-shot app generation:** The agent will either skip i18n entirely or generate placeholder English everywhere, breaking the stated 5-locale parity.

## Issue 15
- **Location (section / step):** §11.2 "Kanji policy escalation" - prerequisite handling
- **Issue description:** The recommendation is "include all N5+N4 in the whitelist (~280 total) and use the `tier` field on each kanji entry to distinguish prerequisite vs new." But the kanji entry's tier values are not enumerated (`prerequisite_n5` vs `new_n4`? `core_n4` vs `prerequisite`? Same tier names as grammar?). The relationship between the kanji-tier field and the grammar-tier field is not specified, and how they interact with the level-strict integrity invariants (JA-13 "no out-of-scope kanji") is undefined.
- **Severity:** Major
- **Impact on one-shot app generation:** Agent will pick an arbitrary tier-naming convention. Subsequent CI checks will not match. The same issue compounds for N3 (must include N4+N3 prerequisites? all four?) and is not addressed.

## Issue 16
- **Location (section / step):** §10 "Zen Modern design system"
- **Issue description:** The design system spec is referenced as `specifications/jlpt-n5-design-system-zen-modern.md` and described in three lines ("hairlines not borders, no shadows, no gradients, weights 300/400/500 only"). The spec itself is not embedded. Without the spec, the agent has no design tokens, type scale, color tokens, component definitions, or page-by-page layouts.
- **Severity:** Major
- **Impact on one-shot app generation:** The UI generation step has only a one-line aesthetic constraint and a file path. Result will diverge significantly from the N5 baseline unless the spec file is provided alongside the manual.

## Issue 17
- **Location (section / step):** §2.1 "Build pipeline first"
- **Issue description:** The build pipeline is described as "KB markdown → JSON" but the parsing rules ("`^- \*\*([一-鿿]+)\*\*` for kanji headers", "section headers + entry lines for vocab", "`### Q\d+` headers" for questions) are partial regex fragments in prose. There is no full grammar for any KB markdown file, no error-handling spec for malformed input, no conflict-resolution rule (e.g., what happens if two patterns in different files share an ID?), and no idempotency definition beyond "re-running on unchanged input = no diff."
- **Severity:** Major
- **Impact on one-shot app generation:** The agent must invent the markdown grammar to write the parser. This will not be byte-compatible with the N5 build pipeline. Subsequent JSON-derived data will diverge silently.

## Issue 18
- **Location (section / step):** §1.3 "Vocab IDs"
- **Issue description:** The vocab ID format `n4.vocab.<section-slug>.<form>[.<disambiguator>]` requires a section-slug encoding. The set of valid section-slugs is not defined, the slug-derivation rule from section title is not given, and the disambiguator rule (numeric? semantic? alphabetic?) is not specified. "Cross-listed in multiple thematic sections" is mentioned but the canonical cross-listing manifest is not provided.
- **Severity:** Major
- **Impact on one-shot app generation:** Different agents (or the same agent on different runs) will produce different IDs for the same word. Cross-listings will be inconsistent. Pattern-to-vocab linkage (link_grammar_examples_to_vocab.py) will fail.

## Issue 19
- **Location (section / step):** §4.4 "Audio" + §10 "self-hosted fonts"
- **Issue description:** The manual instructs "self-hosted fonts subset to N4 kanji range" and "audio: at least listening items SHOULD be native-recorded" but provides neither the subsetting toolchain (pyftsubset? glyphhanger? a specific config?) nor the recording-pipeline spec (sample rate, format, normalization, file naming convention beyond `audio/listening/n4.listen.NNN.mp3`). Native recording is described as an external-blocked item; no fallback procedure for the agent to ship a runnable build is given.
- **Severity:** Major
- **Impact on one-shot app generation:** Either the agent will produce a build with broken audio (since native recordings can't be obtained zero-interaction) or it will use synthetic audio and be silently violating §4.4's "synthetic prosody artifacts at N5 level are tolerable; at N4 they teach learners to discriminate against synthesis artifacts." The procedure offers no defined fallback.

## Issue 20
- **Location (section / step):** §13 "Estimated total effort"
- **Issue description:** The manual states a 17-25 week solo+AI timeline. This is incompatible with "one-shot generation" by a coding agent. The manual is implicitly written for a months-long human-and-agent collaboration, not for a single-pass agent execution. There is no compressed-timeline guidance, no priority-stack identifying the minimum-viable subset.
- **Severity:** Major
- **Impact on one-shot app generation:** The agent reading the manual cannot know whether to attempt full content authoring (impossible in one shot) or scaffold-only (which violates "fully inclusive, production-ready"). The contract between manual and agent is undefined.

## Issue 21
- **Location (section / step):** §5 "Audit cadence" + §5.3 "Native teacher review window"
- **Issue description:** The manual treats native-teacher review as a required quality gate ("don't skip native review before declaring 'done'") but does not provide a fallback procedure when no native reviewer is available. §9 lists "native teacher reviewer (~10-12 hours per full pass)" as external-blocked. Per §13, native-reviewer parallelism is the difference between the 17-25w and 13-19w timelines.
- **Severity:** Major
- **Impact on one-shot app generation:** A zero-interaction agent has no native reviewer. The manual's quality contract assumes one. The agent has no documented "ship-without-review" path that would still produce a defensible product.

## Issue 22
- **Location (section / step):** §3.2.4 "Don't use ko-so-a-do without spatial context" + general question authoring
- **Issue description:** The manual gives one example of how to add scene-setting to a ko-so-a-do question but no procedural rule covering: when to add scene context, what makes scene context sufficient, the format of the scene-direction prefix (parentheses? bracketed? prose?), and which kanji policy applies to scene text (§3.2.4 example uses `自分` and `中` which are N3-N4 kanji even at N5 level).
- **Severity:** Minor
- **Impact on one-shot app generation:** Inconsistent scene-context formatting across the question bank. Not catastrophic but visibly unprofessional.

## Issue 23
- **Location (section / step):** §3.2 "Don't introduce new grammar pattern entries with the same `pattern` string" (§3.2.6)
- **Issue description:** The rule prescribes a grep before authoring but does not specify how the agent should resolve conflicts when found. "Decide: split intentionally OR retire-and-replace" pushes the decision to the human author. For a one-shot agent, there is no decision authority.
- **Severity:** Minor
- **Impact on one-shot app generation:** Agent must invent a tie-breaking rule. Risk of either silent data loss (retire without replacement) or runtime collisions (both kept).

## Issue 24
- **Location (section / step):** §1.2 "TASKS.md" + §8.1
- **Issue description:** TASKS.md is described as the "single source of truth" with very specific section structure (`Live site`, `Status snapshot`, `External-blocked backlog`, `## Pass-N`) but no template. The status-snapshot fields (corpus counts, SW version, vocab/kanji counts, route list) are not enumerated. Update rules ("update on every significant change") are not formally testable.
- **Severity:** Minor
- **Impact on one-shot app generation:** Agent will produce a TASKS.md that diverges in structure from N5. Subsequent Pass-N audits referenced in §5 will operate on a different format than expected.

## Issue 25
- **Location (section / step):** §15 "Open questions / decisions to make for N4"
- **Issue description:** Six unresolved decisions are listed (native voice budget, handwriting, IME-typing, speed-test mode, mock-test timing, monetization) and labeled as blocking ~1-2 weeks of architecture each. The manual does not declare default decisions for an agent operating without a human stakeholder.
- **Severity:** Major
- **Impact on one-shot app generation:** A zero-interaction agent encountering "decide before week 4 of the build" has no decider. Either the agent halts, picks defaults arbitrarily, or omits these features entirely. Either way, output is not "production-ready."

## Issue 26
- **Location (section / step):** §2.2 invariants table - JA-3 (Furigana / catalog match)
- **Issue description:** Furigana handling is mentioned as an invariant ("furigana annotations match catalog entries") but no procedure for *generating* furigana annotations is given. Should the agent generate them per-example via mecab/kuromoji? Per-passage? Manually? The "three-mode furigana" toggle described in §10 implies runtime CSS-based hide/show requires `<ruby>` markup, which is upstream content authoring.
- **Severity:** Major
- **Impact on one-shot app generation:** Furigana coverage at N4 is critical (most passages mix N4 and N5 kanji). Without a generation procedure, the agent will either produce no furigana, machine-generated furigana with errors, or inconsistent partial coverage.

## Issue 27
- **Location (section / step):** §2.2 "Content integrity invariants" - JA-2 particle distractors, JA-23 multi-correct scanner
- **Issue description:** The two particle-related invariants overlap and partially contradict. JA-2 requires "valid particle distractors" but JA-23 says certain pairs are flagged for native review. The interaction (does flagged-by-JA-23 fail JA-2? does JA-23 flag mean reject or just review?) is not defined.
- **Severity:** Minor
- **Impact on one-shot app generation:** The CI tool implementation has ambiguous behavior. Agent will pick one interpretation, possibly the lenient one, leaving multi-correct bugs in shipped questions.

## Issue 28
- **Location (section / step):** §6.1 "Run the integrity check on every commit"
- **Issue description:** The instruction "if a fix introduces a violation, fix the data OR add the kanji/particle/construct to the appropriate augmented set in the integrity check tool with a comment explaining why" describes a human escape valve. An agent has no way to determine which path to take, and the second path (add to augmented set) effectively allows the agent to silence checks while pretending to comply.
- **Severity:** Major
- **Impact on one-shot app generation:** Agent will likely take the easy path and add exceptions to the augmented set, eroding the integrity contract over the run. The manual provides no test for whether an exception is "legitimately in N4 scope."

## Issue 29
- **Location (section / step):** §10 "SM-2 SRS"
- **Issue description:** The SM-2 SRS is specified by name and four button labels (Again/Hard/Good/Easy) with verified intervals (1d/6d/15d, lapse → 1d + EF drops). Several specifics are missing: initial EF value, EF formula, what "lapse" precisely triggers, persistence schema (localStorage key shape?), recovery behavior when localStorage is cleared, cross-device merge semantics on import.
- **Severity:** Major
- **Impact on one-shot app generation:** Agent will produce an SM-2 implementation that diverges from N5's at the parameter level. Different intervals = different review experience = failed parity with N5 baseline.

## Issue 30
- **Location (section / step):** §10 "Diagnostic Summary"
- **Issue description:** "Diagnostic Summary with error patterns + recommended next session + session log" is one line. Error-pattern detection algorithm, "recommended next session" recommendation logic, session-log retention policy, and the UI surface for the Diagnostic Summary are all undefined.
- **Severity:** Major
- **Impact on one-shot app generation:** Agent cannot implement a feature defined only by name. Will produce a placeholder or skip the feature.

## Issue 31
- **Location (section / step):** §1.1 directory structure - missing test directories
- **Issue description:** The directory layout shows `tools/test_build_data.py` but no test directory for the front-end (`tests/`, `e2e/`, etc.). §10 says "browser-runnable test suite (37 tests in N5) - JS + Playwright smoke tests. CI gate." The location and structure of these tests is not defined. The Playwright config, the test framework, and the test list are absent.
- **Severity:** Major
- **Impact on one-shot app generation:** Agent cannot reproduce the 37-test suite as a CI gate. Without it, the "CI gate" requirement is unverifiable.

## Issue 32
- **Location (section / step):** §10 "PWA manifest + service worker stale-while-revalidate"
- **Issue description:** The PWA spec is one line. No manifest field list, no icon-set specification, no precache list, no runtime caching strategy beyond "stale-while-revalidate", no offline fallback policy.
- **Severity:** Minor
- **Impact on one-shot app generation:** Agent will produce a working but ad-hoc service worker. Diverges from N5's `jlpt-n5-tutor-v71` versioning convention referenced in §4.3.

## Issue 33
- **Location (section / step):** §0 + §11.3 - "Borderline grammar promotion"
- **Issue description:** The instruction to promote ~30-40 N5 borderline patterns to N4 core requires retrieving the N5 `late_n5` tier list. That list is not embedded in the manual. The "rename for N4" guidance for invariant JA-21 (§2.2) similarly requires the N5 invariants doc that the manual references but does not contain.
- **Severity:** Major
- **Impact on one-shot app generation:** Agent must first generate or re-discover the N5 `late_n5` set, which is N5 corpus knowledge not in the manual. Without it, the migration manifest cannot be built.

## Issue 34
- **Location (section / step):** §5.4 "LLM audit as a multiplier"
- **Issue description:** The procedure says "use Claude API integration; cost ~$11.50/pass; caught 1.0 finding/pattern." It does not provide the prompt template, the API key handling, the rate-limit strategy, the output parsing rule, or the criteria for "manageable false-positive rate."
- **Severity:** Minor
- **Impact on one-shot app generation:** LLM audit is presented as a continuous quality input but cannot be implemented from the manual. Production readiness without it depends on native review which the agent can't access.

## Issue 35
- **Location (section / step):** §1.1 - i18n locale files location
- **Issue description:** Directory shows `locales/` but no naming convention (locales/en.json? locales/en/grammar.json? per-locale subdirectories?), no key path convention, no source-locale-of-truth declaration. The 5-locale i18n needs translation pipelines that the manual does not describe.
- **Severity:** Major
- **Impact on one-shot app generation:** i18n is structurally undefined. Agent will either skip it (violating §10's stated win) or invent a convention (diverging from N5).

## Issue 36
- **Location (section / step):** §2.1 build pipeline (input contract for KB)
- **Issue description:** The build pipeline must parse KB markdown but the markdown file structure for each KB file (grammar_n4.md, vocab_n4.md, etc.) is not specified. We learn fragments: grammar files use `- **(kanji)**` headers, vocab uses `(Reading) - (Meaning)` lines, questions use `### Q\d+`. The complete grammar of each file (section ordering, optional fields, allowed inline syntax) is not provided.
- **Severity:** Critical
- **Impact on one-shot app generation:** Agent cannot author KB files in a format guaranteed to be parsed correctly without seeing existing N5 files. "Copy from N5" applies again.

## Issue 37
- **Location (section / step):** §3.3 "Authoring cadence" - questions
- **Issue description:** The cadence row "8-10 weeks: Questions (moji + goi + bunpou + dokkai) - 100 each = 400+ questions" omits chokai (listening) and any auth_extracted_n4 corpus. Listening is split out into its own KB file per §1.1 but no question count is specified for it. The mapping between question count and JLPT exam structure (Mondai 1-N for each section) is not documented.
- **Severity:** Major
- **Impact on one-shot app generation:** Agent has no definition of how questions partition by Mondai subtype, leading to under- or over-coverage of test sections. Mock-test mode (referenced in §4.2 Day-1 features) requires this partition.

## Issue 38
- **Location (section / step):** §4.2 "Test mode" + §10 "Mock JLPT-format exams"
- **Issue description:** "Test mode (mock-test flow, hides answer/rationale until commit)" is one line. The actual JLPT exam structure for each level (number of mondai, time per section, scoring breakdown, passing threshold) is not enumerated. N5 passing is 80/180 with section thresholds; N4 is 90/180; N3 is 95/180; etc. None of these are in the manual.
- **Severity:** Major
- **Impact on one-shot app generation:** Mock-test mode cannot mirror real JLPT format without the exam-structure table. Agent will produce a generic timed quiz, not a level-faithful mock test.

## Issue 39
- **Location (section / step):** §3.4 + §10 "External-blocked items"
- **Issue description:** Several items are tagged External-Blocked: native voice talent (§9.1), native teacher reviewer (§9.2), translation (§9.3), recommender ML (§9.4). The manual offers no synthetic-fallback specification that an agent could ship as a stop-gap producing a usable (if degraded) build.
- **Severity:** Major
- **Impact on one-shot app generation:** Without fallback, the agent must either skip these features entirely or produce broken stubs. Either way, "production-ready" is unattainable in one shot.

## Issue 40
- **Location (section / step):** General - no top-level "what does done look like" definition
- **Issue description:** The manual has cadence tables, anti-pattern catalogs, and invariant lists, but no single section says: "the N4 app is complete when X, Y, Z conditions are met, observable via these specific automated checks." Definition-of-Done is implicit and distributed.
- **Severity:** Major
- **Impact on one-shot app generation:** Agent cannot self-evaluate whether it has finished. Will either over-deliver scope-creep or under-deliver while believing the work is done.

---

## Final Summary

### Overall readiness for one-shot generation
**Low.**

The manual is best understood as a *retrospective playbook* written for a human team that has already shipped N5 and is preparing to repeat the process for N4 with the N5 repository in hand. It is not, as written, a self-contained specification. The repeated "copy from N5", "port verbatim", "see N5 spec", "as in N5" instructions presuppose the N5 source files are co-resident and human-readable; without them, the manual is approximately a table of contents.

For the manual to be sufficient for one-shot agent generation, three categories of content would need to be added: (a) the actual N4 content inventories that the manual currently treats as known (kanji list, vocab list, grammar pattern list with tier assignments), (b) the schema and format specifications that the manual currently treats as inheritable from N5 (KB markdown grammar, JSON schemas, file conventions), and (c) the executable specifications for features and invariants that the manual currently states as prose summaries (UI module breakdown, SM-2 parameters, multi-correct rules, fallback procedures for external-blocked items).

### Highest-risk gaps preventing full app creation

1. **N4 content inventories are not embedded.** The agent does not know which kanji, vocabulary items, grammar patterns, and tier classifications constitute N4. (Issues 1, 8, 33)
2. **Data and KB schemas are referenced but never defined.** No JSON contract, no markdown grammar. (Issues 3, 17, 36)
3. **N5 source files are required dependencies but not declared as inputs.** "Copy from N5" appears 14+ times. (Issues 4, 16)
4. **UI is described by feature names only.** No module list, no DOM contracts, no state schema, no design tokens beyond a one-line aesthetic. (Issues 5, 16, 30, 31)
5. **External-blocked items have no zero-interaction fallback.** Native audio, native review, translation pipelines are all human-dependent. (Issues 19, 21, 39)
6. **No definition of done.** Agent cannot self-assess completion. (Issue 40)

### Areas that need explicit procedural definition

- Full N4 content inventories (kanji whitelist, vocab whitelist, grammar pattern catalog with tier).
- Complete JSON schemas for data/*.json files, with field types, enums, required/optional flags.
- Complete KB markdown grammar for each KB file type.
- Full design-system spec (or full inclusion of `jlpt-n5-design-system-zen-modern.md`).
- UI module list with responsibilities and contracts.
- SM-2 parameters with exact constants.
- Translation source-locale file format and string-extraction procedure.
- JLPT exam structure table per level (mondai breakdown, time, scoring threshold).
- Mock-test mode behavior contract (which questions are pulled, in what proportions, with what timing).
- Furigana-generation procedure (manual? automated? from which library?).
- Complete invariant rules in machine-testable form (regex, AST checks, value-set membership).
- Audio manifest schema and fallback (synthetic OK at what quality? when?).
- Definition-of-done for the build.
- Default decisions for each of the §15 open questions, so a zero-interaction agent has answers.
- Question-count budget per Mondai per file.
- ID generation rules (slug derivation, disambiguator, cross-listing manifest).

### Areas that are already strong and reusable across levels

- **§3.2 anti-pattern catalog.** The bumper-sticker list of failure modes (filler MCQs, interchangeable-particle pairs, ko-so-a-do without context, simultaneous parallel-session edits) is concrete, evidence-based, and level-agnostic. Useful for any level.
- **§2.2 invariants table.** Even though individual invariants need rule-level definition, the *list* of catch-points is comprehensive and well-organized. Adding three more for N4 (JA-22..JA-24) is a clean extension model.
- **§7 tooling priority order.** The ranked list of scripts to port is actionable and would help an agent decide what to build first.
- **§14 anti-patterns bumper-sticker list.** Ten concise rules useful as a final sanity-check pass before declaring a level done.
- **§8 process discipline (TASKS.md / commit / backup / MEMORY.md).** Project-management hygiene that scales cleanly across levels.
- **§9 external-blocked anticipation.** The four EB items are correctly identified up front; the schedule guidance (month 1 reviewer, month 3 voice talent) is concrete enough to plan around.
- **§11.1 tier-taxonomy three-tier model** (`core_n4` / `late_n4` / `n3_borderline`). Clean abstraction that scales: at any level X, the three tiers are `core_X`, `late_X`, `(X-1)_borderline`.
- **§13 effort estimates with multiplier for higher levels.** Provides realistic scoping guidance and the 1.5x-per-level rule is a defensible heuristic.

These strong sections collectively constitute roughly 30-40% of the manual's value. The other 60-70% needs the missing-content additions enumerated above before the document can support one-shot agent execution.

---

*End of review. Prepared 2026-05-01.*
