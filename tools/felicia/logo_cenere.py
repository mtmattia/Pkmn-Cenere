# Banner "CENERE" del title screen (sostituisce emerald_version.png, 128x32, 16 colori, stessa palette)
# Lettere bianco cenere con sfumatura grigia, bordo nero e alone scuro come il logo originale.
import sys
from PIL import Image, ImageDraw, ImageFont
OUT = sys.argv[1] if len(sys.argv) > 1 else "graphics/title_screen/emerald_version.png"
FONT = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
W, H = 128, 32
src = Image.open(OUT)  # riusa la palette originale
pal = src.getpalette()[:48]
f = ImageFont.truetype(FONT, 29)
mask = Image.new("L", (W, H), 0)
d = ImageDraw.Draw(mask)
txt = "CENERE"
ws = [d.textbbox((0, 0), c, font=f)[2] - d.textbbox((0, 0), c, font=f)[0] for c in txt]
gap = -1
tot = sum(ws) + gap * (len(txt) - 1)
x = (W - tot) // 2
arc = [3, 1, 0, 0, 1, 3]  # leggero arco come EMERALD
for c, w, dy in zip(txt, ws, arc):
    bb = d.textbbox((0, 0), c, font=f)
    d.text((x - bb[0], 2 + dy - bb[1]), c, font=f, fill=255)
    x += w + gap
m = mask.point(lambda v: 255 if v > 110 else 0)
px = m.load()
def grow(s):
    return {(x + dx, y + dy) for (x, y) in s for dx in (-1, 0, 1) for dy in (-1, 0, 1) if 0 <= x + dx < W and 0 <= y + dy < H}
fill = {(x, y) for x in range(W) for y in range(H) if px[x, y]}
ring1 = grow(fill) - fill
ring2 = grow(fill | ring1) - fill - ring1
out = Image.new("P", (W, H), 0)
out.putpalette(pal + [0] * (768 - 48))
o = out.load()
ys = [y for _, y in fill]; y0, y1 = min(ys), max(ys)
# sfumatura: bianco in alto -> grigio cenere in basso (indici palette: f 255, 6 238, 3 222, c 205, a 189, 8 172)
grad = [15, 15, 6, 3, 12, 10, 8]
for (x, y) in fill:
    t = (y - y0) / max(1, y1 - y0)
    o[x, y] = grad[min(len(grad) - 1, int(t * len(grad)))]
    if (x, y - 1) in ring1:  # riflesso sul bordo alto
        o[x, y] = 15
for p in ring1: o[p] = 4
for p in ring2: o[p] = 14
out.save(OUT)
print("ok", y0, y1, tot)
