# Pokemon Cenere - raccordi tra citta e percorsi, posizioni nel mondo e mare del golfo.
# Eseguito da build_maps.py al posto dei vecchi collegamenti diretti.
#
# Raccordo = mappa corta tra una citta murata e il suo percorso: fuori dalle mura ci sono i sepolcri
# lungo la strada, poi orti e alberi sparsi, poi il bosco del percorso. Le strade restano dritte
# (stessa riga o colonna ai due lati), cosi' le posizioni relative di citta e percorso non cambiano.
import math

def _put(m,ax,u,v,st):
    # timbro con coordinate astratte: u lungo la strada, v di traverso
    x,y=(u,v) if ax=='EW' else (v,u)
    m.put(st,x,y,2)
def _fill(m,ax,u,v,du,dv,val,mark=1):
    x,y,w,h=(u,v,du,dv) if ax=='EW' else (v,u,dv,du)
    m.fill(val,x,y,w,h,mark)
def _libero(m,ax,u,v,du,dv):
    x,y,w,h=(u,v,du,dv) if ax=='EW' else (v,u,dv,du)
    return all(m.ok(x+i,y+j) and m.occ[y+j][x+i]==0 for j in range(h) for i in range(w))

def raccordo(nome,a,lato,b,lung,largo,strade,citta,costa=None,ts=None,nomemappa=None,sec=None,music=None,cartello=None,npc=None):
    """Crea la mappa tra a e b (b sta sul lato `lato` di a) e la collega ai due.
    lung: lunghezza lungo la strada; largo: larghezza di traverso; strade: posizioni di traverso delle strade;
    citta: 'a' o 'b', il lato dove stanno le mura; costa: (inizio_a, inizio_b) riga da cui parte il mare (solo EW)."""
    ax='EW' if lato in 'EW' else 'NS'
    w,h=(lung,largo) if ax=='EW' else (largo,lung)
    ia=M[a][1]
    m=mappa(nome,w,h,id="MAP_"+re.sub(r"(?<!^)([A-Z])",r"_\1",nome).upper(),sec=sec or ia['sec'],nome=nomemappa or ia['nome'],
            music=music or ia['music'],tipo="MAP_TYPE_ROUTE")
    if ts: m.ts=ts
    m.g=[[ERBA]*w for _ in range(h)]; m.occ=[[0]*w for _ in range(h)]
    # u cresce da a verso b quando b e' a est/sud; altrimenti si ribalta
    verso=1 if lato in 'ES' else -1
    lato_citta=0 if citta=='a' else lung-1
    # bordi di traverso: alberi come nei percorsi
    for u in range(0,lung,2):
        _put(m,ax,u,0,ALBERO)
        if costa is None: _put(m,ax,u,largo-2,ALBERO)
    for s in strade: _fill(m,ax,0,s,lung,2,STRADA)
    # mare (solo raccordi est-ovest sulla costa): la riva scende o sale piano tra i due lati
    if costa:
        ca,cb=costa
        for u in range(lung):
            k=u/(lung-1) if lung>1 else 0
            r=round(ca+(cb-ca)*k) if verso==1 else round(cb+(ca-cb)*k)
            for y in range(r,largo): m.g[y][u]=ACQUA['t'] if y==r else ACQUA['c']; m.occ[y][u]=4
            for y in (r-2,r-1):
                if 0<=y and m.occ[y][u]==0: m.g[y][u]=STRADA; m.occ[y][u]=1
    # zona della citta: sepolcri lungo le strade (statue), giardini
    if citta=='a' and verso==-1 or citta=='b' and verso==1: zc=[lung-3,lung-7,lung-11]
    else: zc=[1,5,9]
    for s in strade:
        for i,z in enumerate(zc):
            for dv in (-3,3):
                if _libero(m,ax,z,s+dv,2,2) and (i<2 or dv<0): _put(m,ax,z,s+dv,STATUA)
    # zona di mezzo: orti e alberi sparsi; zona del percorso: bosco fitto
    mezzo=range(11,lung-7) if (zc[0]==1) else range(7,lung-11)
    bosco=range(lung-6,lung-1) if zc[0]==1 else range(1,6)
    for i,u in enumerate(mezzo):
        if i%5==1:
            for v in range(3,largo-3,6):
                if _libero(m,ax,u,v+(i%3),2,2): _put(m,ax,u,v+(i%3),ALBERO)
        if i%5==3:
            for v in range(4,largo-3,7):
                if _libero(m,ax,u,v,3,1): _fill(m,ax,u,v,3,1,FIORI if (i//5)%2 else ERBA_ALTA)
    for u in list(bosco)[::2]:
        for v in range(2,largo-2,2):
            if _libero(m,ax,u,v,2,2): _put(m,ax,u,v,ALBERO)
    # porte: stessa posizione ai due lati (strada dritta)
    g=strade[-1]
    if ax=='EW': m.gates['W']=g; m.gates['E']=g
    else: m.gates['N']=g; m.gates['S']=g
    if cartello:
        cu,cv,ct=cartello; x,y=(cu,cv) if ax=='EW' else (cv,cu); m.cartello(x,y,ct)
    if npc:
        cu,cv,gfx,ct=npc; x,y=(cu,cv) if ax=='EW' else (cv,cu); m.npc(x,y,gfx,ct)
    colleg(a,lato,nome); colleg(nome,lato,b)
    return m

# ---------------- collegamenti di terra, con i raccordi
colleg("Vitelia",'N',"FuoriPortaDelMonte"); colleg("FuoriPortaDelMonte",'N',"PendiciFumario")
raccordo("FuoriPortaDelSale","Vitelia",'E',"ViaSalsedia",26,34,[6,22],'a',
         cartello=(12,4,"VIA DEI SEPOLCRI\\nLe tombe dei Domini di Vitelia."),
         npc=(9,19,"OLD_MAN","Chi ha soldi si fa seppellire\nfuori Porta del Sale.\\pCosi' tutti lo vedono passando."))
raccordo("IngressoSalsedia","ViaSalsedia",'E',"Salsedia",26,24,[10],'b',cartello=(2,9,"{RIGHT_ARROW} SALSEDIA"))
raccordo("LidoSalsedia","Salsedia",'E',"ViaCostiera",26,36,[10],'a',costa=(26,22),
         npc=(8,20,"FISHERMAN","Le barche di Salsedia escono\nall'alba e tornano col garo."))
raccordo("PortaAgorapoli","ViaCostiera",'E',"Agorapoli",26,30,[4],'b',costa=(12,22),cartello=(2,3,"{RIGHT_ARROW} AGORAPOLI"))
raccordo("FuoriAgorapoli","Agorapoli",'E',"GalleriaDelTufo",26,40,[22],'a')
raccordo("FuoriGranaria","GalleriaDelTufo",'E',"Granaria",26,30,[14],'b',cartello=(2,13,"{RIGHT_ARROW} GRANARIA"))
raccordo("FuoriPortaDelleVigne","Vitelia",'S',"ViaDelleVigne",22,32,[14],'a',
         cartello=(4,12,"NECROPOLI DI PORTA DELLE VIGNE"))
raccordo("IngressoOrtensia","ViaDelleVigne",'S',"Ortensia",22,32,[16],'b',cartello=(10,15,"{DOWN_ARROW} ORTENSIA"))
raccordo("FuoriOrtensia","Ortensia",'S',"PendiciAntro",22,32,[20],'a',cartello=(18,19,"{DOWN_ARROW} MONTE ANTRO"))
raccordo("FuoriPortaDelGuado","ViaDelGuado",'E',"Vitelia",26,30,[14],'b',cartello=(22,13,"PORTA DEL GUADO\\n{RIGHT_ARROW} VITELIA"))
raccordo("IngressoRivalia","Rivalia",'E',"ViaDelGuado",26,40,[20],'a',cartello=(2,19,"{LEFT_ARROW} RIVALIA"))
raccordo("FuoriGranariaSud","Granaria",'S',"CampiArdenti",22,40,[37],'a',cartello=(3,35,"{DOWN_ARROW} CAMPI ARDENTI"))
raccordo("IngressoOracolia","CampiArdenti",'S',"Oracolia",22,40,[25],'b',cartello=(10,24,"{DOWN_ARROW} ORACOLIA"))
raccordo("FuoriOracolia","Oracolia",'S',"ViaDellaFlotta",22,32,[12],'a')
raccordo("IngressoClassia","ViaDellaFlotta",'S',"Classia",22,32,[12],'b',cartello=(10,11,"{DOWN_ARROW} CLASSIA"))

# ---------------- posizioni nel mondo (blocchi, Vitelia in 0,0), come in mondo.py
def posizioni():
    ids={info['id']:n for n,(m,info) in M.items()}
    P={"Vitelia":(0,0)}; q=["Vitelia"]
    while q:
        a=q.pop(0); ax_,ay_=P[a]; ma=M[a][0]
        for c in M[a][1].get('conn',[]):
            b=ids[c['map']]
            if b in P: continue
            mb=M[b][0]; o=c['offset']
            P[b]={"right":(ax_+ma.w,ay_+o),"left":(ax_-mb.w,ay_+o),"down":(ax_+o,ay_+ma.h),"up":(ax_+o,ay_-mb.h)}[c['direction']]
            q.append(b)
    return P
P=posizioni()
def R(n): x,y=P[n]; m=M[n][0]; return x,y,x+m.w,y+m.h      # rettangolo x0,y0,x1,y1

# ---------------- mare del golfo: rettangoli ancorati alle citta, divisi in mappe che stanno nel limite del GBA
Ex0,Ey0,Ex1,Ey1=R("Salsedia"); Vx0,Vy0,Vx1,Vy1=R("ViaCostiera"); Nx0,Ny0,Nx1,Ny1=R("Agorapoli")
Sx0,Sy0,Sx1,Sy1=R("Ortensia"); Mx0,My0,Mx1,My1=R("Classia")
assert Vy1==Ny1, (Vy1,Ny1)
Y3=Sy0-12; Yb=Sy1+16
MARI=[  # nome, x0,y0,x1,y1, sezione, nome a schermo, incontri
 ("MareDiSalsedia",   Ex0,Ey1,Vx0,Y3,"MAPSEC_ROUTE_106","MARE DI SALSEDIA","MAP_ROUTE109"),
 ("GolfoDiAgorapoli",Vx0,Vy1,Nx1,Yb,"MAPSEC_ROUTE_108","GOLFO DI AGORAPOLI","MAP_ROUTE124"),
 ("MareDiOrtensia",  Sx1,Y3,Vx0,Yb,"MAPSEC_ROUTE_109","MARE DI ORTENSIA","MAP_ROUTE109"),
 ("MareFumoso",   Vx0+51,Yb,Vx0+131,My1,"MAPSEC_ROUTE_125","MARE FUMOSO","MAP_ROUTE134"),
 ("CanaleDellaNassa",Vx0+92,My1,Mx1,My1+54,"MAPSEC_ROUTE_126","CANALE DELLA NASSA","MAP_ROUTE134"),
]
ISOLE={  # coordinate relative all'angolo del proprio mare: x,y,w,h,cartello
 "MareDiSalsedia":[(14,26,8,6,"SCOGLIO DEL FONDATORE\\nQui approdo' il fondatore.")],
 "GolfoDiAgorapoli":[(50,14,10,7,"SCOGLIO DELL'APPRODO\\nIl primo approdo dei coloni."),(86,40,6,5,None),
                     (20,88,6,5,None),(70,76,8,6,None),(96,104,6,6,None)],
 "MareDiOrtensia":[(30,44,14,10,"ISOLA SMERALDA\\nLe ville dell'imperatore.\\pL'approdo e' chiuso."),(60,20,5,4,None)],
 "MareFumoso":[(20,30,22,18,"ISOLA FUMOSA\\nL'isola dei fumi.\\pL'approdo e' chiuso.")],
 "CanaleDellaNassa":[(70,14,12,8,"ISOLA NASSA\\nCasette di pescatori.")],
}
PERSONE={
 "GolfoDiAgorapoli":[(30,30,"SWIMMER_M","Le navi di Agorapoli vanno\nfino in Kalos.\\pIo ci arrivo a nuoto.\nPrima o poi.","MOVEMENT_TYPE_WANDER_AROUND"),
                     (60,94,"SWIMMER_F","Da qui si vede il Fumario.\\pFuma un po', oggi.","MOVEMENT_TYPE_WANDER_AROUND")],
 "CanaleDellaNassa":[(73,20,"SAILOR","Le navi paldeane passano\ndal canale ogni settimana.\\pCercano qualcosa a nord.","MOVEMENT_TYPE_LOOK_AROUND")],
}
VECCHI_MARI=["MareDiSalsedia","GolfoDiAgorapoli","MareDiOrtensia","GolfoDiFelicia","MareFumoso","CanaleDellaNassa"]
PEZZI=[]   # (nome mappa, x0,y0,x1,y1)
for base,x0,y0,x1,y1,sec,nome,enc in MARI:
    W,H=x1-x0,y1-y0; assert W>0 and H>0,(base,W,H)
    # tela unica per il rettangolo, poi tagliata in pezzi
    tela=Mappa(W,H); tela.g=[[ACQUA['c']]*W for _ in range(H)]; tela.occ=[[4]*W for _ in range(H)]
    for (ix,iy,iw,ih,ct) in ISOLE.get(base,[]):
        if ix+iw<W and iy+ih<H: isola_tela=(ix,iy,iw,ih,ct);
        else: continue
        for i in range(iw):
            if tela.ok(ix+i,iy-1): tela.g[iy-1][ix+i]=ACQUA['b']
            if tela.ok(ix+i,iy+ih): tela.g[iy+ih][ix+i]=ACQUA['t']
        for j in range(ih):
            if tela.ok(ix-1,iy+j): tela.g[iy+j][ix-1]=ACQUA['r']
            if tela.ok(ix+iw,iy+j): tela.g[iy+j][ix+iw]=ACQUA['l']
        tela.fill(STRADA,ix,iy,iw,ih,1)
        if iw>4 and ih>4:
            tela.fill(ERBA,ix+1,iy+1,iw-2,ih-2,1); tela.alberi(ix+2,iy+1,(iw-4)//2*2,(ih-3)//2*2)
        if ct: tela.cartello(ix,iy+ih-1,ct)
    nx=math.ceil(W/80); ny=math.ceil(H/90)
    xs=[round(i*W/nx) for i in range(nx+1)]; ys=[round(j*H/ny) for j in range(ny+1)]
    k=0
    for j in range(ny):
        for i in range(nx):
            px0,px1,py0,py1=xs[i],xs[i+1],ys[j],ys[j+1]
            pn=base if k==0 else f"{base}{k+1}"; k+=1
            s_,n_=(sec,nome)
            if base=="GolfoDiAgorapoli" and j>0: s_,n_="MAPSEC_ROUTE_124","GOLFO DI FELICIA"
            m=mappa(pn,px1-px0,py1-py0,id="MAP_"+re.sub(r"(?<!^)([A-Z0-9]+)",r"_\1",pn).upper(),sec=s_,nome=n_,music="MUS_ROUTE104",tipo="MAP_TYPE_OCEAN_ROUTE")
            m.g=[r[px0:px1] for r in tela.g[py0:py1]]; m.occ=[r[px0:px1] for r in tela.occ[py0:py1]]
            m.border=struct.pack("<4H",*[ACQUA['c']]*4); ENC[pn]=enc
            m.signs=[(sx-px0,sy-py0,st) for sx,sy,st in tela.signs if px0<=sx<px1 and py0<=sy<py1]
            for (qx,qy,gfx,ct,mov) in PERSONE.get(base,[]):
                if px0<=qx<px1 and py0<=qy<py1: m.npc(qx-px0,qy-py0,gfx,ct,mov=mov)
            P[pn]=(x0+px0,y0+py0); PEZZI.append(pn)
RIMOSSE+=[n for n in VECCHI_MARI if n not in M]

# ---------------- connessioni del mare: tra pezzi che si toccano, e con le terre sulla costa
COSTA=["Salsedia","LidoSalsedia","ViaCostiera","PortaAgorapoli","Agorapoli","Ortensia","Classia"]
def tocca(a,b):
    ax0,ay0,ax1,ay1=R(a); bx0,by0,bx1,by1=R(b)
    if ax1==bx0 and min(ay1,by1)>max(ay0,by0): return 'E',by0-ay0
    if bx1==ax0 and min(ay1,by1)>max(ay0,by0): return 'W',by0-ay0
    if ay1==by0 and min(ax1,bx1)>max(ax0,bx0): return 'S',bx0-ax0
    if by1==ay0 and min(ax1,bx1)>max(ax0,bx0): return 'N',bx0-ax0
    return None
DIR={'E':'right','W':'left','N':'up','S':'down'}; OPP={'E':'W','W':'E','N':'S','S':'N'}
def unisci(a,b,lato,off):
    M[a][1].setdefault('conn',[]).append({"map":M[b][1]['id'],"offset":off,"direction":DIR[lato]})
    M[b][1].setdefault('conn',[]).append({"map":M[a][1]['id'],"offset":-off,"direction":DIR[OPP[lato]]})
for i,a in enumerate(PEZZI):
    for b in PEZZI[i+1:]+COSTA:
        t_=tocca(a,b)
        if t_: unisci(a,b,*t_)
# nessuna sovrapposizione tra mappe del mondo
_tutte=list(P)
for i,a in enumerate(_tutte):
    for b in _tutte[i+1:]:
        ax0,ay0,ax1,ay1=R(a); bx0,by0,bx1,by1=R(b)
        assert not (ax0<bx1 and bx0<ax1 and ay0<by1 and by0<ay1), ("sovrapposte",a,b)
for n in PEZZI:
    m=M[n][0]; assert (m.w+15)*(m.h+14)<=10240,(n,m.w,m.h)
