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
assert len(imgs)==29
assert counts['tile']==2318
assert counts['background']==49
assert counts['condition']==207
# Preserve approved assets outside the explicitly requested title/ledge repairs.
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
  assert np.array_equal(np.array(expected),np.array(Image.open(pack/p.name).convert('RGBA'))),p.name
# Screen 1-3 is strictly additive. Removing its three owned sections must
# recover the exact approved mapping file, including ordering and whitespace.
original_rules=re.sub(r'^# BEGIN SCREEN1_3 (IMAGES|CONDITIONS|MAPPINGS)\n.*?^# END SCREEN1_3 \1\n','',content,flags=re.M|re.S)
assert original_rules.encode()==(baseline/'hires.txt').read_bytes()
approved_002=json.loads((root/'evidence/0.0.2-pack-sha256.json').read_text())
for name,digest in approved_002.items():
 if name not in {'README.txt','hires.txt'}:
  assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' approved 0.0.2 bytes changed'
assert imgs[-1]=='Nave_Tiles_2x.png'
nave=json.loads((root/'art/screen1_3/registration.json').read_text())
assert nave['tile_rules']==87 and nave['conditions']==3 and nave['background_rules']==1
assert not nave['collision_modified'] and not nave['existing_rules_modified']
assert content.count('['+nave['scope']+']<tile>28,')==87
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
assert len(re.findall(r'\[randyDefeated\]<tile>',content))==64
assert '<condition>randyDefeated,memoryCheckConstant,0440,==,00' in content
assert not re.search(r'<tile>25,7[4-7],FF160636,',content)
result={'supported_rom_sha1':sha.lower(),'scale':2,'atlas_count':len(imgs),**counts,'references_and_bounds_valid':True,'conditional_priority_valid':True,'rom_patch_bytes':56,'patch_scope':'entrance priorities and conditional thunder masking','replacement_audio':False}
print(json.dumps(result,indent=2))
