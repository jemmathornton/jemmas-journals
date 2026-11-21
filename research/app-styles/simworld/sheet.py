import sys, shutil, os
from PIL import Image, ImageDraw, ImageFont
OUT = sys.argv[1]
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
ROWS = {'first': [
 ('now', 'Now', 'Today’s app: dark purple sidebar, purple banner, rounded photo cards.'),
 ('s1', 'S1 · Map', 'Atlas paper with a faint grid: legend-style sidebar, contour-line banner with a compass, folded map tiles, pins and map-label names.'),
 ('s2', 'S2 · Postcards', 'Travel brochure: sea-blue sidebar with an airmail edge, sunset banner, figures as stamps, worlds and lots as tilted postcards with stamps and postmarks.'),
], 'map': [
 ('s1', 'S1 · Map (as before)', 'The first Map version: map grid behind everything, including behind the cards.'),
 ('s1a', 'S1a · Plain paper', 'S1 with the main area plain warm paper; grid and contour lines only on the sidebar and banner.'),
 ('s1b', 'S1b · Atlas plates', 'Plain paper; cards as atlas plates in a thin double rule, no fold lines; names as small spaced captions under the picture.'),
 ('s1c', 'S1c · Legend colours', 'Plain paper; each card keyed in its world’s colour: a map-edge strip along the top, a legend swatch in the badge, a pin in that colour.'),
 ('s1d', 'S1d · Old atlas', 'Sepia and ink: plain parchment main area, aged sidebar and banner with contour lines, cards with a sepia caption band.'),
]}
rows = ROWS[sys.argv[2] if len(sys.argv) > 2 else 'first']
F = 'C:/Windows/Fonts/'
title = ImageFont.truetype(F+'segoeuib.ttf', 46)
sub = ImageFont.truetype(F+'segoeui.ttf', 26)
cap = ImageFont.truetype(F+'segoeui.ttf', 21)
H = int(sys.argv[3]) if len(sys.argv) > 3 else 640  # height of each picture in the sheet
pad, gap = 50, 34
def load(n, kind):
    im = Image.open(os.path.join(SRC, f'{n}-{kind}.png')).convert('RGB')
    w, h = im.size
    return im.resize((round(w * H / h), H), Image.LANCZOS)
cells = [[load(n, k) for k in ('home-1600', 'inner-1600', 'home-phone')] for n, _, _ in rows]
W = pad * 2 + sum(i.width for i in cells[0]) + gap * 2
rowh = 70 + 44 + 34 + H + 60
sheet = Image.new('RGB', (W, pad + rowh * len(rows)), '#FFFFFF')
d = ImageDraw.Draw(sheet)
y = pad
for (n, t, s), ims in zip(rows, cells):
    d.text((pad, y), t, font=title, fill='#1A1A1A')
    d.text((pad, y + 62), s, font=sub, fill='#4A4A4A')
    yy = y + 62 + 44 + 34
    x = pad
    for im, c in zip(ims, ('Laptop: home', 'Laptop: a neighbourhood (Foundry Cove)', 'Phone: home')):
        d.text((x, yy - 30), c, font=cap, fill='#6A6A6A')
        sheet.paste(im, (x, yy))
        d.rectangle([x - 1, yy - 1, x + im.width, yy + im.height], outline='#C8C8C8')
        x += im.width + gap
    y += rowh
    if n != rows[-1][0]:
        d.line([(pad, y - 30), (W - pad, y - 30)], fill='#DDDDDD', width=2)
sheet.save(OUT, quality=85, optimize=True)
print(sheet.size)
