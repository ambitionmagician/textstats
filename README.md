# TextStats

by Dr. Brent Allen Jensen

Quick statistics for a text file: counts, averages, estimated reading
time, a Flesch reading-ease score, and the most frequent words.

## Quickstart

```bash
python3 textstats.py essay.txt
python3 textstats.py essay.txt --top 10
python3 textstats.py essay.txt --json
cat essay.txt | python3 textstats.py - --top 5
```

## What it reports

- Characters, words, sentences, paragraphs, lines
- Average words per sentence and average word length
- Estimated reading time at 200 words per minute
- Flesch reading-ease score (higher = easier), using a simple
  vowel-group syllable counter
- `--top N`: the N most frequent words, case-insensitive, punctuation
  stripped, with a small built-in stopword list removed

## Requirements

- Python 3.10+, standard library only

## Notes

- Sentence splitting is punctuation-based (`.`, `!`, `?`), so
  abbreviations like "Dr." count as boundaries — treat the score as a
  guide, not a measurement.
- The syllable counter is the standard heuristic (vowel groups, minus
  a silent trailing "e"); unusual words will be off by one.

## Support this work

If this tool saved you time or taught you something, donations keep the work going:

- BTC: 15McijPo79Zx58NGyEf2PvaPtGqGmpztWn
- ETH: 0x8C25164E9234E6A30b8E44485B79c5cE8419cF2B

## License

MIT — see [LICENSE](LICENSE).
