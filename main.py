import zlib,struct,math,sys
from pathlib import Path
W=H=512
o=bytearray(W*H*3)
def p(x,y,r,g,b):
 if 0<=x<W and 0<=y<H:
  i=(y*W+x)*3;o[i],o[i+1],o[i+2]=r,g,b
def q(x,y,r,g,b,a):
 if 0<=x<W and 0<=y<H:
  i=(y*W+x)*3
  o[i]=(r*a+o[i]*(255-a))//255;o[i+1]=(g*a+o[i+1]*(255-a))//255;o[i+2]=(b*a+o[i+2]*(255-a))//255
def D(cx,cy,rr,c):
 for y in range(max(0,cy-rr),min(H,cy+rr+1)):
  dy=y-cy;dx=int((rr*rr-dy*dy)**.5)
  for x in range(max(0,cx-dx),min(W,cx+dx+1)):p(x,y,*c)
def E(cx,cy,rr,c,a):
 for y in range(max(0,cy-rr),min(H,cy+rr+1)):
  dy=y-cy;dx=int((rr*rr-dy*dy)**.5)
  for x in range(max(0,cx-dx),min(W,cx+dx+1)):q(x,y,*c,a)
def L(x0,y0,x1,y1,w,c):
 n=int(max(abs(x1-x0),abs(y1-y0)))*2
 for t in range(n+1):D(int(x0+(x1-x0)*t/n),int(y0+(y1-y0)*t/n),w//2,c)
for y in range(H):
 if y<340:
  t=y/340;r,g,b=247-int(9*t),232-int(22*t),208-int(32*t)
 else:
  t=(y-340)/172;r,g,b=178-int(40*t),124-int(36*t),76-int(28*t)
 o[y*W*3:(y+1)*W*3]=bytes((r,g,b))*W
for y in range(338,342):o[y*W*3:(y+1)*W*3]=bytes((122,76,42))*W
E(256,470,170,(40,20,8),55)
D(256,300,165,(47,59,94))
D(256,300,152,(61,74,112))
for y in range(160,441):
 dy=y-300
 if abs(dy)<140:
  dx=int((140*140-dy*dy)**.5);t=(y-160)/280
  r,g,b=240-int(40*t),154-int(60*t),60-int(30*t)
  s=y*W*3+(256-dx)*3;o[s:s+3*(2*dx+1)]=bytes((r,g,b))*(2*dx+1)
for k in range(9):
 b=212+k*21;ph=k*1.3
 for x in range(132,381):
  y=int(b+9*math.sin(x/17+ph))
  if (x-256)**2+(y-300)**2<132**2:D(x,y,3,(246,215,137))
D(315,255,33,(255,248,236))
D(315,255,17,(245,166,35))
E(308,248,6,(255,255,255),160)
for x,y in [(200,230),(235,330),(300,345),(350,300),(180,300),(270,215)]:
 D(x,y,7,(76,175,80));D(x,y,3,(165,220,120))
for x,y in [(220,270),(330,330),(250,360)]:D(x,y,3,(200,40,30))
D(205,335,13,(244,120,150));D(205,335,9,(255,250,240));D(205,335,4,(244,120,150))
for x,y in [(230,240),(280,350),(360,260)]:D(x,y,2,(255,240,200))
L(430,150,270,300,5,(150,95,45))
L(448,172,288,318,5,(150,95,45))
for cx,ph in [(215,0),(256,1.7),(300,3.4)]:
 for y in range(70,190):
  E(int(cx+11*math.sin(y/20+ph)),y,9,(255,255,255),22)
E(150,215,26,(255,255,255),70)
def C(t,d):return struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
raw=b''.join(b'\0'+bytes(o[y*W*3:(y+1)*W*3]) for y in range(H))
d=Path(sys.argv[1] if len(sys.argv)>1 else '/output')
d.mkdir(parents=True,exist_ok=True)
(d/'entry.png').write_bytes(b'\x89PNG\r\n\x1a\n'+C(b'IHDR',struct.pack('>IIBBBBB',W,H,8,2,0,0,0))+C(b'IDAT',zlib.compress(raw,9))+C(b'IEND',b''))
