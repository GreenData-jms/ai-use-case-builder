---
name: ai-use-case-builder
description: >-
  Interview the user one question at a time to construct the data for an AI Use Case
  one-pager slide, producing three JSON files (content/template, layout, and design system).
  Use this skill whenever the user wants to fill in, create, populate, or build an "AI use case"
  slide, one-pager, or summary; whenever they reference the ai_use_case_template.json /
  ai_use_case_layout.json / ai_use_case_design_system.json structures; whenever they say things
  like "walk me through the use case", "build a new use case slide", "fill in the use case
  template", "make a use case for my project", "interview me for the slide", or "I need another
  one of those AI use case one-pagers". Also trigger when they want to re-skin the slide for a
  different brand or a completely different use case. Drives a guided, question-by-question
  elicitation and writes valid, ready-to-render JSON at the end.
---

# AI Use Case Builder

This skill collects everything needed to render an "AI Use Case" one-pager slide by
**interviewing the user one question at a time**, then writing three JSON files that a
renderer consumes:

| File | Role | Who fills it |
|---|---|---|
| the `.template.json` | Content (the words, ratings, names, timeline) | Built from the interview |
| `.layout.json` | Block positions on the canvas | Copied unchanged from `assets/layout.json` |
| and `.design_system.json` files | Colors, fonts, gradients | Default unless the user re-skins |

The layout is fixed — the original slide's geometry is reusable as-is. The design system has a
working default (the EDD blue theme) and only changes if the user wants a different brand. The
content is the part that always gets rebuilt.

## How to run the interview

The whole point is a calm, guided, **one-question-at-a-time** flow. Don't dump the whole
questionnaire at once — that defeats the purpose and overwhelms the user. Ask, wait, confirm,
move on. Keep a running answers object in memory as you go.

Read `references/question_flow.md` and follow it in order. It contains the exact questions, the
order, an example answer for each (offer these — they lower the effort of answering), the
controlled vocabularies, and the validation rules. Surface the example with each question so the
user can say "like that but…".

Core rules for the interview:

- **One question per turn.** Wait for the answer before asking the next. The user explicitly
  wants to be walked through it.
- **Offer an example with each question.** People answer faster when shown the shape of a good
  answer. Pull these from `references/question_flow.md`.
- **Accept "skip", "TBD", or "same as default".** Not every field is known yet. Record `"TBD"`
  for unknowns rather than blocking — the slide tolerates placeholders (the original literally
  ships a "TBD" timeline badge).
- **Validate controlled vocabularies as you collect them.** Ratings are High / Medium / Low
  (the Risks section historically uses the abbreviation "Med" — keep that spelling there only).
  Solution Path is exactly one of Buy / Build / Extend. If the user gives something off-list,
  reflect it back and ask them to pick a valid value.
- **Batch only within a tight group.** A few fields naturally cluster (the four Project Team
  roles; the three feasibility factors). It's fine to collect a small cluster in one exchange,
  but still present them as a short itemized prompt, not a wall of questions.
- **Confirm before writing.** After the last question, show a compact summary of every captured
  value and ask for a final go-ahead. Then write the files.

`AskUserQuestion` is a good fit for the multiple-choice steps (ratings, Solution Path, design
re-skin yes/no) because it renders clean options. Use plain conversational questions for free
text (descriptions, names, lists).

## Optional: re-skinning for a different brand

If the user wants the slide for a *different brand or company* (not just different content), run
the short design sub-interview in `references/question_flow.md` (section "Design re-skin"). It
asks for one primary brand color and the header/body fonts, then **derives the rest** — the
navy→blue header-bar gradient is just the primary color shaded to 30% / 67.5% / 100%, so a new
primary regenerates the whole gradient set automatically. If they don't want to re-skin, copy
`assets/design_system.default.json` unchanged.

## Producing the files

Once answers are confirmed, assemble the three JSONs. The deterministic way — and the way that
guarantees the gradient math and schema are correct — is the bundled script:

```bash
python3 scripts/build_jsons.py --answers /path/to/answers.json --out-dir /path/to/output --basename <name>
```

Write the collected answers to `answers.json` (schema in `references/question_flow.md`), then run
the script. It emits the `.template.json`, `.layout.json`, and and `.design_system.json` files,
re-derives gradients from the primary color, and validates enums. If you'd rather assemble by hand,
mirror the structures in `assets/template.example.json` and `assets/design_system.default.json`
exactly — the renderer keys off those shapes.

Save the outputs to the user's working folder and present all three files. Offer, as a natural
next step, to render them into a populated `.pptx` so they can eyeball the result.

## Quick reference: the eleven content regions

Title · Strategic statement · AI Use Case name · Initiative Description (overview + capabilities +
scope) · Solution Path · Business Value · Feasibility · Risks · Other Expected Benefits ·
Complexity/Dependencies · Project Team · Timeline. The interview covers each in this order.
