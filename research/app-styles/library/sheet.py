from PIL import Image, ImageDraw, ImageFont
import os
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
DST = r'C:\Users\Jemma\Documents\JemmasJournals\for-jemma\concepts\app-styles'
F = 'C:/Windows/Fonts/'
title = ImageFont.truetype(F+'segoeuib.ttf', 34); sub = ImageFont.truetype(F+'segoeui.ttf', 21)
head = ImageFont.truetype(F+'seguisb.ttf', 20); big = ImageFont.truetype(F+'segoeuib.ttf', 44); note = ImageFont.truetype(F+'segoeuii.ttf', 20)
rows = [('now', 'Now', 'Walnut sidebar, dark banner of tilted covers, rounded cards: the app as it is today (it has no phone layout yet).'),
        ('l1', 'L1 · Bound book', 'Cloth-bound sidebar with gilt rules; cream page with a gutter; title page and a plate of covers; ornaments; book-face reading text.'),
        ('l2', 'L2 · Bookshop shelf', 'Walnut bookcase: shelves as coloured spines, covers standing on shelf boards, brass label holders, shelf-talker panels.')]
names = {'home-1600': 'laptop-home', 'inner-1600': 'laptop-book-page', 'home-phone': 'phone-home'}
for k, _, _ in rows:
    for a, b in names.items():
        Image.open(os.path.join(SRC, f'{k}-{a}.png')).convert('RGB').save(os.path.join(DST, f'library-{k}-{b}.jpg'), quality=88)
LW, LH = 760, round(760*930/1600); PH = LH; PW = round(PH*390/844)
M, G = 44, 28
W = M + LW + G + LW + G + PW + M
ROWH = 96 + LH + 40
H = 150 + ROWH*3 + 70
sheet = Image.new('RGB', (W, H), '#FAF6EE'); d = ImageDraw.Draw(sheet)
d.text((M, 34), 'Jemma’s Library: two styles of its own', font=big, fill='#2A1F16')
x1, x2, x3 = M, M+LW+G, M+2*(LW+G)
for x, t in ((x1, 'Laptop · home'), (x2, 'Laptop · a book’s page (Circe)'), (x3, 'Phone · home')):
    d.text((x, 108), t, font=head, fill='#75664F')
y = 150
for k, t, s in rows:
    d.line((M, y, W-M, y), fill='#D9CDB6', width=2)
    d.text((M, y+14), t, font=title, fill='#2A1F16')
    d.text((M, y+58), s, font=sub, fill='#5A4C3A')
    iy = y + 96
    for x, a, w, h in ((x1, 'home-1600', LW, LH), (x2, 'inner-1600', LW, LH), (x3, 'home-phone', PW, PH)):
        im = Image.open(os.path.join(SRC, f'{k}-{a}.png')).convert('RGB').resize((w, h), Image.LANCZOS)
        d.rectangle((x-1, iy-1, x+w, iy+h), outline='#CDBFA4')
        sheet.paste(im, (x, iy))
    y += ROWH
d.text((M, y+10), 'Phone: the Library has no phone layout yet, so L1 and L2 show a simple one, my suggestion (not decided): the sidebar becomes a band at the top.', font=note, fill='#75664F')
sheet.save(os.path.join(DST, 'library-styles.jpg'), quality=90)
print(sheet.size)
