ViaStabiana_MapScripts::
	.byte 0

ViaStabiana_EventScript_PrimaScossa::
	goto_if_unset FLAG_BADGE02_GET, ViaStabiana_EventScript_PrimaScossaFine
	lockall
	setvar VAR_0x8004, 2
	setvar VAR_0x8005, 2
	setvar VAR_0x8006, 12
	setvar VAR_0x8007, 4
	special ShakeCamera
	waitstate
	msgbox ViaStabiana_Text_Scossa1, MSGBOX_DEFAULT
	msgbox ViaStabiana_Text_Scossa2, MSGBOX_DEFAULT
	setvar VAR_CENERE_SCOSSA, 1
	releaseall
ViaStabiana_EventScript_PrimaScossaFine:
	end

ViaStabiana_Text_Scossa1:
	.string "La terra trema, piu' forte\ndel solito.\p"
	.string "LUCIO: Ancora una scossa...\p"
	.string "A Quintelia non ci fa piu'\n"
	.string "caso nessuno.$"

ViaStabiana_Text_Scossa2:
	.string "La NATURADEX registra un gruppo\n"
	.string "di POKEMON che scende dal VESBIO.\p"
	.string "Vanno tutti verso valle.$"

ViaStabiana_EventScript_Sign0::
	msgbox ViaStabiana_Text_Sign0, MSGBOX_SIGN
	end

ViaStabiana_Text_Sign0:
	.string "VIA STABIANA\nVigne del Vesbio.$"
