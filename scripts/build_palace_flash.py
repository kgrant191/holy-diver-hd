"""Keep existing Palace scenery HD during Thunder and dragon pickup flashes."""
from pathlib import Path
import hashlib,json,re
from PIL import Image
R=Path(__file__).resolve().parents[1];P=R/'build/Holy_Diver_(Tr)';A=R/'art/level5_flash'
text=(P/'hires.txt').read_text();prior=json.loads((R/'evidence/0.22.0-pack-sha256.json').read_text());assert hashlib.sha256(text.encode()).hexdigest()==prior['hires.txt']
lines=text.splitlines();defs={l[11:].split(',')[0]:l[11:].split(',')for l in lines if l.startswith('<condition>')}
conditions=[];rules=[];backgrounds=[];records=[];defined={}
ALPHA=176
# Preserve the accepted panorama RGB. Its opacity lets the native universal
# flash color show through using Mesen's own premultiplied alpha blend.
files={}
for name in ['Cavern','Interior']:
 original=f'Demonic_Palace_{name}.png';target=f'Demonic_Palace_{name}_Flash.png'
 im=Image.open(P/original).convert('RGBA');im.putalpha(Image.new('L',im.size,ALPHA));im.save(P/target);files[original]=target
def head(source,phase):
 terms=[]
 for term in source.split('&'):
  name=term.lstrip('!');neg='!'if term.startswith('!')else''
  if name in {'hmirror','vmirror','bgpriority'}:terms.append(term);continue
  key=(name,phase)
  if key not in defined:
   new='palaceFlash'+phase+'_'+name;d=defs[name].copy();d[0]=new
   if d[1]in ['tileNearby','tileAtPosition']and d[5].startswith('0F'):d[5]=phase+d[5][2:]
   defined[key]=new;conditions.append('<condition>'+','.join(d))
  terms.append(neg+defined[key])
 return '&'.join(terms)
for phase in ['30','31']:
 for line in lines:
  m=re.fullmatch(r'\[([^]]+)\]<(tile|background)>(.*)',line)
  if not m or not m[1].startswith('palace'):continue
  f=m[3].split(',')
  if m[2]=='tile':
   t=int(f[1],16)
   if not (0x1100<=t<=0x11ff or 0x1300<=t<=0x13ff)or not f[2].startswith('0F'):continue
   f[2]=phase+f[2][2:];rule='['+head(m[1],phase)+']<tile>'+','.join(f);rules.append(rule)
  else:
   if f[0]not in files:continue
   guards=[defs[t.lstrip('!')]for t in m[1].split('&')if defs[t.lstrip('!')][1]=='tileAtPosition']
   assert guards and all(d[5].startswith('0F')for d in guards)
   f[0]=files[f[0]];rule='['+head(m[1],phase)+']<background>'+','.join(f);backgrounds.append(rule)
  records.append(dict(source_rule=line,rule=rule,phase=phase,kind=m[2]))
def block(name,ls):return '# BEGIN PALACE_FLASH '+name+'\n'+'\n'.join(ls)+'\n# END PALACE_FLASH '+name+'\n'
start=text.index('# BEGIN PALACE_NEXT CONDITIONS');text=text[:start]+block('CONDITIONS',conditions)+block('MAPPINGS',rules+backgrounds)+text[start:]
(P/'hires.txt').write_text(text);(A/'registration.json').write_text(json.dumps(dict(opacity=ALPHA,files=files,conditions=conditions,mappings=records,tile_rules=len(rules),background_rules=len(backgrounds)),indent=2)+'\n')
print('Palace flash:',len(rules),'tile aliases;',len(backgrounds),'background aliases; unchanged source RGB and native flash color')
