# Genera citta e percorsi di Felicia componendo "timbri" presi da mappe esistenti.
# Scrive layout (map.bin/border.bin), map.json, scripts.inc dei cartelli, gruppo mappe, layouts.json e nomi delle sezioni.
# uso (dalla root del repo): python3 tools/felicia/add_statua.py (una volta) ; python3 tools/felicia/build_maps.py
import struct,os,json,re

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
# case di Ceneride (import_metatiles.py ceneride + case_ceneride.py): id rimappati nel secondario petalburg
SOO=load("SootopolisCity",60,60); SOOMAP={int(k):v for k,v in json.load(open("tools/felicia/import_ceneride.json")).items()}
def soo(x,y,w,h,erba=()):
    st=[[(v&0xfc00)|SOOMAP.get(v&0x3ff,v&0x3ff) for v in r[x:x+w]] for r in SOO[y:y+h]]
    for i,j in erba: st[j][i]=ERBA
    return st
TEMPIO_ID=0x301                                   # da add_tempio.py: tempio piatto 10x6, palette 07
TEMPIO = [[0x3400|(TEMPIO_ID+j*10+i) for i in range(10)] for j in range(6)]
CUBO   = soo(8,23,3,4)                   # casa cubica bianca con porta (import_extra.py)
GUGLIA = soo(8,2,3,5,erba=((0,0),(2,0))) # casa con tetto a guglia
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
        s.ts="gTileset_Petalburg"; s.border=None; s.objs=[]; s.coords=[]; s.script=[]; s.mapscripts=None; s.warps_extra=[]
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
        if getattr(s,'murata',False) and lato in 'EW' and pos-1>=2:   # testata del muro sopra il varco: paramento
            s.fill(PARAMENTO,0 if lato=='W' else s.w-2,pos-1,2,1,3)
        s.gates[lato]=pos
        if nome:
            cx,cy={'E':(s.w-3,pos-1),'W':(2,pos-1),'N':(pos-1,2),'S':(pos-1,s.h-3)}[lato]
            s.cartello(cx,cy,nome)
    def case(s,x0,y0,x1,y1):
        # riempie l'area di case allineate lungo le strade, lasciando libera la riga davanti alla porta
        for st in (CUBO,GUGLIA):
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
    def npc(s,x,y,gfx,testo,mov="MOVEMENT_TYPE_LOOK_AROUND",script=None,local_id=None,flag="0"):
        # personaggio che parla: testo con \n tra le righe e \\p tra i box; con script= usa un'etichetta MAPPA_EventScript_...
        o=dict(graphics_id="OBJ_EVENT_GFX_"+gfx,x=x,y=y,elevation=3 if s.ts=="gTileset_Lavaridge" else 0,movement_type=mov,
            movement_range_x=1,movement_range_y=1,trainer_type="TRAINER_TYPE_NONE",trainer_sight_or_berry_tree_id="0",script=script,flag=flag)
        if local_id: o={"local_id":local_id,**o}
        if script is None: o["_testo"]=testo
        s.objs.append(o)
    def evento(s,celle,var,valore,nome,script):
        # trigger a terra: parte quando il giocatore passa su una delle celle e var == valore.
        # nel testo dello script, MAPPA_ viene sostituito con il nome della mappa
        for x,y in celle: s.coords.append(dict(type="trigger",x=x,y=y,elevation=0,var=var,var_value=str(valore),script="MAPPA_EventScript_"+nome))
        s.script.append(f"MAPPA_EventScript_{nome}::\n"+script)
    def save(s,name):
        for y in (range(s.h-1,0,-1) if s.ts=="gTileset_Petalburg" else ()):     # sommita con altra sommita sopra -> variante continua
            for x in range(s.w):
                if s.g[y][x]&0x3ff==MURA_ID and s.g[y-1][x]&0x3ff in (MURA_ID,0x298): s.g[y][x]=(s.g[y][x]&~0x3ff)|0x298
        os.makedirs(f"data/layouts/{name}",exist_ok=True)
        open(f"data/layouts/{name}/map.bin",'wb').write(struct.pack(f"<{s.w*s.h}H",*[v for r in s.g for v in r]))
        open(f"data/layouts/{name}/border.bin",'wb').write(s.border or struct.pack("<4H",*[v for r in ALBERO for v in r]))

M={}   # nome -> (Mappa, info)
def mappa(cartella,w,h,**info): m=Mappa(w,h); M[cartella]=(m,info); return m
ENC={}   # cartella -> mappa di Smeraldo da cui copiare gli incontri selvatici
def da_smeraldo(cartella,src,w,h,ts,enc=None,**info):
    # mappa di Smeraldo copiata cosi com'e' (con il suo tileset), da ritoccare poi con put/fill
    m=Mappa(w,h); m.g=load(src,w,h); m.occ=[[1]*w for _ in range(h)]; m.ts=ts
    m.border=open(f"data/layouts/{src}/border.bin","rb").read(); M[cartella]=(m,info)
    if enc: ENC[cartella]=enc
    return m

