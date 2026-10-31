# Genera citta e percorsi di Felicia componendo "timbri" presi da mappe esistenti.
# Scrive layout (map.bin/border.bin), map.json, scripts.inc dei cartelli, gruppo mappe, layouts.json e nomi delle sezioni.
# uso (dalla root del repo): python3 tools/felicia/add_statua.py (una volta) ; python3 tools/felicia/build_maps.py
import struct,os,json

def load(name,w,h):
    v=struct.unpack(f"<{w*h}H",open(f"data/layouts/{name}/map.bin",'rb').read())
    return [list(v[y*w:(y+1)*w]) for y in range(h)]
PET=load("PetalburgCity",30,30)
R103=load("Route103",80,22)
def rect(x,y,w,h): return [r[x:x+w] for r in PET[y:y+h]]

# ---- timbri
CASA_A  = rect(5,2,5,4)
CASA_B  = rect(9,16,4,4)
PALESTRA= rect(12,4,6,5)
CENTRO  = rect(19,13,4,4)      # Termopolio Pokemon
MARKET  = rect(24,9,4,4)
ALBERO  = rect(0,4,2,2)
ERBA    = PET[11][3]
STRADA  = PET[12][6]
FIORI   = PET[6][4]
CARTELLO= PET[9][8]
ERBA_ALTA=next(v for r in R103 for v in r if v&0x3ff==13)
STATUA_ID=0x290                # da add_statua.py
PALKIA_ID=0x299                # da add_statua_palkia.py: statua 3x3
BASILICA_ID=0x2a2              # da add_basilica.py: 5x4, palette pompeiana 07
BASILICA=[[0x3400|(BASILICA_ID+j*5+i) for i in range(5)] for j in range(4)]
MURA_ID=0x294                  # da add_mura.py: sommita, paramento, arco sx, arco dx
SOMMITA,PARAMENTO=0x3400|MURA_ID,0x3400|(MURA_ID+1)
ARCO=[0x3000|(MURA_ID+2),0x3000|(MURA_ID+3)]
SOMMITA_INT=0x3400|0x298          # da add_sommita_int.py: sommita senza riga bianca, per muro continuo
STATUA  = [[(STATUA_ID+i)|0x3400 for i in (0,1)],[(STATUA_ID+i)|0x3400 for i in (2,3)]]
ACQUA   = {k:0x1000|v for k,v in dict(c=0x0a1,tl=0x0b0,t=0x0b1,tr=0x0b2,l=0x0b8,r=0x0ba,bl=0x0c8,b=0x0c9,br=0x0ca).items()}

