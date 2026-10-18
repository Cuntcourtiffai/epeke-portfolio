"""Procedurally draws a flat flower silhouette and converts it to gold halftone dots.
Outputs: website/src/halftone.json, assets/halftone-flower.png (static render), pdf/assets/grain.png"""
import numpy as np, json, math
from PIL import Image, ImageDraw, ImageFilter
rng=np.random.default_rng(7); W,H=1000,1250
lum=Image.new('L',(W,H),0)
cx,cy=500,560
def petal(i,n,ring):
    a=i/n*2*math.pi+ring*0.5+rng.normal(0,.08); L=rng.uniform(320,430)*(1-.2*ring); Wd=rng.uniform(250,330)*(1-.1*ring)
    pts=[]
    for t in np.linspace(0,1,40):
        w=Wd*math.sin(math.pi*min(1,t**0.6))**0.7*0.5
        pts.append((t*L, w))
    poly=[(x,y) for x,y in pts]+[(x,-y) for x,y in reversed(pts)]
    ca,sa=math.cos(a),math.sin(a)
    out=[(cx+(x*ca-y*sa), cy+((x*sa+y*ca))*0.82) for x,y in poly]
    return out,a,L
layer=np.zeros((H,W),float)
yy,xx=np.mgrid[0:H,0:W]
for ring,n in [(0,7),(1,6)]:
    for i in range(n):
        poly,a,L=petal(i,n,ring)
        m=Image.new('L',(W,H),0); ImageDraw.Draw(m).polygon(poly,fill=255); m=np.array(m)>0
        dx=(xx-cx); dy=(yy-cy)/0.82
        t=np.clip((dx*math.cos(a)+dy*math.sin(a))/L,0,1); s=(-dx*math.sin(a)+dy*math.cos(a))
        v=0.08+0.85*t**1.3 - 0.35*np.exp(-(s/ (10+16*t))**2)   # midrib fold
        v+=0.10*np.sin(s/18+i)+rng.normal(0,.03,(H,W))*0
        v*=1-0.25*ring
        layer=np.where(m,v,layer)
# stem
st=Image.new('L',(W,H),0); d=ImageDraw.Draw(st)
pts=[(cx+10+60*math.sin(t*2.2)-t*40, cy+60+t*(H-cy-60)) for t in np.linspace(0,1,60)]
d.line(pts,fill=255,width=11); st=np.array(st.filter(ImageFilter.GaussianBlur(1.5)))/255
layer=np.maximum(layer,st*0.7)
# centre
r=np.hypot(xx-cx,(yy-cy)/0.9); layer=np.where(r<60,0.12+0.5*np.clip((r-35)/25,0,1),layer)
layer=np.clip(layer,0,1)
img=Image.fromarray((layer*255).astype('uint8')).filter(ImageFilter.GaussianBlur(2.5))
L=np.array(img)/255
# obscure / dissolve: low-frequency noise mask + decay toward lower-right
def lowfreq(sc,seed):
    g=np.random.default_rng(seed).random((H//sc+2,W//sc+2)); return np.array(Image.fromarray((g*255).astype('uint8')).resize((W,H),Image.BICUBIC))/255
n=lowfreq(140,3)*0.5+lowfreq(40,4)*0.35+lowfreq(14,5)*0.15
decay=np.clip((xx-cx)*0.0010+(yy-cy)*0.0006,0,1)
vis=np.clip(1.15-n*1.35-decay*1.6,0,1)**0.8
L=L*np.clip(vis*1.3,0,1)
# halftone: grid rotated 45 deg
sp=7.4; dots=[]; c45=math.cos(math.pi/4); s45=math.sin(math.pi/4)
for i in range(-230,230):
    for j in range(-230,230):
        x=500+(i*c45-j*s45)*sp; y=625+(i*s45+j*c45)*sp
        if 3<=x<W-3 and 3<=y<H-3:
            v=L[int(y),int(x)]
            if v>0.13: dots.append([int(x),int(y),round(sp*0.66*math.sqrt(v),1)])
print(len(dots),'dots')
json.dump({'w':W,'h':H,'sp':sp,'dots':dots},open('website/src/halftone.json','w'),separators=(',',':'))
# static render (2x) with soft glow
S=2; base=Image.new('RGBA',(W*S,H*S),(0,0,0,0)); dr=ImageDraw.Draw(base)
for x,y,r in dots:
    k=min(1,r/(sp*0.66))**1.4; col=(int(125+130*k),int(80+150*k),int(25+95*k),255)
    dr.ellipse([(x-r)*S,(y-r)*S,(x+r)*S,(y+r)*S],fill=col)
glow=base.filter(ImageFilter.GaussianBlur(18)); glow=Image.blend(Image.new('RGBA',glow.size),glow,1)
out=Image.alpha_composite(glow,base); out.resize((1000,1250),Image.LANCZOS).save('assets/halftone-flower.png',optimize=True)
# grain tile for PDF
g=(rng.normal(128,48,(512,512))).clip(0,255).astype('uint8'); Image.merge('LA',(Image.fromarray(g),Image.new('L',(512,512),255))).save('pdf/assets/grain.png')
