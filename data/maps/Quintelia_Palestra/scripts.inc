Quintelia_Palestra_MapScripts::
	.byte 0

Quintelia_Palestra_EventScript_Celado::
	lock
	faceplayer
	goto_if_set FLAG_BADGE01_GET, Quintelia_Palestra_EventScript_CeladoDopo
	goto_if_lt VAR_CENERE_STORIA, 4, Quintelia_Palestra_EventScript_CeladoPresto
	msgbox Quintelia_Palestra_Text_CeladoSfida, MSGBOX_DEFAULT
	closemessage
	trainerbattle_no_intro TRAINER_BRAWLY_1, Quintelia_Palestra_Text_CeladoSconfitto
	msgbox Quintelia_Palestra_Text_AChiMedaglia, MSGBOX_DEFAULT
	playfanfare MUS_OBTAIN_BADGE
	message Quintelia_Palestra_Text_Medaglia
	waitmessage
	waitfanfare
	setflag FLAG_BADGE01_GET
	setvar VAR_CENERE_STORIA, 5
	msgbox Quintelia_Palestra_Text_CeladoSottovoce, MSGBOX_DEFAULT
	release
	end

Quintelia_Palestra_EventScript_CeladoPresto::
	msgbox Quintelia_Palestra_Text_CeladoPresto, MSGBOX_DEFAULT
	release
	end

Quintelia_Palestra_EventScript_CeladoDopo::
	msgbox Quintelia_Palestra_Text_CeladoDopo, MSGBOX_DEFAULT
	release
	end

Quintelia_Palestra_EventScript_Lucio::
	lock
	faceplayer
	goto_if_set FLAG_BADGE01_GET, Quintelia_Palestra_EventScript_LucioDopo
	msgbox Quintelia_Palestra_Text_LucioPrima, MSGBOX_DEFAULT
	release
	end

Quintelia_Palestra_EventScript_LucioDopo::
	msgbox Quintelia_Palestra_Text_LucioDopo, MSGBOX_DEFAULT
	release
	end

Quintelia_Palestra_Text_CeladoPresto:
	.string "CELADO: La Grande Palestra\nè aperta a tutti.\pMa oggi la città ha altri\nguai. Torna più tardi.$"

Quintelia_Palestra_Text_CeladoSfida:
	.string "CELADO: Ho combattuto all'Arena\nMagna, prima della Rissa.\pVediamo se il tuo Pokémon\nregge un pugno vero!$"

Quintelia_Palestra_Text_CeladoSconfitto:
	.string "Bella lotta, ragazzo.$"

Quintelia_Palestra_Text_AChiMedaglia:
	.string "CELADO: A chi do la medaglia?\pLUCIO: ...A me. I Pokémon sono\ndi casa nostra.\pCELADO: Lo so come funziona.\nAnch'io ero Vincolato.$"

Quintelia_Palestra_Text_Medaglia:
	.string "Lucio riceve la Medaglia Pugno\na nome della casa di Fausto!$"

Quintelia_Palestra_Text_CeladoSottovoce:
	.string "CELADO: (sottovoce) Le medaglie\nvanno al Domino.\pIl nome resta a chi combatte.\nRicordatelo all'Arena Magna.$"

Quintelia_Palestra_Text_CeladoDopo:
	.string "CELADO: Il nome resta a chi\ncombatte, {PLAYER}.$"

Quintelia_Palestra_Text_LucioPrima:
	.string "LUCIO: Celado era un gladiatore.\nCombatti tu, io guardo.$"

Quintelia_Palestra_Text_LucioDopo:
	.string "LUCIO: Severo parla nel Foro!\nAndiamo a sentirlo.$"

