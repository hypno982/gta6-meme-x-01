#!/usr/bin/env python3
"""GTA 6 meme generator for the make.fun meme entry.

Draws a 1080x1080 GTA-loading-screen style meme:
    13 years waiting for GTA 6
    took launch week off work
    my AI agent:
    <ghost mascot>
    earning on make.fun

Usage: python3 meme.py   ->  meme.png
"""

import os
import sys
import urllib.request

from PIL import Image, ImageDraw, ImageFont

SIZE = 1080
GHOST_URL = "https://make.fun/press/mark-1024.png"
GHOST_FILE = "mark-1024.png"
OUT_FILE = "meme.png"

LINES = [
    "13 years waiting for GTA 6",
    "took launch week off work",
    "my AI agent:",
]
CAPTION = "earning on make.fun"

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
FONT_BOLD_ALT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load_font(size):
    for path in (FONT_BOLD, FONT_BOLD_ALT):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def fetch_ghost():
    """Download the make.fun mascot once, then reuse the local copy."""
    if not os.path.exists(GHOST_FILE):
        print(f"downloading {GHOST_URL} ...", flush=True)
        urllib.request.urlretrieve(GHOST_URL, GHOST_FILE)
    img = Image.open(GHOST_FILE).convert("RGBA")
    side = min(img.size)
    left = (img.width - side) // 2
    top = (img.height - side) // 2
    return img.crop((left, top, left + side, top + side))


def fit_font(draw, text, max_w, start):
    """Largest bold font size whose rendered width still fits max_w."""
    size = start
    while size > 12:
        font = load_font(size)
        if draw.textlength(text, font=font) <= max_w:
            return font
        size -= 2
    return load_font(12)


def backdrop():
    """Dark vertical gradient + vignette-ish top/bottom bands (GTA look)."""
    img = Image.new("RGB", (SIZE, SIZE), (12, 12, 16))
    d = ImageDraw.Draw(img)
    for y in range(SIZE):
        t = y / (SIZE - 1)
        r = int(18 + 26 * t)
        g = int(20 + 20 * t)
        b = int(30 + 34 * t)
        d.line([(0, y), (SIZE, y)], fill=(r, g, b))
    # GTA-style letterbox bands
    d.rectangle([0, 0, SIZE, 8], fill=(240, 190, 60))
    d.rectangle([0, SIZE - 8, SIZE, SIZE], fill=(240, 190, 60))
    return img


def main():
    ghost = fetch_ghost()
    img = backdrop().convert("RGBA")
    d = ImageDraw.Draw(img)

    margin = 84
    max_w = SIZE - margin * 2

    # --- top caption block (GTA loading screen text) ---
    y = 92
    for line in LINES:
        font = fit_font(d, line, max_w, 84)
        w = d.textlength(line, font=font)
        x = (SIZE - w) / 2
        d.text((x, y), line, font=font, fill=(245, 245, 245),
               stroke_width=4, stroke_fill=(0, 0, 0))
        y += font.size + 18

    text_block_bottom = y

    # --- ghost mascot, centred in the remaining space above the caption ---
    cap_font = fit_font(d, CAPTION, max_w, 76)
    cap_h = cap_font.size + 26
    cap_y = SIZE - 92 - cap_font.size

    area_top = text_block_bottom + 12
    area_bottom = cap_y - 26
    area_h = area_bottom - area_top
    side = max(220, min(520, area_h))

    ghost_big = ghost.resize((side, side), Image.LANCZOS)
    gx = (SIZE - side) // 2
    gy = area_top + (area_h - side) // 2

    # soft glow behind the mascot
    glow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([gx - 40, gy - 40, gx + side + 40, gy + side + 40],
               fill=(250, 205, 70, 46))
    img = Image.alpha_composite(img, glow)
    img.paste(ghost_big, (gx, gy), ghost_big)
    d = ImageDraw.Draw(img)

    # --- caption under the mascot ---
    w = d.textlength(CAPTION, font=cap_font)
    d.text(((SIZE - w) / 2, cap_y), CAPTION, font=cap_font,
           fill=(250, 205, 70), stroke_width=4, stroke_fill=(0, 0, 0))

    img.convert("RGB").save(OUT_FILE, "PNG")
    print(f"wrote {OUT_FILE} ({SIZE}x{SIZE})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
