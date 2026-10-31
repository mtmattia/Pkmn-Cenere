# Monte Antro (eseguito da build_maps.py prima dei raccordi): la catena di calcare a sud di Ortensia.
# Pendici (esterno) -> Antro delle Cascate (grotte di Cascate Meteora) -> Valico (esterno)
# -> Gallerie dell'Antro (grotte della Via Vittoria) -> Belvedere sopra Approdia.
# Sottotrama: i Littari deviano le sorgenti del monte verso le loro cisterne.

S.porta('S',20); S.strada(20,2,2,34)               # Ortensia: porta verso il monte

def roccia(m,x0,y0,x1,y1):
    # massiccio di calcare: riga y0 = cresta, y1 = piede (dove si aprono le grotte)
    for y in range(y0,y1+1):
        r=(0x068,0x069,0x06a) if y==y0 else (0x078,0x079,0x07a) if y==y1 else (0x070,0x071,0x072)
        for x in range(x0,x1+1):
            m.g[y][x]=(r[0] if x==x0 else r[2] if x==x1 else r[1])|0x0400; m.occ[y][x]=3
BOCCA=0x0a7|0x3000                                  # imbocco di grotta (porta senza animazione)
def bocca(m,x,y,dest,wid): m.g[y][x]=BOCCA; m.occ[y][x]=1; warp(m,x,y,dest,wid,el=0)

def grotta(nome,src,w,h,id_,sec,nomemappa,music,uscite,ts):
    # copia una grotta di Smeraldo e ne rimappa le uscite; uscite: {indice: (mappa, id) o None per toglierla}
    m=da_smeraldo(nome,src,w,h,ts,enc=json.load(open(f"data/maps/{src}/map.json"))["id"],
                  id=id_,sec=sec,nome=nomemappa,music=music,tipo="MAP_TYPE_UNDERGROUND",meteo="WEATHER_NONE")
    for i,wv in enumerate(json.load(open(f"data/maps/{src}/map.json"))["warp_events"]):
        d=uscite[i] if i in uscite else (GROTTE[wv["dest_map"]],int(wv["dest_warp_id"]))
        if d: warp(m,wv["x"],wv["y"],d[0],d[1],el=wv["elevation"])
    return m
GROTTE={"MAP_METEOR_FALLS_1F_1R":"MAP_ANTRO_DELLE_CASCATE","MAP_METEOR_FALLS_1F_2R":"MAP_ANTRO_DELLE_CASCATE2",
        "MAP_METEOR_FALLS_B1F_1R":"MAP_ANTRO_DELLE_CASCATE_B1","MAP_METEOR_FALLS_B1F_2R":"MAP_ANTRO_DELLE_CASCATE_B2",
        "MAP_VICTORY_ROAD_1F":"MAP_GALLERIE_ANTRO","MAP_VICTORY_ROAD_B1F":"MAP_GALLERIE_ANTRO_B1","MAP_VICTORY_ROAD_B2F":"MAP_GALLERIE_ANTRO_B2"}

# ---------------- Pendici dell'Antro: la strada da Ortensia gira attorno al monte fino alla grotta
PA=mappa("PendiciAntro",40,30,id="MAP_PENDICI_ANTRO",sec="MAPSEC_ROUTE_116",nome="MONTE ANTRO",music="MUS_ROUTE119",tipo="MAP_TYPE_ROUTE")
PA.porta('N',20)
for r in ((14,8,26,11),(10,10,19,14),(22,9,31,13),(8,13,14,17),(27,12,33,17),(12,13,29,18),(9,17,17,21),(23,16,32,21),(16,18,25,21)):
    roccia(PA,*r)                                    # gradoni di calcare sovrapposti, dal fondo al davanti
for r in ((2,25,9,27),(6,26,13,28),(28,25,37,27),(26,26,32,28)): roccia(PA,*r)   # la catena continua verso sud
PA.strada(20,0,2,7); PA.strada(4,5,32,2); PA.strada(4,5,2,20); PA.strada(34,5,2,20)
PA.strada(4,23,32,2); PA.strada(19,22,4,1)
bocca(PA,20,21,"MAP_ANTRO_DELLE_CASCATE",0)
PA.erba_alta(6,8,3,14); PA.erba_alta(37,8,1,14); PA.erba_alta(15,25,10,2)
PA.alberi(24,1,4,2); PA.alberi(8,1,4,2); PA.fill(FIORI,12,3,6,1); PA.fill(FIORI,24,3,8,1)
PA.cartello(19,7,"MONTE ANTRO\n{DOWN_ARROW} ANTRO DELLE CASCATE")
PA.npc(30,7,"HIKER","Il monte e' tutto di calcare.\\pL'acqua ci scava dentro\ngrotte e cascate da secoli.")
PA.npc(9,23,"PICNICKER","Da qualche giorno la fonte\nsotto il monte da' meno acqua.\\pA Ortensia le vigne\nhanno sete.",mov="MOVEMENT_TYPE_WANDER_AROUND")
ENC["PendiciAntro"]="MAP_ROUTE115"

