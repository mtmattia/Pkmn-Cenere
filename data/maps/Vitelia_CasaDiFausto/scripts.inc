Vitelia_CasaDiFausto_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Vitelia_CasaDiFausto_OnFrame
	.byte 0

Vitelia_CasaDiFausto_OnFrame:
	map_script_2 VAR_CENERE_STORIA, 0, Vitelia_CasaDiFausto_EventScript_Prologo
	.2byte 0

Vitelia_CasaDiFausto_EventScript_Prologo::
	lockall
	msgbox Vitelia_CasaDiFausto_Text_Calco, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	delay 40
	fadescreen FADE_FROM_BLACK
	msgbox Vitelia_CasaDiFausto_Text_Anno62, MSGBOX_DEFAULT
	closemessage
	setvar VAR_0x8004, 2
	setvar VAR_0x8005, 3
	setvar VAR_0x8006, 16
	setvar VAR_0x8007, 4
	special ShakeCamera
	waitstate
	msgbox Vitelia_CasaDiFausto_Text_Tremito, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	delay 40
	fadescreen FADE_FROM_BLACK
	msgbox Vitelia_CasaDiFausto_Text_DiciassetteAnni, MSGBOX_DEFAULT
	setvar VAR_CENERE_STORIA, 1
	releaseall
	end

Vitelia_CasaDiFausto_Text_Calco:
	.string "Diciotto secoli dopo.\nScavi di Vitelia.\pFIORANI: La cenere ha preso\nla forma dei corpi.\pI corpi sono spariti.\nLa forma è rimasta.\pOPERAIO: Professore!\nHa qualcosa in mano.$"

Vitelia_CasaDiFausto_Text_Anno62:
	.string "Vitelia, anno 62.\nAtrio della casa di Fausto.$"

Vitelia_CasaDiFausto_Text_Tremito:
	.string "Il Grande Tremito!\pUna trave crolla su Lucio.\n{PLAYER} lo tira fuori.\pFAUSTO: Lucio! Guardami!\nStai bene?\pFAUSTO: Tu. Tu lo hai salvato.\pQuando sarai grande, sarai\nsciolto. Lo giuro sulla Lararia.$"

Vitelia_CasaDiFausto_Text_DiciassetteAnni:
	.string "Diciassette anni dopo.\nEstate dell'anno 79.$"

Vitelia_CasaDiFausto_EventScript_Lararia::
	msgbox Vitelia_CasaDiFausto_Text_Lararia, MSGBOX_SIGN
	end

Vitelia_CasaDiFausto_Text_Lararia:
	.string "La Lararia di casa.\nIl serpente dipinto è spaccato\pda una crepa del Grande Tremito.\nNessuno l'ha mai riparata.$"

Vitelia_CasaDiFausto_EventScript_Fausto::
	lock
	faceplayer
	goto_if_eq VAR_CENERE_STORIA, 1, Vitelia_CasaDiFausto_EventScript_Starter
	goto_if_ge VAR_CENERE_STORIA, 6, Vitelia_CasaDiFausto_EventScript_FaustoTorneo
	msgbox Vitelia_CasaDiFausto_Text_FaustoLavoro, MSGBOX_DEFAULT
	release
	end

Vitelia_CasaDiFausto_EventScript_FaustoTorneo::
	msgbox Vitelia_CasaDiFausto_Text_FaustoTorneo, MSGBOX_DEFAULT
	release
	end

Vitelia_CasaDiFausto_EventScript_Starter::
	msgbox Vitelia_CasaDiFausto_Text_FaustoStarter, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	special ChooseStarter
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_ADVENTURE_STARTED
	applymovement LOCALID_CASA_FAUSTO_PINIO, Common_Movement_FacePlayer
	waitmovement 0
	msgbox Vitelia_CasaDiFausto_Text_PinioNaturadex, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_CASA_FAUSTO_LUCIO, Common_Movement_FacePlayer
	waitmovement 0
	msgbox Vitelia_CasaDiFausto_Text_LucioNaturadex, MSGBOX_DEFAULT
	playfanfare MUS_OBTAIN_ITEM
	message Vitelia_CasaDiFausto_Text_PresaNaturadex
	waitmessage
	waitfanfare
	setflag FLAG_SYS_POKEDEX_GET
	special SetUnlockedPokedexFlags
	setflag FLAG_RECEIVED_POKEDEX_FROM_BIRCH
	setflag FLAG_SYS_B_DASH
	setflag FLAG_RECEIVED_RUNNING_SHOES
	msgbox Vitelia_CasaDiFausto_Text_PinioSaluta, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_CASA_FAUSTO_PINIO
	setflag FLAG_CENERE_PINIO_PARTITO
	fadescreen FADE_FROM_BLACK
	setvar VAR_CENERE_STORIA, 2
	msgbox Vitelia_CasaDiFausto_Text_LucioSfida, MSGBOX_DEFAULT
	release
	end

Vitelia_CasaDiFausto_Text_FaustoStarter:
	.string "FAUSTO: {PLAYER}, il Prof. Pinio\nè venuto da Classia.\pHa portato tre Pokémon. Ne ho\ncomprato uno per la casa.\pSceglilo tu. Lo allenerai\nper noi.$"

