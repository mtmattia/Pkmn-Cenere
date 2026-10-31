Quintelia_MapScripts::
	.byte 0

Quintelia_EventScript_Littario::
	lock
	faceplayer
	goto_if_lt VAR_CENERE_STORIA, 3, Quintelia_EventScript_LittarioPresto
	msgbox Quintelia_Text_LittarioSfida, MSGBOX_DEFAULT
	closemessage
	playbgm MUS_ENCOUNTER_MAGMA, TRUE
	trainerbattle_no_intro TRAINER_GRUNT_PETALBURG_WOODS, Quintelia_Text_LittarioSconfitto
	msgbox Quintelia_Text_LittarioFugge, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_QUINTELIA_LITTARIO
	setflag FLAG_CENERE_LITTARI_VIA
	fadescreen FADE_FROM_BLACK
	setvar VAR_CENERE_STORIA, 4
	release
	end

Quintelia_EventScript_LittarioPresto::
	msgbox Quintelia_Text_LittarioPresto, MSGBOX_DEFAULT
	release
	end

Quintelia_Text_LittarioPresto:
	.string "LITTARIO: Circolare! Questo\ncantiere è del Magistro Severo.$"

Quintelia_Text_LittarioSfida:
	.string "LITTARIO: Questa casa è crollata\nnel Grande Tremito.\pIl terreno ora è di Severo.\nLa famiglia se ne va!\pUn Vincolato vuole fare l'eroe?\nAllora lotta!$"

Quintelia_Text_LittarioSconfitto:
	.string "Un Vincolato... mi ha battuto\nun Vincolato!$"

Quintelia_Text_LittarioFugge:
	.string "LITTARIO: Severo lo saprà!\nE lo saprà anche il tuo Domino!$"

Quintelia_EventScript_Sfrattata::
	lock
	faceplayer
	goto_if_set FLAG_CENERE_LITTARI_VIA, Quintelia_EventScript_SfrattataGrazie
	msgbox Quintelia_Text_Sfrattata, MSGBOX_DEFAULT
	release
	end

Quintelia_EventScript_SfrattataGrazie::
	msgbox Quintelia_Text_SfrattataGrazie, MSGBOX_DEFAULT
	release
	end

Quintelia_Text_Sfrattata:
	.string "Diciassette anni che aspettiamo\ni soldi per ricostruire.\pE adesso vogliono il terreno.$"

Quintelia_Text_SfrattataGrazie:
	.string "Grazie, ragazzo. Celado, alla\nGrande Palestra, ti aspettava.$"

Quintelia_EventScript_Severo::
	lock
	faceplayer
	goto_if_eq VAR_CENERE_STORIA, 5, Quintelia_EventScript_Discorso
	goto_if_ge VAR_CENERE_STORIA, 6, Quintelia_EventScript_SeveroDopo
	msgbox Quintelia_Text_SeveroPrima, MSGBOX_DEFAULT
	release
	end

Quintelia_EventScript_SeveroDopo::
	msgbox Quintelia_Text_SeveroDopo, MSGBOX_DEFAULT
	release
	end

Quintelia_EventScript_Discorso::
	msgbox Quintelia_Text_Discorso, MSGBOX_DEFAULT
	setvar VAR_CENERE_STORIA, 6
	setvar VAR_CENERE_USCITE, 1
	msgbox Quintelia_Text_DopoDiscorso, MSGBOX_DEFAULT
	release
	end

Quintelia_Text_SeveroPrima:
	.string "SEVERO: Un altro Vincolato.\nLevati dal Foro, ragazzo.$"

Quintelia_Text_Discorso:
	.string "SEVERO: Popolo di Quintelia!\pDiciassette anni fa il Grande\nTremito ci ha messo in ginocchio.\pOggi vi annuncio che l'Arena\nMagna riaprirà in autunno!\pChi vincerà il torneo avrà\nlo Scioglimento, a spese nostre!\pRicordatevelo quando votate\ni Magistri. Votate Severo!$"

Quintelia_Text_DopoDiscorso:
	.string "LUCIO: {PLAYER}... lo Scioglimento!\nSe vinci, sei libero.\pServono le medaglie di tutta\nFelicia. Partiamo!\pPapà dirà di sì: un campione\nin casa vale oro.$"

Quintelia_Text_SeveroDopo:
	.string "SEVERO: Allenati, Vincolato.\nIl popolo ama i giochi.$"

Quintelia_EventScript_PortaEst::
	lockall
	call Quintelia_EventScript_PortaChiusa
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_WalkLeft
	waitmovement 0
	releaseall
	end

Quintelia_EventScript_PortaOvest::
	lockall
	call Quintelia_EventScript_PortaChiusa
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_WalkRight
	waitmovement 0
	releaseall
	end

Quintelia_EventScript_PortaSud::
	lockall
	call Quintelia_EventScript_PortaChiusa
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_WalkUp
	waitmovement 0
	releaseall
	end