# ================= VITELIA (Pompei, specchiata come la regione) =================
# Assi reali: Via dell'Abbondanza (Foro -> Porta del Guado), Via Stabiana (Porta del Monte -> Porta delle Vigne),
# Via di Nola a nord, Via di Mercurio a nord del Foro, Via Consolare verso Porta del Sale.
# Specchiata: Foro e Porta Marina a est, Anfiteatro e Grande Palestra a sud-ovest, teatri a sud.
Q=mappa("Vitelia",64,48,id="MAP_VITELIA",sec="MAPSEC_LITTLEROOT_TOWN",nome="VITELIA",music="MUS_PETALBURG",tipo="MAP_TYPE_CITY")
Q.mura()
Q.strada(2,10,60,2)                         # Via di Nola
Q.strada(54,6,8,2); Q.strada(54,6,2,6)      # Via Consolare -> Porta del Sale
Q.strada(0,27,44,2)                         # Via dell'Abbondanza
Q.strada(29,2,2,46)                         # Via Stabiana
Q.strada(47,2,2,14)                         # Via di Mercurio
Q.strada(14,2,2,26); Q.strada(38,11,2,17)   # vicoli nord-sud
Q.strada(2,19,42,2)                         # decumano minore
Q.strada(44,15,14,19)                       # Foro
Q.strada(56,22,8,2)                         # Porta Marina
Q.porta('E',6,"PORTA DEL SALE\n{RIGHT_ARROW} VIA SALSEDIA"); Q.porta('E',22,"PORTA MARINA\n{RIGHT_ARROW} VIA SALSEDIA")
Q.porta('W',27,"PORTA DEL GUADO\n{LEFT_ARROW} VIA DEL GUADO"); Q.porta('S',29,"PORTA DELLE VIGNE\n{DOWN_ARROW} VIA DELLE VIGNE")
Q.porta('N',29,"PORTA DEL MONTE\n{UP_ARROW} MONTE FUMARIO")
Q.statua_palkia(50,22); Q.cartello(49,25,"FORO DI VITELIA\nPalkia veglia sul Foro.")
Q.edificio(TEMPIO,46,15,"TEMPIO DI GIOVE")            # testata nord del Foro, come a Pompei
Q.edificio(MARKET,53,28)
Q.edificio(CENTRO,31,22); Q.cartello(35,25,"TERMOPOLIO POKEMON")
Q.edificio(CASA_A,23,22,"TERME CENTRALI"); Q.terme(23,22,"TermeCentrali")
Q.put(CASA_A,32,13); Q.put(CASA_A,37,13); Q.fill(FIORI,32,17,10,1); Q.cartello(31,17,"CASA DI FAUSTO"); Q.casa_interna(32,13,"CasaDiFausto")
Q.anello(3,29,13,14,(8,29,3,2)); Q.cartello(7,31,"ARENA MAGNA\nChiusa dalla Rissa dell'Arena.")
Q.alberi(17,31,12,2); Q.edificio(PALESTRA,19,33); Q.strada(17,38,12,6); Q.cartello(18,37,"GRANDE PALESTRA\nCapopalestra: Celado")
Q.anello(32,33,12,11,(36,33,3,2)); Q.cartello(35,32,"TEATRO GRANDE")
Q.put(CUBO,3,22); Q.put(CUBO,9,22); Q.put(CUBO,17,22)   # case sul lato sud del decumano, allineate alle Terme
Q.case(2,2,62,46)
Q.start=(30,28)

# ================= VIA SALSEDIA: Porta del Sale e Porta Marina -> Salsedia, sotto le pendici del Fumario
R1=mappa("ViaSalsedia",40,48,id="MAP_VIA_SALSEDIA",sec="MAPSEC_ROUTE_101",nome="VIA SALSEDIA",music="MUS_ROUTE101",tipo="MAP_TYPE_ROUTE")
R1.porta('W',22); R1.porta('W',38); R1.porta('E',6)     # sale verso nord-est: Salsedia sta piu in alto di Vitelia
R1.strada(0,22,20,2); R1.strada(0,38,20,2); R1.strada(18,6,2,34); R1.strada(18,6,22,2)
R1.cartello(4,21,"VIA DEI SEPOLCRI\\pLe tombe delle famiglie\ndi Vitelia."); R1.cartello(36,5,"VIA SALSEDIA\n{RIGHT_ARROW} SALSEDIA")
R1.erba_alta(22,10,14,8); R1.erba_alta(4,26,10,8); R1.erba_alta(24,26,12,8)
R1.alberi(2,2,14,14); R1.alberi(22,38,14,8); R1.alberi(2,42,14,6)

# ================= SALSEDIA (Ercolano): griglia regolare di cardini e decumani, citta sul mare
E=mappa("Salsedia",40,36,id="MAP_SALSEDIA",sec="MAPSEC_OLDALE_TOWN",nome="SALSEDIA",music="MUS_OLDALE",tipo="MAP_TYPE_TOWN")
E.mura()
E.porta('W',10,"SALSEDIA\nLa citta del sale sul mare."); E.porta('E',10,"{RIGHT_ARROW} VIA COSTIERA")
E.strada(0,10,40,2)                         # Decumano Massimo
E.strada(2,18,36,2)                         # Decumano Inferiore
for x in (10,20,30): E.strada(x,2,2,23)     # Cardini III, IV, V
E.strada(2,24,36,2)                         # passeggiata sul mare
E.acqua(2,26,36,10,"t")      # il mare arriva al bordo: si prosegue col Surf
E.edificio(CENTRO,13,13); E.cartello(17,16,"TERMOPOLIO POKEMON")
E.edificio(PALESTRA,23,19); E.cartello(22,23,"PALESTRA DI SALSEDIA\nCapopalestra: Rettina")
E.edificio(CASA_A,13,3,"TERME"); E.terme(13,3,"Terme"); E.edificio(MARKET,33,13)
E.case(2,2,38,24)

