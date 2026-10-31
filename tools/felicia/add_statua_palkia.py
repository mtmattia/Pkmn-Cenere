# Statua di Palkia per il Foro di Vitelia (3x3 metatile, 48x48 px) nel tileset secondario petalburg.
# Figura: sprite overworld di Palkia (frontale, 1:1) convertito in pietra sui grigi della palette 03; sotto, un basamento.
# uso (dalla root del repo, una volta sola): python3 tools/felicia/add_statua_palkia.py  -> stampa l'id del primo metatile
import struct
from PIL import Image
T="data/tilesets/secondary/petalburg"
O,W,L,M,D,S=8,1,2,3,4,5
spr=Image.open("graphics/pokemon/palkia/overworld.png").convert("RGBA").crop((0,0,64,64))
raw=Image.open("graphics/pokemon/palkia/overworld.png"); bgi=raw.getpixel((0,0))
x0,x1,y0,y1=12,51,24,63                                   # bbox della figura (39x39)
art=[[0]*48 for _ in range(48)]
lum=lambda c:0.3*c[0]+0.59*c[1]+0.11*c[2]
vals=sorted(lum(spr.getpixel((x,y))) for x in range(x0,x1) for y in range(y0,y1) if raw.getpixel((x,y))!=bgi)
q=[vals[int(len(vals)*f)] for f in (.12,.35,.6,.85)]     # soglie per quantili -> 5 toni di pietra
ox,oy=(48-(x1-x0))//2,2
for y in range(y0,y1):
    for x in range(x0,x1):
        if raw.getpixel((x,y))==bgi: continue
        v=lum(spr.getpixel((x,y)))
        art[oy+y-y0][ox+x-x0]=O if v<q[0] else S if v<q[1] else D if v<q[2] else M if v<q[3] else L if v<vals[-1]*0.97 else W
# contorno scuro attorno alla figura
fig=[[art[y][x]!=0 for x in range(48)] for y in range(48)]
for y in range(48):
    for x in range(48):
        if not fig[y][x] and any(0<=y+b<48 and 0<=x+a<48 and fig[y+b][x+a] for a,b in ((1,0),(-1,0),(0,1),(0,-1))): art[y][x]=O
# basamento (righe 40..47)
for y in range(40,48):
    for x in range(3,45):
        e=x in (3,44) or y in (40,47)
        art[y][x]=O if e else W if y==41 else D if y==46 or x==43 else L if x==4 else M
im=Image.open(f"{T}/tiles.png"); w,h=im.size; ntiles=(w//8)*(h//8)
new=Image.new("P",(w,h+24)); new.putpalette(im.getpalette()); new.paste(im,(0,0)); px=new.load()
for ty in range(6):
    for tx in range(6):
        k=ty*6+tx; bx,by=(k%16)*8,h+(k//16)*8
        for y in range(8):
            for x in range(8): px[bx+x,by+y]=art[ty*8+y][tx*8+x]
new.save(f"{T}/tiles.png")
import re
def load_pet():
    import json
    lay=json.load(open("data/layouts/layouts.json"))["layouts"]
    p=next(l for l in lay if l.get("id")=="LAYOUT_PETALBURG_CITY")["blockdata_filepath"]
    d=open(p,"rb").read(); return struct.unpack_from("<H",d,(12*30+6)*2)[0]&0x3ff
strada=load_pet()
base=open("data/tilesets/primary/general/metatiles.bin","rb").read() if strada<512 else open(f"{T}/metatiles.bin","rb").read()
sotto=struct.unpack_from("<4H",base,(strada%512)*16)    # strato sotto: lastricato del foro
mb=open(f"{T}/metatiles.bin","rb").read(); first=512+len(mb)//16
out=b""
for my in range(3):
    for mx in range(3):
        top=[(3<<12)|(512+ntiles+(my*2+qy)*6+mx*2+qx) for qy in range(2) for qx in range(2)]
        out+=struct.pack("<8H",*sotto,*top)
open(f"{T}/metatiles.bin","ab").write(out)
# prime due righe: normali (la testa copre il giocatore che passa dietro); ultima: coperta
open(f"{T}/metatile_attributes.bin","ab").write(struct.pack("<9H",*[0]*6,*[0x1000]*3))
print(hex(first),"strada",hex(strada))
