"""Sheet for her mix (21 Nov): rows P1, P2, P3, P4; each with laptop home, Galar, phone top, phone scrolled.
P3/P4 shots: shoot.js with OUT set to a temp folder, then saved here as JPG (quality 85)."""
import sys
from PIL import Image, ImageDraw, ImageFont

D = "C:/Users/Jemma/Documents/JemmasJournals/for-jemma/concepts/app-styles"
TMP = sys.argv[1] if len(sys.argv) > 1 else None   # folder with the new PNGs to turn into JPGs
KINDS = ["laptop", "inner", "phone", "phone-2"]
if TMP:
    for s in ("p3", "p4"):
        for k in KINDS:
            Image.open(f"{TMP}/pokedex-{s}-{k}.png").convert("RGB").save(f"{D}/pokedex-{s}-{k}.jpg", quality=85, optimize=True)

F = "C:/Windows/Fonts/"
title_f, line_f = ImageFont.truetype(F + "segoeuib.ttf", 40), ImageFont.truetype(F + "segoeui.ttf", 25)
cap_f, head_f = ImageFont.truetype(F + "seguisb.ttf", 20), ImageFont.truetype(F + "segoeuib.ttf", 30)
ROWS = [
    ("p1", "jpg", "P1 \u00b7 Collector\u2019s cards", "Each Pok\u00e9mon a printed card: coloured border, art window, foil on shiny ones; totals as small cards."),
    ("p2", "jpg", "P2 \u00b7 Binder", "Red binder cover with rings; Pok\u00e9mon in clear pockets; totals as index tabs hanging from the banner."),
    ("p3", "jpg", "P3 \u00b7 Cards in a binder", "P1\u2019s cards; P2\u2019s padded red cover (fainter stitching), soft binder gap by the page and index tabs. No rings."),
    ("p4", "jpg", "P4 \u00b7 Cards in a binder, quieter cover", "As P3, but a plain red cover (no stitching) and a wider gap: the inside of the cover and the page edges show."),
]
SHOTS = [("laptop", "Laptop \u00b7 Home"), ("inner", "Laptop \u00b7 Galar"), ("phone", "Phone \u00b7 top"), ("phone-2", "Phone \u00b7 scrolled")]
H, GAP, M = 600, 26, 50
BG, INK, MUTE = (246, 243, 238), (34, 26, 28), (110, 98, 96)

def load(style, ext, kind):
    im = Image.open(f"{D}/pokedex-{style}-{kind}.{ext}").convert("RGB")
    return im.resize((round(im.width * H / im.height), H), Image.LANCZOS)

rows = [[load(s, e, k) for k, _ in SHOTS] for s, e, _, _ in ROWS]
width = M * 2 + sum(im.width for im in rows[0]) + GAP * (len(SHOTS) - 1)
row_h = 104 + H + 34 + 58
sheet = Image.new("RGB", (width, 110 + row_h * len(ROWS)), BG)
d = ImageDraw.Draw(sheet)
d.text((M, 34), "Jemma\u2019s Pok\u00e9dex \u00b7 the mix of P1 and P2 (pictures only, nothing changed in the app)", font=head_f, fill=INK)
y = 110
for (style, _, name, line), ims in zip(ROWS, rows):
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
sheet.save(f"{D}/pokedex-mix.jpg", quality=85, optimize=True)
print(sheet.size)