# ================= VIA COSTIERA: costa tra Salsedia e Agorapoli
R4=mappa("ViaCostiera",48,30,id="MAP_VIA_COSTIERA",sec="MAPSEC_ROUTE_104",nome="VIA COSTIERA",music="MUS_ROUTE104",tipo="MAP_TYPE_ROUTE")
R4.porta('W',18); R4.porta('E',4)                        # risale la costa verso Agorapoli
R4.strada(0,18,16,2); R4.strada(14,4,2,16); R4.strada(14,4,34,2)
R4.fill(STRADA,18,10,28,2); R4.acqua(18,12,30,18,"tl")
R4.erba_alta(2,2,10,12); R4.erba_alta(18,7,12,3); R4.alberi(30,0,16,4)
R4.cartello(2,17,"VIA COSTIERA\n{RIGHT_ARROW} AGORAPOLI")

# ================= AGORAPOLI (Napoli): impianto greco a plateiai e stenopoi, agora, porto
N=mappa("Agorapoli",64,48,id="MAP_AGORAPOLI",sec="MAPSEC_SLATEPORT_CITY",nome="AGORAPOLI",music="MUS_SLATEPORT",tipo="MAP_TYPE_CITY")
N.mura()
N.porta('W',22,"AGORAPOLI\nLa citta delle piazze greche."); N.porta('E',22,"{RIGHT_ARROW} GALLERIA DEL TUFO")
for y in (10,22,34): N.strada(0 if y==22 else 2,y,64 if y==22 else 60,2)   # tre plateiai
for x in range(8,58,8): N.strada(x,2,2,36)                                    # stenopoi
N.strada(26,24,14,10)                                                         # agora
N.statua(32,28); N.cartello(31,30,"AGORA DI AGORAPOLI\nQui si discute in greco.")
N.edificio(CENTRO,18,12); N.edificio(MARKET,42,12)
N.edificio(PALESTRA,42,27); N.cartello(41,31,"PALESTRA DI AGORAPOLI\nCapopalestra: il Filosofo")
N.anello(10,24,14,10,(15,24,3,2)); N.cartello(14,23,"TEATRO\nVi canto' anche un imperatore.")
N.fill(STRADA,2,38,60,2); N.acqua(2,40,60,8,"t")
N.case(2,2,62,38)
N.cartello(22,15,"TERMOPOLIO POKEMON")

# ================= GALLERIA DEL TUFO: la galleria scavata nella collina verso Granaria
R5=mappa("GalleriaDelTufo",48,20,id="MAP_GALLERIA_DEL_TUFO",sec="MAPSEC_ROUTE_105",nome="GALLERIA DEL TUFO",music="MUS_ROUTE110",tipo="MAP_TYPE_ROUTE")
R5.porta('W',4); R5.porta('E',14)                        # scende dalla collina verso Granaria
R5.strada(0,4,24,2); R5.strada(22,4,2,12); R5.strada(22,14,26,2)
R5.alberi(0,8,20,12); R5.alberi(26,0,22,12); R5.erba_alta(24,6,2,6)
R5.cartello(2,3,"GALLERIA DEL TUFO\nGalleria lunga settecento passi.")

# ================= GRANARIA (Pozzuoli): porto del grano, macellum, anfiteatro flavio
P=mappa("Granaria",56,44,id="MAP_GRANARIA",sec="MAPSEC_PETALBURG_CITY",nome="GRANARIA",music="MUS_LILYCOVE",tipo="MAP_TYPE_CITY")
P.mura()
P.porta('W',14,"GRANARIA\nIl porto del grano di Felicia."); P.strada(24,38,2,6); P.porta('S',24,"{DOWN_ARROW} CAMPI ARDENTI\nZolfaia e Tre Laghi")
P.strada(0,14,56,2); P.strada(2,26,38,2); P.strada(24,2,2,38); P.strada(38,16,2,12)
P.anello(4,2,16,12,(10,12,3,2)); P.cartello(9,15,"ANFITEATRO DEL PORTO")
P.strada(26,17,12,8); P.statua(31,20); P.cartello(30,22,"MACELLUM\nIl mercato del porto.")
P.edificio(MARKET,27,17)
P.edificio(CENTRO,16,17); P.cartello(20,20,"TERMOPOLIO POKEMON")
P.edificio(PALESTRA,28,30); P.strada(26,35,12,4); P.cartello(27,34,"PALESTRA DI GRANARIA\nCapopalestra: il Mercante")
P.acqua(40,28,14,14,"tl"); P.strada(38,28,2,14); P.strada(26,39,12,2)
P.case(2,2,54,42)

# Via Cumana e' sostituita dai Campi Ardenti (Percorso 114), piu' sotto con le altre mappe di Smeraldo
RIMOSSE=["ViaCumana"]

# ================= ORACOLIA (Cuma): acropoli sul colle, antro della Sibila, citta bassa, mare a est
C=mappa("Oracolia",44,40,id="MAP_ORACOLIA",sec="MAPSEC_FALLARBOR_TOWN",nome="ORACOLIA",music="MUS_FORTREE",tipo="MAP_TYPE_TOWN")
C.mura()
C.strada(10,0,2,14); C.porta('N',10,"ORACOLIA\nLa citta piu antica di Felicia."); C.porta('S',30,"{DOWN_ARROW} VIA DELLA FLOTTA")
C.anello(20,2,16,16,(26,16,3,2),pietra=False); C.edificio(PALESTRA,25,4); C.strada(22,9,12,7)
C.cartello(24,8,"ANTRO DELLA SIBILA\nCapopalestra: la Sibila"); C.edificio(CASA_A,22,10,"TEMPIO DI APOLLO")
C.strada(2,12,18,2); C.strada(18,18,2,20); C.strada(18,18,20,2); C.strada(30,18,2,22)
C.strada(4,24,12,8); C.statua(9,27); C.cartello(8,29,"FORO DI ORACOLIA")
C.edificio(CENTRO,22,22); C.cartello(26,25,"TERMOPOLIO POKEMON")
C.acqua(36,20,6,18,"l")
C.case(2,2,36,38)

