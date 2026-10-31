# Pokemon Cenere - prologo e Atto I a Vitelia (eseguito da build_maps.py, prima della scrittura dei file)
# Avanzamento in VAR_CENERE_STORIA:
#   0 prologo (calco, Grande Tremito, giuramento)   1 Fausto affida lo starter, Pinio, Naturadex
#   2 prima lotta con Lucio                          3 Littari davanti alle Terme
#   4 Celado nella Grande Palestra                   5 discorso di Severo nel Foro
#   6 Atto I finito: VAR_CENERE_USCITE = 1, le porte di Vitelia si aprono
# Testi: "\n" va a capo, "|" apre un nuovo box. Al massimo 33 caratteri per riga (lint_testi.py).

def T(lab,s): return f"{lab}:\n\t.string \"{s.replace(chr(10),'\\n').replace('|','\\p')}$\"\n"
def obj(lid,gfx,x,y,mov,script,flag="0",el=3):
    o={"graphics_id":"OBJ_EVENT_GFX_"+gfx,"x":x,"y":y,"elevation":el,"movement_type":mov,"movement_range_x":0,"movement_range_y":0,
       "trainer_type":"TRAINER_TYPE_NONE","trainer_sight_or_berry_tree_id":"0","script":script,"flag":flag}
    return {"local_id":lid,**o} if lid else o
SCOSSA="\tsetvar VAR_0x8004, 2\n\tsetvar VAR_0x8005, 3\n\tsetvar VAR_0x8006, 16\n\tsetvar VAR_0x8007, 4\n\tspecial ShakeCamera\n\twaitstate\n"
NERO="\tfadescreen FADE_TO_BLACK\n\tdelay 40\n\tfadescreen FADE_FROM_BLACK\n"

