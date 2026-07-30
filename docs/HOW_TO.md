# How To: Build an AI Use Case One-Pager

A short operating guide for producing a single-slide AI Use Case summary using the `ai-use-case-builder` process. The activity turns a guided interview into three JSON files (content, layout, design) and renders them into a populated slide. Plan on 15–20 minutes for a first pass.

## Before you start

Have the repository or skill available (`ai-use-case-builder`), and know one thing: whether this one-pager keeps the default EDD blue look or needs re-skinning for a different brand. Everything else is captured during the interview, and unknowns are allowed — the slide tolerates `TBD` placeholders.

## The steps

**1. Start the builder.** Invoke the `ai-use-case-builder` skill (or open `skill/SKILL.md`). It runs a calm, one-question-at-a-time interview rather than a single long form.

**2. Answer the interview, one question at a time.** Walk the eleven content regions in order — Title, Strategic statement, Use case name, Initiative Description (overview + capabilities + scope), Solution Path, Business Value, Feasibility, Risks, Other Expected Benefits, Complexity/Dependencies, Project Team, and Timeline. Each question offers an example answer; reply "same" to accept it, give your own, or say "TBD" for anything not yet known.

**3. Respect the controlled vocabularies.** Business Value and Feasibility ratings are High / Medium / Low. Risks use High / Med / Low (note the abbreviated "Med"). Solution Path is exactly one of Buy / Build / Extend. Timeline months are Jan–Dec, captured as a start and end month.

**4. Decide on branding.** Keep the default blue theme, or re-skin. If re-skinning, supply one primary hex color plus optional header and body fonts — the header-bar and timeline gradients are derived automatically from that single color, so you never hand-tune the gradient stops.

**5. Confirm the captured answers.** Review the compact summary the builder shows before anything is written. This is the checkpoint — fix wording, ratings, or names here rather than after generation.

**6. Generate the three JSON files.** Save the confirmed answers to `answers.json`, then run the assembler:

```
python3 skill/scripts/build_jsons.py --answers answers.json --out-dir ./out --basename <name>
```

It emits `<name>.template.json` (content), `<name>.layout.json` (layout, copied unchanged), and `<name>.design_system.json` (design). It validates the vocabularies and re-derives the gradients — so the output is schema-correct by construction.

**7. Render and review.** Render the three JSONs into a populated `.pptx` and eyeball the result. Because the layout geometry is fixed, only the content and (optionally) the palette change between one-pagers; the composition stays consistent.

**8. Iterate or save.** If copy overflows a card or a rating reads wrong, adjust the answers and regenerate — the JSON is the source of truth, not the slide. When it's right, save the answers file alongside the outputs so the one-pager is fully reproducible later.

## What you end up with

A single 16:9 slide plus the three JSON files that produced it. Keep the `answers.json` — it's the reproducible record, and the fastest starting point for a revision or a re-skin.

*AI Use Case Build — How To v1.0 — July 2026*
