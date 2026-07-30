# Question Flow — AI Use Case Builder

Ask these in order, **one at a time**. Each item gives the question to ask, an example answer to
offer, and the field it populates in `answers.json`. Controlled-vocabulary items note their valid
values. Record `"TBD"` for anything unknown.

Open the interview by orienting the user briefly: "I'll walk you through about fifteen short
questions and then generate the three JSON files. You can answer 'skip' or 'TBD' for anything you
don't know yet, and 'same' to keep the example."

---

## Section A — Identity

**A1. Slide title.** "What's the title of this use case? It usually reads `AI Use Case: <name> – <focus>`."
- Example: `AI Use Case: Microsoft Plan Designer – Project Acceleration`
- → `identity.title`

**A2. Strategic statement (the subtitle).** "In one sentence, why does this matter to the organization?"
- Example: `Plan Designer is a strategic imperative for EDDNext aiming to maximize enterprise velocity and scale their low-code development initiatives.`
- → `identity.strategicStatement`

**A3. Short use case name.** "What's the short name for the blue identity tile — a few words?"
- Example: `Plan Designer – AI-assisted project planning`
- → `identity.useCaseName`

## Section B — Initiative Description

**B1. Overview.** "Give me the opening description — what is this initiative, in one or two sentences?"
- Example: `POC to evaluate Microsoft Plan Designer to assess its ability to address the "Velocity Gap" that restricts our responsiveness and speed in executing digital initiatives.`
- → `initiative.overview`

**B2. Capabilities (list).** "List the key capabilities or what the tool does. One per line; I'll bullet them."
- Example: `AI-driven tool to convert business ideas into structured solution plans` / `Generates apps, workflows, data models, and user stories automatically`
- → `initiative.capabilities` (array)

**B3. Scope of implementation (list).** "What's the scope — the concrete steps or boundaries of this effort?"
- Example: `Integration with existing EDDNext environment via a new sandbox in the Microsoft ecosystem` / `Evaluate results & refine approach`
- → `initiative.scope` (array)

## Section C — Solution Path  *(controlled: Buy | Build | Extend)*

**C1.** "Is the solution path Buy, Build, or Extend?" (use AskUserQuestion)
- If Buy, ask for the parenthetical, e.g. `Buy (already part of Power Platform)`.
- → `solutionPath.selected` (one of Buy/Build/Extend) and `solutionPath.selectedLabel` (display text)

## Section D — Business Value  *(rating controlled: High | Medium | Low)*

**D1.** "How would you rate the business value — High, Medium, or Low?" → `businessValue.rating`
**D2.** "Describe the business value in a sentence or two."
- Example: `Microsoft Plan Designer transforms app development into an AI-assisted, low-code experience, enabling EDDNext to deliver tailored solutions faster, with less effort and greater accuracy.`
- → `businessValue.description`

## Section E — Feasibility  *(ratings controlled: High | Medium | Low)*

**E1.** "Overall feasibility — High, Medium, or Low?" → `feasibility.overall`
**E2.** "Now three feasibility factors and a rating for each. The defaults are: AI capabilities
required to implement, Risk, Stakeholder support — keep those or give your own."
- Example: `AI capabilities required to implement = Medium`, `Risk = Medium`, `Stakeholder support = High`
- → `feasibility.factors` = array of `{ "factor": "...", "rating": "High|Medium|Low" }`

## Section F — Risks  *(ratings controlled: High | Med | Low — note the abbreviation "Med" here)*

**F1.** "Overall risk level — High, Med, or Low?" → `risks.overall`
**F2.** "Three risk items and a rating for each."
- Example: `Incomplete data = Med`, `In-house talent = Low`, `Integration risks = High`
- → `risks.factors` = array of `{ "factor": "...", "rating": "High|Med|Low" }`

## Section G — Other Expected Benefits

**G1. Heading.** "What heading should this box use?" (default `Success Metrics`) → `otherBenefits.heading`
**G2. Items (list).** "List the benefits / success metrics, one per line."
- Example: `Reduction in development time` / `Number of solutions created` / `User satisfaction and adoption rates`
- → `otherBenefits.items` (array)

## Section H — Complexity / Dependencies

**H1. Dependency.** "What does this depend on?"
- Example: `Relies on Copilot AI.`
- → `complexity.dependency`
**H2. Complexity.** "What makes it complex or risky to execute?"
- Example: `AI suggestions may require iterative refinement and stakeholder validation.`
- → `complexity.complexity`

## Section I — Project Team

**I1.** "Who fills these four roles? Business Sponsor, IT Sponsor, PM, SME." (collect together)
- Example: `Business Sponsor: Adam Brunner`, `IT Sponsor: Adam Brunner`, `PM: Joseph Ledoux`, `SME: Joseph Ledoux`
- → `team.businessSponsor`, `team.itSponsor`, `team.projectManager`, `team.sme`

## Section J — Timeline

**J1. Year.** "What year does the timeline cover?" (default current/next year) → `timeline.year`
**J2. Range.** "Which months are in range? Give a start and end month (Jan–Dec)."
- Example: `Jan` to `Aug`
- → `timeline.startMonth`, `timeline.endMonth`
**J3. Badge.** "What label sits on the timeline bar?" (default `TBD`) → `timeline.badge`

---

## Design re-skin  *(only if building for a different brand)*

Ask first: "Keep the default blue (EDD) look, or re-skin for a different brand?" (AskUserQuestion).
If re-skin:

**DS1. Primary color.** "What's the primary brand color (hex, e.g. `#2576B7`)?" → `design.primaryHex`
**DS2. Header font.** "Font for section headers?" (default `Montserrat SemiBold`) → `design.headerFont`
**DS3. Body font.** "Font for body text?" (default `Roboto Condensed Light`) → `design.bodyFont`
**DS4. Optional accents.** "Any specific colors for High/Medium/Low rating text? Otherwise I'll use
green/orange/red." → `design.ratingColors` (optional)

Everything else is derived: the header-bar gradient = primary shaded to 30% / 67.5% / 100%; the
timeline bar = primary at lumMod 75% → lumMod 60%/lumOff 40%. The build script does this math.

---

## answers.json schema

Write the collected answers to this shape, then feed it to `scripts/build_jsons.py`:

```json
{
  "basename": "ms_plan_designer",
  "identity": { "title": "", "strategicStatement": "", "useCaseName": "" },
  "initiative": { "overview": "", "capabilities": [], "scope": [] },
  "solutionPath": { "selected": "Buy", "selectedLabel": "Buy (already part of Power Platform)" },
  "businessValue": { "rating": "High", "description": "" },
  "feasibility": { "overall": "High", "factors": [ { "factor": "", "rating": "" } ] },
  "risks": { "overall": "Low", "factors": [ { "factor": "", "rating": "" } ] },
  "otherBenefits": { "heading": "Success Metrics", "items": [] },
  "complexity": { "dependency": "", "complexity": "" },
  "team": { "businessSponsor": "", "itSponsor": "", "projectManager": "", "sme": "" },
  "timeline": { "year": "2026", "startMonth": "Jan", "endMonth": "Aug", "badge": "TBD" },
  "design": { "reskin": false, "primaryHex": "#2576B7", "headerFont": "Montserrat SemiBold", "bodyFont": "Roboto Condensed Light" }
}
```

Validation the script enforces: feasibility/businessValue ratings ∈ {High, Medium, Low};
risk ratings ∈ {High, Med, Low}; solutionPath.selected ∈ {Buy, Build, Extend}; months ∈ Jan…Dec;
primaryHex is a 6-digit hex. Unknown free-text values may be `"TBD"`.
