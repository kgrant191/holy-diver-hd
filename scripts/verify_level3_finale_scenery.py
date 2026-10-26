"""Reconstruct Final climb and boss backgrounds/terrain from captured PPU state and source cells."""
from pathlib import Path
import argparse,json
import numpy as np
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--capture',required=True);p.add_argument('--out',required=True);a=p.parse_args()
r=Path(__file__).resolve().parents[1];c=Path(a.capture);pack=c/'mesen_home/HdPacks/Holy_Diver_(Tr)'
assert json.loads((c/'installed_pack.json').read_text())==json.loads((r/'evidence/0.15.0-pack-sha256.json').read_text()),'Capture is not the final candidate'
reg=json.loads((r/'art/level3_finale/registration.json').read_text());atlas=Image.open(pack/'Level3_Finale_Tiles_2x.png').convert('RGBA');cells={}
for m in reg['mappings']:
 if not m['scope'].startswith('l3f9'):continue
 x,y=m['xy'];im=np.array(atlas.crop((x,y,x+16,y+16)));factor=int(float(m['brightness'])*255)/255;im[:,:,:3]=(im[:,:,:3]*factor).astype('uint8')
 cells[m['scope'][3:7],int(m['tile'],16),m['palette']]=im
bg=Image.open(pack/'Poison_Moss_Ruins_Background.png').convert('RGB');stride=json.loads((c/'result.json').read_text())['stride'];frames=sorted(int(p.stem)for p in(c/'ram').glob('*.bin'))
data={k:{}for k in ['ram','ppu','oam','view']}
for n in frames:
 for k in data:
  p=c/k/(f'{n:06}'+('.json'if k=='view'else'.bin'));raw=p.read_bytes();data[k][n]=json.loads(raw)if k=='view'else raw
def render(n,dx,dy):
 ram,pp,v=data['ram'][n],data['ppu'][n],data['view'][n];room=f'{int.from_bytes(ram[0x78:0x7a],"little"):04X}';t=v['vram']
 sx=(t&31)*8+v['xscroll']+(256 if t&0x400 else 0);sy=((t>>5)&31)*8+((t>>12)&7)+(240 if t&0x800 else 0)
 if False:
  sx+=round((int.from_bytes(ram[0x60:0x62],'little')-sx)/512)*512
 sx+=dx;sy+=dy
 # Defeat shakes the native arena between the measured Y=0/Y=4 scrolls.
 # End-frame view metadata can describe the next picture's shake phase.
 if room=='9F92':sx=0;sy=dy
 out=np.array(bg.crop((0,0,512,480)))
 if room=='9F92':
  pa=(pp[0x23c4]>>4)&3;pal=pp[0x3f01+pa*4:0x3f04+pa*4].hex().upper()
  factor={'081737':1,'091929':1,'0A1A29':1,'0F0727':.65,'0F0919':.65,'0F0A19':.65,'0F0F17':.30,'0F0F09':.30,'0F0F07':.12,'0F0F0F':0}[pal]
  out=(out.astype(float)*int(factor*255)/255).astype('uint8')
 coverage=np.zeros((480,512),bool);unmapped={}
 for yy in range(sy//8,(sy+239)//8+1):
  for xx in range(sx//8,(sx+255)//8+1):
   tx,ty=xx%32,yy%30;nt=0x2000+((xx//32)%2)*0x400+((yy//30)%2)*0x800;t=pp[nt+ty*32+tx]+(0x700 if room=='9F1A'else 0x900);at=pp[nt+960+ty//4*8+tx//4];pa=(at>>((ty%4)//2*4+(tx%4)//2*2))&3;pal=(bytes([pp[0x3f00]])+pp[0x3f01+pa*4:0x3f04+pa*4]).hex().upper();im=cells.get((room,t,pal))
   X,Y=(xx*8-sx)*2,(yy*8-sy)*2;left,right=max(0,X),min(512,X+16);top,bottom=max(0,Y),min(480,Y+16)
   if right<=left or bottom<=top:continue
   if im is None:unmapped[f'{t:04X}/{pal}']=unmapped.get(f'{t:04X}/{pal}',0)+1;continue
   tile=im[top-Y:bottom-Y,left-X:right-X];mask=tile[:,:,3]>0;part=out[top:bottom,left:right];part[mask]=tile[:,:,:3][mask];coverage[top:bottom,left:right]=mask
 return out,coverage,unmapped
checks=[]
for n in frames:
 room=int.from_bytes(data['ram'][n][0x78:0x7a],'little')
 if room not in[0x9f1a,0x9f92]or (n%120 and n not in[4356,4364,4372]):continue
 if data['ppu'][n][0x3f00]!=0x0f:continue
 path=c/'frames'/f'{n:06}.png'
 if not path.stat().st_size:continue
 im=np.array(Image.open(path).convert('RGB'))
 if not im.any():continue
 near=[j for j in[n-stride,n,n+stride]if j in data['ram']and int.from_bytes(data['ram'][j][0x78:0x7a],'little')==room]
 exposed=np.ones((480,512),bool);exposed[:112]=False
 for j in near:
  o=data['oam'][j]
  for i in range(0,256,4):
   yy,t,at,xx=o[i:i+4]
   if yy>=239:continue
   x,y=xx*2,(yy+1)*2;exposed[max(0,y-12):min(480,y+28),max(0,x-12):min(512,x+28)]=False
  ram=data['ram'][j]
  for i in range(16):
   if ram[0x300+i]in[1,2,3,4,6,0x26,0x27,0x2c,0x2f,0x53,0x55]:
    x,y=ram[0x340+i]*2,ram[0x350+i]*2;exposed[max(0,y-72):min(480,y+32),max(0,x-48):min(512,x+48)]=False
 if room==0x9f92:
  # A growth cell can disappear between the screenshot and its sampled PPU.
  # Exclude only native nametable cells that actually change in this interval.
  for cell in range(960):
   if len({data['ppu'][j][0x2000+cell]for j in near})<=1:continue
   x,y=cell%32*16,cell//32*16
   exposed[max(0,y-8):min(480,y+16),x:x+16]=False
 best=None
 for j in near:
  # Vertical camera moves several native pixels per frame during jumps.
  # Search only the scroll interval actually bounded by adjacent captures.
  ds=range(-stride,stride+1)
  if room==0x9f92:ds=[0,4]
  if room==0x9f1a:
   def scroll_y(k):
    t=data['view'][k]['vram'];return ((t>>5)&31)*8+((t>>12)&7)+(240 if t&0x800 else 0)
   sy=scroll_y(j);deltas=[(scroll_y(k)-sy+240)%480-240 for k in near];ds=range(min(deltas),max(deltas)+1)
  for d in ds:
   e,cov,unknown=render(j,0,d);ratio=float(np.all(np.abs(e.astype(int)-im.astype(int))<=1,axis=2)[exposed].mean());item=(ratio,j,d,int((cov&exposed).sum()),unknown)
   if best is None or ratio>best[0]:best=item
 checks.append(dict(frame=n,room=f'{room:04X}',fraction=best[0],ppu_frame=best[1],scroll_adjustment=best[2],exposed_pixels=int(exposed.sum()),terrain_pixels=best[3],unmapped=best[4]))
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(dict(checks=checks,minimum_match=min(q['fraction']for q in checks)),indent=2)+'\n')
print(json.dumps(dict(samples=len(checks),minimum=min(q['fraction']for q in checks),failures=[q for q in checks if q['fraction']<.995]),indent=2))
assert all(q['fraction']>.995 for q in checks),'Source reconstruction failed; inspect report'
