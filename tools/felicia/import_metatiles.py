# Importa nel tileset secondario petalburg i metatile usati in una zona di una mappa di Hoenn (con tile, palette e attributi).
# uso: python3 tools/felicia/import_metatiles.py SRC_TILESET MAPPA W H x0 y0 x1 y1 PAL_SRC:PAL_DST[,..] NOME
#  es.: python3 tools/felicia/import_metatiles.py sootopolis SootopolisCity 60 60 0 0 30 23 6:11,7:12 ceneride
# scrive tools/felicia/import_NOME.json con la corrispondenza vecchio id -> nuovo id.
import struct,sys,json,shutil
from PIL import Image
src,mapn,W,H,x0,y0,x1,y1,pm,nome=sys.argv[1],sys.argv[2],*map(int,sys.argv[3:9]),sys.argv[9],sys.argv[10]
S=f"data/tilesets/secondary/{src}"; T="data/tilesets/secondary/petalburg"
pal={int(a):int(b) for a,b in (p.split(":") for p in pm.split(","))}
for a,b in pal.items(): shutil.copy(f"{S}/palettes/{a:02}.pal",f"{T}/palettes/{b:02}.pal")
g=struct.unpack(f"<{W*H}H",open(f"data/layouts/{mapn}/map.bin","rb").read())
ids=[]
for y in range(y0,y1):
    for x in range(x0,x1):
        m=g[y*W+x]&0x3ff
        if m>=512 and m not in ids: ids.append(m)
smb=open(f"{S}/metatiles.bin","rb").read(); sat=open(f"{S}/metatile_attributes.bin","rb").read()
sim=Image.open(f"{S}/tiles.png"); sw=sim.size[0]//8; spx=sim.load()
tim=Image.open(f"{T}/tiles.png"); w,h=tim.size; tw=w//8; ntiles=tw*(h//8)
tl=[]; tmap={}
for m in ids:
    for v in struct.unpack_from("<8H",smb,(m-512)*16):
        t=v&0x3ff
        if t>=512 and t not in tmap: tmap[t]=ntiles+len(tl); tl.append(t)
rows=-(-len(tl)//tw)
new=Image.new("P",(w,h+rows*8)); new.putpalette(tim.getpalette()); new.paste(tim,(0,0)); px=new.load()
for k,t in enumerate(tl):
    s=t-512; sx,sy=(s%sw)*8,(s//sw)*8; d=ntiles+k-ntiles; dx,dy=(d%tw)*8,h+(d//tw)*8
    for y in range(8):
        for x in range(8): px[dx+x,dy+y]=spx[sx+x,sy+y]
new.save(f"{T}/tiles.png")
mb=open(f"{T}/metatiles.bin","rb").read(); first=512+len(mb)//16
out=b""; att=b""; mmap={}
for k,m in enumerate(ids):
    e=[]
    for v in struct.unpack_from("<8H",smb,(m-512)*16):
        t=v&0x3ff; p=v>>12
        if t>=512: t=512+tmap[t]
        if p in pal: p=pal[p]
        e.append((v&0x0c00)|t|(p<<12))
    out+=struct.pack("<8H",*e); att+=sat[(m-512)*2:(m-512)*2+2]; mmap[m]=first+k
open(f"{T}/metatiles.bin","ab").write(out); open(f"{T}/metatile_attributes.bin","ab").write(att)
json.dump({str(k):v for k,v in mmap.items()},open(f"tools/felicia/import_{nome}.json","w"))
print(nome,len(ids),"metatile da",hex(first),"|",len(tl),"tile | totale tile",ntiles+len(tl),"metatile",first+len(ids)-512)
