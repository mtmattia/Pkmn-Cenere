Vitelia_MapScripts::
	.byte 0

Vitelia_EventScript_Littario::
	lock
	faceplayer
	goto_if_lt VAR_CENERE_STORIA, 3, Vitelia_EventScript_LittarioPresto
	msgbox Vitelia_Text_LittarioSfida, MSGBOX_DEFAULT
	closemessage
	playbgm MUS_ENCOUNTER_MAGMA, TRUE
	trainerbattle_no_intro TRAINER_GRUNT_PETALBURG_WOODS, Vitelia_Text_LittarioSconfitto
	msgbox Vitelia_Text_LittarioFugge, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_VITELIA_LITTARIO
	setflag FLAG_CENERE_LITTARI_VIA
	fadescreen FADE_FROM_BLACK
	setvar VAR_CENERE_STORIA, 4
	release
	end

Vitelia_EventScript_LittarioPresto::
	msgbox Vitelia_Text_LittarioPresto, MSGBOX_DEFAULT
	release
	end

Vitelia_Text_LittarioPresto:
	.string "LITTARIO: Circolare! Questo\ncantiere è del Magistro Severo.$"

Vitelia_Text_LittarioSfida:
	.string "LITTARIO: Questa casa è crollata\nnel Grande Tremito.\pIl terreno ora è di Severo.\nLa famiglia se ne va!\pUn Vincolato vuole fare l'eroe?\nAllora lotta!$"

Vitelia_Text_LittarioSconfitto:
	.string "Un Vincolato... mi ha battuto\nun Vincolato!$"

Vitelia_Text_LittarioFugge:
	.string "LITTARIO: Severo lo saprà!\nE lo saprà anche il tuo Domino!$"

Vitelia_EventScript_Sfrattata::
	lock
	faceplayer
	goto_if_set FLAG_CENERE_LITTARI_VIA, Vitelia_EventScript_SfrattataGrazie
	msgbox Vitelia_Text_Sfrattata, MSGBOX_DEFAULT
	release
	end

Vitelia_EventScript_SfrattataGrazie::
	msgbox Vitelia_Text_SfrattataGrazie, MSGBOX_DEFAULT
	release
	end

Vitelia_Text_Sfrattata:
	.string "Diciassette anni che aspettiamo\ni soldi per ricostruire.\pE adesso vogliono il terreno.$"

Vitelia_Text_SfrattataGrazie:
	.string "Grazie, ragazzo. Celado, alla\nGrande Palestra, ti aspettava.$"

Vitelia_EventScript_Severo::
	lock
	faceplayer
	goto_if_eq VAR_CENERE_STORIA, 5, Vitelia_EventScript_Discorso
	goto_if_ge VAR_CENERE_STORIA, 6, Vitelia_EventScript_SeveroDopo
	msgbox Vitelia_Text_SeveroPrima, MSGBOX_DEFAULT
	release
	end

Vitelia_EventScript_SeveroDopo::
	msgbox Vitelia_Text_SeveroDopo, MSGBOX_DEFAULT
	release
	end

Vitelia_EventScript_Discorso::
	msgbox Vitelia_Text_Discorso, MSGBOX_DEFAULT
	setvar VAR_CENERE_STORIA, 6
	setvar VAR_CENERE_USCITE, 1
	msgbox Vitelia_Text_DopoDiscorso, MSGBOX_DEFAULT
	release
	end

Vitelia_Text_SeveroPrima:
	.string "SEVERO: Un altro Vincolato.\nLevati dal Foro, ragazzo.$"

Vitelia_Text_Discorso:
	.string "SEVERO: Popolo di Vitelia!\pDiciassette anni fa il Grande\nTremito ci ha messo in ginocchio.\pOggi vi annuncio che l'Arena\nMagna riaprirà in autunno!\pChi vincerà il torneo avrà\nlo Scioglimento, a spese nostre!\pRicordatevelo quando votate\ni Magistri. Votate Severo!$"

Vitelia_Text_DopoDiscorso:
	.string "LUCIO: {PLAYER}... lo Scioglimento!\nSe vinci, sei libero.\pServono le medaglie di tutta\nFelicia. Partiamo!\pPapà dirà di sì: un campione\nin casa vale oro.$"

Vitelia_Text_SeveroDopo:
	.string "SEVERO: Allenati, Vincolato.\nIl popolo ama i giochi.$"

Vitelia_EventScript_PortaEst::
	lockall
	call Vitelia_EventScript_PortaChiusa
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_WalkLeft
	waitmovement 0
	releaseall
	end

Vitelia_EventScript_PortaOvest::
	lockall
	call Vitelia_EventScript_PortaChiusa
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_WalkRight
	waitmovement 0
	releaseall
	end

Vitelia_EventScript_PortaSud::
	lockall
	call Vitelia_EventScript_PortaChiusa
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_WalkUp
	waitmovement 0
	releaseall
	end

