CampiFlegrei_CasaDelCustode_MapScripts::
	.byte 0

CampiFlegrei_CasaDelCustode_EventScript_Custode::
	lock
	faceplayer
	goto_if_ge VAR_CENERE_STORIA, 6, CampiFlegrei_CasaDelCustode_EventScript_CustodeLibero
	msgbox CampiFlegrei_CasaDelCustode_Text_Custode, MSGBOX_DEFAULT
	release
	end

CampiFlegrei_CasaDelCustode_EventScript_CustodeLibero::
	msgbox CampiFlegrei_CasaDelCustode_Text_Custode, MSGBOX_DEFAULT
	msgbox CampiFlegrei_CasaDelCustode_Text_CustodeLibero, MSGBOX_DEFAULT
	release
	end

CampiFlegrei_CasaDelCustode_Text_Custode:
	.string "Custodisco i Tre Laghi da\nquando ero ragazzo.\pAvernio, Lucrinio, Fusario.\nUno spirito per ogni lago.\pIl sapere, il sentimento,\nla volontà.\pSi mostrano solo a chi\nnon appartiene a nessuno.$"

CampiFlegrei_CasaDelCustode_Text_CustodeLibero:
	.string "Tu porti il segno di un Domino.\nGli spiriti lo vedono.\pTorna quando sarai sciolto.\nAllora ti aspetteranno.$"

