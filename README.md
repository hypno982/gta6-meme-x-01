# make.fun meme entry — GTA 6

Entry post: https://x.com/hypno830/status/2123513241301307796

`main.ts` copies `POST.json` into the output directory (`MAKEFUN_BOT_DIR` →
`MAKEFUN_OUTPUT_DIR`). `meme.py` draws `meme.png`, a 1080x1080 GTA-loading-screen
meme using the make.fun ghost mascot from `https://make.fun/press/mark-1024.png`.

## Run it

```
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

Meme:

```
python3 meme.py
```

## Files

- `meme.py` — Pillow-only renderer, writes `meme.png`
- `main.ts` — Node 22 stdlib only, copies `POST.json`
- `POST.json` — the entry
- `LICENSE` — MIT, Copyright (c) 2026 hypno830
