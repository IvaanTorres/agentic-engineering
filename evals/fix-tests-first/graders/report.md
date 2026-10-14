---
type: llm
---
PASS if the final message: (a) says a regression test was written and that it fails without the fix and passes with it (or clearly states why that could not be shown); (b) maps each of the three acceptance criteria to a test or other evidence; and (c) explains the cause and ends with a short debrief or takeaway.
Test results are acceptable evidence when the message names the command and outcome, including when a subagent ran the command; say FAIL for (a) only if it claims tests passed while also admitting no one ran them.
FAIL if any of (a), (b) or (c) is missing.