# ---------------- Antro delle Cascate (Cascate Meteora): ingresso dalle Pendici, uscita sul Valico
C1=grotta("AntroDelleCascate","MeteorFalls_1F_1R",30,42,"MAP_ANTRO_DELLE_CASCATE","MAPSEC_METEOR_FALLS","ANTRO DELLE CASCATE",
          "MUS_CAVE_OF_ORIGIN",{0:("MAP_PENDICI_ANTRO",0),1:("MAP_VALICO_ANTRO",0),5:None},"gTileset_MeteorFalls")
C2=grotta("AntroDelleCascate2","MeteorFalls_1F_2R",30,32,"MAP_ANTRO_DELLE_CASCATE2","MAPSEC_METEOR_FALLS","ANTRO DELLE CASCATE",
          "MUS_CAVE_OF_ORIGIN",{},"gTileset_MeteorFalls")
C3=grotta("AntroDelleCascateB1","MeteorFalls_B1F_1R",29,38,"MAP_ANTRO_DELLE_CASCATE_B1","MAPSEC_METEOR_FALLS","ANTRO DELLE CASCATE",
          "MUS_CAVE_OF_ORIGIN",{},"gTileset_MeteorFalls")
C4=grotta("AntroDelleCascateB2","MeteorFalls_B1F_2R",11,18,"MAP_ANTRO_DELLE_CASCATE_B2","MAPSEC_METEOR_FALLS","ANTRO DELLE CASCATE",
          "MUS_CAVE_OF_ORIGIN",{},"gTileset_MeteorFalls")
C1.npc(20,18,"HIKER","Senti? Le cascate fanno\nmeno rumore del solito.\\pQualcuno ha chiuso le\nsorgenti piu' in alto.")
C1.npc(8,27,"MAGMA_MEMBER_F","Non mi hai vista. Sto solo\nmisurando l'acqua.\\pOrdini dall'alto.",mov="MOVEMENT_TYPE_FACE_DOWN")
C4.npc(5,4,"OLD_MAN","Questa e' la sorgente piu'\nantica del monte.\\pI Domini ci costruirono\nsopra un acquedotto.",mov="MOVEMENT_TYPE_FACE_DOWN")

# ---------------- Valico dell'Antro: esterno tra le due grotte
VA=mappa("ValicoAntro",36,40,id="MAP_VALICO_ANTRO",sec="MAPSEC_ROUTE_115",nome="VALICO DELL'ANTRO",music="MUS_ROUTE119",tipo="MAP_TYPE_ROUTE")
for r in ((0,0,35,3),(0,2,12,6),(16,2,27,5),(25,3,35,7),(4,4,13,6)): roccia(VA,*r)   # parete nord con l'uscita dell'Antro delle Cascate
for r in ((26,13,35,18),(22,16,31,20),(30,17,35,22),(24,19,33,24)): roccia(VA,*r)   # sperone est con l'imbocco delle Gallerie
for r in ((0,33,9,39),(5,35,15,39),(28,31,35,39),(24,34,31,39)): roccia(VA,*r)   # rocce a sud
bocca(VA,8,6,"MAP_ANTRO_DELLE_CASCATE",1)
bocca(VA,28,24,"MAP_GALLERIE_ANTRO",0)
VA.strada(8,7,2,22); VA.strada(8,27,22,2); VA.strada(28,25,2,2)
VA.acqua(13,9,6,5)                                   # laghetto di sorgente, quasi asciutto
VA.erba_alta(2,8,5,18); VA.erba_alta(11,16,9,9); VA.erba_alta(17,30,8,3)
VA.alberi(2,28,4,4); VA.alberi(20,8,2,4); VA.alberi(31,8,2,6)
VA.cartello(10,7,"VALICO DELL'ANTRO\n{RIGHT_ARROW} GALLERIE DELL'ANTRO")
VA.signs.append((16,9,"SORGENTE DEL VALICO\nL'acqua arriva appena."))
VA.npc(12,20,"HIKER","Le Gallerie le scavarono i\nminatori del calcare.\\pDall'altra parte si vede\nl'Isola Smeralda.")
VA.npc(25,27,"MAGMA_MEMBER_M",None,"MOVEMENT_TYPE_FACE_LEFT",script="ValicoAntro_EventScript_Littario")
VA.objs[-1].update(trainer_type="TRAINER_TYPE_NORMAL",trainer_sight_or_berry_tree_id="4",movement_range_x=0,movement_range_y=0)
VA.script.append("""MAPPA_EventScript_Littario::
\ttrainerbattle_single TRAINER_GRUNT_JAGGED_PASS, MAPPA_Text_LittarioSfida, MAPPA_Text_LittarioSconfitto
\tmsgbox MAPPA_Text_LittarioDopo, MSGBOX_AUTOCLOSE
\tend

MAPPA_Text_LittarioSfida:
\t.string "Alt! Il valico e' chiuso.\\n"
\t.string "Lavori dei Littari.$"

MAPPA_Text_LittarioSconfitto:
\t.string "Va bene, va bene!$"

MAPPA_Text_LittarioDopo:
\t.string "L'acqua del monte serve a\\n"
\t.string "riempire le nostre cisterne.\\p"
\t.string "Chi tiene l'acqua tiene la\\n"
\t.string "citta'. Lo dice Severo.$"
""")
ENC["ValicoAntro"]="MAP_ROUTE120"