# ================= VIA DELLA FLOTTA: costa di Baia, terme sul mare
R7=mappa("ViaDellaFlotta",32,40,id="MAP_VIA_DELLA_FLOTTA",sec="MAPSEC_ROUTE_107",nome="VIA DELLA FLOTTA",music="MUS_ROUTE119",tipo="MAP_TYPE_ROUTE")
R7.porta('N',12); R7.porta('S',12)
R7.strada(12,0,2,14); R7.strada(6,12,8,2); R7.strada(6,12,2,14); R7.strada(6,24,8,2); R7.strada(12,24,2,16)
R7.acqua(22,2,8,36,"l"); R7.edificio(CASA_A,15,16,"TERME DEL GOLFO\nI Domini vengono qui d'inverno."); R7.terme(15,16,"TermeDelGolfo")
R7.erba_alta(2,2,8,8); R7.erba_alta(14,28,6,8); R7.alberi(2,28,4,10)

# ================= CLASSIA (Miseno): porto della flotta, capo, villa di Pinio
Mi=mappa("Classia",48,40,id="MAP_CLASSIA",sec="MAPSEC_RUSTBORO_CITY",nome="CLASSIA",music="MUS_RUSTBORO",tipo="MAP_TYPE_CITY")
Mi.mura()
Mi.porta('N',20,"CLASSIA\nPorto della flotta di Amoria.")
Mi.strada(20,2,2,24); Mi.strada(2,10,44,2); Mi.strada(4,24,40,2)
Mi.acqua(4,26,40,14,"t")
Mi.put(CASA_A,4,3); Mi.put(CASA_A,9,3); Mi.fill(FIORI,4,7,10,2); Mi.cartello(3,8,"VILLA DEL PROF. PINIO"); Mi.casa_interna(4,3,"VillaDiPinio")
Mi.edificio(PALESTRA,36,3); Mi.strada(34,8,10,2); Mi.cartello(35,7,"PALESTRA DI CLASSIA\nCapopalestra: il Navarca")
Mi.edificio(CENTRO,23,13); Mi.cartello(27,16,"TERMOPOLIO POKEMON"); Mi.edificio(MARKET,28,13)
Mi.cartello(44,23,"GROTTA DEL DRAGO")
Mi.case(2,2,46,24)

# ================= VIA DELLE VIGNE: vigne tra Vitelia e Ortensia
R2=mappa("ViaDelleVigne",32,40,id="MAP_VIA_DELLE_VIGNE",sec="MAPSEC_ROUTE_102",nome="VIA DELLE VIGNE",music="MUS_ROUTE110",tipo="MAP_TYPE_ROUTE")
R2.porta('N',14); R2.porta('S',16)
R2.strada(14,0,2,16); R2.strada(14,14,4,2); R2.strada(16,14,2,26)
for y in range(4,30,3): R2.erba_alta(3,y,9,1); R2.erba_alta(20,y,9,1)   # filari di vigne
R2.cartello(12,3,"VIA DELLE VIGNE\nVigne del Fumario.")
R2.evento([(16,20),(17,20)],"VAR_CENERE_SCOSSA",0,"PrimaScossa",
"""\tgoto_if_unset FLAG_BADGE02_GET, MAPPA_EventScript_PrimaScossaFine
\tlockall
\tsetvar VAR_0x8004, 2
\tsetvar VAR_0x8005, 2
\tsetvar VAR_0x8006, 12
\tsetvar VAR_0x8007, 4
\tspecial ShakeCamera
\twaitstate
\tmsgbox MAPPA_Text_Scossa1, MSGBOX_DEFAULT
\tmsgbox MAPPA_Text_Scossa2, MSGBOX_DEFAULT
\tsetvar VAR_CENERE_SCOSSA, 1
\treleaseall
MAPPA_EventScript_PrimaScossaFine:
\tend

MAPPA_Text_Scossa1:
\t.string "La terra trema, piu' forte\\ndel solito.\\p"
\t.string "LUCIO: Ancora una scossa...\\p"
\t.string "A Vitelia non ci fa piu'\\n"
\t.string "caso nessuno.$"

MAPPA_Text_Scossa2:
\t.string "La NATURADEX registra un gruppo\\n"
\t.string "di POKEMON che scende dal monte.\\p"
\t.string "Vanno tutti verso valle.$"
""")

# ================= ORTENSIA (Stabia): ville sulla collina a picco sul mare
S=mappa("Ortensia",44,36,id="MAP_ORTENSIA",sec="MAPSEC_DEWFORD_TOWN",nome="ORTENSIA",music="MUS_DEWFORD",tipo="MAP_TYPE_TOWN")
S.mura()
S.porta('N',20,"ORTENSIA\nLe ville dei Domini sul mare.")
S.strada(20,2,2,30); S.strada(2,14,34,2); S.strada(2,28,34,2)
S.acqua(36,2,8,32,"l")
for x,y,n in ((4,3,"VILLA SAN MARCO"),(24,3,"VILLA ARIANNA")):
    S.put(CASA_A,x,y); S.put(CASA_A,x+5,y); S.fill(FIORI,x,y+4,10,2); S.cartello(x+10,y+5,n)
S.edificio(PALESTRA,6,19); S.erba_alta(4,24,12,3); S.cartello(5,23,"PALESTRA DI ORTENSIA\nCapopalestra: la Vignaiola")
S.edificio(CENTRO,24,17); S.cartello(28,20,"TERMOPOLIO POKEMON")
S.case(2,2,36,34)

