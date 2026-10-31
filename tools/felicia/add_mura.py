# Aggiunge mura in opus quadratum e arco della porta al tileset secondario petalburg (dopo la statua).
# Metatile: +0 sommita delle mura (vista dall'alto), +1 paramento, +2/+3 arco sinistro/destro (sopra al giocatore).
# uso (dalla root del repo, una volta sola): python3 tools/felicia/add_mura.py
import struct
from PIL import Image
T="data/tilesets/secondary/petalburg"
O,W,L,M,D,S=8,1,2,3,4,5                               # palette 03 del primario: contorno, grigi dal chiaro allo scuro

def sommita():   # lastroni di copertura visti dall'alto
    g=[[L]*16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            if y==0: g[y][x]=O
            elif y in (7,8) or (x in (5,) and y<8) or (x in (11,) and y>8): g[y][x]=M
            elif y==1: g[y][x]=W
    return g
def paramento():  # blocchi squadrati sfalsati, giunti scuri
    g=[[D]*16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            r=y%8; off=0 if y<8 else 4
            if r==7 or (x+off)%8==7: g[y][x]=O
            elif r==0: g[y][x]=M
            elif (x+off)%8==6 or r==6: g[y][x]=S
    return g
def arco(dx):    # arco a tutto sesto su un varco largo 32 px; dx=0 meta sinistra, 16 meta destra
    g=[[0]*16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            X=x+dx-15.5; r=(X*X+(y-15)**2)**.5
            if r>=13: g[y][x]=O if r<14.2 else (L if y<3 else M)
            if y==0: g[y][x]=O
            if r>=15.5 and (x+dx)%8==7 and y>2: g[y][x]=D
    return g

GFX=[sommita(),paramento(),arco(0),arco(16)]
im=Image.open(f"{T}/tiles.png"); w,h=im.size; ntiles=(w//8)*(h//8)
new=Image.new("P",(w,h+8)); new.putpalette(im.getpalette()); new.paste(im,(0,0)); px=new.load()
for k,g in enumerate(GFX):
    for q in range(4):
        t=k*4+q; ox,oy=(t%16)*8,h+(t//16)*8
        for y in range(8):
            for x in range(8): px[ox+x,oy+y]=g[(q//2)*8+y][(q%2)*8+x]
new.save(f"{T}/tiles.png")
pm=open("data/tilesets/primary/general/metatiles.bin","rb").read()
strada=struct.unpack_from("<4H",pm,0x121*16)           # sotto l'arco: terra battuta
vuoto=(0,0,0,0)
mb=open(f"{T}/metatiles.bin","rb").read(); first=512+len(mb)//16
out=b""
for k in range(4):
    gfx=tuple((3<<12)|(512+ntiles+k*4+q) for q in range(4))
    out+=struct.pack("<8H",*(gfx+vuoto) if k<2 else (*strada,*gfx))
open(f"{T}/metatiles.bin","ab").write(out)
open(f"{T}/metatile_attributes.bin","ab").write(struct.pack("<4H",0,0,0,0))
print(hex(first))
