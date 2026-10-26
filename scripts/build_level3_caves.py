"""Continue the four recorded Level 3 caves with approved terrain materials."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
r=Path(__file__).resolve().parents[1];pack=r/'build/Holy_Diver_(Tr)';art=r/'art/level3_caves'
text=(pack/'hires.txt').read_text();images=[s[5:]for s in text.splitlines()if s.startswith('<img>')];assert len(images)==44
atlas=Image.new('RGBA',(512,256));cache={};rules=[];conditions=[];backgrounds=[];records=[]
patterns={int(k,16):bytes.fromhex(v)for k,v in json.loads((art/'native_patterns.json').read_text()).items()}
observed=json.loads((art/'observed_backgrounds.json').read_text())
def reg(im,size):
 im=im.convert('RGBA').resize(size,Image.Resampling.LANCZOS);alpha=im.getchannel('A').point(lambda v:255 if v>=128 else 0)
 im=im.convert('RGB').quantize(colors=64).convert('RGBA');im.putalpha(alpha);return im
def add(t,pal,im,kind,scope):
 assert im.size==(16,16);key=hashlib.sha256(im.tobytes()).hexdigest()
 if key not in cache:
  n=len(cache);xy=(n%32*16,n//32*16);assert xy[1]<256;cache[key]=xy;atlas.paste(im,xy)
 x,y=cache[key];rule=('['+scope+']'if scope else '')+f'<tile>44,{t:04X},{pal},{x},{y},1,N';rules.append(rule)
 records.append(dict(tile=f'{t:04X}',palette=pal,xy=[x,y],kind=kind,scope=scope,rule=rule))
def native(t):
 b=patterns[t];return np.array([[255 if ((b[y]|b[y+8])>>(7-x))&1 else 0 for x in range(8)]for y in range(8)],dtype=np.uint8)
def hull(t):
 a=native(t)
 for y in range(8):
  xs=np.flatnonzero(a[y])
  if len(xs):a[y,xs[0]:xs[-1]+1]=255
 for x in range(8):
  ys=np.flatnonzero(a[:,x])
  if len(ys):a[ys[0]:ys[-1]+1,x]=255
 return Image.fromarray(a).resize((16,16),Image.Resampling.NEAREST)
base=json.loads((r/'art/level3_lava/registration.json').read_text());old=Image.open(pack/'Stage3_Lava_Tiles_2x.png').convert('RGBA')
basecells={}
for m in base['mappings']:
 if m['scope'].startswith('l3lavaRoom'):
  x,y=m['xy'];basecells[int(m['tile'],16),m['palette']]=old.crop((x,y,x+16,y+16))
empty=Image.new('RGBA',(16,16));body=Image.new('RGBA',(32,32))
for i,t in enumerate([0x744,0x745,0x746,0x747]):body.paste(basecells[t,'0F0A1A29'],(i%2*16,i//2*16))
raw=Image.open(r/'art/generated/screen2_5_stair_tread_generated.png').convert('RGBA');raw=raw.crop(raw.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox());step=reg(raw,(32,32))
solidcap={0x77f:(0,0),0x77e:(1,0),0x77d:(0,1),0x77c:(1,1)}
room_modes={'9B96':0x10,'9C86':0x04,'9CFE':0x10,'9DEE':0x14}
terrain_masks={}
for room,pals in observed.items():
 ptr=int(room,16);name='l3c'+room
 for suffix,addr,val in [('Mode',0x72,room_modes[room]),('Lo',0x78,ptr&255),('Hi',0x79,ptr>>8)]:conditions.append(f'<condition>{name}{suffix},memoryCheckConstant,{addr:04X},==,{val:02X}')
 scope=f'{name}Mode&{name}Lo&{name}Hi'
 # Only visible palette states are registered. Exact tile/palette guards keep
 # blank room changes and the native menu from revealing the panorama early.
 for pi,(pal,ts)in enumerate(pals.items()):
  for t in sorted(set(ts)|{0x700}):
   if 0x73e<=t<=0x743:
    alias=next((m for m in base['lava_aliases']if int(m['tile'],16)==t and m['palette']==pal),None)
    if alias:
     f=alias['source_rule'].split('<tile>')[1].split(',');f[1]=f'{t:04X}';rules.append('['+scope+']<tile>'+','.join(f));records.append(dict(tile=f'{t:04X}',palette=pal,scope=scope,kind='approved lava/ice',rule=rules[-1]));continue
   if t==0x700 or (t in [0x78c,0x78d]and pal in ['0F0F0A1A','0F0A1A29','0F1B2B3B'])or(t in[0x796,0x797]and room=='9C86'and pal=='0F0F0A1A'):
    im=empty;kind='nonsolid cave backdrop'
   elif t in solidcap:
    x,y=solidcap[t];im=step.crop((x*16,y*16,x*16+16,y*16+16));im.putalpha(hull(t));kind='approved carved stone / native block cap'
   elif 0x774<=t<=0x77b:
    im=body.crop((t%2*16,(t//2)%2*16,t%2*16+16,(t//2)%2*16+16));im.putalpha(hull(t));kind='approved brown stone / native ledge contour'
   else:
    sourcepal='0F071727'if pal in ['0F071727','0F081737','0F072830']else '0F0A1A29'
    im=basecells.get((t,sourcepal))
    if im is None:
     # Unrendered cells retained in the second nametable can contain earlier
     # tree/forest data; do not invent scenery for those stale identities.
     continue
    kind='approved corridor terrain'
   for q in [im]:terrain_masks[f'{room}/{t:04X}/{pal}']=np.array(q.getchannel('A')).tolist()
   add(t,pal,im,kind,scope)
  # Guards at the HUD-side row are the actual rendered native background.
  for t in sorted(set(ts)|{0x700}):
   guard=f'{name}View{pi}_{t:04X}';conditions.append(f'<condition>{guard},tileAtPosition,128,16,{t:04X},{pal}')
   background='Stage2_Cave_Background.png';sx=1 if room in ['9B96','9CFE']else 0
   backgrounds.append(f'[{scope}&{guard}]<background>{background},1,{sx},0,11,0,0')
# One complete painted sprite, preserving the native absent cells and facing.
raw=Image.open(r/'art/generated/level3_green_creature_generated.png').convert('RGBA');raw=raw.crop(raw.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox())
creature=Image.new('RGBA',(64,64));creature.paste(reg(raw,(62,62)),(1,1));a=np.array(creature);assert not a[:16,:48,3].any()and not a[48:,48:,3].any()
rows=[[None,None,None,0x6d1],[0x6d2,0x6d3,0x6d4,0x6d5],[0x6d6,0x6d7,0x6d8,0x6d9],[0x6da,0x6db,0x6dc,None]]
for y,row in enumerate(rows):
 for x,t in enumerate(row):
  if t:add(t,'FF371908',creature.crop((x*16,y*16,x*16+16,y*16+16)),'green floating creature','')
creature.save(art/'green_creature.png')
def block(part,items):return '# BEGIN LEVEL3_CAVES '+part+'\n'+'\n'.join(items)+'\n# END LEVEL3_CAVES '+part+'\n'
end=text.index('\n',text.rfind('<img>'))+1;text=text[:end]+block('IMAGES',['<img>Stage3_Caves_Tiles_2x.png'])+text[end:]
lines=text.splitlines(keepends=True);first=next(i for i,l in enumerate(lines)if '<tile>'in l or '<background>'in l);lines[first:first]=[block('CONDITIONS',conditions),block('MAPPINGS',rules+backgrounds)]
(pack/'hires.txt').write_text(''.join(lines));atlas.save(pack/'Stage3_Caves_Tiles_2x.png');atlas.save(art/'Stage3_Caves_Tiles_2x.png')
(art/'registration.json').write_text(json.dumps(dict(tile_rules=len(rules),conditions=len(conditions),background_rules=len(backgrounds),rooms=room_modes,mappings=records,terrain_masks=terrain_masks,creature_rows=rows,atlas_cells=len(cache),native_gameplay_modified=False),indent=2)+'\n')
print('Level 3 caves:',len(rules),'tile rules; four recorded rooms; approved materials and one new creature.')
