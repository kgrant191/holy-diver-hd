"""Validate pack references, conditional ordering, tile bounds and unchanged scope."""
from pathlib import Path
from PIL import Image
import numpy as np
import sys,re,json,hashlib
pack=Path(sys.argv[1]);content=(pack/'hires.txt').read_text();lines=content.splitlines();imgs=[];sizes={};conditions={'hmirror','vmirror','bgpriority'};counts={'tile':0,'background':0,'condition':0}
sha='FE2FCD0AD334D792DB16535D09F3AB9FB2BEA3AC'
if len(sys.argv)>2:assert hashlib.sha1(Path(sys.argv[2]).read_bytes()).hexdigest().upper()==sha
assert '<supportedRom>'+sha in lines
assert '<scale>2' in lines
for line in lines:
 m=re.match(r'(?:\[([^]]+)\])?<([^>]+)>(.*)',line)
 if not m:continue
 prefix,tag,value=m.groups()
 if prefix:assert all(n.lstrip('!') in conditions for n in prefix.split('&')),line
 assert tag not in {'bgm','sfx','album','bgmloop'},tag
 if tag=='patch':
  assert value=='Entrance_SFX_Priority.ips,'+sha
  patch=(pack/'Entrance_SFX_Priority.ips').read_bytes()
  manifest=json.loads((Path(__file__).resolve().parents[1]/'audio_priority_patch.json').read_text())
  expected=bytearray(b'PATCH')
  for e in manifest['edits']:
   data=bytes.fromhex(e['after_hex']);expected+=int(e['file_offset_hex'],16).to_bytes(3,'big')+len(data).to_bytes(2,'big')+data
  expected+=b'EOF';assert patch==expected
 if tag=='condition':
  name=value.split(',')[0];assert name not in conditions;conditions.add(name);counts[tag]+=1
 if tag=='img':
  assert value not in imgs;imgs.append(value);assert(pack/value).is_file();sizes[value]=Image.open(pack/value).size
 if tag=='background':assert(pack/value.split(',')[0]).is_file();counts[tag]+=1
 if tag=='tile':
  p=value.split(',');idx=int(p[0]);x=int(p[3]);y=int(p[4]);assert 0<=idx<len(imgs);w,h=sizes[imgs[idx]]
  assert x>=0 and y>=0 and x+16<=w and y+16<=h,line
  counts[tag]+=1
