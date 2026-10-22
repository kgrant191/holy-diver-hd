"""Shared two-phase defeat effect and native-data-driven intermission presentation."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,re,shutil
root=Path(__file__).resolve().parents[1];art=root/'art';pack=root/'build/Holy_Diver_(Tr)';seed=root/'rollback/approved_v14_1'
shutil.copytree(seed,pack,dirs_exist_ok=True);s=(pack/'hires.txt').read_text();lines=s.splitlines()
lines=[l for l in lines if not re.search(r'<tile>25,(6[C-F]|7[0-3]),FF301116,',l)]
assert sum(l.startswith('<img>')for l in lines)==27
pos=max(i for i,l in enumerate(lines)if l.startswith('<img>'))+1;lines.insert(pos,'<img>Death_Bursts_2x.png')
# Register each generated ring into its actual native sparse sprite layout.
source=Image.open(art/'generated/death_rings_generated.png').convert('RGBA');atlas=Image.new('RGBA',(128,64));effect_rules=[];effect_meta=[]
layouts=[[(0x64,0,0),(0x65,8,0),(0x66,16,0),(0x67,0,8),(0x68,16,8),(0x69,0,16),(0x6a,8,16),(0x6b,16,16)],[(0x6c,8,0),(0x6d,16,0),(0x6e,0,8),(0x6f,24,8),(0x70,0,16),(0x71,24,16),(0x72,8,24),(0x73,16,24)]]
for phase,size in [(0,48),(1,64)]:
 im=source.crop((phase*source.width//2,0,(phase+1)*source.width//2,source.height));im=im.crop(im.getchannel('A').point(lambda a:255 if a>=120 else 0).getbbox()).resize((size,size),Image.Resampling.LANCZOS)
 alpha=im.getchannel('A').point(lambda a:255 if a>=125 else 0);im=im.convert('RGB').quantize(colors=40,method=Image.Quantize.MEDIANCUT).convert('RGBA');im.putalpha(alpha)
 registered=Image.new('RGBA',(size,size))
 for t,x,y in layouts[phase]:
  cell=im.crop((x*2,y*2,x*2+16,y*2+16));registered.paste(cell,(x*2,y*2));atlas.paste(cell,(phase*64+x*2,y*2));effect_rules.append(f'<tile>27,{t:02X},FF301116,{phase*64+x*2},{y*2},1,N')
 registered.save(art/f'death_ring_{phase}_registered.png');effect_meta.append({'phase':phase,'size':[size,size],'layout':layouts[phase]})
# The supported ROM repeats these same effect bytes in every even CHR bank.
# Register each exact copy, so later rooms do not need another room-specific fix.
base_effect_rules=effect_rules;effect_rules=[]
for bank in range(0,32,2):
 for rule in base_effect_rules:
  m=re.match(r'<tile>27,([^,]+),(.*)',rule);effect_rules.append(f'<tile>27,{bank*256+int(m[1],16):04X},{m[2]}')
atlas.save(pack/'Death_Bursts_2x.png')
# The generated background remains unpainted; native-data text is a separate UI layer.
bg=Image.open(art/'generated/intermission_generated.png').convert('RGBA').resize((512,480),Image.Resampling.LANCZOS);bg.save(pack/'Intermission_HD.png')
font_path=art/'fonts/DejaVuSerif-Bold.ttf'
def font(n):return ImageFont.truetype(str(font_path),n)
def spaced(d,text,xy,face,fill,spacing=1):
 widths=[d.textlength(c,font=face)for c in text];width=sum(widths)+spacing*(len(text)-1);x=xy[0]-width/2
 for c,w in zip(text,widths):d.text((x,xy[1]),c,font=face,fill=fill,anchor='lt',stroke_width=1,stroke_fill='#020815');x+=w+spacing
stages=['CURSED CHAPEL','HELL OF ENTRAILS','POISON MOSS LAND','GOLDEN TEMPLE','DEMONIC PALACE','BLACK SLAYER']
conditions=[];rules=[];backgrounds=[]
def probe(name,address,value):conditions.append(f'<condition>{name},ppuMemoryCheckConstant,{address:04X},==,{value:02X}');return name
palette='&'.join([probe('cardPal1',0x3f01,0x21),probe('cardPal2',0x3f02,0x30),probe('cardPal3',0x3f03,0x29)])
stage_sig='&'.join([probe('stageCardS',0x214c,0x34),probe('stageCardT',0x214d,0x35),probe('stageCardA',0x214e,0x20),probe('stageCardG',0x214f,0x26),probe('stageCardE',0x2150,0x24),probe('stageRandy',0x224c,0x33)])
respawn_sig='&'.join([probe('livesR',0x21cc,0x33),probe('livesA',0x21cd,0x20),probe('livesN',0x21ce,0x2d),probe('livesD',0x21cf,0x23),probe('livesY',0x21d0,0x3a),probe('livesTimes',0x21d2,0x3f)])
conditions.append('<condition>cardRendering,memoryCheckConstant,00FE,==,08,08')
stage_scope=palette+'&cardRendering&'+stage_sig;respawn_scope=palette+'&cardRendering&'+respawn_sig
for scope in [stage_scope,respawn_scope]:
 backgrounds.append(f'[{scope}]<background>Intermission_HD.png,1,0,0,10,0,0')
 for tile in [0,*range(0x10,0x40)]:rules.append(f'[{scope}]<tile>21,{0x1f00+tile:04X},0F213029,0,0,1,N')
for i,title in enumerate(stages,1):
 im=Image.new('RGBA',(512,480));d=ImageDraw.Draw(im)
 spaced(d,f'STAGE {i}',(256,160),font(16),'#d4ab62',3)
 size=26
 while d.textlength(title,font=font(size))+len(title)-1>314:size-=1
 spaced(d,title,(256,206),font(size),'#f5ddb0',1)
 d.line((186,256,244,256),fill='#8e713d',width=1);d.line((268,256,326,256),fill='#8e713d',width=1);d.polygon([(256,252),(260,256),(256,260),(252,256)],fill='#cfaa65')
 im.save(pack/f'Stage_Title_{i}.png');condition=probe(f'stageNumber{i}',0x2152,0x11+i);backgrounds.append(f'[{stage_scope}&{condition}]<background>Stage_Title_{i}.png,1,0,0,30,0,0')
for value in range(10):
 for kind,scope,address,y in [('Stage',stage_scope,0x2254,286),('Lives',respawn_scope,0x21d4,222)]:
  im=Image.new('RGBA',(512,480));d=ImageDraw.Draw(im);spaced(d,f'RANDY × {value}',(256,y),font(23),'#f3e4c7',1)
  if kind=='Lives':
   d.line((186,266,244,266),fill='#8e713d',width=1);d.line((268,266,326,266),fill='#8e713d',width=1);d.polygon([(256,262),(260,266),(256,270),(252,266)],fill='#cfaa65')
  name=f'{kind}_Lives_{value}.png';im.save(pack/name);condition=probe(f'{kind.lower()}Lives{value}',address,0x11+value);backgrounds.append(f'[{scope}&{condition}]<background>{name},1,0,0,31,0,0')
# Reuse the exact approved gameplay HUD cells for the post-death card's CHR bank.
cells=json.loads((art/'screen_ui_cells.json').read_text())
for tile,char in {0x50:'L',0x54:'M',0x55:'-',**{0x56+i:str(i)for i in range(10)}}.items():
 x,y=cells['game_hud_'+char]
 for bank in range(0,32,2):rules.append(f'[{respawn_scope}]<tile>21,{bank*256+tile:04X},FF301116,{x},{y},1,N')
for tile,key in [(0x51,'game_life_bar'),(0x52,'game_life_half'),(0x53,'game_life_empty')]:
 x,y=cells[key]
 for bank in range(0,32,2):rules.append(f'[{respawn_scope}]<tile>21,{bank*256+tile:04X},FF301116,{x},{y},1,N')
# Conditions must precede consumers; these specific HUD rules precede global HUD.
pos=next(i for i,l in enumerate(lines)if re.search(r'<tile>',l));lines[pos:pos]=conditions+rules+effect_rules+backgrounds
(pack/'hires.txt').write_text('\n'.join(lines)+'\n')
(art/'v15_registration.json').write_text(json.dumps({'effect_phases':effect_meta,'effect_palette':'FF301116','effect_scope':'shared native CHR tiles, independent of room palette','stage_names':stages,'stage_name_source':'translated ROM text table at file offsets 0x1b3f8–0x1b4e8','lives_range':list(range(10)),'hud_source':'unchanged approved Screen_UI_2x.png gameplay cells','new_rule_count':len(rules)+len(effect_rules),'new_conditions':len(conditions),'new_background_rules':len(backgrounds)},indent=2)+'\n')
print('New rules',len(rules)+len(effect_rules),'conditions',len(conditions),'backgrounds',len(backgrounds))