Vitelia_EventScript_PortaNord::
	lockall
	call Vitelia_EventScript_PortaChiusa
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_WalkDown
	waitmovement 0
	releaseall
	end

Vitelia_EventScript_PortaChiusa::
	goto_if_lt VAR_CENERE_STORIA, 3, Vitelia_EventScript_PortaCasa
	goto_if_eq VAR_CENERE_STORIA, 3, Vitelia_EventScript_PortaTerme
	goto_if_eq VAR_CENERE_STORIA, 4, Vitelia_EventScript_PortaPalestra
	msgbox Vitelia_Text_PortaForo, MSGBOX_DEFAULT
	return

Vitelia_EventScript_PortaCasa::
	msgbox Vitelia_Text_PortaCasa, MSGBOX_DEFAULT
	return

Vitelia_EventScript_PortaTerme::
	msgbox Vitelia_Text_PortaTerme, MSGBOX_DEFAULT
	return

Vitelia_EventScript_PortaPalestra::
	msgbox Vitelia_Text_PortaPalestra, MSGBOX_DEFAULT
	return

Vitelia_Text_PortaCasa:
	.string "Un Vincolato non esce dalle mura\nsenza il permesso di Fausto.$"

Vitelia_Text_PortaTerme:
	.string "GUARDIA: Fermo. Ci sono guai\ndavanti alle Terme Centrali.$"

Vitelia_Text_PortaPalestra:
	.string "GUARDIA: Celado ti cercava alla\nGrande Palestra, a sud-ovest.$"

Vitelia_Text_PortaForo:
	.string "GUARDIA: Il Magistro Severo sta\nper parlare nel Foro. Vai!$"

Vitelia_EventScript_Sign0::
	msgbox Vitelia_Text_Sign0, MSGBOX_SIGN
	end

Vitelia_Text_Sign0:
	.string "PORTA DEL SALE\n{RIGHT_ARROW} VIA SALSEDIA$"

Vitelia_EventScript_Sign1::
	msgbox Vitelia_Text_Sign1, MSGBOX_SIGN
	end

Vitelia_Text_Sign1:
	.string "PORTA MARINA\n{RIGHT_ARROW} VIA SALSEDIA$"

Vitelia_EventScript_Sign2::
	msgbox Vitelia_Text_Sign2, MSGBOX_SIGN
	end

Vitelia_Text_Sign2:
	.string "PORTA DEL GUADO\n{LEFT_ARROW} VIA DEL GUADO$"

Vitelia_EventScript_Sign3::
	msgbox Vitelia_Text_Sign3, MSGBOX_SIGN
	end

Vitelia_Text_Sign3:
	.string "PORTA DELLE VIGNE\n{DOWN_ARROW} VIA DELLE VIGNE$"

Vitelia_EventScript_Sign4::
	msgbox Vitelia_Text_Sign4, MSGBOX_SIGN
	end

Vitelia_Text_Sign4:
	.string "PORTA DEL MONTE\n{UP_ARROW} MONTE FUMARIO$"

Vitelia_EventScript_Sign5::
	msgbox Vitelia_Text_Sign5, MSGBOX_SIGN
	end

Vitelia_Text_Sign5:
	.string "FORO DI VITELIA\nPalkia veglia sul Foro.$"

Vitelia_EventScript_Sign6::
	msgbox Vitelia_Text_Sign6, MSGBOX_SIGN
	end

Vitelia_Text_Sign6:
	.string "TEMPIO DI GIOVE$"

Vitelia_EventScript_Sign7::
	msgbox Vitelia_Text_Sign7, MSGBOX_SIGN
	end

Vitelia_Text_Sign7:
	.string "TERMOPOLIO POKEMON$"

Vitelia_EventScript_Sign8::
	msgbox Vitelia_Text_Sign8, MSGBOX_SIGN
	end

Vitelia_Text_Sign8:
	.string "TERME CENTRALI$"

Vitelia_EventScript_Sign9::
	msgbox Vitelia_Text_Sign9, MSGBOX_SIGN
	end

Vitelia_Text_Sign9:
	.string "CASA DI FAUSTO$"

Vitelia_EventScript_Sign10::
	msgbox Vitelia_Text_Sign10, MSGBOX_SIGN
	end

Vitelia_Text_Sign10:
	.string "ARENA MAGNA\nChiusa dalla Rissa dell'Arena.$"

Vitelia_EventScript_Sign11::
	msgbox Vitelia_Text_Sign11, MSGBOX_SIGN
	end

Vitelia_Text_Sign11:
	.string "GRANDE PALESTRA\nCapopalestra: Celado$"

Vitelia_EventScript_Sign12::
	msgbox Vitelia_Text_Sign12, MSGBOX_SIGN
	end

Vitelia_Text_Sign12:
	.string "TEATRO GRANDE$"