# ================= VIA DEL GUADO: verso Rivalia, guado del fiume Sarno
R3=mappa("ViaDelGuado",48,30,id="MAP_VIA_DEL_GUADO",sec="MAPSEC_ROUTE_103",nome="VIA DEL GUADO",music="MUS_ROUTE120",tipo="MAP_TYPE_ROUTE")
R3.porta('E',14); R3.porta('W',14)
R3.strada(0,14,48,2)
R3.acqua(22,2,4,12,"lr"); R3.acqua(22,16,4,12,"lr"); R3.cartello(20,13,"GUADO DEL FIUME")
R3.erba_alta(4,4,14,8); R3.erba_alta(30,18,12,8); R3.alberi(30,2,14,8); R3.alberi(4,20,12,6)
R3.cartello(44,13,"VIA DEL GUADO\n{LEFT_ARROW} RIVALIA")

# ================= RIVALIA (Nocera): citta murata dell'entroterra, anfiteatro dei tifosi
Nu=mappa("Rivalia",44,40,id="MAP_RIVALIA",sec="MAPSEC_LAVARIDGE_TOWN",nome="RIVALIA",music="MUS_FALLARBOR",tipo="MAP_TYPE_TOWN")
Nu.mura()
Nu.porta('E',20,"RIVALIA\\pQui nessuno ha dimenticato\nla Rissa.")
Nu.strada(2,20,42,2); Nu.strada(20,2,2,36); Nu.strada(2,10,40,2); Nu.strada(2,30,40,2)
Nu.anello(4,22,14,14,(9,22,3,2)); Nu.cartello(8,21,"ANFITEATRO DI RIVALIA")
Nu.edificio(PALESTRA,26,23); Nu.strada(24,28,10,2); Nu.cartello(25,27,"PALESTRA DI RIVALIA\nCapo dei tifosi rivaliani")
Nu.edificio(CENTRO,24,13); Nu.cartello(28,16,"TERMOPOLIO POKEMON"); Nu.edificio(MARKET,30,13)
Nu.statua(10,14); Nu.cartello(9,16,"FORO DI RIVALIA")
Nu.case(2,2,42,38)


# ================= MONTE FUMARIO: pendici con le vigne, salita, cratere (Percorso 112, Passo Selvaggio, Monte Camino)
def togli(m,ids,terra):
    # toglie la funivia di Smeraldo: ogni metatile in ids diventa terra, con collisione/quota del vicino a sinistra
    for y in range(m.h):
        for x in range(m.w):
            if m.g[y][x]&0x3ff in ids:
                vic=next((m.g[y][xx] for xx in range(x-1,-1,-1) if m.g[y][xx]&0x3ff not in ids),m.g[y][x])
                m.g[y][x]=(vic&0xfc00)|(terra(m.g[y][x]&0x3ff) if callable(terra) else terra)
def warp(m,x,y,dest,wid,el=3): m.warps_extra.append({"x":x,"y":y,"elevation":el,"dest_map":dest,"dest_warp_id":str(wid)})

V1=da_smeraldo("PendiciFumario","Route112",40,60,"gTileset_Lavaridge",enc="MAP_ROUTE112",id="MAP_PENDICI_FUMARIO",sec="MAPSEC_ROUTE_112",
               nome="PENDICI FUMARIO",music="MUS_ROUTE110",tipo="MAP_TYPE_ROUTE")
for y in range(60):                                # cavo sopra il pendio: lo sostituisco col terreno a sinistra
    for x in range(40):
        if V1.g[y][x]&0x3ff in (0x250,0x251,0x259):
            V1.g[y][x]=next(V1.g[y][xx] for xx in range(x-1,-1,-1) if V1.g[y][xx]&0x3ff not in (0x250,0x251,0x259))
togli(V1,{0x252,0x253,0x254,0x255,0x25a,0x25b,0x25c,0x25d,0x264,0x265},0x208)
via=V1.g[46][20]
for y in range(52,60): V1.g[y][20]=via; V1.g[y][21]=via        # sentiero verso Porta del Monte
V1.gates['S']=20
warp(V1,6,46,"MAP_SALITA_FUMARIO",0); warp(V1,7,46,"MAP_SALITA_FUMARIO",1)
V1.signs.append((19,44,"{UP_ARROW} MONTE FUMARIO\n{DOWN_ARROW} VITELIA, PORTA DEL MONTE"))
V1.signs.append((22,37,"VILLA RUSTICA\\pVino del Fumario\nper tutta Felicia."))
V1.signs.append((4,49,"VIGNE DEL FUMARIO\nVietato cogliere l'uva.\\pIl Domino."))
V1.npc(24,34,"MAN_4","Le viti del Fumario danno il vino\npiu' buono di Felicia.\\pIl monte e' generoso.\nChissa' perche'.")
V1.npc(15,40,"HIKER","Da qualche settimana i Pokemon\nscendono dal monte verso valle.\\pNon era mai successo.")
V1.npc(29,49,"MAN_3","Lavoro qui da quando ero\nVincolato.\\pOra sono Affrancato,\nma l'uva e' la stessa.",mov="MOVEMENT_TYPE_WANDER_AROUND")

V2=da_smeraldo("SalitaFumario","JaggedPass",30,46,"gTileset_Lavaridge",enc="MAP_JAGGED_PASS",id="MAP_SALITA_FUMARIO",sec="MAPSEC_JAGGED_PASS",
               nome="SALITA FUMARIO",music="MUS_PETALBURG_WOODS",tipo="MAP_TYPE_ROUTE")
warp(V2,14,40,"MAP_PENDICI_FUMARIO",0); warp(V2,15,40,"MAP_PENDICI_FUMARIO",1)
warp(V2,13,5,"MAP_CRATERE_FUMARIO",0); warp(V2,14,5,"MAP_CRATERE_FUMARIO",1)
V2.npc(10,8,"HIKER","Lo chiamano il monte di Spartaro.\\pCento anni fa i Vincolati ribelli\nsi nascosero quassu'.\\pDicono che il monte\nli protegga ancora.")
V2.npc(16,35,"OLD_MAN","La cenere qui e' vecchia\ndi secoli.\\pO almeno, cosi' dicono.")

