# Pokemon Cenere - personaggi ed eventi delle zone nuove (eseguito da build_maps.py dopo storia_atto1.py)

# ---------------- Campi Ardenti: sottotrama dei Tre Laghi (Uxie, Mesprit, Azelf)
K="CampiArdenti_CasaDelCustode"
STORIA_INT[K]=dict(
 objs=[obj(None,"OLD_MAN",6,4,"MOVEMENT_TYPE_FACE_LEFT",f"{K}_EventScript_Custode")],
 script=[f"""{K}_EventScript_Custode::
\tlock
\tfaceplayer
\tgoto_if_ge VAR_CENERE_STORIA, 6, {K}_EventScript_CustodeLibero
\tmsgbox {K}_Text_Custode, MSGBOX_DEFAULT
\trelease
\tend

{K}_EventScript_CustodeLibero::
\tmsgbox {K}_Text_Custode, MSGBOX_DEFAULT
\tmsgbox {K}_Text_CustodeLibero, MSGBOX_DEFAULT
\trelease
\tend
""",
T(f"{K}_Text_Custode","Custodisco i Tre Laghi da\nquando ero ragazzo.|Ombroso, Perlato, Nebbioso.\nUno spirito per ogni lago.|Il sapere, il sentimento,\nla volontà.|Si mostrano solo a chi\nnon appartiene a nessuno."),
T(f"{K}_Text_CustodeLibero","Tu porti il segno di un Domino.\nGli spiriti lo vedono.|Torna quando sarai sciolto.\nAllora ti aspetteranno."),
])
F="CampiArdenti_CasaDelFumarolaro"
STORIA_INT[F]=dict(
 objs=[obj(None,"MAN_4",5,4,"MOVEMENT_TYPE_FACE_DOWN",f"{F}_EventScript_Fumarolaro")],
 script=[f"""{F}_EventScript_Fumarolaro::
\tmsgbox {F}_Text_Fumarolaro, MSGBOX_NPC
\tend
""",
T(f"{F}_Text_Fumarolaro","Raccolgo lo zolfo della\nZolfaia per i tintori.|Da qualche settimana la terra\nsi alza, piano piano.|Il porto di Granaria è più\nbasso di un palmo. Strano."),
])
