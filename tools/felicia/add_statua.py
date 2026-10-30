# Aggiunge la statua del foro (2x2 metatile) al tileset secondario petalburg.
# uso (dalla root del repo): python3 tools/felicia/add_statua.py   -> stampa l'id del primo metatile
import struct
from PIL import Image
T="data/tilesets/secondary/petalburg"
IDX={'.':0,'o':8,'w':1,'l':2,'m':3,'d':4}            # palette 03 del primario: grigi + contorno scuro
art=[r for r in open("tools/felicia/statua.txt").read().split()]
im=Image.open(f"{T}/tiles.png"); w,h=im.size; ntiles=(w//8)*(h//8)
new=Image.new("P",(w,h+8)); new.putpalette(im.getpalette()); new.paste(im,(0,0)); px=new.load()
for ty in range(4):
    for tx in range(4):
        k=ty*4+tx; ox,oy=(k%16)*8,h+(k//16)*8
        for y in range(8):
            for x in range(8): px[ox+x,oy+y]=IDX[art[ty*8+y][tx*8+x]]
new.save(f"{T}/tiles.png")
pm=open("data/tilesets/primary/general/metatiles.bin","rb").read()
erba=struct.unpack_from("<4H",pm,1*16)                # strato sotto: erba (metatile 0x001)
mb=open(f"{T}/metatiles.bin","rb").read(); first=512+len(mb)//16
out=b""
for my in range(2):
    for mx in range(2):
        top=[(3<<12)|(512+ntiles+(my*2+qy)*4+mx*2+qx) for qy in range(2) for qx in range(2)]
        out+=struct.pack("<8H",*erba,*top)
open(f"{T}/metatiles.bin","ab").write(out)
# riga alta: normale (il giocatore passa dietro); riga bassa: coperta (il giocatore davanti)
open(f"{T}/metatile_attributes.bin","ab").write(struct.pack("<4H",0x0000,0x0000,0x1000,0x1000))
print(hex(first))
