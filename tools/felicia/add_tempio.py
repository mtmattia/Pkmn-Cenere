# Tempio piatto (10x6 metatile, 160x96 px) ispirato al portico della Piramide Lotta: attico piatto in marmo,
# trabeazione, colonnato con interno rosso pompeiano, porta e scalinata. Palette pompeiana 07.
# Disegnato con ritmo di 16 px e tile deduplicati per occupare pochi tile.
# uso (una volta sola, dopo add_basilica.py): python3 tools/felicia/add_tempio.py -> id del primo metatile
import struct
from PIL import Image
T="data/tilesets/secondary/petalburg"
_,O,MW,L,M,D,S,T1,T2,T3,T4,RED,OC,WD,DK,BR=range(16)
Wd,Hd=160,96
a=[[0]*Wd for _ in range(Hd)]
for y in range(Hd):
    for x in range(Wd):
        e=x in (0,Wd-1)
        if y<40:                                   # attico piatto
            c=O if y==0 or e else (MW if y==1 or x in (1,) else L)
            if 0<y<34 and not e and x%16==0: c=M  # giunti delle lastre
            if 34<=y<40 and not e: c=MW if y==34 else (M if y<38 else D)   # cornice
            if y==39: c=O
        elif y<52:                                 # trabeazione con fregio
            k=x%16
            c=O if e or y==51 else (MW if y==40 else L if y<44 else (D if k in (6,9) and y<50 else M) if y<50 else S)
        elif y<84:                                 # colonnato
            k=x%16; yy=y-52
            if 4<=k<12:
                if yy<3: c=O if yy==0 or k in (4,11) else MW                      # capitello
                elif yy>=29: c=O if k in (4,11) or yy==31 else L                   # base
                else: c=O if k in (5,10) else (MW if k==6 else L if k==7 else M if k==8 else D) if 5<k<10 else 0
                if c==0: c=DK
            else: c=DK if yy<6 else (RED if yy<26 else BR)
            if e: c=O
        else:                                      # scalinata
            r=(y-84)%4
            c=O if e or y==Hd-1 else (MW if r==0 else L if r<3 else D)
        a[y][x]=c
for y in range(55,84):                             # porta centrale (tra le due colonne di mezzo)
    for x in range(76,84):
        a[y][x]=O if y==55 else (WD if x not in (79,80) else BR)
im=Image.open(f"{T}/tiles.png"); w,h=im.size; tw=w//8; tp=im.load(); ntiles=tw*(h//8)
def tdata(p,x0,y0): return tuple(p[x0+x,y0+y] for y in range(8) for x in range(8))
have={}; newt=[]
for k in range(ntiles): have.setdefault(tdata(tp,(k%tw)*8,(k//tw)*8),k)
def tile(d):
    if d not in have: have[d]=ntiles+len(newt); newt.append(d)
    return have[d]
ids=[[tile(tuple(a[ty*8+y][tx*8+x] for y in range(8) for x in range(8))) for tx in range(Wd//8)] for ty in range(Hd//8)]
rows=-(-len(newt)//tw)
new=Image.new("P",(w,h+rows*8)); new.putpalette(im.getpalette()); new.paste(im,(0,0)); px=new.load()
for k,d in enumerate(newt):
    for i,c in enumerate(d): px[(k%tw)*8+i%8,h+(k//tw)*8+i//8]=c
new.save(f"{T}/tiles.png")
pm=open("data/tilesets/primary/general/metatiles.bin","rb").read(); sotto=struct.unpack_from("<4H",pm,0x121*16)
mb=open(f"{T}/metatiles.bin","rb").read(); first=512+len(mb)//16
out=b""
for my in range(Hd//16):
    for mx in range(Wd//16):
        top=[(7<<12)|(512+ids[my*2+qy][mx*2+qx]) for qy in range(2) for qx in range(2)]
        out+=struct.pack("<8H",*sotto,*top)
open(f"{T}/metatiles.bin","ab").write(out)
n=(Wd//16)*(Hd//16); att=[0x1000]*n
att[(Hd//16-1)*(Wd//16)+Wd//32]=0  # (la porta diventera un warp quando faremo l'interno)
open(f"{T}/metatile_attributes.bin","ab").write(struct.pack(f"<{n}H",*att))
print(hex(first),"|",len(newt),"tile nuovi | totale",ntiles+len(newt))