Quintelia_EventScript_PortaNord::
	lockall
	call Quintelia_EventScript_PortaChiusa
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_WalkDown
	waitmovement 0
	releaseall
	end

Quintelia_EventScript_PortaChiusa::
	goto_if_lt VAR_CENERE_STORIA, 3, Quintelia_EventScript_PortaCasa
	goto_if_eq VAR_CENERE_STORIA, 3, Quintelia_EventScript_PortaTerme
	goto_if_eq VAR_CENERE_STORIA, 4, Quintelia_EventScript_PortaPalestra
	msgbox Quintelia_Text_PortaForo, MSGBOX_DEFAULT
	return

Quintelia_EventScript_PortaCasa::
	msgbox Quintelia_Text_PortaCasa, MSGBOX_DEFAULT
	return

Quintelia_EventScript_PortaTerme::
	msgbox Quintelia_Text_PortaTerme, MSGBOX_DEFAULT
	return

Quintelia_EventScript_PortaPalestra::
	msgbox Quintelia_Text_PortaPalestra, MSGBOX_DEFAULT
	return

Quintelia_Text_PortaCasa:
	.string "Un Vincolato non esce dalle mura\nsenza il permesso di Fausto.$"

Quintelia_Text_PortaTerme:
	.string "GUARDIA: Fermo. Ci sono guai\ndavanti alle Terme Stabiane.$"

Quintelia_Text_PortaPalestra:
	.string "GUARDIA: Celado ti cercava alla\nGrande Palestra, a sud-ovest.$"

Quintelia_Text_PortaForo:
	.string "GUARDIA: Il Magistro Severo sta\nper parlare nel Foro. Vai!$"

Quintelia_EventScript_Sign0::
	msgbox Quintelia_Text_Sign0, MSGBOX_SIGN
	end

Quintelia_Text_Sign0:
	.string "PORTA ERCOLANO\n{RIGHT_ARROW} VIA ERCOLIA$"

Quintelia_EventScript_Sign1::
	msgbox Quintelia_Text_Sign1, MSGBOX_SIGN
	end

Quintelia_Text_Sign1:
	.string "PORTA MARINA\n{RIGHT_ARROW} VIA ERCOLIA$"

Quintelia_EventScript_Sign2::
	msgbox Quintelia_Text_Sign2, MSGBOX_SIGN
	end

Quintelia_Text_Sign2:
	.string "PORTA SARNO\n{LEFT_ARROW} VIA NUCERINA$"

Quintelia_EventScript_Sign3::
	msgbox Quintelia_Text_Sign3, MSGBOX_SIGN
	end

Quintelia_Text_Sign3:
	.string "PORTA STABIA\n{DOWN_ARROW} VIA STABIANA$"

Quintelia_EventScript_Sign4::
	msgbox Quintelia_Text_Sign4, MSGBOX_SIGN
	end

Quintelia_Text_Sign4:
	.string "PORTA VESUVIO\n{UP_ARROW} MONTE VESBIO$"

Quintelia_EventScript_Sign5::
	msgbox Quintelia_Text_Sign5, MSGBOX_SIGN
	end

Quintelia_Text_Sign5:
	.string "FORO DI QUINTELIA\nPalkia veglia sul Foro.$"

Quintelia_EventScript_Sign6::
	msgbox Quintelia_Text_Sign6, MSGBOX_SIGN
	end

Quintelia_Text_Sign6:
	.string "TEMPIO DI GIOVE$"

Quintelia_EventScript_Sign7::
	msgbox Quintelia_Text_Sign7, MSGBOX_SIGN
	end

Quintelia_Text_Sign7:
	.string "TERMOPOLIO POKEMON$"

Quintelia_EventScript_Sign8::
	msgbox Quintelia_Text_Sign8, MSGBOX_SIGN
	end

Quintelia_Text_Sign8:
	.string "TERME STABIANE$"

Quintelia_EventScript_Sign9::
	msgbox Quintelia_Text_Sign9, MSGBOX_SIGN
	end

Quintelia_Text_Sign9:
	.string "CASA DI FAUSTO$"

Quintelia_EventScript_Sign10::
	msgbox Quintelia_Text_Sign10, MSGBOX_SIGN
	end

Quintelia_Text_Sign10:
	.string "ARENA MAGNA\nChiusa dalla Rissa dell'Arena.$"

Quintelia_EventScript_Sign11::
	msgbox Quintelia_Text_Sign11, MSGBOX_SIGN
	end

Quintelia_Text_Sign11:
	.string "GRANDE PALESTRA\nCapopalestra: Celado$"

Quintelia_EventScript_Sign12::
	msgbox Quintelia_Text_Sign12, MSGBOX_SIGN
	end

Quintelia_Text_Sign12:
	.string "TEATRO GRANDE$"
