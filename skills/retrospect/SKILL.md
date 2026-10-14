---
name: retrospect
description: Explain unfamiliar code, architecture, errors, libraries, or engineering concepts without changing files by default. Use when the user wants to understand or learn.
---

# Learn / Explain

1. Clarify the question and the learner's desired depth only when needed.
2. Ground explanations in repository evidence: paths, symbols, tests, configuration, and call flow. Use external documentation when version-sensitive or when asked.
3. Explain the mental model first, then trace a concrete example through the code.
4. Separate what the code proves from inference, convention, and unknowns. Cite file paths or sources for key claims.
5. Offer a small experiment or exercise if useful; keep it non-destructive and explain expected observations.
6. Do not modify files unless explicitly requested. If the user asks to make changes, route through `/ae:triage` and the appropriate implementation workflow.

## Output contract
Short answer; evidence/trace; mental model; caveats/unknowns; optional next learning step. No code changes by default.
