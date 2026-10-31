PendiciFumario_MapScripts::
	.byte 0

PendiciFumario_EventScript_Npc0::
	msgbox PendiciFumario_Text_Npc0, MSGBOX_NPC
	end

PendiciFumario_Text_Npc0:
	.string "Le viti del Fumario danno il vino\npiu' buono di Felicia.\pIl monte e' generoso.\nChissa' perche'.$"

PendiciFumario_EventScript_Npc1::
	msgbox PendiciFumario_Text_Npc1, MSGBOX_NPC
	end

PendiciFumario_Text_Npc1:
	.string "Da qualche settimana i Pokemon\nscendono dal monte verso valle.\pNon era mai successo.$"

PendiciFumario_EventScript_Npc2::
	msgbox PendiciFumario_Text_Npc2, MSGBOX_NPC
	end

PendiciFumario_Text_Npc2:
	.string "Lavoro qui da quando ero\nVincolato.\pOra sono Affrancato,\nma l'uva e' la stessa.$"

PendiciFumario_EventScript_Sign0::
	msgbox PendiciFumario_Text_Sign0, MSGBOX_SIGN
	end

PendiciFumario_Text_Sign0:
	.string "{UP_ARROW} MONTE FUMARIO\n{DOWN_ARROW} VITELIA, PORTA DEL MONTE$"

PendiciFumario_EventScript_Sign1::
	msgbox PendiciFumario_Text_Sign1, MSGBOX_SIGN
	end

PendiciFumario_Text_Sign1:
	.string "VILLA RUSTICA\pVino del Fumario\nper tutta Felicia.$"

PendiciFumario_EventScript_Sign2::
	msgbox PendiciFumario_Text_Sign2, MSGBOX_SIGN
	end

PendiciFumario_Text_Sign2:
	.string "VIGNE DEL FUMARIO\nVietato cogliere l'uva.\pIl Domino.$"