# ---------------- Casa di Fausto (House1, 10x9): prologo, starter, Naturadex, prima lotta
C="Vitelia_CasaDiFausto"
STORIA_INT[C]=dict(
 mapscripts=f"""{C}_MapScripts::
\tmap_script MAP_SCRIPT_ON_FRAME_TABLE, {C}_OnFrame
\t.byte 0

{C}_OnFrame:
\tmap_script_2 VAR_CENERE_STORIA, 0, {C}_EventScript_Prologo
\t.2byte 0
""",
 objs=[obj("LOCALID_CASA_FAUSTO_FAUSTO","GENTLEMAN",6,4,"MOVEMENT_TYPE_FACE_LEFT",f"{C}_EventScript_Fausto"),
       obj("LOCALID_CASA_FAUSTO_PINIO","PROF_BIRCH",7,3,"MOVEMENT_TYPE_FACE_DOWN",f"{C}_EventScript_Pinio","FLAG_CENERE_PINIO_PARTITO"),
       obj("LOCALID_CASA_FAUSTO_LUCIO","WALLY",8,5,"MOVEMENT_TYPE_FACE_LEFT",f"{C}_EventScript_Lucio")],
 bg=[{"type":"sign","x":2,"y":1,"elevation":0,"player_facing_dir":"BG_EVENT_PLAYER_FACING_NORTH","script":f"{C}_EventScript_Lararia"}],
 script=[
f"""{C}_EventScript_Prologo::
\tlockall
\tmsgbox {C}_Text_Calco, MSGBOX_DEFAULT
\tclosemessage
{NERO}\tmsgbox {C}_Text_Anno62, MSGBOX_DEFAULT
\tclosemessage
{SCOSSA}\tmsgbox {C}_Text_Tremito, MSGBOX_DEFAULT
\tclosemessage
{NERO}\tmsgbox {C}_Text_DiciassetteAnni, MSGBOX_DEFAULT
\tsetvar VAR_CENERE_STORIA, 1
\treleaseall
\tend
""",
T(f"{C}_Text_Calco","Diciotto secoli dopo.\nScavi di Vitelia.|FIORANI: La cenere ha preso\nla forma dei corpi.|I corpi sono spariti.\nLa forma è rimasta.|OPERAIO: Professore!\nHa qualcosa in mano."),
T(f"{C}_Text_Anno62","Vitelia, anno 62.\nAtrio della casa di Fausto."),
T(f"{C}_Text_Tremito","Il Grande Tremito!|Una trave crolla su Lucio.\n{PLAYER} lo tira fuori.|FAUSTO: Lucio! Guardami!\nStai bene?|FAUSTO: Tu. Tu lo hai salvato.|Quando sarai grande, sarai\nsciolto. Lo giuro sulla Lararia."),
T(f"{C}_Text_DiciassetteAnni","Diciassette anni dopo.\nEstate dell'anno 79."),
f"""{C}_EventScript_Lararia::
\tmsgbox {C}_Text_Lararia, MSGBOX_SIGN
\tend
""",
T(f"{C}_Text_Lararia","La Lararia di casa.\nIl serpente dipinto è spaccato|da una crepa del Grande Tremito.\nNessuno l'ha mai riparata."),
# Fausto: affida lo starter
f"""{C}_EventScript_Fausto::
\tlock
\tfaceplayer
\tgoto_if_eq VAR_CENERE_STORIA, 1, {C}_EventScript_Starter
\tgoto_if_ge VAR_CENERE_STORIA, 6, {C}_EventScript_FaustoTorneo
\tmsgbox {C}_Text_FaustoLavoro, MSGBOX_DEFAULT
\trelease
\tend

{C}_EventScript_FaustoTorneo::
\tmsgbox {C}_Text_FaustoTorneo, MSGBOX_DEFAULT
\trelease
\tend

{C}_EventScript_Starter::
\tmsgbox {C}_Text_FaustoStarter, MSGBOX_DEFAULT
\tclosemessage
\tfadescreen FADE_TO_BLACK
\tspecial ChooseStarter
\tsetflag FLAG_SYS_POKEMON_GET
\tsetflag FLAG_ADVENTURE_STARTED
\tapplymovement LOCALID_CASA_FAUSTO_PINIO, Common_Movement_FacePlayer
\twaitmovement 0
\tmsgbox {C}_Text_PinioNaturadex, MSGBOX_DEFAULT
\tclosemessage
\tapplymovement LOCALID_CASA_FAUSTO_LUCIO, Common_Movement_FacePlayer
\twaitmovement 0
\tmsgbox {C}_Text_LucioNaturadex, MSGBOX_DEFAULT
\tplayfanfare MUS_OBTAIN_ITEM
\tmessage {C}_Text_PresaNaturadex
\twaitmessage
\twaitfanfare
\tsetflag FLAG_SYS_POKEDEX_GET
\tspecial SetUnlockedPokedexFlags
\tsetflag FLAG_RECEIVED_POKEDEX_FROM_BIRCH
\tsetflag FLAG_SYS_B_DASH
\tsetflag FLAG_RECEIVED_RUNNING_SHOES
\tmsgbox {C}_Text_PinioSaluta, MSGBOX_DEFAULT
\tclosemessage
\tfadescreen FADE_TO_BLACK
\tremoveobject LOCALID_CASA_FAUSTO_PINIO
\tsetflag FLAG_CENERE_PINIO_PARTITO
\tfadescreen FADE_FROM_BLACK
\tsetvar VAR_CENERE_STORIA, 2
\tmsgbox {C}_Text_LucioSfida, MSGBOX_DEFAULT
\trelease
\tend
""",
T(f"{C}_Text_FaustoStarter","FAUSTO: {PLAYER}, il Prof. Pinio\nè venuto da Classia.|Ha portato tre Pokémon. Ne ho\ncomprato uno per la casa.|Sceglilo tu. Lo allenerai\nper noi."),
T(f"{C}_Text_PinioNaturadex","PINIO: Buona scelta!|E questa è la Naturadex.\nRegistra ogni Pokémon che vedi.|Lucio, sei libero: la affido\na te. Riempila per me."),
T(f"{C}_Text_LucioNaturadex","LUCIO: (sottovoce) Tieni, {PLAYER}.\nTu li conosci meglio di me."),
T(f"{C}_Text_PresaNaturadex","{PLAYER} riceve la Naturadex!"),
T(f"{C}_Text_PinioSaluta","PINIO: Torno a Classia.\nScrivetemi cosa trovate!"),
T(f"{C}_Text_LucioSfida","LUCIO: {PLAYER}! Proviamo il\nPokémon nuovo. In cortile!"),
T(f"{C}_Text_FaustoLavoro","FAUSTO: Le anfore di garo non\nsi portano da sole, {PLAYER}.|E tieni d'occhio Lucio."),
T(f"{C}_Text_FaustoTorneo","FAUSTO: Un campione in casa\nvale oro. Vinci all'Arena!"),
f"""{C}_EventScript_Pinio::
\tmsgbox {C}_Text_PinioNaturadex, MSGBOX_NPC
\tend
""",
# Lucio: prima lotta, poi Mercato, Termopolio e Peculio
f"""{C}_EventScript_Lucio::
\tlock
\tfaceplayer
\tgoto_if_eq VAR_CENERE_STORIA, 2, {C}_EventScript_LucioLotta
\tgoto_if_ge VAR_CENERE_STORIA, 3, {C}_EventScript_LucioDopo
\tmsgbox {C}_Text_LucioPrima, MSGBOX_DEFAULT
\trelease
\tend

{C}_EventScript_LucioDopo::
\tmsgbox {C}_Text_LucioDopo, MSGBOX_DEFAULT
\trelease
\tend

{C}_EventScript_LucioLotta::
\tmsgbox {C}_Text_LucioVia, MSGBOX_DEFAULT
\tclosemessage
\tplaybgm MUS_ENCOUNTER_BRENDAN, TRUE
\tswitch VAR_STARTER_MON
\tcase 0, {C}_EventScript_LottaTreecko
\tcase 1, {C}_EventScript_LottaTorchic
\tcase 2, {C}_EventScript_LottaMudkip
\tend

{C}_EventScript_LottaTreecko::
\ttrainerbattle_no_intro TRAINER_BRENDAN_ROUTE_103_TREECKO, {C}_Text_LucioSconfitto
\tgoto {C}_EventScript_DopoLotta

{C}_EventScript_LottaTorchic::
\ttrainerbattle_no_intro TRAINER_BRENDAN_ROUTE_103_TORCHIC, {C}_Text_LucioSconfitto
\tgoto {C}_EventScript_DopoLotta

{C}_EventScript_LottaMudkip::
\ttrainerbattle_no_intro TRAINER_BRENDAN_ROUTE_103_MUDKIP, {C}_Text_LucioSconfitto
\tgoto {C}_EventScript_DopoLotta

{C}_EventScript_DopoLotta::
\tspecial HealPlayerParty
\tmsgbox {C}_Text_LucioTutorial, MSGBOX_DEFAULT
\tgiveitem ITEM_POKE_BALL, 5
\tgiveitem ITEM_POTION, 2
\tsetvar VAR_CENERE_STORIA, 3
\tmsgbox {C}_Text_LucioLittari, MSGBOX_DEFAULT
\trelease
\tend
""",
T(f"{C}_Text_LucioPrima","LUCIO: Papà sta trattando\ncon il Prof. Pinio."),
T(f"{C}_Text_LucioVia","LUCIO: Pronto? Non risparmiarti\nsolo perché sono il padroncino!"),
T(f"{C}_Text_LucioSconfitto","Come sempre.\nTu li capisci, io no."),
T(f"{C}_Text_LucioTutorial","LUCIO: Se si stanca, portalo\nal Termopolio Pokémon.|Lì lo curano gratis. Al Mercato\ncompri Poké Ball e Pozioni.|E i premi delle lotte... vanno\na papà. Sei Vincolato.|Una piccola parte però resta a\nte: è il tuo Peculio.|Mettilo da parte. Con il\nPeculio ci si compra la libertà.|Prendi, me le ha date papà\nma servono più a te."),
T(f"{C}_Text_LucioLittari","LUCIO: Dicono che i Littari\nsiano davanti alle Terme.|Andiamo a vedere?"),
T(f"{C}_Text_LucioDopo","LUCIO: La Grande Palestra è\na sud-ovest, vicino all'Arena."),
])