class Mappa:
    def __init__(s,w,h):
        s.w,s.h=w,h; s.g=[[ERBA]*w for _ in range(h)]; s.occ=[[0]*w for _ in range(h)]
        s.gates={}; s.signs=[]; s.interni=[]
        s.alberi(0,0,w,2); s.alberi(0,h-2,w,2); s.alberi(0,0,2,h); s.alberi(w-2,0,2,h)
    def ok(s,x,y): return 0<=x<s.w and 0<=y<s.h
    def put(s,st,x,y,mark=2):
        for j,r in enumerate(st):
            for i,v in enumerate(r):
                if s.ok(x+i,y+j): s.g[y+j][x+i]=v; s.occ[y+j][x+i]=mark
    def fill(s,v,x,y,w,h,mark=1): s.put([[v]*w for _ in range(h)],x,y,mark)
    def strada(s,x,y,w,h): s.fill(STRADA,x,y,w,h,1)
    def alberi(s,x,y,w,h):
        for j in range(0,h,2):
            for i in range(0,w,2): s.put(ALBERO,x+i,y+j,3)
    def anello(s,x,y,w,h,ingresso=None,pietra=True):
        # recinto ellittico semplificato: in pietra per anfiteatri e teatri, di alberi per le acropoli
        if pietra:
            for yy,v in ((y,SOMMITA),(y+1,PARAMENTO),(y+h-2,SOMMITA),(y+h-1,PARAMENTO)): s.fill(v,x,yy,w,1,3)
            for xx in (x,x+1,x+w-2,x+w-1): s.fill(SOMMITA,xx,y+1,1,h-3,3)   # lati fino alla riga y+1 (angoli continui)
        else:
            s.alberi(x,y,w,2); s.alberi(x,y+h-2,w,2); s.alberi(x,y,2,h); s.alberi(x+w-2,y,2,h)
        s.strada(x+2,y+2,w-4,h-4)
        if ingresso:
            ix,iy=ingresso[0],ingresso[1]
            if pietra: s.put([ARCO],ix,iy,1); s.strada(ix,iy+1,2,1)
            else: s.strada(*ingresso)
    def acqua(s,x,y,w,h,lati="tblr"):
        for j in range(h):
            for i in range(w):
                t='t' in lati and j==0; b='b' in lati and j==h-1; l='l' in lati and i==0; r='r' in lati and i==w-1
                k=('t' if t else 'b' if b else '')+('l' if l else 'r' if r else '')
                s.fill(ACQUA[k or 'c'],x+i,y+j,1,1,4)
    def cartello(s,x,y,testo):
        s.fill(CARTELLO,x,y,1,1,2); s.signs.append((x,y,testo))
    def statua(s,x,y): s.put(STATUA,x,y,2)
    def statua_palkia(s,x,y): s.put([[0x3400|(PALKIA_ID+j*3+i) for i in range(3)] for j in range(3)],x,y,2)
    def edificio(s,st,x,y,nome=None):
        s.put(st,x,y,2)
        tipo={id(CENTRO):'pc',id(MARKET):'mart',id(PALESTRA):'gym'}.get(id(st))
        if tipo: s.interni.append((tipo,x,y,None))
        if nome: s.cartello(x-1 if x>2 else x+len(st[0]),y+len(st)-1,nome)
    def mura(s):
        # cinta in opus quadratum: sommita + paramento a nord e a sud, sommita sui lati
        s.murata=True
        for y,v in ((0,SOMMITA),(1,PARAMENTO),(s.h-2,SOMMITA),(s.h-1,PARAMENTO)): s.fill(v,0,y,s.w,1,3)
        for x in (0,1,s.w-2,s.w-1): s.fill(SOMMITA,x,1,1,s.h-3,3)   # i lati salgono fino alla riga 1 (angoli continui)
    def porta(s,lato,pos,nome=None):
        # varco nelle mura di alberi, largo 2, con strada fino al bordo
        if lato=='E': s.strada(s.w-2,pos,2,2)
        if lato=='W': s.strada(0,pos,2,2)
        if lato=='N': s.strada(pos,0,2,2)
        if lato=='S': s.strada(pos,s.h-2,2,2)
        if getattr(s,'murata',False) and lato in 'NS':
            s.put([ARCO],pos,0 if lato=='N' else s.h-2,1)
        s.gates[lato]=pos
        if nome:
            cx,cy={'E':(s.w-3,pos-1),'W':(2,pos-1),'N':(pos-1,2),'S':(pos-1,s.h-3)}[lato]
            s.cartello(cx,cy,nome)
    def case(s,x0,y0,x1,y1):
        # riempie l'area di case allineate lungo le strade, lasciando libera la riga davanti alla porta
        for st in (CASA_A,CASA_B):
            h,w=len(st),len(st[0]); y=y0
            while y+h<y1:
                x=x0; placed=False
                while x+w<=x1:
                    if all(s.ok(x+i,y+j) and s.occ[y+j][x+i]==0 for j in range(h+1) for i in range(w)):
                        s.put(st,x,y,2); x+=w+1; placed=True
                    else: x+=1
                y+=h+1 if placed else 1
    def casa_interna(s,x,y,cartella):
        s.interni.append(('casa',x,y,cartella))
    def terme(s,x,y,cartella):
        s.interni.append(('terme',x,y,cartella))
    def erba_alta(s,x,y,w,h): s.fill(ERBA_ALTA,x,y,w,h,1)
    def save(s,name):
        for y in range(s.h-1,0,-1):     # sommita con altra sommita sopra -> variante continua
            for x in range(s.w):
                if s.g[y][x]&0x3ff==MURA_ID and s.g[y-1][x]&0x3ff in (MURA_ID,0x298): s.g[y][x]=(s.g[y][x]&~0x3ff)|0x298
        os.makedirs(f"data/layouts/{name}",exist_ok=True)
        open(f"data/layouts/{name}/map.bin",'wb').write(struct.pack(f"<{s.w*s.h}H",*[v for r in s.g for v in r]))
        open(f"data/layouts/{name}/border.bin",'wb').write(struct.pack("<4H",*[v for r in ALBERO for v in r]))

M={}   # nome -> (Mappa, info)
def mappa(cartella,w,h,**info): m=Mappa(w,h); M[cartella]=(m,info); return m

