"""Register illustrated title/pause screens while retaining live game UI tiles."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import numpy as np,json
root=Path(__file__).resolve().parents[1];art=root/'art';out=root/'build/Holy_Diver_(Tr)'
title=Image.open(art/'generated/title_generated.png').convert('RGBA').resize((512,480),Image.Resampling.LANCZOS)
title.save(out/'Title_HD.png');title.save(art/'Title_HD.png')
src=Image.open(art/'generated/pause_generated.png').convert('RGBA').resize((512,480),Image.Resampling.LANCZOS)
# Align the generated decorative panel edges with the existing live text grid.
xx=np.interp(np.arange(512),[0,48,208,464,511],[0,50,213,459,511]).round().astype(int)
yy=np.interp(np.arange(480),[0,112,272,336,479],[0,110,252,308,479]).round().astype(int)
pause=Image.fromarray(np.asarray(src)[yy[:,None],xx[None,:]])
d=ImageDraw.Draw(pause)
for box in [(90,107,166,133),(265,107,359,133),(25,42,186,88),(58,284,194,308)]:
 d.rounded_rectangle(box,radius=3,fill='#07101e',outline='#8e713d',width=1)
font_path=str(art/'fonts/DejaVuSerif-Bold.ttf')
font=ImageFont.truetype(font_path,14)
d.text((376,64),'PAUSED',font=font,fill='#e7c98c',anchor='mm',stroke_width=1,stroke_fill='#020713')
d.text((256,400),'START  ·  RETURN',font=ImageFont.truetype(font_path,12),fill='#dcc390',anchor='mm',stroke_width=1,stroke_fill='#020713')
pause.save(out/'Pause_HD.png');pause.save(art/'Pause_HD.png')
# Gameplay uses individually shaded glyphs without a fixed-width backplate.
# The native HUD can therefore grow to its full health capacity unobstructed.
for obsolete in [out/'Gameplay_HUD.png',art/'Gameplay_HUD.png']:
 if obsolete.exists():obsolete.unlink()
# Light-only animation derived from the existing flame. No new silhouette or
# repainting: the approved title and character stay byte-identical to v7.
a=np.asarray(title); yy0,xx0=np.mgrid[:480,:512]
flame=((xx0>=181)&(xx0<=213)&(yy0>=200)&(yy0<=247)&
       (a[:,:,0]>190)&(a[:,:,1]>70)&(a[:,:,0]>a[:,:,2]*1.4))
mask=Image.fromarray((flame*255).astype('uint8'))
halo=np.asarray(mask.filter(ImageFilter.GaussianBlur(7))).astype(float)
core=np.asarray(mask.filter(ImageFilter.GaussianBlur(1))).astype(float)
for phase,strength in enumerate([0.18,0.40,0.70,1.0]):
 light=np.zeros((480,512,4),dtype=np.uint8);light[:,:,:3]=(255,169,58)
 light[:,:,3]=np.clip((halo*.6+core*.16)*strength,0,80).astype('uint8')
 Image.fromarray(light).save(out/f'Title_Glow_{phase}.png')
atlas=Image.new('RGBA',(256,128));cells={'blank':(0,0)};next_slot=1
def cell(key,img):
 global next_slot
 if key not in cells:
  cells[key]=((next_slot%16)*16,(next_slot//16)*16);next_slot+=1
  atlas.alpha_composite(img,cells[key])
 return cells[key]
def glyph(char,color='#f4deb0',shadow=False):
 im=Image.new('RGBA',(16,16));dr=ImageDraw.Draw(im)
 f=ImageFont.truetype(font_path,14 if char!='W' else 13)
 dr.text((8,8),char,font=f,anchor='mm',fill=color,stroke_width=1 if shadow else 0,stroke_fill='#07101e')
 return im
known={0x49:'0',0x4a:'G',0x4c:'P',0x4d:'U',0x57:'C',0x58:'W',0x59:'L',0x5a:'A',0x5b:'N',0x5c:'Y',0x5d:'R',0x5e:':',0x62:'Z',0x63:'F',0x66:'-',0x67:'K',0x68:'I',0x6b:'B',0x6c:'Y',0x73:'R',0x80:'M',0x81:'E',0x82:'T',0x83:'I'}
known.update({0x86+i:str(i) for i in range(1,10)})
rules=[]
hud_rules=[]
scope='gameplay&entranceLowerA&entranceLowerB&entrancePillar&litPalette'
for t,char in known.items():
 x,y=cell('glyph_'+char,glyph(char));rules.append(f'[pauseScreen]<tile>21,{0x900+t:04X},0F072830,{x},{y},1,N')
# Clear the original ornamental frame and empty background tile only. Unknown
# inventory/spell tiles retain their original mapping and behavior.
border={0,0x44,0x45,0x46,0x47,0x48,0x4b,0x4e,0x4f,0x50,0x51,0x52,0x53,0x54,0x55,0x56,0x5f,0x60,0x61,0x69,0x6a,0x6d,0x6e,0x6f,0x70,0x71,0x72,0x74,0x75,0x76,0x77,0x78,0x79,0x7a,0x7b,0x7c,0x7d,0x7e,0x7f,0x84,0x85,0x86}
for t in sorted(border):rules.append(f'[pauseScreen]<tile>21,{0x900+t:04X},0F072830,0,0,1,N')
# Pause HUD and life digits remain driven by the original sprite engine.
for t,char in {0x50:'L',0x54:'M',0x55:'-',**{0x56+i:str(i) for i in range(10)}}.items():
 x,y=cell('hud_'+char,glyph(char,'#d9eafa'))
 for bank in [0,8]:rules.append(f'[pauseScreen]<tile>21,{bank*256+t:04X},FF301116,{x},{y},1,N')
 x,y=cell('game_hud_'+char,glyph(char,'#d9eafa',shadow=True))
 hud_rules.append(f'[{scope}]<tile>21,{t:04X},FF301116,{x},{y},1,N')
for t,amount,label in [(0x51,1,'life_bar'),(0x52,.5,'life_half'),(0x53,0,'life_empty')]:
 heart=Image.new('RGBA',(16,16));h=ImageDraw.Draw(heart)
 h.rounded_rectangle((1,3,14,12),radius=2,fill='#151e30',outline='#ecd59b')
 if amount:
  right=12 if amount==1 else 7
  h.rectangle((3,5,right,10),fill='#a92538');h.line((3,5,right,5),fill='#ee6972')
 # Preserve the previously approved full-pip artwork exactly.
 if amount==1:
  h.rounded_rectangle((1,3,14,12),radius=2,fill='#a92538',outline='#ecd59b');h.line((3,5,12,5),fill='#ee6972')
 x,y=cell(label,heart)
 for bank in [0,8]:rules.append(f'[pauseScreen]<tile>21,{bank*256+t:04X},FF301116,{x},{y},1,N')
 shaded=Image.new('RGBA',(16,16));sd=ImageDraw.Draw(shaded)
 sd.rounded_rectangle((0,2,15,13),radius=3,fill='#07101e')
 shaded.alpha_composite(heart)
 x,y=cell('game_'+label,shaded)
 hud_rules.append(f'[{scope}]<tile>21,{t:04X},FF301116,{x},{y},1,N')
cursor=Image.new('RGBA',(16,16));c=ImageDraw.Draw(cursor)
c.polygon([(8,1),(14,8),(8,14),(2,8)],fill='#71d9fa',outline='#fff1c7');c.polygon([(8,4),(11,8),(8,11),(5,8)],fill='#1f72b6')
x,y=cell('equipped_marker',cursor)
for bank in [0,8]:rules.append(f'[pauseScreen]<tile>21,{bank*256+0x48:04X},FF301116,{x},{y},1,N')
for t in [0x1eee,0x1eef]:rules.append(f'[titleScreen]<tile>21,{t:04X},FF112130,0,0,1,N')
atlas.save(art/'Screen_UI_2x.png');atlas.save(out/'Screen_UI_2x.png')
conditions=[
 '<condition>pauseScreen,ppuMemoryCheckConstant,20E3,==,86',
 '<condition>pauseMagicRow,ppuMemoryCheckConstant,212F,==,82',
 '<condition>pausedPalette,ppuMemoryCheckConstant,3F11,==,0F',
 '<condition>titleScreen,ppuMemoryCheckConstant,2084,==,40',
 '<condition>titleLogoB,ppuMemoryCheckConstant,20A4,==,43',
]
conditions += [f'<condition>titleGlowPhase{i},frameRange,96,{i*12}' for i in range(1,8)]
# All pause tile rules also require the measured menu/palette signature.
rules=[r.replace('[pauseScreen]','[pauseScreen&pauseMagicRow&pausedPalette]').replace('[titleScreen]','[titleScreen&titleLogoB]') for r in rules]+hud_rules
backgrounds=['[pauseScreen&pauseMagicRow&pausedPalette]<background>Pause_HD.png,1,0,0,10,0,0',
 '[titleScreen&titleLogoB]<background>Title_HD.png,1,0,0,30,0,0']
for phase,asset in enumerate([0,1,2,3,2,1,2,1]):
 cond='titleScreen&titleLogoB'
 if phase:cond+=f'&titleGlowPhase{phase}'
 if phase<7:cond+=f'&!titleGlowPhase{phase+1}'
 backgrounds.append(f'[{cond}]<background>Title_Glow_{asset}.png,1,0,0,31,0,0')
base=(out/'hires.txt').read_text();pos=base.index('#Chr_00_0.png')
base=base[:pos]+'<img>Screen_UI_2x.png\n'+'\n'.join(conditions+rules+backgrounds)+'\n'+base[pos:]
(out/'hires.txt').write_text(base)
(art/'screen_ui_cells.json').write_text(json.dumps(cells,indent=2))
