# Challenge Questions

The user wants to understand changes well enough to defend them, not just receive a verdict. When a skill calls for a challenge (PR review, shipping the user's own change, explaining a change), question the user before or alongside giving answers.

## How to challenge

1. Ask **3 to 5 questions**, specific to this diff. Never ask generic questions that would fit any PR.
2. Mix these kinds, weighted toward where the real risk is:
   - **Predict behavior:** "What happens when `<input>` is empty / the request fails / two users do this at once?"
   - **Justify a decision:** "Why `<approach>` instead of `<alternative>`? What does it cost?"
   - **Side effects:** "What else calls `<changed symbol>`, and does it still behave the same?"
   - **Tests:** "Which test would fail if `<line>` were reverted? What case is not tested?"
   - **Scope and delivery:** "Does this meet acceptance criterion `<n>`? What would QA or the PO try first?"
3. Ask the questions, then **stop and wait** for the user's answers. Do not answer your own questions in the same message.
4. For each answer, say whether it matches the code, with evidence (file/line, test, command). Correct misunderstandings plainly.
5. If an answer exposes a real gap (an unhandled edge case, an untested path, a side effect nobody considered), add it to the findings or the PR's open questions.
6. Finish with a one-line summary of what the user clearly understands and what to look at again.

## Proportionality and opt-out

- For a trivial change, one or two questions are enough.
- The user can skip the challenge by saying so (for example "quick", "no questions", "skip"). Then give findings directly and list the questions as "questions worth answering" at the end.
- Don't turn the challenge into a quiz for its own sake; every question should either check understanding of something that matters or surface a possible gap.
