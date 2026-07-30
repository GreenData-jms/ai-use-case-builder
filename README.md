# AI Use Case Builder

A reusable system for generating **AI Use Case one-pager slides** from a guided interview. The process captures a use case through a one-question-at-a-time elicitation, writes three JSON files (content, layout, design system), and renders them into a populated slide.

This repository is the working home for refining the process and its aesthetic quality — the JSON contract, the interview flow, the design system, and worked examples — so it can be iterated on collaboratively (including with Claude Design).

## What the three JSON files do

| File | Role | Changes per use case? |
|---|---|---|
| `*.template.json` | **Content** — the words, ratings, names, timeline | Yes — rebuilt every time from the interview |
| `*.layout.json` | **Layout** — block positions on the 16:9 canvas (inches) | No — geometry is reused as-is |
| `*.design_system.json` | **Design** — colors, fonts, gradients | Only when re-skinning for a different brand |

A composition engine iterates the layout blocks, resolves each `fieldRef` against the template instance, and renders it with the component + text style from the design system.

## Repository structure

```
ai-use-case-builder/
├── README.md
├── templates/                      # The canonical JSON contract (source of truth)
│   ├── ai_use_case_template.json       # Content schema + example values
│   ├── ai_use_case_layout.json         # Absolute block layout (inches / EMU)
│   └── ai_use_case_design_system.json  # Palette, gradients, typography, components
├── skill/                          # The ai-use-case-builder skill (unpacked)
│   ├── SKILL.md                        # How the interview runs
│   ├── references/
│   │   └── question_flow.md            # The exact questions, in order, with examples
│   ├── scripts/
│   │   └── build_jsons.py              # Deterministic assembler + gradient math
│   └── assets/
│       ├── template.example.json       # (= templates/ai_use_case_template.json)
│       ├── layout.json                 # (= templates/ai_use_case_layout.json)
│       └── design_system.default.json  # (= templates/ai_use_case_design_system.json)
└── examples/
    └── github_copilot/             # One full worked example
        ├── github_copilot.answers.json         # Captured interview answers
        ├── github_copilot.template.json        # Generated content
        ├── github_copilot.layout.json          # Generated layout (copied unchanged)
        ├── github_copilot.design_system.json   # Generated design (copied unchanged)
        └── *.pptx                              # Rendered deck outputs
```

> **Note:** The packaged `.skill` bundle is a zip of `skill/`; the unpacked tree here is the editable source of truth. The rendered `.pptx` decks under `examples/` are binary and are uploaded directly (not through the text-based Git API).

## How to generate a new one-pager

1. Run the interview in `skill/SKILL.md` / `skill/references/question_flow.md` — one question at a time.
2. Write the collected answers to an `answers.json` (schema in `question_flow.md`).
3. Build the three files:

   ```bash
   python3 skill/scripts/build_jsons.py \
     --answers answers.json \
     --out-dir ./out \
     --basename my_use_case
   ```

   The script validates the controlled vocabularies (ratings, solution path, months), copies the layout unchanged, and — when re-skinning — regenerates the header/timeline gradients from a single primary brand color.

## Re-skinning for a different brand

Provide one primary hex color plus optional header/body fonts. Everything else derives: the navy→blue header-bar gradient is the primary shaded to 30% / 67.5% / 100%, and the timeline bar is the primary at lumMod 75% → lumMod 60% / lumOff 40%. See the "Design re-skin" section of `question_flow.md` and `build_design()` in `build_jsons.py`.

## The eleven content regions

Title · Strategic statement · AI Use Case name · Initiative Description (overview + capabilities + scope) · Solution Path · Business Value · Feasibility · Risks · Other Expected Benefits · Complexity/Dependencies · Project Team · Timeline.
