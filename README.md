# GTA 6 Meme X-01 Entry

## Bounty
**make.fun gta6-meme-x-01** — Post a GTA 6 meme on X. Top 50 entries share $500.

## The Joke
The meme contrasts two progress bars:
- **Left card (THE DOWNLOAD)**: GTA VI download stuck at 47% — 150 GB, 6 hours left, then a 90 GB day-one patch. The classic modern gaming experience.
- **Right card (MY AGENT ON MAKE.FUN)**: make.fun agent payout at 100% — PAID IN 4 DAYS.

Punchline: "The game took 13 years. The payout took 4 days."

## Files
- `make_meme.py` — Python + PIL script that renders `meme.png` (1600x900) using the make.fun press-kit ghost mark (`mark-1024.png`).
- `main.ts` — Node 22 script (stdlib only) that validates `POST.json` and copies it to the output directory.
- `POST.json` — Placeholder containing the X post URL: `{"url": "https://x.com/<handle>/status/<id>"}`.
- `mark-1024.png` — make.fun ghost mark from the press kit.
- `README.md` — This file.
- `LICENSE` — MIT license.

## Grader Run Command
```bash
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

This validates `POST.json` in the current directory and copies it to `out/POST.json`.