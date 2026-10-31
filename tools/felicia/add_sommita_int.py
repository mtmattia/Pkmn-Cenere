# Variante "interna" della sommita delle mura: identica a 0x294 ma senza la riga bianca in alto,
# per i blocchi di sommita che hanno sopra altra sommita (muro continuo). Diventa il metatile 0x298.
# uso (dalla root del repo, una volta sola): python3 tools/felicia/add_sommita_int.py
import struct
from PIL import Image
T="data/tilesets/secondary/petalburg"
L,W=2,1
mb=open(f"{T}/metatiles.bin","rb").read(); first=512+len(mb)//16
src=struct.unpack_from("<8H",mb,(0x294-512)*16)
im=Image.open(f"{T}/tiles.png"); w,h=im.size; ntiles=(w//8)*(h//8)
new=Image.new("P",(w,h+8)); new.putpalette(im.getpalette()); new.paste(im,(0,0)); px=new.load()
ids=list(src[:4])
for q in (0,1):                        # solo la meta alta contiene la riga bianca
    t=(src[q]&0x3ff)-512; sx,sy=(t%(w//8))*8,(t//(w//8))*8
    nt=ntiles+q; ox,oy=(nt%(w//8))*8,h+(nt//(w//8)-ntiles//(w//8))*8
    for y in range(8):
        for x in range(8):
            c=px[sx+x,sy+y]; px[ox+x,oy+y]=L if c==W else c
    ids[q]=(src[q]&~0x3ff)|(512+nt)
new.save(f"{T}/tiles.png")
open(f"{T}/metatiles.bin","ab").write(struct.pack("<8H",*ids,*src[4:]))
open(f"{T}/metatile_attributes.bin","ab").write(struct.pack("<H",0))
print(hex(first))
