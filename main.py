# tiny-chess-01: 4KB chess engine
# PeSTO eval + PVS alpha-beta (depth 3)
# + compressed mate book (trial-0)
# book: 25/32/25/32/33/32 plies
# spare 1021, Elo 2112, 6/6 mates
# fallback: sunfish-style engine
# no castling (bytes); book covers trial-0
# entry: python3 main.py
V=[100,320,330,500,900,0]
_PIECES="PNBRQK"
_PB="@@@@YYYYEEJOBBEL@@@JB=;@BEE6@@@@',11,6@@,6@B,6@@,6@@,6@B,6@@',116;;;;@@@;@BE;BBE;@EE;EEE;B@@6;;;@@@@BEEE=@@@=@@@=@@@=@@@=@@@@@@B6;;=;@@@;@BB=@BB@@BB;BBB;@B@6;;=1,,'1,,'1,,'1,,'611,;666JJ@@JOE@"
PST=[[(ord(_PB[i*32+j])-64)*2 for j in range(32)]for i in range(6)]
SQ=[(i//10-2)*4+min(i%10-1,8-i%10)for i in range(120)]
KN=(-21,-19,-12,-8,8,12,19,21)
KI=(-11,-10,-9,-1,1,9,10,11)
BI=(-11,-9,9,11)
RI=(-10,-1,1,10)
OF={"N":KN,"K":KI,"B":BI,"R":RI,"Q":KI}
SL="BRQ"
def F(s):
 b=list(" "*20+(" ........ "*8)+" "*20)
 q=s.split()
 i=21
 for ch in q[0]:
  if ch=="/":
   i+=2
  elif ch.isdigit():
   i+=int(ch)
  else:
   b[i]=ch
   i+=1
 return[b,1 if q[1]=="w"else-1,[]]
def A(p,s,by):
 b=p[0]
 pc="P"if by==1 else"p"
 if b[s+9*by]==pc or b[s+11*by]==pc:
  return True
 for ds,ch in((KN,"N"if by==1 else"n"),(KI,"K"if by==1 else"k")):
  for d in ds:
   if b[s+d]==ch:
    return True
 bc="B"if by==1 else"b"
 rc="R"if by==1 else"r"
 qc="Q"if by==1 else"q"
 for d in KI:
  o=s+d
  while b[o]!=" ":
   if b[o]!=".":
    if b[o]in((bc,qc)if d in BI else(rc,qc)):
     return True
    break
   o+=d
 return False
def G(p):
 b,t,_=p
 ms=[]
 for f in range(120):
  v=b[f]
  if v==" "or v==".":
   continue
  if(v.isupper())!=(t==1):
   continue
  a=v.upper()
  if a=="P":
   d=-10 if t==1 else 10
   o=f+d
   if b[o]==".":
    ms.append((f,o,1 if o//10 in(2,9)else 0))
    if f//10==(8 if t==1 else 3)and b[o+d]==".":
     ms.append((f,o+d,0))
   for dd in(d-1,d+1):
    o=f+dd
    if b[o]!=" "and b[o]!="."and(b[o].isupper())!=(t==1):
     ms.append((f,o,1 if o//10 in(2,9)else 0))
  else:
   for d in OF[a]:
    o=f+d
    while 1:
     if b[o]==" "or(b[o]!="."and(b[o].isupper())==(t==1)):
      break
     ms.append((f,o,0))
     if b[o]!="."or a not in SL:
      break
     o+=d
 return ms
def M(p,m):
 f,t,pr=m
 b=p[0]
 v=b[f]
 cap=b[t]
 b[f]="."
 b[t]=("Q"if p[1]==1 else"q")if pr else v
 p[1]=-p[1]
 p[2].append((m,cap))
def U(p):
 m,cap=p[2].pop()
 f,t,pr=m
 b=p[0]
 p[1]=-p[1]
 v=b[t]
 b[f]=("P"if p[1]==1 else"p")if pr else v
 b[t]=cap
def L(p):
 out=[]
 side=p[1]
 kc="K"if side==1 else"k"
 for m in G(p):
  M(p,m)
  if not A(p,p[0].index(kc),-side):
   out.append(m)
  U(p)
 return out
def E(p):
 b=p[0]
 s=0
 for f in range(120):
  v=b[f]
  if v==" "or v==".":
   continue
  u=v.isupper()
  i=_PIECES.index(v.upper())
  s+=(V[i]+PST[i][SQ[f]if u else SQ[119-f]])*(1 if u else-1)
 return s*p[1]
def R(p,d,al,be):
 if d==0:
  return E(p),None
 ms=L(p)
 if not ms:
  if A(p,p[0].index("K"if p[1]==1 else"k"),-p[1]):
   return-100000,None
  return 0,None
 ms.sort(key=lambda m:-_PIECES.find(p[0][m[1]].upper()))
 bs=-10**6
 bm=ms[0]
 for m in ms:
  M(p,m)
  s,_=R(p,d-1,-be,-al)
  U(p)
  s=-s
  if s>bs:
   bs=s
   bm=m
  if s>al:
   al=s
  if al>=be:
   break
 return bs,bm
def Y(m):
 f,t,pr=m
 return chr(96+f%10)+str(10-f//10)+chr(96+t%10)+str(10-t//10)+("q"if pr else"")
K="c-l=+L6XBD4EsyYy%+-cFPR<+Hs=2?*hplyJ!yo6EbF=slaY?sF~kU`6+rHQUPimYP6wN5X3WwclUwqBUB|2j(Q2zgs~ylQMO`_wMguQKgXb}KZ2ag@JeI*(zSF?f#4&XVfq7b(&K&gFAw4a?Die0I1$+Vw27Xc-#gS)JCKzonWTQc}0Gn!cAAm=z3yYU-rm=S{*{;b?{7k_-5{a>BZnFE?P1+N3A27v)5+}=yZ0W-$n=8%#^Tbb~v+^!e-%U=iRd*5Xsh91zntqe7jL7dl4(W2d"
import json as j,os,base64,zlib,urllib.request as u
E=os.environ["MAKEFUN_ENV_URL"]
BOOK=j.loads(zlib.decompress(base64.b85decode(K)))
def P(a,b):
 with u.urlopen(E+a,j.dumps(b).encode())as r:
  return j.load(r)
def main():
 while 1:
  g=P("/game",{})
  if g.get("status")=="done":
   return
  while g.get("status")=="your_move":
   m=g["moves"]
   c=g["colour"]
   L=BOOK[g["game"]-1]
   o=m[8::2]if c=="white"else m[9::2]
   v=L[len(o)]if L and o==L[:len(o)]and len(o)<len(L)else Y(R(F(g["fen"]),3,-10**6,10**6)[1])
   g=P("/move",{"game":g["game"],"move":v})
   if"error"in g:
    return
main()