V3=da_smeraldo("CratereFumario","MtChimney",40,47,"gTileset_Lavaridge",id="MAP_CRATERE_FUMARIO",sec="MAPSEC_MT_CHIMNEY",
               nome="MONTE FUMARIO",music="MUS_MT_CHIMNEY",tipo="MAP_TYPE_ROUTE")
togli(V3,{0x250,0x251,0x252,0x253,0x254,0x259,0x25a,0x25b,0x25c,0x264},0x271)
for x,y in ((14,5),(14,6)): V3.g[y][x]=(V3.g[y][x-1]&0xfc00)|0x271
warp(V3,20,41,"MAP_SALITA_FUMARIO",2); warp(V3,21,41,"MAP_SALITA_FUMARIO",3)
V3.signs.append((24,37,"CRATERE DEL FUMARIO\nIl punto piu' alto di Felicia."))
V3.npc(19,39,"OLD_WOMAN","Mio nonno diceva che il Fumario\ne' un monte addormentato.\\pPero' la terra qui e' calda.\nI monti addormentati scaldano?")
V3.npc(24,19,"SCIENTIST_1","Il Prof. Pinio mi ha chiesto\ndi raccogliere queste rocce.\\pSembrano bruciate. Curioso, no?")

# ================= CAMPI ARDENTI (Percorso 114): tra Granaria e Oracolia, i Tre Laghi e la Zolfaia
CF=da_smeraldo("CampiArdenti","Route114",40,80,"gTileset_Fallarbor",enc="MAP_ROUTE114",id="MAP_CAMPI_ARDENTI",sec="MAPSEC_ROUTE_114",
               nome="CAMPI ARDENTI",music="MUS_ROUTE110",tipo="MAP_TYPE_ROUTE")
terra=CF.g[9][31]
for y in range(0,5):                               # varco nella scarpata verso Granaria, a nord
    for x in (37,38): CF.g[y][x]=terra
CF.gates['N']=37
fondo=CF.g[73][25]
for y in range(74,80):                             # sentiero tra le rocce verso Oracolia, a sud
    for x in (25,26): CF.g[y][x]=fondo
CF.gates['S']=25
warp(CF,8,63,"MAP_ZOLFAIA",0,el=0)
CF.casa_interna(27,2,"CasaDelFumarolaro"); CF.casa_interna(25,33,"CasaDelCustode")
CF.signs.append((31,7,"CAMPI ARDENTI\n{UP_ARROW} GRANARIA  {DOWN_ARROW} ORACOLIA"))
CF.signs.append((25,38,"CASA DEL CUSTODE DEI LAGHI"))
CF.signs.append((24,14,"LAGO PERLATO\nLe ostriche di Felicia."))          # cartelli invisibili sulla riva
CF.signs.append((18,21,"LAGO OMBROSO\nGli uccelli non lo sorvolano.\\pDicono che sia la porta\ndegli Inferi."))
CF.signs.append((17,13,"LAGO NEBBIOSO\nAcqua ferma, nebbia al mattino."))
CF.signs.append((7,64,"ZOLFAIA\nLa terra fuma e ribolle.\\pNon andate senza Pokemon."))
CF.npc(30,11,"FISHERMAN","Tre laghi, tre spiriti.\\pChi li ha visti dice che\nnon si fanno toccare.")
CF.npc(21,40,"WOMAN_2","Mio marito lavora alle fumarole.\\pTorna giallo di zolfo\nogni sera.",mov="MOVEMENT_TYPE_WANDER_AROUND")
CF.npc(14,58,"HIKER","La Zolfaia borbotta da\nqualche settimana.\\pCome il Fumario. Strano, no?")

SO=da_smeraldo("Zolfaia","FieryPath",35,38,"gTileset_Lavaridge",enc="MAP_FIERY_PATH",id="MAP_ZOLFAIA",sec="MAPSEC_FIERY_PATH",
               nome="ZOLFAIA",music="MUS_PETALBURG_WOODS",tipo="MAP_TYPE_UNDERGROUND",meteo="WEATHER_NONE")
warp(SO,26,36,"MAP_CAMPI_ARDENTI",0); warp(SO,26,4,"MAP_CAMPI_ARDENTI",0)

# ---- raccordo tra Pendici del Fumario e Vitelia: le due montagne finiscono, poi campi, vigne e sepolcri fuori Porta del Monte
RV=mappa("FuoriPortaDelMonte",40,18,id="MAP_FUORI_PORTA_DEL_MONTE",sec="MAPSEC_ROUTE_112",nome="PENDICI FUMARIO",music="MUS_ROUTE110",tipo="MAP_TYPE_ROUTE")
RV.ts="gTileset_Lavaridge"
PASSA,BLOCCA=0x3000,0x0400
RV.g=[[ERBA]*40 for _ in range(18)]; RV.occ=[[0]*40 for _ in range(18)]
def blocco(x0,x1,y0,y1,sx,fx,dx,bsx,bfx,bdx,lato_sx=True,lato_dx=True):
    # massiccio roccioso: righe y0..y1-1 piene, riga y1 = piede; lato_sx/lato_dx False se esce dalla mappa
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            piede=y==y1
            if x==x0 and lato_sx: v=bsx if piede else sx
            elif x==x1 and lato_dx: v=bdx if piede else dx
            else: v=bfx if piede else fx
            RV.g[y][x]=v|BLOCCA; RV.occ[y][x]=3
