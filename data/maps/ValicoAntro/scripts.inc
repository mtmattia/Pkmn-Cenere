ValicoAntro_MapScripts::
	.byte 0

ValicoAntro_EventScript_Littario::
	trainerbattle_single TRAINER_GRUNT_JAGGED_PASS, ValicoAntro_Text_LittarioSfida, ValicoAntro_Text_LittarioSconfitto
	msgbox ValicoAntro_Text_LittarioDopo, MSGBOX_AUTOCLOSE
	end

ValicoAntro_Text_LittarioSfida:
	.string "Alt! Il valico e' chiuso.\n"
	.string "Lavori dei Littari.$"

ValicoAntro_Text_LittarioSconfitto:
	.string "Va bene, va bene!$"

ValicoAntro_Text_LittarioDopo:
	.string "L'acqua del monte serve a\n"
	.string "riempire le nostre cisterne.\p"
	.string "Chi tiene l'acqua tiene la\n"
	.string "citta'. Lo dice Severo.$"

ValicoAntro_EventScript_Npc0::
	msgbox ValicoAntro_Text_Npc0, MSGBOX_NPC
	end

ValicoAntro_Text_Npc0:
	.string "Le Gallerie le scavarono i\nminatori del calcare.\pDall'altra parte si vede\nl'Isola Smeralda.$"

ValicoAntro_EventScript_Sign0::
	msgbox ValicoAntro_Text_Sign0, MSGBOX_SIGN
	end

ValicoAntro_Text_Sign0:
	.string "VALICO DELL'ANTRO\n{RIGHT_ARROW} GALLERIE DELL'ANTRO$"

ValicoAntro_EventScript_Sign1::
	msgbox ValicoAntro_Text_Sign1, MSGBOX_SIGN
	end

ValicoAntro_Text_Sign1:
	.string "SORGENTE DEL VALICO\nL'acqua arriva appena.$"
