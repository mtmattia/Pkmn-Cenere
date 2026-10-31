# Tempio a gradoni ricavato dalla Piramide Lotta (Parco Lotta, BattleFrontier_OutsideEast x53..64 y5..15),
# ricolorato in marmo sulla palette pompeiana 07 del secondario petalburg. Scrive tools/felicia/import_tempio.json.
# uso (una volta sola, dopo add_basilica.py): python3 tools/felicia/add_tempio.py
import struct,json
from PIL import Image
S="data/tilesets/secondary/battle_frontier_outside_east"; T="data/tilesets/secondary/petalburg"; P="data/tilesets/primary/general"
def pal(f): return [tuple(map(int,l.split())) for l in open(f).read().split("\n")[3:19]]
P07=pal(f"{T}/palettes/07.pal")
SRC={i:pal(f"{P}/palettes/{i:02}.pal") for i in range(6)}
for i in range(6,13): SRC[i]=pal(f"{S}/palettes/{i:02}.pal")
WANT={(255,189,131):(248,244,232),(238,148,115):(224,216,196),(222,106,98):(150,140,124),(205,65,82):(108,98,90)}
def near(c):
    c=WANT.get(c,c)
    return min(range(1,16),key=lambda i:sum((a-b)**2 for a,b in zip(P07[i],c)))
W=72; X0,Y0,X1,Y1=53,5,65,16
g=struct.unpack(f"<{W*72}H",open("data/layouts/BattleFrontier_OutsideEast/map.bin","rb").read())
smb=open(f"{S}/metatiles.bin","rb").read(); pmb=open(f"{P}/metatiles.bin","rb").read()
sat=open(f"{S}/metatile_attributes.bin","rb").read()
sim=Image.open(f"{S}/tiles.png"); spx=sim.load(); sw=sim.size[0]//8
pim=Image.open(f"{P}/tiles.png"); ppx=pim.load(); pw=pim.size[0]//8
tim=Image.open(f"{T}/tiles.png"); w,h=tim.size; tw=w//8; ntiles=tw*(h//8)
def entry(m): return struct.unpack_from("<8H",pmb if m<512 else smb,(m%512)*16)
ids=[]
for y in range(Y0,Y1):
    for x in range(X0,X1):
        m=g[y*W+x]&0x3ff
        if m not in ids: ids.append(m)
newt=[]; tkey={}
def tile(v):
    t=v&0x3ff; p=v>>12
    if (t,p) in tkey: return tkey[(t,p)]
    if t<512: src,sx,sy=ppx,(t%pw)*8,(t//pw)*8
    else: src,sx,sy=spx,((t-512)%sw)*8,((t-512)//sw)*8
    lut=[0]+[near(SRC[p][i]) for i in range(1,16)]
    newt.append([[lut[src[sx+x,sy+y]] for x in range(8)] for y in range(8)])
    tkey[(t,p)]=ntiles+len(newt)-1; return tkey[(t,p)]
ents=[]
for m in ids:
    e=[]
    for v in entry(m):
        if v&0x3ff==0 and m>=0: e.append(v if (v>>12) in (0,) and v&0x3ff==0 else (v&0x0c00)|(512+tile(v))|(7<<12)); continue
        e.append((v&0x0c00)|(512+tile(v))|(7<<12))
    ents.append(e)
rows=-(-len(newt)//tw)
new=Image.new("P",(w,h+rows*8)); new.putpalette(tim.getpalette()); new.paste(tim,(0,0)); px=new.load()
for k,a in enumerate(newt):
    dx,dy=(k%tw)*8,h+(k//tw)*8
    for y in range(8):
        for x in range(8): px[dx+x,dy+y]=a[y][x]
new.save(f"{T}/tiles.png")
mb=open(f"{T}/metatiles.bin","rb").read(); first=512+len(mb)//16
open(f"{T}/metatiles.bin","ab").write(b"".join(struct.pack("<8H",*e) for e in ents))
att=b""
for m in ids:
    a=struct.unpack_from("<H",sat if m>=512 else open(f"{P}/metatile_attributes.bin","rb").read(),(m%512)*2)[0]
    att+=struct.pack("<H",a)
open(f"{T}/metatile_attributes.bin","ab").write(att)
stamp=[[(g[y*W+x]&0xfc00)|(first+ids.index(g[y*W+x]&0x3ff)) for x in range(X0,X1)] for y in range(Y0,Y1)]
stamp[-1][9]=stamp[-1][8]   # via il cartello del Parco Lotta
json.dump(stamp,open("tools/felicia/import_tempio.json","w"))
print("tempio",len(ids),"metatile da",hex(first),"|",len(newt),"tile | totale",ntiles+len(newt))
