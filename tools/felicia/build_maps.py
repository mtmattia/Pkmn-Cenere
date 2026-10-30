# Genera i layout di Felicia componendo "timbri" presi da mappe esistenti.
# uso (dalla root del repo): python3 tools/felicia/build_maps.py
import struct,os

def load(name,w,h):
    b=open(f"data/layouts/{name}/map.bin",'rb').read()
    v=struct.unpack(f"<{w*h}H",b); return [list(v[y*w:(y+1)*w]) for y in range(h)]
PET=load("PetalburgCity",30,30)
R103=load("Route103",80,22)

def rect(src,x,y,w,h): return [row[x:x+w] for row in src[y:y+h]]
def cell(src,x,y): return src[y][x]
# timbri (coordinate in blocchi sulla mappa sorgente)
CASA_A  = rect(PET,5,2,5,4)
CASA_B  = rect(PET,9,16,4,4)
PALESTRA= rect(PET,12,4,6,5)
CENTRO  = rect(PET,19,13,4,4)   # Termopolio Pokémon
MARKET  = rect(PET,24,9,4,4)
ALBERO  = rect(PET,0,4,2,2)
ERBA    = cell(PET,3,11)
STRADA  = cell(PET,6,12)
FIORI   = cell(PET,4,6)
CARTELLO= cell(PET,8,9)
ERBA_ALTA=next(v for r in R103 for v in r if v&0x3ff==13)

class Mappa:
    def __init__(s,w,h,fill): s.w,s.h=w,h; s.g=[[fill]*w for _ in range(h)]
    def put(s,st,x,y):
        for j,r in enumerate(st):
            for i,v in enumerate(r):
                if 0<=x+i<s.w and 0<=y+j<s.h: s.g[y+j][x+i]=v
    def fill(s,v,x,y,w,h): s.put([[v]*w for _ in range(h)],x,y)
    def alberi(s,x,y,w,h):
        for j in range(0,h,2):
            for i in range(0,w,2): s.put(ALBERO,x+i,y+j)
    def save(s,name):
        os.makedirs(f"data/layouts/{name}",exist_ok=True)
        open(f"data/layouts/{name}/map.bin",'wb').write(struct.pack(f"<{s.w*s.h}H",*[v for r in s.g for v in r]))
        open(f"data/layouts/{name}/border.bin",'wb').write(struct.pack("<4H",*[v for r in ALBERO for v in r]))

# ---------------- Quintelia: griglia di insulae, Grande Palestra, Arena Magna a est
Q=Mappa(44,36,ERBA)
Q.alberi(0,0,44,2); Q.alberi(0,34,44,2); Q.alberi(0,0,2,36); Q.alberi(42,0,2,36)
# decumani (est-ovest) e cardini (nord-sud), larghi 2
for y in (10,22): Q.fill(STRADA,2,y,40,2)
for x in (12,26): Q.fill(STRADA,x,2,2,32)
Q.fill(STRADA,42,22,2,2)                       # uscita est verso la Via per Ercolia
# insula nord-ovest: Casa di Fausto (doppia) con giardino
Q.put(CASA_A,3,3); Q.put(CASA_A,7,3); Q.fill(FIORI,3,7,9,2)
# insula nord-centro: Grande Palestra
Q.put(PALESTRA,16,4); Q.fill(FIORI,15,9,2,1); Q.fill(FIORI,22,9,2,1)
# insula nord-est: case
Q.put(CASA_B,29,5); Q.put(CASA_B,35,5)
# insula centro-ovest: case dei Vincolati
Q.put(CASA_B,3,14); Q.put(CASA_B,7,14); Q.put(CASA_B,3,18)
# insula centrale: Termopolio Pokémon e mercato
Q.put(CENTRO,15,15); Q.put(MARKET,20,15); Q.put([[CARTELLO]],19,20)
# insula est: Arena Magna (segnaposto: grande spianata con anello di alberi)
Q.alberi(28,12,14,2); Q.alberi(28,12,2,10); Q.alberi(40,12,2,10)
Q.fill(STRADA,30,14,10,8); Q.fill(STRADA,33,12,4,2)
# insulae sud: case e Porta Marina
Q.put(CASA_A,3,25); Q.put(CASA_B,15,26); Q.put(CASA_B,20,26); Q.put(CASA_A,29,25); Q.put(CASA_B,36,26)
Q.fill(STRADA,12,34,2,2)                       # Porta Marina (sud, verso il mare: da collegare)
Q.save("Quintelia")

# ---------------- Via per Ercolia: da Quintelia verso est, ai piedi del Vesbio
V=Mappa(50,20,ERBA)
V.alberi(0,0,50,4); V.alberi(0,16,50,4); V.alberi(48,0,2,20)
V.fill(STRADA,0,10,30,2); V.fill(STRADA,28,6,2,6); V.fill(STRADA,28,6,20,2)
V.fill(ERBA_ALTA,6,5,8,4); V.fill(ERBA_ALTA,16,12,10,3); V.fill(ERBA_ALTA,34,9,8,5)
V.alberi(18,4,4,4); V.alberi(40,14,6,2)
V.put([[CARTELLO]],3,9)
V.save("ViaErcolia")
print("ok")