Vitelia_CasaDiFausto_Text_PinioNaturadex:
	.string "PINIO: Buona scelta!\pE questa è la Naturadex.\nRegistra ogni Pokémon che vedi.\pLucio, sei libero: la affido\na te. Riempila per me.$"

Vitelia_CasaDiFausto_Text_LucioNaturadex:
	.string "LUCIO: (sottovoce) Tieni, {PLAYER}.\nTu li conosci meglio di me.$"

Vitelia_CasaDiFausto_Text_PresaNaturadex:
	.string "{PLAYER} riceve la Naturadex!$"

Vitelia_CasaDiFausto_Text_PinioSaluta:
	.string "PINIO: Torno a Classia.\nScrivetemi cosa trovate!$"

Vitelia_CasaDiFausto_Text_LucioSfida:
	.string "LUCIO: {PLAYER}! Proviamo il\nPokémon nuovo. In cortile!$"

Vitelia_CasaDiFausto_Text_FaustoLavoro:
	.string "FAUSTO: Le anfore di garo non\nsi portano da sole, {PLAYER}.\pE tieni d'occhio Lucio.$"

Vitelia_CasaDiFausto_Text_FaustoTorneo:
	.string "FAUSTO: Un campione in casa\nvale oro. Vinci all'Arena!$"

Vitelia_CasaDiFausto_EventScript_Pinio::
	msgbox Vitelia_CasaDiFausto_Text_PinioNaturadex, MSGBOX_NPC
	end

Vitelia_CasaDiFausto_EventScript_Lucio::
	lock
	faceplayer
	goto_if_eq VAR_CENERE_STORIA, 2, Vitelia_CasaDiFausto_EventScript_LucioLotta
	goto_if_ge VAR_CENERE_STORIA, 3, Vitelia_CasaDiFausto_EventScript_LucioDopo
	msgbox Vitelia_CasaDiFausto_Text_LucioPrima, MSGBOX_DEFAULT
	release
	end

Vitelia_CasaDiFausto_EventScript_LucioDopo::
	msgbox Vitelia_CasaDiFausto_Text_LucioDopo, MSGBOX_DEFAULT
	release
	end

Vitelia_CasaDiFausto_EventScript_LucioLotta::
	msgbox Vitelia_CasaDiFausto_Text_LucioVia, MSGBOX_DEFAULT
	closemessage
	playbgm MUS_ENCOUNTER_BRENDAN, TRUE
	switch VAR_STARTER_MON
	case 0, Vitelia_CasaDiFausto_EventScript_LottaTreecko
	case 1, Vitelia_CasaDiFausto_EventScript_LottaTorchic
	case 2, Vitelia_CasaDiFausto_EventScript_LottaMudkip
	end

Vitelia_CasaDiFausto_EventScript_LottaTreecko::
	trainerbattle_no_intro TRAINER_BRENDAN_ROUTE_103_TREECKO, Vitelia_CasaDiFausto_Text_LucioSconfitto
	goto Vitelia_CasaDiFausto_EventScript_DopoLotta

Vitelia_CasaDiFausto_EventScript_LottaTorchic::
	trainerbattle_no_intro TRAINER_BRENDAN_ROUTE_103_TORCHIC, Vitelia_CasaDiFausto_Text_LucioSconfitto
	goto Vitelia_CasaDiFausto_EventScript_DopoLotta

Vitelia_CasaDiFausto_EventScript_LottaMudkip::
	trainerbattle_no_intro TRAINER_BRENDAN_ROUTE_103_MUDKIP, Vitelia_CasaDiFausto_Text_LucioSconfitto
	goto Vitelia_CasaDiFausto_EventScript_DopoLotta

Vitelia_CasaDiFausto_EventScript_DopoLotta::
	special HealPlayerParty
	msgbox Vitelia_CasaDiFausto_Text_LucioTutorial, MSGBOX_DEFAULT
	giveitem ITEM_POKE_BALL, 5
	giveitem ITEM_POTION, 2
	setvar VAR_CENERE_STORIA, 3
	msgbox Vitelia_CasaDiFausto_Text_LucioLittari, MSGBOX_DEFAULT
	release
	end

Vitelia_CasaDiFausto_Text_LucioPrima:
	.string "LUCIO: Papà sta trattando\ncon il Prof. Pinio.$"

Vitelia_CasaDiFausto_Text_LucioVia:
	.string "LUCIO: Pronto? Non risparmiarti\nsolo perché sono il padroncino!$"

Vitelia_CasaDiFausto_Text_LucioSconfitto:
	.string "Come sempre.\nTu li capisci, io no.$"

Vitelia_CasaDiFausto_Text_LucioTutorial:
	.string "LUCIO: Se si stanca, portalo\nal Termopolio Pokémon.\pLì lo curano gratis. Al Mercato\ncompri Poké Ball e Pozioni.\pE i premi delle lotte... vanno\na papà. Sei Vincolato.\pUna piccola parte però resta a\nte: è il tuo Peculio.\pMettilo da parte. Con il\nPeculio ci si compra la libertà.\pPrendi, me le ha date papà\nma servono più a te.$"

Vitelia_CasaDiFausto_Text_LucioLittari:
	.string "LUCIO: Dicono che i Littari\nsiano davanti alle Terme.\pAndiamo a vedere?$"

Vitelia_CasaDiFausto_Text_LucioDopo:
	.string "LUCIO: La Grande Palestra è\na sud-ovest, vicino all'Arena.$"

