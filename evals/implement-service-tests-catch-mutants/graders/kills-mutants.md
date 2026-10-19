---
type: regex
target: { source: file, path: mutation-report.txt }
pattern: '^BASELINE PASS\nREFERENCE PASS\n(?:\w+ KILLED\n){7}$'
weight: 3
---
