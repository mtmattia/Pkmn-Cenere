# acqua a caustiche (celle scure + rete chiara + riflessi). uso: water_caustic.py SRC_GENERAL DST_GENERAL [frame_statico]
# il metatile d'acqua e' a scacchiera (tile A B / B A): pattern periodico sui vettori (8,8) e (8,-8)
import sys,os,shutil,struct,glob,math,collections
from PIL import Image
src,dst=sys.argv[1:3]; SF=int(sys.argv[3]) if len(sys.argv)>3 else 0
if os.path.exists(dst): shutil.rmtree(dst)
shutil.copytree(src,dst)
WATER={12,13,14}; BIANCO,RETE_LUCE,RETE,MEDIO,SCURO=1,11,12,13,14
SEEDS=[(2.0,2.5,0),(10.5,1.0,2),(6.5,7.0,4.5)]          # x,y,fase (dominio 16x16)
LAT=[(i*8+j*8,i*8-j*8) for i in range(-3,4) for j in range(-3,4)]
def field(f):
    a=f/8*2*math.pi; S=[(x+0.9*math.cos(a+p),y+0.9*math.sin(a+p*1.3)) for x,y,p in SEEDS]
    out={}
    for y in range(16):
        for x in range(16):
            d=sorted(((x+.5-sx-lx)**2+(y+.5-sy-ly)**2)**.5 for sx,sy in S for lx,ly in LAT)[:2]
            m=d[1]-d[0]
            c=RETE_LUCE if m<0.45 else RETE if m<1.1 else (MEDIO if d[0]>2.4 else SCURO)
            out[x,y]=c
    # riflessi: piccolo trattino bianco in alto a sinistra di ogni cella
    for sx,sy in S[:1]:
        for dx in (-2.0,-1.0):
            out[int(sx+dx)%16,int(sy-1.6)%16]=BIANCO
    return out
# offset di ogni tile nel pattern: quadranti 0/3 -> (0,0), 1/2 -> (8,0)
b=open(f"{dst}/metatiles.bin",'rb').read(); E=struct.unpack(f'<{len(b)//2}H',b); Q=collections.defaultdict(collections.Counter)
for i,e in enumerate(E):
    if e>>12==4: Q[e&0x3ff][(i%4) in (1,2)]+=1
OFF={t:(8 if c.most_common(1)[0][0] else 0) for t,c in Q.items()}
def tile(px,tx,ty,t,F):
    o=OFF.get(t,0)
    for y in range(8):
        for x in range(8):
            if px[tx+x,ty+y] in WATER: px[tx+x,ty+y]=F[(x+o)%16,y]
FR=[field(f) for f in range(8)]
for fp in sorted(glob.glob(f"{dst}/anim/water/*.png")):
    f=int(os.path.basename(fp)[0]); im=Image.open(fp); px=im.load(); w=im.size[0]//8
    for ty in range(0,im.size[1],8):
        for tx in range(0,im.size[0],8): tile(px,tx,ty,432+(ty//8)*w+tx//8,FR[f])
    im.save(fp)
im=Image.open(f"{dst}/tiles.png"); px=im.load()
for t in Q: tile(px,(t%16)*8,(t//16)*8,t,FR[SF])
im.save(f"{dst}/tiles.png")
