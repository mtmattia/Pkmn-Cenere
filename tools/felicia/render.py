# render layout -> png. uso: render.py ROOT PRIM SEC MAPBIN W H OUT [PALDIR_PRIM]
import sys,struct
from PIL import Image
root,prim,sec,mapbin,W,H,out=sys.argv[1:8]; W,H=int(W),int(H)
palp=sys.argv[8] if len(sys.argv)>8 else f"{root}/data/tilesets/primary/{prim}/palettes"
def pal(f): return [tuple(map(int,l.split())) for l in open(f).read().split('\n')[3:19]]
pals=[pal(f"{palp}/{i:02}.pal") for i in range(6)]+[pal(f"{root}/data/tilesets/secondary/{sec}/palettes/{i:02}.pal") for i in range(6,13)]
def tiles(p):
    im=Image.open(p); px=im.load(); w,h=im.size; T=[]
    for ty in range(h//8):
        for tx in range(w//8): T.append([[px[tx*8+x,ty*8+y]&15 for x in range(8)] for y in range(8)])
    return T
T=tiles(f"{root}/data/tilesets/primary/{prim}/tiles.png"); T+= [[[0]*8]*8]*(512-len(T)); T+=tiles(f"{root}/data/tilesets/secondary/{sec}/tiles.png")
def mts(p): b=open(p,'rb').read(); return [struct.unpack_from('<8H',b,i) for i in range(0,len(b),16)]
M=mts(f"{root}/data/tilesets/primary/{prim}/metatiles.bin"); M+=[(0,)*8]*(512-len(M)); M+=mts(f"{root}/data/tilesets/secondary/{sec}/metatiles.bin")
blocks=struct.unpack(f'<{W*H}H',open(mapbin,'rb').read())
img=Image.new('RGB',(W*16,H*16)); P=img.load()
for bi,b in enumerate(blocks):
    m=M[b&0x3ff]; bx,by=(bi%W)*16,(bi//W)*16
    for layer in range(2):
        for q in range(4):
            e=m[layer*4+q]; t=T[e&0x3ff] if (e&0x3ff)<len(T) else [[0]*8]*8; hf,vf,pl=e>>10&1,e>>11&1,e>>12
            for y in range(8):
                for x in range(8):
                    c=t[7-y if vf else y][7-x if hf else x]
                    if c==0 and layer: continue
                    P[bx+(q%2)*8+x,by+(q//2)*8+y]=pals[pl][c] if c or layer==0 else pals[pl][0]
img.save(out)
