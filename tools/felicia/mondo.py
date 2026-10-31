# Mappa unica di Felicia: incolla tutte le mappe secondo le connessioni reali (come le mappe interattive di Hoenn).
# uso: python3 tools/felicia/mondo.py OUT.png [RENDER.py]
import json,sys,subprocess,os,glob
from PIL import Image,ImageDraw,ImageFont
out=sys.argv[1]; render=sys.argv[2] if len(sys.argv)>2 else "tools/felicia/render.py"
lay={l["id"]:l for l in json.load(open("data/layouts/layouts.json"))["layouts"] if "id" in l}
maps={}
for f in glob.glob("data/maps/*/map.json"):
    m=json.load(open(f)); maps[m["id"]]=(os.path.basename(os.path.dirname(f)),m)
pos={"MAP_VITELIA":(0,0)}; q=["MAP_VITELIA"]
def size(i): l=lay[maps[i][1]["layout"]]; return l["width"],l["height"]
while q:
    a=q.pop(0); ax,ay=pos[a]; aw,ah=size(a)
    for c in maps[a][1].get("connections") or []:
        b=c["map"]
        if b not in maps or b in pos: continue
        bw,bh=size(b); o=c["offset"]; d=c["direction"]
        pos[b]={"right":(ax+aw,ay+o),"left":(ax-bw,ay+o),"down":(ax+o,ay+ah),"up":(ax+o,ay-bh)}[d]; q.append(b)
x0=min(p[0] for p in pos.values()); y0=min(p[1] for p in pos.values())
X1=max(pos[i][0]+size(i)[0] for i in pos); Y1=max(pos[i][1]+size(i)[1] for i in pos)
W,H=X1-x0,Y1-y0; m=28
im=Image.new("RGB",(W*16+m,H*16+m),(20,24,40)); dr=ImageDraw.Draw(im)
tmp="/tmp/claude-0/-home-claude/01fdd385-2078-57ce-a650-6cec9de82114/scratchpad/_m.png"
for i,(px,py) in pos.items():
    l=lay[maps[i][1]["layout"]]; sec=l["secondary_tileset"].replace("gTileset_","")
    sec=__import__("re").sub(r"(?<!^)([A-Z])",r"_\1",sec).lower()
    subprocess.run(["python3",render,".","general",sec,l["blockdata_filepath"],str(l["width"]),str(l["height"]),tmp],check=True)
    im.paste(Image.open(tmp).convert("RGB"),(m+(px-x0)*16,m+(py-y0)*16))
try: font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",22); small=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",11)
except: font=small=ImageFont.load_default()
for x in range(0,W+1,10):
    dr.line([(m+x*16,m),(m+x*16,m+H*16)],fill=(255,60,60),width=1); dr.text((m+x*16+2,8),str(x),fill="white",font=small)
for y in range(0,H+1,10):
    dr.line([(m,m+y*16),(m+W*16,m+y*16)],fill=(255,60,60),width=1); dr.text((2,m+y*16+2),str(y),fill="white",font=small)
for i,(px,py) in pos.items():
    w,h=size(i); X,Y=m+(px-x0)*16,m+(py-y0)*16
    dr.rectangle([X,Y,X+w*16-1,Y+h*16-1],outline=(255,230,0),width=3)
    t=maps[i][0]; dr.rectangle([X+6,Y+6,X+14+dr.textlength(t,font=font),Y+34],fill=(0,0,0)); dr.text((X+10,Y+8),t,fill=(255,230,0),font=font)
im.save(out); print(W,H,len(pos),"mappe")
