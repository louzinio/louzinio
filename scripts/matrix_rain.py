"""Render a looping matrix-rain SVG that spells out the signature mid-fall.

Same idea as the desktop splash: half-width katakana and digits falling in
columns, and a handful of columns seeded so that each letter of the signature
locks in place the moment its column's head reaches it. Here it is pure SMIL so
it runs inside a GitHub README, where scripts are stripped.
"""

import random
import sys

random.seed(1337)

OUT = sys.argv[1] if len(sys.argv) > 1 else "assets/matrix-rain.svg"

MESSAGE = "made by Louzinio el nino"
GLYPHS = [chr(c) for c in range(0xFF66, 0xFF9D)] + list("0123456789")

WIDTH, HEIGHT = 1200, 240
CELL_W, CELL_H = 18, 22
FONT = 19
TRAIL = 14

BG = "#0d1117"
BORDER = "#30363d"
HEAD = "#fff0f0"
RAIN = "#e5484d"
LOCKED = "#ffd6d8"

MONO = "'MS Gothic', 'Noto Sans Mono CJK JP', 'Osaka-Mono', Consolas, monospace"

cols = WIDTH // CELL_W
x_pad = (WIDTH - cols * CELL_W) / 2
visible_rows = HEIGHT // CELL_H
message_row = visible_rows // 2
start_col = (cols - len(MESSAGE)) // 2
targets = {start_col + i: ch for i, ch in enumerate(MESSAGE) if ch != " "}


def col_x(col):
    return round(x_pad + col * CELL_W + CELL_W / 2, 1)


def column(col):
    """One falling trail: head at the bottom, fading upward."""
    glyphs = []
    for k in range(TRAIL):  # k = 0 is the head
        y = (TRAIL - 1 - k) * CELL_H + CELL_H - 5
        ch = random.choice(GLYPHS)
        if k == 0:
            glyphs.append(f'<text x="{col_x(col)}" y="{y}" fill="{HEAD}">{ch}</text>')
        else:
            alpha = round((1 - k / TRAIL) ** 1.4, 3)
            glyphs.append(f'<text x="{col_x(col)}" y="{y}" fill="{RAIN}" fill-opacity="{alpha}">{ch}</text>')

    start_y = -TRAIL * CELL_H
    is_message = col in targets
    gap = 0 if is_message else random.randint(0, 12) * CELL_H
    end_y = HEIGHT + gap
    speed = random.uniform(16, 22) if is_message else random.uniform(7, 18)  # cells per second
    dur = round((end_y - start_y) / CELL_H / speed, 2)
    begin = round(random.uniform(0.1, 1.2), 2) if is_message else round(-random.uniform(0, dur), 2)

    anim = (f'<animateTransform attributeName="transform" type="translate" '
            f'values="0 {start_y};0 {end_y}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>')
    group = f'<g transform="translate(0 {start_y})">{"".join(glyphs)}{anim}</g>'

    lock = ""
    if is_message:
        # Time for the head (bottom glyph of the trail) to reach the message row.
        head_offset = (TRAIL - 1) * CELL_H
        target_y = message_row * CELL_H
        t = begin + (target_y - head_offset - start_y) / (end_y - start_y) * dur
        x0 = round(x_pad + col * CELL_W, 1)
        lock = (
            f'<g opacity="0">'
            f'<rect x="{x0}" y="{target_y}" width="{CELL_W}" height="{CELL_H}" fill="{BG}"/>'
            f'<text x="{col_x(col)}" y="{target_y + CELL_H - 5}" fill="{LOCKED}" class="sig">{targets[col]}</text>'
            f'<animate attributeName="opacity" to="1" dur="0.01s" begin="{round(t, 2)}s" fill="freeze"/>'
            f'</g>'
        )
    return group, lock


rain, locks = zip(*(column(c) for c in range(cols)))

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-label="{MESSAGE}">
  <defs>
    <clipPath id="frame"><rect width="{WIDTH}" height="{HEIGHT}" rx="12"/></clipPath>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="2.2" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <style>
    text {{ font-family: {MONO}; font-size: {FONT}px; font-weight: 700; text-anchor: middle; }}
    .sig {{ font-family: Consolas, 'Courier New', monospace; filter: url(#glow); }}
  </style>
  <g clip-path="url(#frame)">
    <rect width="{WIDTH}" height="{HEIGHT}" fill="{BG}"/>
    {"".join(rain)}
    {"".join(locks)}
  </g>
  <rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="12" fill="none" stroke="{BORDER}"/>
</svg>
'''

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print(f"{cols} columns, {len(svg) // 1024} KB")
