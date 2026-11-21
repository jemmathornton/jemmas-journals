"""Labelled comparison sheet for the Pokédex style mock-ups: Now, P1, P2; each with laptop home, inner page, phone (top and scrolled)."""
from PIL import Image, ImageDraw, ImageFont

D = "C:/Users/Jemma/Documents/JemmasJournals/for-jemma/concepts/app-styles"
F = "C:/Windows/Fonts/"
title_f = ImageFont.truetype(F + "segoeuib.ttf", 40)
line_f = ImageFont.truetype(F + "segoeui.ttf", 25)
cap_f = ImageFont.truetype(F + "seguisb.ttf", 20)
head_f = ImageFont.truetype(F + "segoeuib.ttf", 30)

ROWS = [
    ("now", "Now", "Dark sidebar, rounded cream cards: built the same way as Library and Sim World."),
    ("p1", "P1 \u00b7 Collector\u2019s cards", "Each Pok\u00e9mon a printed card: coloured border, art window, foil on shiny ones, number like a set; totals as small cards."),
    ("p2", "P2 \u00b7 Binder", "Padded red binder cover with rings; Pok\u00e9mon in clear pockets, four across, empty pockets for ones not caught; totals as index tabs."),
]
SHOTS = [("laptop", "Laptop \u00b7 Home"), ("inner", "Laptop \u00b7 Galar"), ("phone", "Phone \u00b7 top"), ("phone-2", "Phone \u00b7 scrolled")]
H, GAP, M = 600, 26, 50
BG, INK, MUTE = (246, 243, 238), (34, 26, 28), (110, 98, 96)

def load(style, kind):
    im = Image.open(f"{D}/pokedex-{style}-{kind}.png").convert("RGB")
    return im.resize((round(im.width * H / im.height), H), Image.LANCZOS)

rows = [[load(s, k) for k, _ in SHOTS] for s, _, _ in ROWS]
width = M * 2 + sum(im.width for im in rows[0]) + GAP * (len(SHOTS) - 1)
row_h = 64 + 40 + 18 + H + 34 + 40
sheet = Image.new("RGB", (width, 110 + row_h * len(ROWS) + 10), BG)
d = ImageDraw.Draw(sheet)
d.text((M, 34), "Jemma\u2019s Pok\u00e9dex \u00b7 style mock-ups (pictures only, nothing changed in the app)", font=head_f, fill=INK)
y = 110
for (style, name, line), ims in zip(ROWS, rows):
    d.line((M, y - 14, width - M, y - 14), fill=(214, 205, 194), width=2)
    d.text((M, y), name, font=title_f, fill=INK)
    d.text((M, y + 56), line, font=line_f, fill=MUTE)
    x, iy = M, y + 104
    for im, (_, cap) in zip(ims, SHOTS):
        sheet.paste(im, (x, iy))
        d.rectangle((x - 1, iy - 1, x + im.width, iy + im.height), outline=(200, 190, 178))
        d.text((x, iy + H + 8), cap, font=cap_f, fill=MUTE)
        x += im.width + GAP
    y += row_h
sheet.save(f"{D}/pokedex-styles.jpg", quality=88, optimize=True)
print(sheet.size)
