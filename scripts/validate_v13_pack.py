"""Validate pack references, conditional ordering, tile bounds and unchanged scope."""
from pathlib import Path
from PIL import Image
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
assert len(imgs)==26
assert counts['tile']==1565
assert counts['background']==20
assert counts['condition']==162
# The approved entrance/title assets and its exact audio patch are retained.
baseline=Path(__file__).resolve().parents[1]/'rollback/entrance_v12'
for p in baseline.glob('*.png'):assert p.read_bytes()==(pack/p.name).read_bytes(),p.name
assert (baseline/'Entrance_SFX_Priority.ips').read_bytes()==(pack/'Entrance_SFX_Priority.ips').read_bytes()
# Conditional pose rules must precede any corresponding ordinary mappings.
first_unconditional={}
for index,line in enumerate(lines):
 m=re.match(r'(?:\[([^]]+)\])?<tile>(.*)',line)
 if not m:continue
 prefix,v=m.groups();p=v.split(',');key=(p[1],p[2])
 if prefix:assert key not in first_unconditional,line
 else:first_unconditional[key]=index
assert content.count('<patch>')==1
result={'supported_rom_sha1':sha.lower(),'scale':2,'atlas_count':len(imgs),**counts,'references_and_bounds_valid':True,'conditional_priority_valid':True,'rom_patch_bytes':56,'patch_scope':'entrance priorities and conditional thunder masking','replacement_audio':False}
print(json.dumps(result,indent=2))