# ---------------- Grande Palestra: Celado, la medaglia va a Lucio
G="Vitelia_Palestra"
STORIA_INT[G]=dict(
 objs=[obj(None,"BRAWLY",5,2,"MOVEMENT_TYPE_FACE_DOWN",f"{G}_EventScript_Celado"),
       obj(None,"WALLY",7,3,"MOVEMENT_TYPE_FACE_LEFT",f"{G}_EventScript_Lucio")],
 script=[
f"""{G}_EventScript_Celado::
\tlock
\tfaceplayer
\tgoto_if_set FLAG_BADGE01_GET, {G}_EventScript_CeladoDopo
\tgoto_if_lt VAR_CENERE_STORIA, 4, {G}_EventScript_CeladoPresto
\tmsgbox {G}_Text_CeladoSfida, MSGBOX_DEFAULT
\tclosemessage
\ttrainerbattle_no_intro TRAINER_BRAWLY_1, {G}_Text_CeladoSconfitto
\tmsgbox {G}_Text_AChiMedaglia, MSGBOX_DEFAULT
\tplayfanfare MUS_OBTAIN_BADGE
\tmessage {G}_Text_Medaglia
\twaitmessage
\twaitfanfare
\tsetflag FLAG_BADGE01_GET
\tsetvar VAR_CENERE_STORIA, 5
\tmsgbox {G}_Text_CeladoSottovoce, MSGBOX_DEFAULT
\trelease
\tend

{G}_EventScript_CeladoPresto::
\tmsgbox {G}_Text_CeladoPresto, MSGBOX_DEFAULT
\trelease
\tend

{G}_EventScript_CeladoDopo::
\tmsgbox {G}_Text_CeladoDopo, MSGBOX_DEFAULT
\trelease
\tend

{G}_EventScript_Lucio::
\tlock
\tfaceplayer
\tgoto_if_set FLAG_BADGE01_GET, {G}_EventScript_LucioDopo
\tmsgbox {G}_Text_LucioPrima, MSGBOX_DEFAULT
\trelease
\tend

{G}_EventScript_LucioDopo::
\tmsgbox {G}_Text_LucioDopo, MSGBOX_DEFAULT
\trelease
\tend
""",
T(f"{G}_Text_CeladoPresto","CELADO: La Grande Palestra\nè aperta a tutti.|Ma oggi la città ha altri\nguai. Torna più tardi."),
T(f"{G}_Text_CeladoSfida","CELADO: Ho combattuto all'Arena\nMagna, prima della Rissa.|Vediamo se il tuo Pokémon\nregge un pugno vero!"),
T(f"{G}_Text_CeladoSconfitto","Bella lotta, ragazzo."),
T(f"{G}_Text_AChiMedaglia","CELADO: A chi do la medaglia?|LUCIO: ...A me. I Pokémon sono\ndi casa nostra.|CELADO: Lo so come funziona.\nAnch'io ero Vincolato."),
T(f"{G}_Text_Medaglia","Lucio riceve la Medaglia Pugno\na nome della casa di Fausto!"),
T(f"{G}_Text_CeladoSottovoce","CELADO: (sottovoce) Le medaglie\nvanno al Domino.|Il nome resta a chi combatte.\nRicordatelo all'Arena Magna."),
T(f"{G}_Text_CeladoDopo","CELADO: Il nome resta a chi\ncombatte, {PLAYER}."),
T(f"{G}_Text_LucioPrima","LUCIO: Celado era un gladiatore.\nCombatti tu, io guardo."),
T(f"{G}_Text_LucioDopo","LUCIO: Severo parla nel Foro!\nAndiamo a sentirlo."),
])