# ---------------- Gallerie dell'Antro (Via Vittoria): dal Valico al Belvedere sopra Approdia
G1=grotta("GallerieAntro","VictoryRoad_1F",46,45,"MAP_GALLERIE_ANTRO","MAPSEC_VICTORY_ROAD","GALLERIE DELL'ANTRO",
          "MUS_VICTORY_ROAD",{0:("MAP_VALICO_ANTRO",1),1:("MAP_BELVEDERE_ANTRO",0)},"gTileset_Cave")
G2=grotta("GallerieAntroB1","VictoryRoad_B1F",46,31,"MAP_GALLERIE_ANTRO_B1","MAPSEC_VICTORY_ROAD","GALLERIE DELL'ANTRO",
          "MUS_VICTORY_ROAD",{},"gTileset_Cave")
G3=grotta("GallerieAntroB2","VictoryRoad_B2F",46,31,"MAP_GALLERIE_ANTRO_B2","MAPSEC_VICTORY_ROAD","GALLERIE DELL'ANTRO",
          "MUS_VICTORY_ROAD",{},"gTileset_Cave")
G1.npc(13,25,"HIKER","Qui sotto c'erano le cave\ndi calcare dei Domini.\\pCon quella pietra hanno\ncostruito Vitelia.")
G1.npc(31,8,"BLACK_BELT","Ancora poco e sei fuori.\\pL'aria di mare si sente\ngia' da qui.")
G3.npc(2,13,"MAGMA_MEMBER_M","Le tubature arrivano fino\nalle cisterne in citta'.\\pNon dirlo a nessuno.",mov="MOVEMENT_TYPE_FACE_DOWN")

# ---------------- Belvedere dell'Antro: affaccio sul mare, sentiero per Approdia (ancora franato)
BA=mappa("BelvedereAntro",30,20,id="MAP_BELVEDERE_ANTRO",sec="MAPSEC_ROUTE_117",nome="BELVEDERE DELL'ANTRO",music="MUS_ROUTE119",tipo="MAP_TYPE_ROUTE")
for r in ((0,0,29,2),(0,1,9,4),(20,1,29,4),(8,2,21,5)): roccia(BA,*r)
bocca(BA,14,5,"MAP_GALLERIE_ANTRO",1)
BA.strada(14,6,2,8); BA.strada(6,12,18,2)
BA.acqua(0,16,30,4,"t")                              # il mare verso l'Isola Smeralda
BA.fill(FIORI,4,8,6,1); BA.fill(FIORI,20,8,6,1); BA.alberi(2,10,2,2); BA.alberi(26,10,2,2)
roccia(BA,20,11,24,14)                               # frana sul sentiero per Approdia
BA.cartello(16,8,"BELVEDERE DELL'ANTRO\nIn basso: Approdia e il mare.")
BA.cartello(18,11,"{RIGHT_ARROW} APPRODIA\nSentiero chiuso per frana.")
BA.npc(8,13,"SAILOR","Da qui si vede l'Isola\nSmeralda nelle giornate belle.\\pApprodia e' giu' al porto.\nCon la frana ci vuole pazienza.")
