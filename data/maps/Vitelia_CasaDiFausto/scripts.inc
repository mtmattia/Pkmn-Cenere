Vitelia_CasaDiFausto_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Vitelia_CasaDiFausto_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Vitelia_CasaDiFausto_OnFrame
	.byte 0

Vitelia_CasaDiFausto_OnTransition:
	call_if_eq VAR_CENERE_STORIA, 0, Vitelia_CasaDiFausto_EventScript_PrologoPosizioni
	end

@ anno 62: Pinio non c'è ancora, Fausto è fuori e Lucio gioca col giocatore
Vitelia_CasaDiFausto_EventScript_PrologoPosizioni::
	setflag FLAG_CENERE_PINIO_PARTITO
	setflag FLAG_TEMP_11
	setobjectxyperm LOCALID_CASA_FAUSTO_FAUSTO, 4, 8
	setobjectxyperm LOCALID_CASA_FAUSTO_LUCIO, 7, 6
	setobjectmovementtype LOCALID_CASA_FAUSTO_LUCIO, MOVEMENT_TYPE_FACE_LEFT
	return

Vitelia_CasaDiFausto_OnFrame:
	map_script_2 VAR_CENERE_STORIA, 0, Vitelia_CasaDiFausto_EventScript_Prologo
	.2byte 0

Vitelia_CasaDiFausto_EventScript_Prologo::
	lockall
	msgbox Vitelia_CasaDiFausto_Text_Anno62, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_CASA_FAUSTO_LUCIO, Vitelia_CasaDiFausto_Movement_LucioScappa
	waitmovement 0
	msgbox Vitelia_CasaDiFausto_Text_LucioGioca, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_PLAYER, Vitelia_CasaDiFausto_Movement_PlayerInsegue
	waitmovement 0
	playse SE_M_EARTHQUAKE
	setvar VAR_0x8004, 2
	setvar VAR_0x8005, 3
	setvar VAR_0x8006, 16
	setvar VAR_0x8007, 4
	special ShakeCamera
	waitstate
	applymovement LOCALID_CASA_FAUSTO_LUCIO, Common_Movement_ExclamationMark
	applymovement LOCALID_PLAYER, Common_Movement_ExclamationMark
	waitmovement 0
	msgbox Vitelia_CasaDiFausto_Text_Trema, MSGBOX_DEFAULT
	closemessage
	playse SE_M_ROCK_THROW
	setvar VAR_0x8004, 2
	setvar VAR_0x8005, 3
	setvar VAR_0x8006, 16
	setvar VAR_0x8007, 4
	special ShakeCamera
	waitstate
	applymovement LOCALID_CASA_FAUSTO_LUCIO, Vitelia_CasaDiFausto_Movement_LucioColpito
	waitmovement 0
	msgbox Vitelia_CasaDiFausto_Text_Trave, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_PLAYER, Vitelia_CasaDiFausto_Movement_PlayerSolleva
	waitmovement 0
	playse SE_M_STRENGTH
	applymovement LOCALID_PLAYER, Vitelia_CasaDiFausto_Movement_PlayerTira
	waitmovement 0
	applymovement LOCALID_CASA_FAUSTO_LUCIO, Vitelia_CasaDiFausto_Movement_LucioFuori
	waitmovement 0
	msgbox Vitelia_CasaDiFausto_Text_Salvato, MSGBOX_DEFAULT
	closemessage
	clearflag FLAG_TEMP_11
	addobject LOCALID_CASA_FAUSTO_FAUSTO
	playse SE_DOOR
	applymovement LOCALID_CASA_FAUSTO_FAUSTO, Vitelia_CasaDiFausto_Movement_FaustoCorre
	waitmovement 0
	msgbox Vitelia_CasaDiFausto_Text_FaustoLucio, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_CASA_FAUSTO_FAUSTO, Vitelia_CasaDiFausto_Movement_FaustoVersoPlayer
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	msgbox Vitelia_CasaDiFausto_Text_Giuramento, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_CASA_FAUSTO_FAUSTO, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	msgbox Vitelia_CasaDiFausto_Text_LarariaCrepata, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
@ diciassette anni dopo: tutti al loro posto, Pinio e' venuto da Classia con gli starter
	setobjectxyperm LOCALID_CASA_FAUSTO_FAUSTO, 6, 4
	setobjectxyperm LOCALID_CASA_FAUSTO_LUCIO, 8, 5
	setobjectxy LOCALID_CASA_FAUSTO_FAUSTO, 6, 4
	setobjectxy LOCALID_CASA_FAUSTO_LUCIO, 8, 5
	turnobject LOCALID_CASA_FAUSTO_FAUSTO, DIR_WEST
	turnobject LOCALID_CASA_FAUSTO_LUCIO, DIR_WEST
	clearflag FLAG_CENERE_PINIO_PARTITO
	addobject LOCALID_CASA_FAUSTO_PINIO
	turnobject LOCALID_CASA_FAUSTO_PINIO, DIR_SOUTH
	applymovement LOCALID_PLAYER, Vitelia_CasaDiFausto_Movement_PlayerAlPosto
	waitmovement 0
	delay 30
	fadescreen FADE_FROM_BLACK
	msgbox Vitelia_CasaDiFausto_Text_DiciassetteAnni, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_CASA_FAUSTO_FAUSTO, Common_Movement_ExclamationMark
	waitmovement 0
	msgbox Vitelia_CasaDiFausto_Text_FaustoChiama, MSGBOX_DEFAULT
	setrespawn HEAL_LOCATION_VITELIA
	setvar VAR_CENERE_STORIA, 1
	releaseall
	end