blocco(0,16,0,3,0x270,0x271,0x272,0x278,0x279,0x27a,lato_sx=False)           # monte rosso a sinistra
blocco(0,9,4,5,0x270,0x271,0x272,0x278,0x279,0x27a,lato_sx=False)            # scende piu' in basso verso ovest
blocco(23,39,0,5,0x070,0x071,0x072,0x078,0x079,0x07a,lato_dx=False)          # rocce grigie a destra
blocco(31,39,6,7,0x070,0x071,0x072,0x078,0x079,0x07a,lato_dx=False)
for y in range(0,5):                                     # boschetto tra il monte e la strada, che si dirada
    for x in (17,18,19,22):
        if y<3 or x in (18,22): RV.g[y][x]=0x0c6|0x0400
RV.strada(20,0,2,18)
RV.alberi(12,6,2,2); RV.alberi(26,8,2,2); RV.alberi(4,12,2,2); RV.alberi(34,12,2,2)
RV.erba_alta(2,8,8,2); RV.erba_alta(24,10,6,2); RV.erba_alta(30,14,8,2)    # filari di vite
RV.fill(FIORI,14,10,4,1); RV.fill(FIORI,23,15,5,1)
RV.strada(8,14,12,2)                                     # viottolo verso la necropoli
RV.gates['N']=20; RV.gates['S']=20
RV.cartello(19,15,"NECROPOLI DI PORTA DEL MONTE\\pI Domini riposano fuori\ndalle mura, lungo la strada.")
RV.npc(10,13,"OLD_WOMAN","Porto fiori alla tomba di\nmio marito ogni mese.\\pDa qui il Fumario sembra\ncosi' tranquillo.")

# ================= collegamenti (offset calcolati dalle porte)
def colleg(a,lato,b):
    ma,_=M[a]; mb,_=M[b]
    opp={'E':'W','W':'E','N':'S','S':'N'}[lato]
    off=ma.gates[lato]-mb.gates[opp]
    dir={'E':'right','W':'left','N':'up','S':'down'}
    M[a][1].setdefault('conn',[]).append({"map":M[b][1]['id'],"offset":off,"direction":dir[lato]})
    M[b][1].setdefault('conn',[]).append({"map":M[a][1]['id'],"offset":-off,"direction":dir[opp]})
exec(open("tools/felicia/monte_antro.py",encoding="utf-8").read())    # Monte Antro: grotte e valico a sud di Ortensia
exec(open("tools/felicia/raccordi_mare.py",encoding="utf-8").read())   # raccordi citta-percorso, posizioni nel mondo, mare del golfo

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
    m.warps=list(m.warps_extra)
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
    elif cart not in STORIA_INT or not STORIA_INT[cart].get('mapscripts'):
        sc.append(f"{cart}_MapScripts::\n\t.byte 0\n")
    bg=[]
    if cart in STORIA_INT:                       # eventi della storia principale negli interni
        st=STORIA_INT[cart]
        if st.get('mapscripts'): sc.insert(0,st['mapscripts'])
        obj+=st.get('objs',[]); sc+=st.get('script',[]); bg+=st.get('bg',[])
    if d['tipo']=='mart':
        sc.append(f"{cart}_EventScript_Clerk::\n\tlock\n\tfaceplayer\n\tmessage gText_HowMayIServeYou\n\twaitmessage\n\tpokemart {cart}_Pokemart\n\tmsgbox gText_PleaseComeAgain, MSGBOX_DEFAULT\n\trelease\n\tend\n")
        sc.append(f"\t.align 2\n{cart}_Pokemart:\n\t.2byte ITEM_POKE_BALL\n\t.2byte ITEM_POTION\n\t.2byte ITEM_ANTIDOTE\n\t.2byte ITEM_PARALYZE_HEAL\n\t.2byte ITEM_AWAKENING\n\t.2byte ITEM_ESCAPE_ROPE\n\tpokemartlistend\n")
        obj.append({"graphics_id":"OBJ_EVENT_GFX_MART_EMPLOYEE","x":1,"y":3,"elevation":3,"movement_type":"MOVEMENT_TYPE_FACE_RIGHT",
            "movement_range_x":0,"movement_range_y":0,"trainer_type":"TRAINER_TYPE_NONE","trainer_sight_or_berry_tree_id":"0",
            "script":f"{cart}_EventScript_Clerk","flag":"0"})
    return {"id":"MAP_"+snake(cart),"name":cart,"layout":d['layout'],"music":d['music'],"region":"REGION_HOENN","region_map_section":d['sec'],
        "requires_flash":False,"weather":"WEATHER_SUNNY" if d['tipo']=='terme' else "WEATHER_NONE","map_type":"MAP_TYPE_TOWN" if d['tipo']=='terme' else "MAP_TYPE_INDOOR","allow_cycling":False,"allow_escaping":False,
        "allow_running":False,"show_map_name":False,"battle_scene":"MAP_BATTLE_SCENE_NORMAL","connections":None,
        "object_events":obj,"warp_events":d['uscite'],"coord_events":[],"bg_events":bg}, "\n".join(sc)

# ================= storia principale (prologo e Atto I a Vitelia)
STORIA_INT={}
exec(open("tools/felicia/storia_atto1.py",encoding='utf-8').read())
exec(open("tools/felicia/storia_zone.py",encoding='utf-8').read())   # eventi e personaggi delle zone nuove

