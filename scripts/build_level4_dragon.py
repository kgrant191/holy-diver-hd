"""Dragon form, visible pickups and scoped decorative-column removal."""
from pathlib import Path
import hashlib,json,re
from PIL import Image
from prepare_player_dragon import prepare
r=Path(__file__).resolve().parents[1];p=r/'build/Holy_Diver_(Tr)';a=r/'art/level4_dragon'
text=(p/'hires.txt').read_text();prior=json.loads((r/'evidence/0.18.0-pack-sha256.json').read_text())
assert hashlib.sha256(text.encode()).hexdigest()==prior['hires.txt']
images=[l[5:]for l in text.splitlines()if l.startswith('<img>')];assert len(images)==52
old=json.loads((r/'art/level4_staff/registration.json').read_text());court=json.loads((r/'art/level4_courtyard/registration.json').read_text());temple=json.loads((r/'art/level4/registration.json').read_text())
aliases=json.loads((a/'native_aliases.json').read_text());patterns=json.loads((a/'native_patterns.json').read_text())
defs={l[11:].split(',')[0]:l for l in text.splitlines()if l.startswith('<condition>')}
atlas=Image.new('RGBA',(512,512));cache={};rules=[];records=[];conditions=[];clones=[];removed=[]
arena=old['scopes']['ACD9']
def tile(key,pal,im,kind,scope=''):
 assert im.size==(16,16)
 digest=hashlib.sha256(im.tobytes()).hexdigest()
 if digest not in cache:
  i=len(cache);xy=(i%32*16,i//32*16);assert xy[1]<512;cache[digest]=xy;atlas.paste(im,xy)
 x,y=cache[digest];line=('['+scope+']'if scope else '')+f'<tile>52,{key},{pal},{x},{y},1,N'
 rules.append(line);records.append(dict(tile=key,palette=pal,xy=[x,y],scope=scope,kind=kind,rule=line));return line

def reg(raw,size):
 raw=raw.convert('RGBA');box=raw.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox();raw=raw.crop(box).resize(size,Image.Resampling.LANCZOS)
 alpha=raw.getchannel('A').point(lambda v:255 if v>=128 else 0);raw=raw.convert('RGB').quantize(colors=128).convert('RGBA');raw.putalpha(alpha);return raw

def aliased(key,pal,im,kind,scope=''):
 for target in aliases[key]:
  assert patterns[key]==patterns[target]
  tile(target,pal,im,kind,scope)

# Follow only identified decorative column rules, including their later clones.
seeds={m['rule']for m in temple['mappings']if m['kind']=='outdoor gold column'}
seeds|={m['rule']for m in court['mappings']if m['kind']=='approved outdoor capital'}
for layer in [court,old]:
 for m in layer['clones']:
  if m['source_rule']in seeds:seeds.add(m['rule'])
empty=Image.new('RGBA',(16,16))
for line in text.splitlines():
 if line not in seeds:continue
 scope,fields=line[1:].split(']<tile>');fields=fields.split(',')
 assert int(fields[1],16)&255 not in range(0x78,0x88)
 new=tile(fields[1],fields[2],empty,'decorative column reveal',scope)
 removed.append(dict(source_rule=line,rule=new))
 if fields[1].startswith('0D'):
  # These column scopes have no neighbor probes; retain the native pickup flash.
  assert all(',tileNearby,'not in defs.get(t.lstrip('!'),'')for t in scope.split('&'))
  tile(fields[1],'31'+fields[2][2:],empty,'flash decorative column reveal',scope)

# Strong ivory silhouette and emerald crown, shared by pickup and menu.
staff=Image.new('RGBA',(16,32));staff.paste(reg(Image.open(r/'art/generated/temple_staff_visible.png'),(14,30)),(1,1));staff.save(a/'staff.png')
for i,key in enumerate(['0A95','0A96']):aliased(key,'FF26173A',staff.crop((0,i*16,16,i*16+16)),'visible staff')
menu=Image.new('RGBA',(32,32));menu.paste(staff,(8,0));menu.save(a/'staff_menu.png')
for y,row in enumerate([['096A','0969'],['0968','0956']]):
 for x,key in enumerate(row):
  scope=next(m['scope']for m in old['mappings']if m['kind']=='same staff in Start menu'and m['tile']==key)
  tile(key,'0F172737',menu.crop((x*16,y*16,x*16+16,y*16+16)),'visible staff menu',scope)
raw=Image.open(r/'art/generated/temple_drops_visible.png').convert('RGBA');w,h=raw.size
for i,(key,name)in enumerate([('0A47','heart'),('0A48','magic')]):
 im=Image.new('RGBA',(16,16));im.paste(reg(raw.crop((i*w//2,0,(i+1)*w//2,h)),(14,14)),(1,1));im.save(a/(name+'.png'))
 for scope in {**temple['scopes'],**court['scopes'],**old['scopes']}.values():aliased(key,'FF301116',im,'visible '+name,scope)
item=Image.new('RGBA',(32,32));item.paste(reg(Image.open(r/'art/generated/dragon_pickup.png'),(30,30)),(1,1));item.save(a/'dragon_pickup.png')
for y,row in enumerate([['0CB1','0CB2'],['0CB3','0CB4']]):
 for x,key in enumerate(row):aliased(key,'FF301116',item.crop((x*16,y*16,x*16+16,y*16+16)),'dragon pickup')
poses,fit=prepare(r);layouts=json.loads((a/'native_dragon_layouts.json').read_text());seen={}
for im,layout in zip(poses,layouts):
 for key,x,y in layout['layout']:
  part=im.crop((x*2,y*2,x*2+16,y*2+16))
  if key in seen:assert seen[key]==part.tobytes();continue
  seen[key]=part.tobytes();aliased(key,'FF190927',part,'dragon native animation')
shot=reg(Image.open(r/'art/boss1/boss_fireball_registered.png'),(16,16));shot.save(a/'dragon_shot.png');aliased('0CB0','FF301116',shot,'dragon fire')
star=reg(Image.open(p/'Death_Bursts_2x.png').crop((0,0,64,64)),(16,16));star.save(a/'transform_star.png')
conditions.append('<condition>dragonTransform,memoryCheckConstant,0300,==,23')
aliased('0C74','FF301116',star,'native transformation twinkle',arena+'&dragonTransform')

# Full-room native 31 flash remains pale blue; retain HD masonry during it.
# No panorama is added for this palette. Bounds stay before every neighbor read.
renames={}
flash_source=[m['rule']for m in old['clones']if m['kind']=='outdoor scenery reuse']
for line in flash_source:
 for term in line[1:].split(']')[0].split('&'):
  name=term.lstrip('!');fields=defs[name][11:].split(',')
  if fields[1]=='tileNearby'and fields[5].startswith('0F')and name not in renames:
   new='dragonFlash_'+name;renames[name]=new;fields[0]=new;fields[5]='31'+fields[5][2:];conditions.append('<condition>'+','.join(fields))
for line in flash_source:
 head,tail=line[1:].split(']<tile>');fields=tail.split(',')
 if not fields[2].startswith('0F'):continue
 terms=[('!'if t.startswith('!')else '')+renames.get(t.lstrip('!'),t.lstrip('!'))for t in head.split('&')]
 fields[2]='31'+fields[2][2:];new='['+'&'.join(terms)+']<tile>'+','.join(fields);rules.append(new);clones.append(dict(source_rule=line,rule=new,kind='native pickup flash foreground'))

def block(name,lines):return '# BEGIN TEMPLE_DRAGON '+name+'\n'+'\n'.join(lines)+'\n# END TEMPLE_DRAGON '+name+'\n'
end=text.index('\n',text.rfind('<img>'))+1;text=text[:end]+block('IMAGES',['<img>Golden_Temple_Dragon_2x.png'])+text[end:]
marker='# BEGIN TEMPLE_STAFF MAPPINGS';text=text.replace(marker,block('CONDITIONS',conditions)+block('MAPPINGS',rules)+marker)
(p/'hires.txt').write_text(text);atlas.save(p/'Golden_Temple_Dragon_2x.png')
(a/'registration.json').write_text(json.dumps(dict(tile_rules=len(rules),conditions=len(conditions),background_rules=0,mappings=records,clones=clones,removed=removed,dragon_fit=fit,atlas_cells=len(cache),native_gameplay_modified=False,prior_artwork_modified=False),indent=2)+'\n')
print('Dragon/items:',len(rules),'tile rules;',len(removed),'decorative column rules;',len(cache),'atlas cells')