Vitelia_CasaDiFausto_Movement_LucioScappa:
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_in_place_faster_down
	step_end

Vitelia_CasaDiFausto_Movement_PlayerInsegue:
	walk_right
	walk_right
	walk_right
	walk_up
	walk_up
	step_end

Vitelia_CasaDiFausto_Movement_LucioColpito:
	jump_in_place_down
	walk_in_place_faster_down
	step_end

Vitelia_CasaDiFausto_Movement_PlayerSolleva:
	walk_in_place_fast_up
	walk_in_place_fast_up
	walk_in_place_fast_up
	step_end

Vitelia_CasaDiFausto_Movement_PlayerTira:
	lock_facing_direction
	walk_slow_down
	unlock_facing_direction
	step_end

Vitelia_CasaDiFausto_Movement_LucioFuori:
	lock_facing_direction
	walk_slow_down
	unlock_facing_direction
	step_end

Vitelia_CasaDiFausto_Movement_FaustoCorre:
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_right
	walk_fast_right
	walk_fast_up
	walk_in_place_faster_right
	step_end

Vitelia_CasaDiFausto_Movement_FaustoVersoPlayer:
	walk_down
	walk_in_place_faster_right
	step_end

Vitelia_CasaDiFausto_Movement_PlayerAlPosto:
	walk_left
	walk_left
	walk_left
	walk_down
	walk_in_place_faster_right
	step_end

Vitelia_CasaDiFausto_Text_Anno62:
	.string "Vitelia, anno 62.\nAtrio della casa di Fausto.$"

Vitelia_CasaDiFausto_Text_LucioGioca:
	.string "LUCIO: {PLAYER}! Scommetto\nche non mi prendi!$"

Vitelia_CasaDiFausto_Text_Trema:
	.string "La terra trema!$"

Vitelia_CasaDiFausto_Text_Trave:
	.string "Una trave si stacca dal\nsoffitto e cade su Lucio!$"

Vitelia_CasaDiFausto_Text_Salvato:
	.string "{PLAYER} solleva la trave con\ntutte le forze...\p...e tira fuori Lucio.\nLUCIO: (tossisce) {PLAYER}...$"

Vitelia_CasaDiFausto_Text_FaustoLucio:
	.string "FAUSTO: Lucio! Lucio, guardami.\nStai bene?\pLUCIO: Sì, papà.\nMi ha tirato fuori {PLAYER}.$"

Vitelia_CasaDiFausto_Text_Giuramento:
	.string "FAUSTO: Tu. Tu lo hai salvato.\pQuando sarai grande, sarai\nsciolto. Lo giuro sulla Lararia.$"

Vitelia_CasaDiFausto_Text_LarariaCrepata:
	.string "Sull'altare di casa, il serpente\ndipinto si è spaccato in due.$"

Vitelia_CasaDiFausto_Text_DiciassetteAnni:
	.string "Diciassette anni dopo.\nEstate dell'anno 79.$"

Vitelia_CasaDiFausto_Text_FaustoChiama:
	.string "FAUSTO: {PLAYER}! Vieni qui.\nIl Prof. Pinio è arrivato.$"

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