# ---------------- Vitelia: Littari alle Terme, Severo nel Foro, porte chiuse fino al discorso
Q.npc(24,27,"MAGMA_MEMBER_M",None,"MOVEMENT_TYPE_FACE_LEFT",script="Vitelia_EventScript_Littario",flag="FLAG_CENERE_LITTARI_VIA",local_id="LOCALID_VITELIA_LITTARIO")
Q.npc(22,27,"WOMAN_2",None,"MOVEMENT_TYPE_FACE_RIGHT",script="Vitelia_EventScript_Sfrattata")
Q.npc(51,21,"MAXIE",None,"MOVEMENT_TYPE_FACE_DOWN",script="Vitelia_EventScript_Severo")
Q.script+=[
"""MAPPA_EventScript_Littario::
\tlock
\tfaceplayer
\tgoto_if_lt VAR_CENERE_STORIA, 3, MAPPA_EventScript_LittarioPresto
\tmsgbox MAPPA_Text_LittarioSfida, MSGBOX_DEFAULT
\tclosemessage
\tplaybgm MUS_ENCOUNTER_MAGMA, TRUE
\ttrainerbattle_no_intro TRAINER_GRUNT_PETALBURG_WOODS, MAPPA_Text_LittarioSconfitto
\tmsgbox MAPPA_Text_LittarioFugge, MSGBOX_DEFAULT
\tclosemessage
\tfadescreen FADE_TO_BLACK
\tremoveobject LOCALID_VITELIA_LITTARIO
\tsetflag FLAG_CENERE_LITTARI_VIA
\tfadescreen FADE_FROM_BLACK
\tsetvar VAR_CENERE_STORIA, 4
\trelease
\tend

MAPPA_EventScript_LittarioPresto::
\tmsgbox MAPPA_Text_LittarioPresto, MSGBOX_DEFAULT
\trelease
\tend
""",
T("MAPPA_Text_LittarioPresto","LITTARIO: Circolare! Questo\ncantiere è del Magistro Severo."),
T("MAPPA_Text_LittarioSfida","LITTARIO: Questa casa è crollata\nnel Grande Tremito.|Il terreno ora è di Severo.\nLa famiglia se ne va!|Un Vincolato vuole fare l'eroe?\nAllora lotta!"),
T("MAPPA_Text_LittarioSconfitto","Un Vincolato... mi ha battuto\nun Vincolato!"),
T("MAPPA_Text_LittarioFugge","LITTARIO: Severo lo saprà!\nE lo saprà anche il tuo Domino!"),
"""MAPPA_EventScript_Sfrattata::
\tlock
\tfaceplayer
\tgoto_if_set FLAG_CENERE_LITTARI_VIA, MAPPA_EventScript_SfrattataGrazie
\tmsgbox MAPPA_Text_Sfrattata, MSGBOX_DEFAULT
\trelease
\tend

MAPPA_EventScript_SfrattataGrazie::
\tmsgbox MAPPA_Text_SfrattataGrazie, MSGBOX_DEFAULT
\trelease
\tend
""",
T("MAPPA_Text_Sfrattata","Diciassette anni che aspettiamo\ni soldi per ricostruire.|E adesso vogliono il terreno."),
T("MAPPA_Text_SfrattataGrazie","Grazie, ragazzo. Celado, alla\nGrande Palestra, ti aspettava."),
"""MAPPA_EventScript_Severo::
\tlock
\tfaceplayer
\tgoto_if_eq VAR_CENERE_STORIA, 5, MAPPA_EventScript_Discorso
\tgoto_if_ge VAR_CENERE_STORIA, 6, MAPPA_EventScript_SeveroDopo
\tmsgbox MAPPA_Text_SeveroPrima, MSGBOX_DEFAULT
\trelease
\tend

MAPPA_EventScript_SeveroDopo::
\tmsgbox MAPPA_Text_SeveroDopo, MSGBOX_DEFAULT
\trelease
\tend

MAPPA_EventScript_Discorso::
\tmsgbox MAPPA_Text_Discorso, MSGBOX_DEFAULT
\tsetvar VAR_CENERE_STORIA, 6
\tsetvar VAR_CENERE_USCITE, 1
\tmsgbox MAPPA_Text_DopoDiscorso, MSGBOX_DEFAULT
\trelease
\tend
""",
T("MAPPA_Text_SeveroPrima","SEVERO: Un altro Vincolato.\nLevati dal Foro, ragazzo."),
T("MAPPA_Text_Discorso","SEVERO: Popolo di Vitelia!|Diciassette anni fa il Grande\nTremito ci ha messo in ginocchio.|Oggi vi annuncio che l'Arena\nMagna riaprirà in autunno!|Chi vincerà il torneo avrà\nlo Scioglimento, a spese nostre!|Ricordatevelo quando votate\ni Magistri. Votate Severo!"),
T("MAPPA_Text_DopoDiscorso","LUCIO: {PLAYER}... lo Scioglimento!\nSe vinci, sei libero.|Servono le medaglie di tutta\nFelicia. Partiamo!|Papà dirà di sì: un campione\nin casa vale oro."),
T("MAPPA_Text_SeveroDopo","SEVERO: Allenati, Vincolato.\nIl popolo ama i giochi."),
]
# porte: finché VAR_CENERE_USCITE è 0 un passo indietro, con un indizio sulla prossima tappa
PORTE={"Est":([(62,6),(62,7),(62,22),(62,23)],"Left"),"Ovest":([(1,27),(1,28)],"Right"),
       "Sud":([(29,46),(30,46)],"Up"),"Nord":([(29,1),(30,1)],"Down")}
