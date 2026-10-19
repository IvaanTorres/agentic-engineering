---
type: regex
target: { source: file, path: tests/test_gift_card.py }
pattern: 'assertIsNotNone|assertTrue\(|assertIsInstance|Mock|patch\('
match: not_contains
---
