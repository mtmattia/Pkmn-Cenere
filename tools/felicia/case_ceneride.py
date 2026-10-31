# Dopo import_metatiles.py (ceneride): le case di Ceneride hanno sotto la roccia bianca; qui lo strato basso diventa erba,
# cosi si possono posare nelle citta di Felicia. uso (una volta sola): python3 tools/felicia/case_ceneride.py
import struct,json
T="data/tilesets/secondary/petalburg"
M=json.load(open("tools/felicia/import_ceneride.json"))
CASE=[0x201,0x202,0x218,0x209,0x20a,0x20b,0x223,0x214,0x224,0x22b,0x21c,0x22c,0x239,   # casa a guglia
      0x24b,0x24c,0x24d,0x20d,0x20e,0x20f,0x225,0x237,0x227,0x22d,0x23f,0x22f]         # casa cubica
pm=open("data/tilesets/primary/general/metatiles.bin","rb").read()
erba=struct.unpack_from("<4H",pm,1*16)
mb=bytearray(open(f"{T}/metatiles.bin","rb").read())
for m in CASE:
    n=M[str(m)]; struct.pack_into("<4H",mb,(n-512)*16,*erba)
open(f"{T}/metatiles.bin","wb").write(mb)
print("ok",len(CASE))