# ================= scrittura file
def esc(t): return t.replace("\n","\\n")
groups=json.load(open("data/maps/map_groups.json",encoding='utf-8'))
RIMOSSE+=[n for n in groups.get("gMapGroup_Felicia",[]) if n not in M and n not in INTERNI and n not in RIMOSSE]   # mappe rinominate o tolte
layouts=json.load(open("data/layouts/layouts.json",encoding='utf-8'))
layouts["layouts"]=[l for l in layouts["layouts"] if l.get("id") not in {f"LAYOUT_{M[n][1]['id'][4:]}" for n in M} and l.get("name") not in {r+"_Layout" for r in RIMOSSE}]
import shutil
for r in RIMOSSE:
    for d in (f"data/maps/{r}",f"data/layouts/{r}"): shutil.rmtree(d,ignore_errors=True)
sections=json.load(open("src/data/region_map/region_map_sections.json",encoding='utf-8'))
inc=[]
for nome,(m,info) in M.items():
    m.save(nome)
    lid="LAYOUT_"+info['id'][4:]
    layouts["layouts"].append({"id":lid,"name":f"{nome}_Layout","width":m.w,"height":m.h,"primary_tileset":"gTileset_General",
        "secondary_tileset":m.ts,"border_filepath":f"data/layouts/{nome}/border.bin",
        "blockdata_filepath":f"data/layouts/{nome}/map.bin","layout_version":"emerald"})
    bg=[]; sc=[m.mapscripts or f"{nome}_MapScripts::\n\t.byte 0\n"]+m.script
    for i,o in enumerate(m.objs):
        if o.get("_testo") is not None:
            lab=f"{nome}_EventScript_Npc{i}"; o["script"]=lab
            sc.append(f"{lab}::\n\tmsgbox {nome}_Text_Npc{i}, MSGBOX_NPC\n\tend\n"); sc.append(f"{nome}_Text_Npc{i}:\n\t.string \"{esc(o.pop('_testo'))}$\"\n")
    for c in m.coords: c["script"]=c["script"].replace("MAPPA_",nome+"_")
    sc=[t.replace("MAPPA_",nome+"_") for t in sc]
    for i,(x,y,t) in enumerate(m.signs):
        lab=f"{nome}_EventScript_Sign{i}"
        bg.append({"type":"sign","x":x,"y":y,"elevation":0,"player_facing_dir":"BG_EVENT_PLAYER_FACING_ANY","script":lab})
        sc.append(f"{lab}::\n\tmsgbox {nome}_Text_Sign{i}, MSGBOX_SIGN\n\tend\n")
        sc.append(f"{nome}_Text_Sign{i}:\n\t.string \"{esc(t)}$\"\n")
    os.makedirs(f"data/maps/{nome}",exist_ok=True)
    mj={"id":info['id'],"name":nome,"layout":lid,"music":info['music'],"region":"REGION_HOENN","region_map_section":info['sec'],
        "requires_flash":False,"weather":info.get('meteo',"WEATHER_SUNNY"),"map_type":info['tipo'],"allow_cycling":True,"allow_escaping":info['tipo']=="MAP_TYPE_UNDERGROUND",
        "allow_running":True,"show_map_name":True,"battle_scene":"MAP_BATTLE_SCENE_NORMAL","connections":info.get('conn',[]),
        "object_events":m.objs,"warp_events":m.warps,"coord_events":m.coords,"bg_events":bg}
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
ids={c["id"] for c in CURE}; via={"MAP_"+snake(r) for r in RIMOSSE}
hl["heal_locations"]=[h for h in hl["heal_locations"] if h["id"] not in ids and h["map"] not in via]+CURE
open("src/data/heal_locations.json","w",encoding='utf-8').write(json.dumps(hl,indent=2,ensure_ascii=False)+"\n")
layouts["layouts"]=[l for l in layouts["layouts"] if l.get("id")!="LAYOUT_TERME"]+[{"id":"LAYOUT_TERME","name":"Terme_Layout","width":16,"height":14,
    "primary_tileset":"gTileset_General","secondary_tileset":"gTileset_Lavaridge","border_filepath":"data/layouts/Terme/border.bin",
    "blockdata_filepath":"data/layouts/Terme/map.bin","layout_version":"emerald"}]
for p,d in (("data/maps/map_groups.json",groups),("data/layouts/layouts.json",layouts),("src/data/region_map/region_map_sections.json",sections)):
    open(p,"w",encoding='utf-8').write(json.dumps(d,indent=2,ensure_ascii=False)+"\n")
# incontri selvatici copiati dalle mappe di Smeraldo d'origine
we=json.load(open("src/data/wild_encounters.json",encoding='utf-8')); grp=we["wild_encounter_groups"][0]
nostri={M[c][1]['id'] for c in M}
import glob as _glob
esistenti={json.load(open(f,encoding='utf-8'))["id"] for f in _glob.glob("data/maps/*/map.json")}
grp["encounters"]=[e for e in grp["encounters"] if e.get("map") not in nostri and (e.get("map") is None or e.get("map") in esistenti)]
for c,src in ENC.items():
    e=json.loads(json.dumps(next(x for x in grp["encounters"] if x.get("map")==src)))
    e["map"]=M[c][1]['id']; e["base_label"]="g"+c; grp["encounters"].append(e)
open("src/data/wild_encounters.json","w",encoding='utf-8').write(json.dumps(we,indent=2,ensure_ascii=False)+"\n")
# include degli script, fuori dal blocco FRLG
es=open("data/event_scripts.s").read().split("\n")
es=[l for l in es if not any(f"data/maps/{n}/scripts.inc" in l for n in list(M)+list(INTERNI)+RIMOSSE)]
k=es.index(".if IS_FRLG")
while es[k-1].strip()=="": k-=1
es[k:k]=inc
open("data/event_scripts.s","w").write("\n".join(es))
print("start",Q.start, {n:(m.w,m.h) for n,(m,_) in M.items()})
