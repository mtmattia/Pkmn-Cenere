# Importa metatile singoli da un secondario di Hoenn nel secondario petalburg, riusando i tile gia presenti (dedup sui pixel)
# e aggiornando tools/felicia/import_NOME.json. Lo strato basso dei metatile elencati in ERBA diventa erba.
# uso: python3 tools/felicia/import_extra.py sootopolis ceneride 6:11,7:12 259,25a,215,216,217,21d,21e,21f [erba=tutti]
import struct,sys,json
from PIL import Image
src,nome,pm,lst=sys.argv[1:5]
S=f"data/tilesets/secondary/{src}"; T="data/tilesets/secondary/petalburg"
pal={int(a):int(b) for a,b in (p.split(":") for p in pm.split(","))}
J=f"tools/felicia/import_{nome}.json"; M=json.load(open(J))
ids=[int(x,16) for x in lst.split(",") if str(int(x,16)) not in M]
smb=open(f"{S}/metatiles.bin","rb").read(); sat=open(f"{S}/metatile_attributes.bin","rb").read()
sim=Image.open(f"{S}/tiles.png"); sp=sim.load(); sw=sim.size[0]//8
tim=Image.open(f"{T}/tiles.png"); w,h=tim.size; tw=w//8; tp=tim.load()
def tdata(p,x0,y0): return tuple(p[x0+x,y0+y] for y in range(8) for x in range(8))
have={}
for k in range(tw*(h//8)): have.setdefault(tdata(tp,(k%tw)*8,(k//tw)*8),k)
newt=[]
def tile(t):
    d=tdata(sp,((t-512)%sw)*8,((t-512)//sw)*8)
    if d in have: return have[d]
    have[d]=tw*(h//8)+len(newt); newt.append(d); return have[d]
pmb=open("data/tilesets/primary/general/metatiles.bin","rb").read(); erba=struct.unpack_from("<4H",pmb,16)
ents=[]
for m in ids:
    e=[]
    for v in struct.unpack_from("<8H",smb,(m-512)*16):
        t=v&0x3ff; p=v>>12
        if t>=512: t=512+tile(t)
        e.append((v&0x0c00)|t|(pal.get(p,p)<<12))
    e[:4]=erba; ents.append(e)
rows=-(-len(newt)//tw)
new=Image.new("P",(w,h+rows*8)); new.putpalette(tim.getpalette()); new.paste(tim,(0,0)); px=new.load()
for k,d in enumerate(newt):
    dx,dy=(k%tw)*8,h+(k//tw)*8
    for i,c in enumerate(d): px[dx+i%8,dy+i//8]=c
new.save(f"{T}/tiles.png")
mb=open(f"{T}/metatiles.bin","rb").read(); first=512+len(mb)//16
open(f"{T}/metatiles.bin","ab").write(b"".join(struct.pack("<8H",*e) for e in ents))
open(f"{T}/metatile_attributes.bin","ab").write(b"".join(sat[(m-512)*2:(m-512)*2+2] for m in ids))
for k,m in enumerate(ids): M[str(m)]=first+k
json.dump(M,open(J,"w"))
print(len(ids),"metatile da",hex(first),"|",len(newt),"tile nuovi | totale tile",tw*(h//8)+rows*tw-(rows*tw-len(newt)))
