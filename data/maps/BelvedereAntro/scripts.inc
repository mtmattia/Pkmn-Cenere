BelvedereAntro_MapScripts::
	.byte 0

BelvedereAntro_EventScript_Npc0::
	msgbox BelvedereAntro_Text_Npc0, MSGBOX_NPC
	end

BelvedereAntro_Text_Npc0:
	.string "Da qui si vede l'Isola\nSmeralda nelle giornate belle.\pApprodia e' giu' al porto.\nCon la frana ci vuole pazienza.$"

BelvedereAntro_EventScript_Sign0::
	msgbox BelvedereAntro_Text_Sign0, MSGBOX_SIGN
	end

BelvedereAntro_Text_Sign0:
	.string "BELVEDERE DELL'ANTRO\nIn basso: Approdia e il mare.$"

BelvedereAntro_EventScript_Sign1::
	msgbox BelvedereAntro_Text_Sign1, MSGBOX_SIGN
	end

BelvedereAntro_Text_Sign1:
	.string "{RIGHT_ARROW} APPRODIA\nSentiero chiuso per frana.$"
