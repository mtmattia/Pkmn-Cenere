# ricolore "Felicia": uso recolor.py SRC_PALDIR DST_PALDIR
import sys,os,colorsys
src,dst=sys.argv[1:3]; os.makedirs(dst,exist_ok=True)
def tf(r,g,b):
    h,s,v=colorsys.rgb_to_hsv(r/255,g/255,b/255); d=h*360
    if s<0.12: pass                                   # grigi: invariati
    elif 75<=d<175:                                   # verdi -> oliva secco mediterraneo
        if v<0.62: d=d-(d-75)*0.35; s=min(1,s*1.05); v*=0.88   # chiome: verde oliva scuro
        else: d=d-(d-75)*0.55-6; s*=0.72; v*=0.97          # erba: secca
    elif 175<=d<255:                                  # acqua -> turchese tirrenico
        d=d-(d-175)*0.8; s=min(1,s*1.2); v=min(1,v*0.98)
    elif d<55 or d>=330:                              # bruni/rocce -> tufo e ocra caldi
        d=d+(40-d)*0.75 if d<55 else 30; s*=0.42; v=v+(1-v)*0.36
    elif 55<=d<75:                                    # sabbia -> ocra
        d=d-10; s=min(1,s*1.1)
    r,g,b=colorsys.hsv_to_rgb((d%360)/360,s,min(1,v))
    q=lambda x: min(248,int(round(x*255/8))*8)        # 5 bit GBA
    return q(r),q(g),q(b)
for f in sorted(os.listdir(src)):
    L=open(f"{src}/{f}").read().split('\n'); cols=[tuple(map(int,l.split())) for l in L[3:19]]
    open(f"{dst}/{f}",'w',newline='\r\n').write("JASC-PAL\n0100\n16\n"+"".join(f"{a} {b} {c}\n" for a,b,c in map(lambda c:tf(*c),cols)))
# override: rampa calcare coerente per rocce/montagne (pal 03, indici 8-14)
CALCARE=[(64,56,56),(248,240,224),(224,216,200),(200,192,176),(168,160,152),(136,128,120),(104,96,96)]
p=f"{dst}/03.pal"; L=open(p).read().split('\n'); cols=[tuple(map(int,l.split())) for l in L[3:19]]
cols[8:15]=CALCARE
open(p,'w',newline='\r\n').write("JASC-PAL\n0100\n16\n"+"".join(f"{a} {b} {c}\n" for a,b,c in cols))
