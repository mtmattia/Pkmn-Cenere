# Basilica del Foro (5x4 metatile, 80x64 px) con una palette pompeiana nuova (secondaria petalburg, slot 07, prima vuoto).
# Facciata: tetto in coppi, frontone in marmo, colonnato con interno in rosso pompeiano, scalinata.
# uso (dalla root del repo, una volta sola): python3 tools/felicia/add_basilica.py -> stampa l'id del primo metatile
import struct
from PIL import Image
T="data/tilesets/secondary/petalburg"
PAL=[(24,41,82),(56,40,40),(248,244,232),(224,216,196),(192,182,160),(150,140,124),(108,98,90),
     (232,140,96),(200,100,64),(152,68,48),(104,44,40),(176,48,40),(216,168,88),(120,72,40),(40,32,32),(88,56,40)]
open(f"{T}/palettes/07.pal","w").write("JASC-PAL\r\n0100\r\n16\r\n"+"".join(f"{r} {g} {b}\r\n" for r,g,b in PAL))
_,O,MW,L,M,D,S,T1,T2,T3,T4,RED,OC,WD,DK,BR=range(16)
Wd,Hd=80,64
a=[[0]*Wd for _ in range(Hd)]
def px(x,y,c):
    if 0<=x<Wd and 0<=y<Hd: a[y][x]=c
# tetto in coppi (y 0..23): file orizzontali di tegole con nervature verticali sfalsate
for y in range(0,24):
    for x in range(1,Wd-1):
        r=y%4; off=0 if (y//4)%2==0 else 3
        c=T2
        if r==3: c=T4
        elif r==0: c=T1
        elif (x+off)%6==0: c=T3
        a[y][x]=c
for x in range(Wd): a[0][x]=O
for y in range(24): a[y][0]=O; a[y][Wd-1]=O
# frontone triangolare (apice y=3, base y=23)
cx=Wd/2
for y in range(3,24):
    half=(y-3)*(Wd/2-2)/20
    for x in range(Wd):
        d=abs(x+0.5-cx)
        if d<=half:
            edge=d>half-1.6 or y==23
            a[y][x]=O if edge else (MW if d>half-3 or y==22 else L)
    # timpano piu scuro con un fregio
for y in range(9,21):
    half=(y-3)*(Wd/2-2)/20-4
    for x in range(Wd):
        d=abs(x+0.5-cx)
        if d<=half: a[y][x]=M if y<20 else D
for x in range(37,43):
    for y in range(13,18): a[y][x]=OC if 0<x-37<5 and 13<y<17 else D      # clipeo/scudo al centro
# trabeazione (y 24..28)
for y in range(24,29):
    for x in range(Wd):
        a[y][x]=O if y in (24,28) or x in (0,Wd-1) else (MW if y==25 else L if y==26 else M)
# colonnato (y 29..53): interno rosso, 6 colonne
for y in range(29,54):
    for x in range(1,Wd-1):
        a[y][x]=DK if y<34 else (RED if y<50 else BR)
    a[y][0]=O; a[y][Wd-1]=O
cols=[4,16,28,46,58,70]               # x sinistra di ogni colonna (larga 6), varco centrale piu largo
for c0 in cols:
    for y in range(29,54):
        for x in range(c0-1,c0+7):
            if y in (29,30):          # capitello
                a[y][x]=O if x in (c0-1,c0+6) or y==29 else MW
            elif y>=51:               # base
                a[y][x]=O if x in (c0-1,c0+6) else (L if y==51 else M)
            elif c0<=x<c0+6:
                k=x-c0; a[y][x]=O if k in (0,5) else (MW if k==1 else L if k==2 else M if k==3 else D)
# porta centrale in legno
for y in range(36,54):
    for x in range(35,45):
        a[y][x]=O if x in (35,44) or y==36 else (WD if (x-36)%4 else BR)
# scalinata (y 54..63)
for y in range(54,64):
    for x in range(Wd):
        r=(y-54)%3
        a[y][x]=O if x in (0,Wd-1) or y==63 else (MW if r==0 else L if r==1 else D)
im=Image.open(f"{T}/tiles.png"); w,h=im.size; ntiles=(w//8)*(h//8)
need=(Wd//8)*(Hd//8); rows=-(-need//(w//8))
new=Image.new("P",(w,h+rows*8)); new.putpalette(im.getpalette()); new.paste(im,(0,0)); p=new.load()
for ty in range(Hd//8):
    for tx in range(Wd//8):
        k=ty*(Wd//8)+tx; bx,by=(k%16)*8,h+(k//16)*8
        for y in range(8):
            for x in range(8): p[bx+x,by+y]=a[ty*8+y][tx*8+x]
new.save(f"{T}/tiles.png")
pm=open("data/tilesets/primary/general/metatiles.bin","rb").read()
sotto=struct.unpack_from("<4H",pm,0x121*16)            # lastricato sotto
mb=open(f"{T}/metatiles.bin","rb").read(); first=512+len(mb)//16
out=b""
for my in range(4):
    for mx in range(5):
        top=[(7<<12)|(512+ntiles+(my*2+qy)*10+mx*2+qx) for qy in range(2) for qx in range(2)]
        out+=struct.pack("<8H",*sotto,*top)
open(f"{T}/metatiles.bin","ab").write(out)
open(f"{T}/metatile_attributes.bin","ab").write(struct.pack("<20H",*[0x1000]*20))   # coperto: il giocatore resta davanti
Image.frombytes("RGB",(Wd,Hd),bytes(c for row in a for i in row for c in PAL[i])).resize((Wd*4,Hd*4),0).save("/tmp/claude-0/-home-claude/01fdd385-2078-57ce-a650-6cec9de82114/scratchpad/bas.png")
print(hex(first))
