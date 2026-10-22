"""Layered crypt backdrop plus exact native platform/stair tile registration."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageOps
import numpy as np,json,re
root=Path(__file__).resolve().parents[1];art=root/'art/room2';out=root/'build/Holy_Diver_(Tr)';art.mkdir(exist_ok=True)
# A 512-native-pixel repeat matches the PPU horizontal scroll wrap. The last
# half-screen is duplicated so the viewport always has image data at wrap.
bg=Image.open(root/'art/generated/crypt_background_generated.png').convert('RGB').resize((1024,480),Image.Resampling.LANCZOS)
a=np.array(bg).astype(float);edge=(a[:,0]+a[:,-1])/2
for x in range(24):
 w=(1-x/24)**2
 a[:,x]=a[:,x]*(1-w)+edge*w;a[:,-1-x]=a[:,-1-x]*(1-w)+edge*w
bg=Image.fromarray(a.astype('uint8'));pan=Image.new('RGBA',(1536,480));pan.paste(bg,(0,0));pan.paste(bg.crop((0,0,512,480)),(1024,0));pan.save(out/'Crypt_Background.png');pan.save(art/'Crypt_Background.png')
src=Image.open(root/'art/generated/crypt_terrain_generated.png').convert('RGBA');cells=[]
for i in range(8):
 cell=src.crop((round(i%4*src.width/4),round(i//4*src.height/2),round((i%4+1)*src.width/4),round((i//4+1)*src.height/2)))
 bbox=cell.getchannel('A').point(lambda p:255 if p>180 else 0).getbbox();assert bbox;cell=cell.crop(bbox).resize((32,32),Image.Resampling.LANCZOS)
 alpha=cell.getchannel('A').point(lambda p:255 if p>=125 else 0)
 cell=cell.convert('RGB').quantize(colors=44,method=Image.Quantize.MEDIANCUT).convert('RGBA');cell.putalpha(alpha)
 if i in [0,1,2,3,7]:
  solid=Image.new('RGBA',(32,32),'#152035');solid.alpha_composite(cell);cell=solid
 cells.append(cell);cell.save(art/f'terrain_cell_{i}.png')
atlas=Image.new('RGBA',(256,128));rules=[];scope='cryptPalette&cryptStonePalette&cryptSpritePalette'
# Slots are exact 16x16 HD pixels (one native 8x8 tile).
slot=1
mapping={}
def register(t,pal,img):
 global slot
 x=slot%16*16;y=slot//16*16;slot+=1;atlas.alpha_composite(img,(x,y))
 rules.append(f'[{scope}]<tile>24,{0x100+t:04X},{pal},{x},{y},1,N');mapping[f'{t:02X}:{pal}']=[x,y]
def meta(ts,pal,im):
 for j,t in enumerate(ts):register(t,pal,im.crop((j%2*16,j//2*16,j%2*16+16,j//2*16+16)))
stone='0F001030';rock='0F071728';blue='0F021222'
meta([0x70,0x71,0x72,0x73],stone,cells[0]);meta([0x74,0x75,0x76,0x77],stone,cells[1])
meta([0xa4,0xa5,0xa6,0xa7],stone,cells[4])
meta([0xb5,0xb6,0xb7,0xb8],stone,cells[5])
meta([0xac,0xad,0xae,0xaf],stone,cells[5])
register(0xb2,stone,cells[6].crop((0,0,16,16)));register(0xb4,stone,cells[6].crop((0,16,16,32)))
for i,ts in enumerate([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]):
 cell=cells[2+i%2]
 if i>=2:cell=ImageOps.mirror(cell)
 meta(ts,rock,cell)
meta([0xa8,0xa9,0xaa,0xab],rock,cells[2])
# Original blue skull masonry is replaced by the illustrated background.
# Only its exact native palette is cleared; platforms/hazards remain tile-bound.
for t in range(256):rules.append(f'[{scope}]<tile>24,{0x100+t:04X},{blue},0,0,1,N')
# Original transparent tile remains transparent across the room's palettes.
for pal in [stone,rock,'0F0F0F0F']:
 rules.append(f'[{scope}]<tile>24,0100,{pal},0,0,1,N')
atlas.save(out/'Crypt_Terrain_2x.png');atlas.save(art/'Crypt_Terrain_2x.png')
p=out/'hires.txt';s=p.read_text();last=s.rfind('<img>');end=s.index('\n',last);s=s[:end]+'\n<img>Crypt_Terrain_2x.png'+s[end:]
pos=s.index('<condition>');s=s[:pos]+'<condition>cryptSpritePalette,ppuMemoryCheckConstant,3F11,==,37\n<condition>cryptPalette,ppuMemoryCheckConstant,3F05,==,02\n<condition>cryptStonePalette,ppuMemoryCheckConstant,3F0B,==,30\n'+s[pos:]
pos=s.index('#Chr_00_0.png');s=s[:pos]+'\n'.join(rules)+f'\n[{scope}]<background>Crypt_Background.png,1,1,0,10,0,0\n'+s[pos:]
p.write_text(s);(art/'terrain_mapping.json').write_text(json.dumps(mapping,indent=2)+'\n')
print('Crypt terrain rules',len(rules),'native platform geometry retained')
