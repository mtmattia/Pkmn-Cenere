# Controlla i testi delle mappe di Felicia: righe al massimo di 33 caratteri e al massimo 2 righe per box (\p o \l per andare avanti).
import re,json
names=json.load(open("data/maps/map_groups.json"))["gMapGroup_Felicia"]; err=0
for n in names:
    try: t=open(f"data/maps/{n}/scripts.inc").read()
    except FileNotFoundError: continue
    for lab,body in re.findall(r'^(\w+_Text_\w+):\n((?:\t\.string ".*"\n?)+)',t,re.M):
        s="".join(re.findall(r'\.string "(.*)"',body)).replace("$","")
        for box in s.split("\\p"):
            righe=re.split(r'\\n|\\l',box)
            if len([r for r in box.split("\\n")])>2: print("3+ righe:",lab,repr(box)); err+=1
            for r in righe:
                if len(re.sub(r'\{[A-Z_]+\}','X',r))>33: print("lunga:",lab,repr(r)); err+=1
print(err,"problemi")
