# Knowledge Transfer

The user uses this toolkit to learn from the work, not only to get it done. Whenever a skill changed, reviewed, or explained something non-trivial, end with a **Debrief** section so the user can understand and own the result without re-reading the whole session.

Give **one debrief per user request**. When a skill runs inside another skill (for example `explore`, `implement` or `verify` inside `feature`), it returns its findings to the outer skill without a debrief, and the outermost skill writes a single debrief covering the whole task.

## Debrief

Keep it short and specific to this task; skip any item that genuinely does not apply, and say so for decisions.

1. **What changed and why**: two or three sentences on the intent and the approach taken.
2. **Decisions**: each material choice, the alternatives considered, and why this one won. Include choices made by default or by convention, not only deliberate ones.
3. **Reading order**: the files or commits to read, in the order that makes the change easiest to follow, with one line on what to look for in each.
4. **Assumptions and gaps**: what was assumed, what was not checked or tested, and known limitations. Mark inferences as inferences.
5. **Check yourself**: the one to three things the user should verify personally (a behavior to try, a risky line to read, a question to ask the author).
6. **Concepts**: at most two ideas (patterns, library behaviors, domain rules) that are worth understanding to maintain this code, each with a one-line explanation and where it shows up.

## Sources

Build the debrief from evidence: the diff, commit messages, task artifacts (`plan.md`, `execution-log.md` decisions table, `verification.md`, `review.md`), PR discussion, and command output. Do not invent rationale that is not recorded; if the reason for a decision is unknown, say "reason not recorded" and give your best inference, labelled as such.

## Proportionality

For a one-line change, a single sentence per item (or "none") is enough. Never pad the debrief; it exists to transfer understanding, not to look thorough.