# ================= QUINTELIA (Pompei, specchiata come la regione) =================
# Assi reali: Via dell'Abbondanza (Foro -> Porta Sarno), Via Stabiana (Porta Vesuvio -> Porta Stabia),
# Via di Nola a nord, Via di Mercurio a nord del Foro, Via Consolare verso Porta Ercolano.
# Specchiata: Foro e Porta Marina a est, Anfiteatro e Grande Palestra a sud-ovest, teatri a sud.
Q=mappa("Quintelia",64,48,id="MAP_QUINTELIA",sec="MAPSEC_LITTLEROOT_TOWN",nome="QUINTELIA",music="MUS_PETALBURG",tipo="MAP_TYPE_CITY")
Q.mura()
Q.strada(2,10,60,2)                         # Via di Nola
Q.strada(54,6,8,2); Q.strada(54,6,2,6)      # Via Consolare -> Porta Ercolano
Q.strada(0,27,44,2)                         # Via dell'Abbondanza
Q.strada(29,2,2,46)                         # Via Stabiana
Q.strada(47,2,2,14)                         # Via di Mercurio
Q.strada(14,2,2,26); Q.strada(38,11,2,17)   # vicoli nord-sud
Q.strada(2,19,42,2)                         # decumano minore
Q.strada(44,15,14,19)                       # Foro
Q.strada(56,22,8,2)                         # Porta Marina
Q.porta('E',6,"PORTA ERCOLANO\n{RIGHT_ARROW} VIA ERCOLIA"); Q.porta('E',22,"PORTA MARINA\n{RIGHT_ARROW} VIA ERCOLIA")
Q.porta('W',27,"PORTA SARNO\n{LEFT_ARROW} VIA NUCERINA"); Q.porta('S',29,"PORTA STABIA\n{DOWN_ARROW} VIA STABIANA")
Q.porta('N',29,"PORTA VESUVIO\n{UP_ARROW} MONTE VESBIO")
Q.statua_palkia(50,22); Q.cartello(49,25,"FORO DI QUINTELIA\nPalkia veglia sul Foro.")
Q.edificio(BASILICA,48,15,"BASILICA"); Q.edificio(MARKET,44,15)
Q.edificio(CENTRO,31,22); Q.cartello(35,25,"TERMOPOLIO POKEMON")
Q.edificio(CASA_A,23,22,"TERME STABIANE"); Q.terme(23,22,"TermeStabiane")
Q.put(CASA_A,32,13); Q.put(CASA_A,37,13); Q.fill(FIORI,32,17,10,1); Q.cartello(31,17,"CASA DI FAUSTO"); Q.casa_interna(32,13,"CasaDiFausto")
Q.anello(3,29,13,14,(8,29,3,2)); Q.cartello(7,31,"ARENA MAGNA\nChiusa dalla Rissa dell'Arena.")
Q.alberi(17,31,12,2); Q.edificio(PALESTRA,19,33); Q.strada(17,38,12,6); Q.cartello(18,37,"GRANDE PALESTRA\nCapopalestra: Celado")
Q.anello(32,33,12,11,(36,33,3,2)); Q.cartello(35,32,"TEATRO GRANDE")
Q.put(CASA_A,2,22); Q.put(CASA_A,8,22); Q.put(CASA_A,16,22)   # case sul lato sud del decumano, allineate alle Terme
Q.case(2,2,62,46)
Q.start=(30,28)

# ================= VIA ERCOLIA: Porta Ercolano e Porta Marina -> Ercolia, sotto le pendici del Vesbio
R1=mappa("ViaErcolia",40,48,id="MAP_VIA_ERCOLIA",sec="MAPSEC_ROUTE_101",nome="VIA ERCOLIA",music="MUS_ROUTE101",tipo="MAP_TYPE_ROUTE")
R1.porta('W',6); R1.porta('W',22); R1.porta('E',16)
R1.strada(0,6,20,2); R1.strada(18,6,2,12); R1.strada(0,22,20,2); R1.strada(18,16,2,8); R1.strada(18,16,22,2)
R1.cartello(4,5,"VIA DEI SEPOLCRI\nLe tombe delle famiglie di Quintelia."); R1.cartello(36,15,"VIA ERCOLIA\n{RIGHT_ARROW} ERCOLIA")
R1.erba_alta(22,3,14,5); R1.erba_alta(4,10,10,6); R1.erba_alta(24,22,12,6); R1.erba_alta(4,28,12,8)
R1.alberi(22,10,6,4); R1.alberi(8,38,10,6); R1.alberi(22,32,14,8)

# ================= ERCOLIA (Ercolano): griglia regolare di cardini e decumani, citta sul mare
E=mappa("Ercolia",40,36,id="MAP_ERCOLIA",sec="MAPSEC_OLDALE_TOWN",nome="ERCOLIA",music="MUS_OLDALE",tipo="MAP_TYPE_TOWN")
E.mura()
E.porta('W',10,"ERCOLIA\nLa citta di Ercole sul mare."); E.porta('E',10,"{RIGHT_ARROW} VIA NEAPOLITANA")
E.strada(0,10,40,2)                         # Decumano Massimo
E.strada(2,18,36,2)                         # Decumano Inferiore
for x in (10,20,30): E.strada(x,2,2,23)     # Cardini III, IV, V
E.strada(2,24,36,2)                         # passeggiata sul mare
E.acqua(2,26,36,8,"t"); E.alberi(0,34,40,2)
E.edificio(CENTRO,13,13); E.cartello(17,16,"TERMOPOLIO POKEMON")
E.edificio(PALESTRA,23,19); E.cartello(22,23,"PALESTRA DI ERCOLIA\nCapopalestra: Rettina")
E.edificio(CASA_A,13,3,"TERME"); E.terme(13,3,"Terme"); E.edificio(MARKET,33,13)
E.case(2,2,38,24)

