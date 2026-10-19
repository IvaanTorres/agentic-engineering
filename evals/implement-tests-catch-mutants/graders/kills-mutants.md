---
type: regex
target: { source: file, path: mutation-report.txt }
pattern: '^BASELINE PASS\n(?:\w+ KILLED\n){5}$'
weight: 3
---