for nome,(celle,passo) in PORTE.items():
    Q.evento(celle,"VAR_CENERE_USCITE",0,"Porta"+nome,
f"""\tlockall
\tcall MAPPA_EventScript_PortaChiusa
\tapplymovement OBJ_EVENT_ID_PLAYER, Common_Movement_Walk{passo}
\twaitmovement 0
\treleaseall
\tend
""")
Q.script+=["""MAPPA_EventScript_PortaChiusa::
\tgoto_if_lt VAR_CENERE_STORIA, 3, MAPPA_EventScript_PortaCasa
\tgoto_if_eq VAR_CENERE_STORIA, 3, MAPPA_EventScript_PortaTerme
\tgoto_if_eq VAR_CENERE_STORIA, 4, MAPPA_EventScript_PortaPalestra
\tmsgbox MAPPA_Text_PortaForo, MSGBOX_DEFAULT
\treturn

MAPPA_EventScript_PortaCasa::
\tmsgbox MAPPA_Text_PortaCasa, MSGBOX_DEFAULT
\treturn

MAPPA_EventScript_PortaTerme::
\tmsgbox MAPPA_Text_PortaTerme, MSGBOX_DEFAULT
\treturn

MAPPA_EventScript_PortaPalestra::
\tmsgbox MAPPA_Text_PortaPalestra, MSGBOX_DEFAULT
\treturn
""",
T("MAPPA_Text_PortaCasa","Un Vincolato non esce dalle mura\nsenza il permesso di Fausto."),
T("MAPPA_Text_PortaTerme","GUARDIA: Fermo. Ci sono guai\ndavanti alle Terme Centrali."),
T("MAPPA_Text_PortaPalestra","GUARDIA: Celado ti cercava alla\nGrande Palestra, a sud-ovest."),
T("MAPPA_Text_PortaForo","GUARDIA: Il Magistro Severo sta\nper parlare nel Foro. Vai!"),
]