# ================= VIA NEAPOLITANA: costa tra Ercolia e Neapolia
R4=mappa("ViaNeapolitana",48,24,id="MAP_VIA_NEAPOLITANA",sec="MAPSEC_ROUTE_104",nome="VIA NEAPOLITANA",music="MUS_ROUTE104",tipo="MAP_TYPE_ROUTE")
R4.porta('W',8); R4.porta('E',8)
R4.strada(0,8,16,2); R4.strada(14,8,2,6); R4.strada(14,12,20,2); R4.strada(32,8,2,6); R4.strada(32,8,16,2)
R4.fill(STRADA,2,15,44,2); R4.acqua(2,17,44,5,"t")
R4.erba_alta(4,3,10,4); R4.erba_alta(18,3,12,8); R4.erba_alta(36,11,8,3); R4.alberi(36,2,8,4)
R4.cartello(4,7,"VIA NEAPOLITANA\n{RIGHT_ARROW} NEAPOLIA")

# ================= NEAPOLIA (Napoli): impianto greco a plateiai e stenopoi, agora, porto
N=mappa("Neapolia",64,48,id="MAP_NEAPOLIA",sec="MAPSEC_SLATEPORT_CITY",nome="NEAPOLIA",music="MUS_SLATEPORT",tipo="MAP_TYPE_CITY")
N.mura()
N.porta('W',22,"NEAPOLIA\nLa citta nuova dei Greci."); N.porta('E',22,"{RIGHT_ARROW} CRYPTA NEAPOLITANA")
for y in (10,22,34): N.strada(0 if y==22 else 2,y,64 if y==22 else 60,2)   # tre plateiai
for x in range(8,58,8): N.strada(x,2,2,36)                                    # stenopoi
N.strada(26,24,14,10)                                                         # agora
N.statua(32,28); N.cartello(31,30,"AGORA DI NEAPOLIA\nQui si discute in greco.")
N.edificio(CENTRO,18,12); N.edificio(MARKET,42,12)
N.edificio(PALESTRA,42,27); N.cartello(41,31,"PALESTRA DI NEAPOLIA\nCapopalestra: il Filosofo")
N.anello(10,24,14,10,(15,24,3,2)); N.cartello(14,23,"TEATRO\nVi canto' anche un imperatore.")
N.fill(STRADA,2,38,60,2); N.acqua(2,40,60,6,"t")
N.case(2,2,62,38)
N.cartello(22,15,"TERMOPOLIO POKEMON")

# ================= CRYPTA NEAPOLITANA: la galleria scavata nella collina verso Puteola
R5=mappa("CryptaNeapolitana",48,20,id="MAP_CRYPTA_NEAPOLITANA",sec="MAPSEC_ROUTE_105",nome="CRYPTA NEAPOLIS",music="MUS_ROUTE110",tipo="MAP_TYPE_ROUTE")
R5.porta('W',10); R5.porta('E',10)
R5.alberi(2,2,44,7); R5.alberi(2,12,44,6)
R5.strada(0,10,48,2); R5.erba_alta(20,9,8,1)
R5.cartello(4,9,"CRYPTA NEAPOLITANA\nGalleria lunga settecento passi.")

# ================= PUTEOLA (Pozzuoli): porto del grano, macellum, anfiteatro flavio
P=mappa("Puteola",56,44,id="MAP_PUTEOLA",sec="MAPSEC_PETALBURG_CITY",nome="PUTEOLA",music="MUS_LILYCOVE",tipo="MAP_TYPE_CITY")
P.mura()
P.porta('W',14,"PUTEOLA\nIl porto del grano di Felicia."); P.porta('E',14,"{RIGHT_ARROW} VIA CUMANA")
P.strada(0,14,56,2); P.strada(2,26,38,2); P.strada(24,2,2,38); P.strada(38,16,2,12)
P.anello(4,2,16,12,(10,12,3,2)); P.cartello(9,15,"ANFITEATRO FLAVIO")
P.strada(26,17,12,8); P.statua(31,20); P.cartello(30,22,"MACELLUM\nIl mercato del porto.")
P.edificio(MARKET,27,17)
P.edificio(CENTRO,16,17); P.cartello(20,20,"TERMOPOLIO POKEMON")
P.edificio(PALESTRA,28,30); P.strada(26,35,12,4); P.cartello(27,34,"PALESTRA DI PUTEOLA\nCapopalestra: il Mercante")
P.acqua(40,28,14,14,"tl"); P.strada(38,28,2,14); P.strada(26,39,12,2)
P.case(2,2,54,42)

# ================= VIA CUMANA: lungo il Lago Avernio
R6=mappa("ViaCumana",48,32,id="MAP_VIA_CUMANA",sec="MAPSEC_ROUTE_106",nome="VIA CUMANA",music="MUS_ROUTE113",tipo="MAP_TYPE_ROUTE")
R6.porta('W',14); R6.porta('E',10)
R6.strada(0,14,12,2); R6.strada(10,10,2,6); R6.strada(10,10,38,2)
R6.acqua(16,14,18,12); R6.cartello(14,13,"LAGO AVERNIO\nGli uccelli non lo sorvolano.")
R6.erba_alta(4,18,10,10); R6.erba_alta(36,14,8,12); R6.alberi(14,2,20,6)