assert len(imgs)==32
assert counts['tile']==5063
assert counts['background']==54
assert counts['condition']==1362
# Preserve approved assets outside the requested title/ledge, arm and crouch repairs.
root=Path(__file__).resolve().parents[1]
baseline=root/'rollback/approved_v15'
arm_atlases={'Randy_Entrance_2x.png','Randy_Equipped_2x.png'}
repaired_backgrounds={'Title_HD.png','Title_Intro_HD.png','EntranceScene.png'}
for p in baseline.glob('*.png'):
 if p.name in repaired_backgrounds:
  before=np.array(Image.open(p).convert('RGBA'));after=np.array(Image.open(pack/p.name).convert('RGBA'))
  assert before.shape==after.shape,p.name
  allowed=np.zeros(before.shape[:2],dtype=bool)
  if p.name.startswith('Title_'):allowed[390:452,100:412]=True
  else:
   allowed[192:236,0:128]=True
   allowed[544:588,0:160]=True
  assert np.any(before!=after),p.name+' repair missing'
  assert not np.any(np.any(before!=after,axis=2)&~allowed),p.name+' changed outside repair'
 elif p.name not in arm_atlases:assert p.read_bytes()==(pack/p.name).read_bytes(),p.name
 else:
  expected=Image.open(p).convert('RGBA')
  patch=Image.open(root/'art/randy_arm_patch.png').convert('RGBA')
  for pose,(x,y) in json.loads((root/'art/arm_repair.json').read_text())['pose_positions'].items():
   i=int(pose);expected.alpha_composite(patch,(i%4*64+x,i//4*64+y))
  mode=0 if p.name=='Randy_Entrance_2x.png' else 1
  for phase in range(2):
   sprite=Image.open(root/f'art/review_fixes/randy_{mode}_{phase}.png').convert('RGBA')
   expected.paste(sprite,((phase+2)*64,128))
  foot=json.loads((root/'art/randy_foot/registration.json').read_text())
  assert foot['target_pose']==0 and foot['target_rectangle']==[16,32,32,64]
  boot=Image.open(root/'art/randy_foot'/foot['patches'][p.name]).convert('RGBA')
  assert boot.size==(16,32)
  expected.paste(boot,(16,32))
  assert np.array_equal(np.array(expected),np.array(Image.open(pack/p.name).convert('RGBA'))),p.name
# Both additions own marked sections. Removing these must recover the exact
# approved mapping file, including ordering and whitespace.
approved_rules=re.sub(r'^# BEGIN RECOVERY_ITEMS (IMAGES|MAPPINGS)\n.*?^# END RECOVERY_ITEMS \1\n','',content,flags=re.M|re.S)
approved_rules=re.sub(r'^# BEGIN BOSS1 (IMAGES|CONDITIONS|MAPPINGS|ALIASES|OPTIONS)\n.*?^# END BOSS1 \1\n','',approved_rules,flags=re.M|re.S)
approved_rules=re.sub(r'^# BEGIN STANDING_LEG CONDITIONS\n.*?^# END STANDING_LEG CONDITIONS\n','',approved_rules,flags=re.M|re.S)
approved_rules=approved_rules.replace('[standingLegNormal]<tile>18,07,','[randySig8]<tile>18,07,').replace('[standingLegTwin]<tile>19,07,','[randyEquippedSig8]<tile>19,07,')
approved_021=json.loads((root/'evidence/0.2.1-pack-sha256.json').read_text())
assert hashlib.sha256(approved_rules.encode()).hexdigest()==approved_021['hires.txt']
for name,digest in approved_021.items():
 if name not in {'README.txt','hires.txt'}|arm_atlases:
  assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' approved 0.2.1 bytes changed'
boss=json.loads((root/'art/boss1/registration.json').read_text())
assert boss['tile_rules']==2433 and boss['conditions']==1083 and boss['background_rules']==4
assert boss['shared_bank_aliases']==758 and not boss['collision_modified'] and not boss['existing_rules_modified']
assert boss['global_sprite_limit_changed']
assert [line for line in lines if line.startswith('<options>')]==['<options>disableSpriteLimit']
assert '<addition>' not in content
assert boss['menu_glyphs']=={'0964':'R','0965':'D'}
assert boss['pre_announcement_fade']=={'FF202020':255,'FF101010':173,'FF000000':102}
wall=np.array(Image.open(pack/'Nave_Background.png').convert('RGB'))
ascent=np.array(Image.open(pack/'Blizzard_Ascent_Background.png').convert('RGB'))
assert ascent.shape==(wall.shape[0]*3,wall.shape[1],3)
assert all(np.array_equal(ascent[i*wall.shape[0]:(i+1)*wall.shape[0]],wall) for i in range(3))
for identity in boss['menu_glyphs']:
 assert sum(f'[pauseScreen&pauseMagicRow&pausedPalette]<tile>30,{identity},0F072830,' in line for line in lines)==1
assert imgs[30]=='Boss_Tiles_2x.png'
assert imgs[31]=='Recovery_Items_2x.png'
prior=json.loads((root/'evidence/0.3.4-pack-sha256.json').read_text())
for name,digest in prior.items():
 if name not in {'README.txt','hires.txt'}:
  assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' confirmed 0.3.4 art changed'
without_items=re.sub(r'^# BEGIN RECOVERY_ITEMS (IMAGES|MAPPINGS)\n.*?^# END RECOVERY_ITEMS \1\n','',content,flags=re.M|re.S)
assert hashlib.sha256(without_items.encode()).hexdigest()==prior['hires.txt']
items=json.loads((root/'art/pickups/registration.json').read_text())
assert items['tile_rules']==64 and not items['native_geometry_changed'] and not items['existing_rules_modified']
item_atlas=Image.open(pack/'Recovery_Items_2x.png').convert('RGBA')
assert item_atlas.size==(32,32)
assert not np.any(np.array(item_atlas)[:8,:,3])
for i,name in enumerate(['hp','magic']):
 assert np.array_equal(np.array(item_atlas)[:,i*16:(i+1)*16],np.array(Image.open(root/f'art/pickups/{name}_flask.png').convert('RGBA')))
previous_rules=re.sub(r'^# BEGIN SCREEN1_4 (IMAGES|CONDITIONS|MAPPINGS)\n.*?^# END SCREEN1_4 \1\n','',approved_rules,flags=re.M|re.S)
approved_011=json.loads((root/'evidence/0.1.1-pack-sha256.json').read_text())
assert hashlib.sha256(previous_rules.encode()).hexdigest()==approved_011['hires.txt']
for name,digest in approved_011.items():
 if name not in {'README.txt','hires.txt'}|arm_atlases:
  assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' approved 0.1.1 bytes changed'
tree=json.loads((root/'art/screen1_4/registration.json').read_text())
assert tree['tile_rules']==198 and tree['new_atlas_cells']==150 and tree['shared_enemy_rules']==48
assert tree['conditions']==4 and tree['background_rules']==1
assert not tree['collision_modified'] and not tree['existing_rules_modified']
assert content.count('['+tree['scope']+']<tile>29,')==150
original_rules=re.sub(r'^# BEGIN REVIEW_FIXES (CONDITIONS|MAPPINGS)\n.*?^# END REVIEW_FIXES \1\n','',previous_rules,flags=re.M|re.S)
original_rules=re.sub(r'^# BEGIN SCREEN1_3 (IMAGES|CONDITIONS|MAPPINGS)\n.*?^# END SCREEN1_3 \1\n','',original_rules,flags=re.M|re.S)
assert original_rules.encode()==(baseline/'hires.txt').read_bytes()
approved_002=json.loads((root/'evidence/0.0.2-pack-sha256.json').read_text())
for name,digest in approved_002.items():
 if name not in {'README.txt','hires.txt'}|arm_atlases:
  assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' approved 0.0.2 bytes changed'
assert imgs[28]=='Nave_Tiles_2x.png' and imgs[29]=='Tree_Court_Tiles_2x.png'
nave=json.loads((root/'art/screen1_3/registration.json').read_text())
assert nave['tile_rules']==87 and nave['conditions']==3 and nave['background_rules']==1
assert not nave['collision_modified'] and not nave['existing_rules_modified']
assert content.count('['+nave['scope']+']<tile>28,')==87
# The old 87 atlas cells (including every rolling frame) remain byte-identical
# at the pixel level; only twelve previously empty standing cells are added.
before=np.array(Image.open(root/'art/screen1_3/Nave_Tiles_2x.png').convert('RGBA'))
after=np.array(Image.open(pack/'Nave_Tiles_2x.png').convert('RGBA'))
allowed=np.zeros(before.shape[:2],dtype=bool)
for slot in range(87,99):
 x,y=slot%16*16,slot//16*16;allowed[y:y+16,x:x+16]=True
assert not np.any(np.any(before!=after,axis=2)&~allowed)
repairs=json.loads((root/'art/review_fixes/registration.json').read_text())
assert repairs['tile_rules']==50 and repairs['conditions']==66
assert repairs['rolling_pixels_changed']==0 and repairs['existing_pose_pixels_changed']==0
assert (baseline/'Entrance_SFX_Priority.ips').read_bytes()==(pack/'Entrance_SFX_Priority.ips').read_bytes()
# Conditional pose rules must precede any corresponding ordinary mappings.
first_unconditional={}
for index,line in enumerate(lines):
 m=re.match(r'(?:\[([^]]+)\])?<tile>(.*)',line)
 if not m:continue
 prefix,v=m.groups();p=v.split(',');key=(p[1],p[2])
 if prefix:assert key not in first_unconditional,line
 else:first_unconditional[key]=index
assert len(re.findall(r'^<tile>27,[0-9A-F]{2}(?:6[4-9A-F]|7[0-3]),FF301116,',content,re.M))==256
assert not re.search(r'<tile>25,(?:6[C-F]|7[0-3]),FF301116,',content)
assert content.count('<patch>')==1
assert len(re.findall(r'\[pauseScreen&pauseMagicRow&pausedPalette\]<tile>26,097[5-8],0F172737,',content))==4
for asset in (Path(__file__).resolve().parents[1]/'rollback/bracelet_v14').glob('*.png'):
 if asset.name not in arm_atlases|repaired_backgrounds:assert asset.read_bytes()==(pack/asset.name).read_bytes(),asset.name
assert 'cryptBatPhase' not in content
assert len(re.findall(r'<tile>26,7[4-7],FF160636,',content))==4
assert len(re.findall(r'\[randyDefeated\]<tile>',approved_rules))==64
assert len(re.findall(r'\[randyDefeated\]<tile>',content))==192
assert '<condition>randyDefeated,memoryCheckConstant,0440,==,00' in content
assert not re.search(r'<tile>25,7[4-7],FF160636,',content)
result={'supported_rom_sha1':sha.lower(),'scale':2,'atlas_count':len(imgs),**counts,'references_and_bounds_valid':True,'conditional_priority_valid':True,'rom_patch_bytes':56,'patch_scope':'entrance priorities and conditional thunder masking','replacement_audio':False}
print(json.dumps(result,indent=2))