# ================= CUMARA (Cuma): acropoli sul colle, antro della Sibila, citta bassa, mare a est
C=mappa("Cumara",44,40,id="MAP_CUMARA",sec="MAPSEC_FALLARBOR_TOWN",nome="CUMARA",music="MUS_FORTREE",tipo="MAP_TYPE_TOWN")
C.mura()
C.porta('W',12,"CUMARA\nLa citta piu antica di Felicia."); C.porta('S',30,"{DOWN_ARROW} VIA MISENA")
C.anello(20,2,16,16,(26,16,3,2),pietra=False); C.edificio(PALESTRA,25,4); C.strada(22,9,12,7)
C.cartello(24,8,"ANTRO DELLA SIBILA\nCapopalestra: la Sibila"); C.edificio(CASA_A,22,10,"TEMPIO DI APOLLO")
C.strada(0,12,20,2); C.strada(18,18,2,20); C.strada(18,18,20,2); C.strada(30,18,2,22)
C.strada(4,24,12,8); C.statua(9,27); C.cartello(8,29,"FORO DI CUMARA")
C.edificio(CENTRO,22,22); C.cartello(26,25,"TERMOPOLIO POKEMON")
C.acqua(36,20,6,18,"l")
C.case(2,2,36,38)

# ================= VIA MISENA: costa di Baia, terme sul mare
R7=mappa("ViaMisena",32,40,id="MAP_VIA_MISENA",sec="MAPSEC_ROUTE_107",nome="VIA MISENA",music="MUS_ROUTE119",tipo="MAP_TYPE_ROUTE")
R7.porta('N',12); R7.porta('S',12)
R7.strada(12,0,2,14); R7.strada(6,12,8,2); R7.strada(6,12,2,14); R7.strada(6,24,8,2); R7.strada(12,24,2,16)
R7.acqua(22,2,8,36,"l"); R7.edificio(CASA_A,15,16,"TERME DI BAIA\nI Domini vengono qui d'inverno."); R7.terme(15,16,"TermeDiBaia")
R7.erba_alta(2,2,8,8); R7.erba_alta(14,28,6,8); R7.alberi(2,28,4,10)

# ================= MISENIA (Miseno): porto della flotta, capo, villa di Pinio
Mi=mappa("Misenia",48,40,id="MAP_MISENIA",sec="MAPSEC_RUSTBORO_CITY",nome="MISENIA",music="MUS_RUSTBORO",tipo="MAP_TYPE_CITY")
Mi.mura()
Mi.porta('N',20,"MISENIA\nPorto della flotta di Amoria.")
Mi.strada(20,2,2,24); Mi.strada(2,10,44,2); Mi.strada(4,24,40,2)
Mi.acqua(4,26,40,12,"t")
Mi.put(CASA_A,4,3); Mi.put(CASA_A,9,3); Mi.fill(FIORI,4,7,10,2); Mi.cartello(3,8,"VILLA DEL PROF. PINIO"); Mi.casa_interna(4,3,"VillaDiPinio")
Mi.edificio(PALESTRA,36,3); Mi.strada(34,8,10,2); Mi.cartello(35,7,"PALESTRA DI MISENIA\nCapopalestra: il Navarca")
Mi.edificio(CENTRO,23,13); Mi.cartello(27,16,"TERMOPOLIO POKEMON"); Mi.edificio(MARKET,28,13)
Mi.cartello(44,23,"GROTTA DELLA DRAGONARA")
Mi.case(2,2,46,24)

# ================= VIA STABIANA: vigne tra Quintelia e Stabella
R2=mappa("ViaStabiana",32,40,id="MAP_VIA_STABIANA",sec="MAPSEC_ROUTE_102",nome="VIA STABIANA",music="MUS_ROUTE110",tipo="MAP_TYPE_ROUTE")
R2.porta('N',14); R2.porta('S',16)
R2.strada(14,0,2,16); R2.strada(14,14,4,2); R2.strada(16,14,2,26)
for y in range(4,30,3): R2.erba_alta(3,y,9,1); R2.erba_alta(20,y,9,1)   # filari di vigne
R2.cartello(12,3,"VIA STABIANA\nVigne del Vesbio.")

# ================= STABELLA (Stabia): ville sulla collina a picco sul mare
S=mappa("Stabella",44,36,id="MAP_STABELLA",sec="MAPSEC_DEWFORD_TOWN",nome="STABELLA",music="MUS_DEWFORD",tipo="MAP_TYPE_TOWN")
S.mura()
S.porta('N',20,"STABELLA\nLe ville dei Domini sul mare.")
S.strada(20,2,2,30); S.strada(2,14,34,2); S.strada(2,28,34,2)
S.acqua(36,2,6,32,"l")
for x,y,n in ((4,3,"VILLA SAN MARCO"),(24,3,"VILLA ARIANNA")):
    S.put(CASA_A,x,y); S.put(CASA_A,x+5,y); S.fill(FIORI,x,y+4,10,2); S.cartello(x+10,y+5,n)
S.edificio(PALESTRA,6,19); S.erba_alta(4,24,12,3); S.cartello(5,23,"PALESTRA DI STABELLA\nCapopalestra: la Vignaiola")
S.edificio(CENTRO,24,17); S.cartello(28,20,"TERMOPOLIO POKEMON")
S.case(2,2,36,34)

# ================= VIA NUCERINA: verso Nucelia, guado del fiume Sarno
R3=mappa("ViaNucerina",48,30,id="MAP_VIA_NUCERINA",sec="MAPSEC_ROUTE_103",nome="VIA NUCERINA",music="MUS_ROUTE120",tipo="MAP_TYPE_ROUTE")
R3.porta('E',14); R3.porta('W',14)
R3.strada(0,14,48,2)
R3.acqua(22,2,4,12,"lr"); R3.acqua(22,16,4,12,"lr"); R3.cartello(20,13,"GUADO DEL SARNO")
R3.erba_alta(4,4,14,8); R3.erba_alta(30,18,12,8); R3.alberi(30,2,14,8); R3.alberi(4,20,12,6)
R3.cartello(44,13,"VIA NUCERINA\n{LEFT_ARROW} NUCELIA")

# ================= NUCELIA (Nocera): citta murata dell'entroterra, anfiteatro dei tifosi
Nu=mappa("Nucelia",44,40,id="MAP_NUCELIA",sec="MAPSEC_LAVARIDGE_TOWN",nome="NUCELIA",music="MUS_FALLARBOR",tipo="MAP_TYPE_TOWN")
Nu.mura()
Nu.porta('E',20,"NUCELIA\nNessuno qui ha dimenticato la Rissa.")
Nu.strada(2,20,42,2); Nu.strada(20,2,2,36); Nu.strada(2,10,40,2); Nu.strada(2,30,40,2)
Nu.anello(4,22,14,14,(9,22,3,2)); Nu.cartello(8,21,"ANFITEATRO DI NUCELIA")
Nu.edificio(PALESTRA,26,23); Nu.strada(24,28,10,2); Nu.cartello(25,27,"PALESTRA DI NUCELIA\nCapo dei tifosi nuceliani")
Nu.edificio(CENTRO,24,13); Nu.cartello(28,16,"TERMOPOLIO POKEMON"); Nu.edificio(MARKET,30,13)
Nu.statua(10,14); Nu.cartello(9,16,"FORO DI NUCELIA")
Nu.case(2,2,42,38)

# ================= collegamenti (offset calcolati dalle porte)
def colleg(a,lato,b):
    ma,_=M[a]; mb,_=M[b]
    opp={'E':'W','W':'E','N':'S','S':'N'}[lato]
    off=ma.gates[lato]-mb.gates[opp]
    dir={'E':'right','W':'left','N':'up','S':'down'}
    M[a][1].setdefault('conn',[]).append({"map":M[b][1]['id'],"offset":off,"direction":dir[lato]})
    M[b][1].setdefault('conn',[]).append({"map":M[a][1]['id'],"offset":-off,"direction":dir[opp]})
# Quintelia ha due porte a est sulla stessa Via Ercolia: l'offset si calcola sulla prima
colleg("Quintelia",'E',"ViaErcolia"); colleg("ViaErcolia",'E',"Ercolia"); colleg("Ercolia",'E',"ViaNeapolitana")
colleg("ViaNeapolitana",'E',"Neapolia"); colleg("Neapolia",'E',"CryptaNeapolitana"); colleg("CryptaNeapolitana",'E',"Puteola")
colleg("Puteola",'E',"ViaCumana"); colleg("ViaCumana",'E',"Cumara"); colleg("Cumara",'S',"ViaMisena"); colleg("ViaMisena",'S',"Misenia")
colleg("Quintelia",'S',"ViaStabiana"); colleg("ViaStabiana",'S',"Stabella")
colleg("Quintelia",'W',"ViaNucerina"); colleg("ViaNucerina",'W',"Nucelia")

# ================= interni: porte -> Termopolio, mercato, palestra, case importanti
PORTA={'pc':(1,3),'mart':(1,3),'gym':(3,4),'casa':(2,3),'terme':(2,3)}
INT={'pc':("Termopolio","LAYOUT_POKEMON_CENTER_1F","MUS_POKE_CENTER",[(6,8),(7,8)]),
     'mart':("Mercato","LAYOUT_MART","MUS_POKE_MART",[(3,7),(4,7)]),
     'gym':("Palestra","LAYOUT_RUSTBORO_CITY_GYM","MUS_GYM",[(5,19),(6,19)]),
     'casa':(None,"LAYOUT_HOUSE1",None,[(3,8),(4,8)]),
     'terme':(None,"LAYOUT_TERME",None,[(7,12),(8,12)])}

# ---- layout delle terme: due vasche calde e sabbie calde di Cuordilava (tileset lavaridge)
LAV=(lambda v:[list(v[y*20:(y+1)*20]) for y in range(20)])(struct.unpack("<400H",open("data/layouts/LavaridgeTown/map.bin","rb").read()))
TERME=Mappa(16,14)
for ox in (2,8): TERME.put([r[2:8] for r in LAV[2:11]],ox,2,2)
TERME.strada(2,11,12,1); TERME.fill(0x3024,7,12,2,1,1)     # uscita (freccia verso sud)
TERME.save("Terme")
def snake(n): return "".join("_"+c if c.isupper() and i and n[i-1]!="_" else c for i,c in enumerate(n)).upper()
INTERNI={}   # cartella -> dict
CURE=[]
for citta,(m,info) in list(M.items()):
    m.warps=[]
    for tipo,x,y,nome in m.interni:
        suff,layout,music,uscite=INT[tipo]
        cart=f"{citta}_{nome or suff}"
        dx,dy=PORTA[tipo]; m.warps.append({"x":x+dx,"y":y+dy,"elevation":0,"dest_map":"MAP_"+snake(cart),"dest_warp_id":"0"})
        INTERNI[cart]=dict(tipo=tipo,citta=citta,layout=layout,music=music or info['music'],sec=info['sec'],
            uscite=[{"x":ux,"y":uy,"elevation":0 if tipo!='pc' else 3,"dest_map":info['id'],"dest_warp_id":str(len(m.warps)-1)} for ux,uy in uscite])
        if tipo=='pc': CURE.append({"id":"HEAL_LOCATION_"+snake(citta),"map":info['id'],"x":x+dx,"y":y+dy+1,
            "respawn_map":"MAP_"+snake(cart),"respawn_npc":"LOCALID_"+snake(citta)+"_NURSE"})

def interno_json(cart,d):
    obj=[]; sc=[]
    if d['tipo']=='pc':
        sc.append(f"{cart}_MapScripts::\n\tmap_script MAP_SCRIPT_ON_TRANSITION, {cart}_OnTransition\n\tmap_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume\n\t.byte 0\n")
        sc.append(f"{cart}_OnTransition:\n\tsetrespawn HEAL_LOCATION_{snake(d['citta'])}\n\tend\n")
        sc.append(f"{cart}_EventScript_Nurse::\n\tsetvar VAR_0x800B, LOCALID_{snake(d['citta'])}_NURSE\n\tcall Common_EventScript_PkmnCenterNurse\n\twaitmessage\n\twaitbuttonpress\n\trelease\n\tend\n")
        obj.append({"local_id":f"LOCALID_{snake(d['citta'])}_NURSE","graphics_id":"OBJ_EVENT_GFX_NURSE","x":7,"y":2,"elevation":3,
            "movement_type":"MOVEMENT_TYPE_FACE_DOWN","movement_range_x":0,"movement_range_y":0,"trainer_type":"TRAINER_TYPE_NONE",
            "trainer_sight_or_berry_tree_id":"0","script":f"{cart}_EventScript_Nurse","flag":"0"})
    else:
        sc.append(f"{cart}_MapScripts::\n\t.byte 0\n")
    if d['tipo']=='mart':
        sc.append(f"{cart}_EventScript_Clerk::\n\tlock\n\tfaceplayer\n\tmessage gText_HowMayIServeYou\n\twaitmessage\n\tpokemart {cart}_Pokemart\n\tmsgbox gText_PleaseComeAgain, MSGBOX_DEFAULT\n\trelease\n\tend\n")
        sc.append(f"\t.align 2\n{cart}_Pokemart:\n\t.2byte ITEM_POKE_BALL\n\t.2byte ITEM_POTION\n\t.2byte ITEM_ANTIDOTE\n\t.2byte ITEM_PARALYZE_HEAL\n\t.2byte ITEM_AWAKENING\n\t.2byte ITEM_ESCAPE_ROPE\n\tpokemartlistend\n")
        obj.append({"graphics_id":"OBJ_EVENT_GFX_MART_EMPLOYEE","x":1,"y":3,"elevation":3,"movement_type":"MOVEMENT_TYPE_FACE_RIGHT",
            "movement_range_x":0,"movement_range_y":0,"trainer_type":"TRAINER_TYPE_NONE","trainer_sight_or_berry_tree_id":"0",
            "script":f"{cart}_EventScript_Clerk","flag":"0"})
    return {"id":"MAP_"+snake(cart),"name":cart,"layout":d['layout'],"music":d['music'],"region":"REGION_HOENN","region_map_section":d['sec'],
        "requires_flash":False,"weather":"WEATHER_SUNNY" if d['tipo']=='terme' else "WEATHER_NONE","map_type":"MAP_TYPE_TOWN" if d['tipo']=='terme' else "MAP_TYPE_INDOOR","allow_cycling":False,"allow_escaping":False,
        "allow_running":False,"show_map_name":False,"battle_scene":"MAP_BATTLE_SCENE_NORMAL","connections":None,
        "object_events":obj,"warp_events":d['uscite'],"coord_events":[],"bg_events":[]}, "\n".join(sc)

# ================= scrittura file
def esc(t): return t.replace("\n","\\n")
groups=json.load(open("data/maps/map_groups.json",encoding='utf-8'))
layouts=json.load(open("data/layouts/layouts.json",encoding='utf-8'))
layouts["layouts"]=[l for l in layouts["layouts"] if l.get("id") not in {f"LAYOUT_{M[n][1]['id'][4:]}" for n in M}]
sections=json.load(open("src/data/region_map/region_map_sections.json",encoding='utf-8'))
inc=[]
for nome,(m,info) in M.items():
    m.save(nome)
    lid="LAYOUT_"+info['id'][4:]
    layouts["layouts"].append({"id":lid,"name":f"{nome}_Layout","width":m.w,"height":m.h,"primary_tileset":"gTileset_General",
        "secondary_tileset":"gTileset_Petalburg","border_filepath":f"data/layouts/{nome}/border.bin",
        "blockdata_filepath":f"data/layouts/{nome}/map.bin","layout_version":"emerald"})
    bg=[]; sc=[f"{nome}_MapScripts::\n\t.byte 0\n"]
    for i,(x,y,t) in enumerate(m.signs):
        lab=f"{nome}_EventScript_Sign{i}"
        bg.append({"type":"sign","x":x,"y":y,"elevation":0,"player_facing_dir":"BG_EVENT_PLAYER_FACING_ANY","script":lab})
        sc.append(f"{lab}::\n\tmsgbox {nome}_Text_Sign{i}, MSGBOX_SIGN\n\tend\n")
        sc.append(f"{nome}_Text_Sign{i}:\n\t.string \"{esc(t)}$\"\n")
    os.makedirs(f"data/maps/{nome}",exist_ok=True)
    mj={"id":info['id'],"name":nome,"layout":lid,"music":info['music'],"region":"REGION_HOENN","region_map_section":info['sec'],
        "requires_flash":False,"weather":"WEATHER_SUNNY","map_type":info['tipo'],"allow_cycling":True,"allow_escaping":False,
        "allow_running":True,"show_map_name":True,"battle_scene":"MAP_BATTLE_SCENE_NORMAL","connections":info.get('conn',[]),
        "object_events":[],"warp_events":m.warps,"coord_events":[],"bg_events":bg}
    open(f"data/maps/{nome}/map.json","w",encoding='utf-8').write(json.dumps(mj,indent=2,ensure_ascii=False)+"\n")
    open(f"data/maps/{nome}/scripts.inc","w",encoding='utf-8').write("\n".join(sc))
    inc.append(f'\t.include "data/maps/{nome}/scripts.inc"')
    for s in sections["map_sections"]:
        if s["id"]==info['sec']: s["name"]=info['nome']
if "gMapGroup_Felicia" not in groups["group_order"]: groups["group_order"].append("gMapGroup_Felicia")
for cart,d in INTERNI.items():
    mj,sc=interno_json(cart,d); os.makedirs(f"data/maps/{cart}",exist_ok=True)
    open(f"data/maps/{cart}/map.json","w",encoding='utf-8').write(json.dumps(mj,indent=2,ensure_ascii=False)+"\n")
    open(f"data/maps/{cart}/scripts.inc","w",encoding='utf-8').write(sc+"\n")
    inc.append(f'\t.include "data/maps/{cart}/scripts.inc"')
groups["gMapGroup_Felicia"]=list(M)+list(INTERNI)
hl=json.load(open("src/data/heal_locations.json",encoding='utf-8'))
ids={c["id"] for c in CURE}; hl["heal_locations"]=[h for h in hl["heal_locations"] if h["id"] not in ids]+CURE
open("src/data/heal_locations.json","w",encoding='utf-8').write(json.dumps(hl,indent=2,ensure_ascii=False)+"\n")
layouts["layouts"]=[l for l in layouts["layouts"] if l.get("id")!="LAYOUT_TERME"]+[{"id":"LAYOUT_TERME","name":"Terme_Layout","width":16,"height":14,
    "primary_tileset":"gTileset_General","secondary_tileset":"gTileset_Lavaridge","border_filepath":"data/layouts/Terme/border.bin",
    "blockdata_filepath":"data/layouts/Terme/map.bin","layout_version":"emerald"}]
for p,d in (("data/maps/map_groups.json",groups),("data/layouts/layouts.json",layouts),("src/data/region_map/region_map_sections.json",sections)):
    open(p,"w",encoding='utf-8').write(json.dumps(d,indent=2,ensure_ascii=False)+"\n")
# include degli script, fuori dal blocco FRLG
es=open("data/event_scripts.s").read().split("\n")
es=[l for l in es if not any(f"data/maps/{n}/scripts.inc" in l for n in list(M)+list(INTERNI))]
k=es.index(".if IS_FRLG")
while es[k-1].strip()=="": k-=1
es[k:k]=inc
open("data/event_scripts.s","w").write("\n".join(es))
print("start",Q.start, {n:(m.w,m.h) for n,(m,_) in M.items()})
