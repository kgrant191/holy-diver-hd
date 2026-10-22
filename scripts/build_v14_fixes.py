"""Replace the mistaken bracelet art; retain HD player fallback during death."""
from pathlib import Path
from PIL import Image
import re,json,shutil
root=Path(__file__).resolve().parents[1];out=root/'build/Holy_Diver_(Tr)';art=root/'art';seed=root/'rollback/screen2_v13'
shutil.copytree(seed,out,dirs_exist_ok=True)
p=out/'hires.txt';lines=p.read_text().splitlines()
# Remove both erroneous wing-animation phases for the same native pickup.
lines=[l for l in lines if not l.startswith('<condition>cryptBatPhase,') and not re.search(r'<tile>25,7[4-7],FF160636,',l)]
idx=sum(l.startswith('<img>')for l in lines);assert idx==26
last=max(i for i,l in enumerate(lines)if l.startswith('<img>'));lines.insert(last+1,'<img>Bracelet_2x.png')
src=Image.open(art/'generated/bracelet_generated.png').convert('RGBA');bb=src.getchannel('A').point(lambda a:255 if a>=120 else 0).getbbox();src=src.crop(bb).resize((30,22),Image.Resampling.LANCZOS)
a=src.getchannel('A').point(lambda a:255 if a>=125 else 0);src=src.convert('RGB').quantize(colors=32,method=Image.Quantize.MEDIANCUT).convert('RGBA');src.putalpha(a)
bracelet=Image.new('RGBA',(32,32));bracelet.alpha_composite(src,(1,0));bracelet.save(out/'Bracelet_2x.png');bracelet.save(art/'room2/bracelet_hd.png')
bracelet_rules=[f'[cryptPalette&cryptStonePalette&cryptSpritePalette]<tile>26,{0x74+j:02X},FF160636,{j%2*16},{j//2*16},1,N'for j in range(4)]
insert=next(i for i,l in enumerate(lines)if '#Chr_00_0.png' in l);lines[insert:insert]=bracelet_rules
# Keep pose-specific rules first. If a frozen/flickering death frame no longer
# supplies a complete sprite-neighborhood signature, fall back to approved HD
# tiles for that native tile/palette rather than to the original CHR atlas.
condition='<condition>randyDefeated,memoryCheckConstant,0440,==,00'
insert=next(i for i,l in enumerate(lines)if l.startswith('<condition>'));lines.insert(insert,condition)
known={};unconditional=set()
for l in lines:
 m=re.match(r'(?:\[([^]]+)\])?<tile>(18|19|22),([^,]+),([^,]+),(.*)',l)
 if not m:continue
 prefix,atlas,t,palette,tail=m.groups();key=(t,palette)
 if not prefix:unconditional.add(key)
 # Prefer the ordinary approved pose as a fallback; raised casts have their
 # dedicated signature rules, which still run first.
 if key not in known or (known[key][0]=='22' and atlas!='22'):known[key]=(atlas,tail)
fallback={k:v for k,v in known.items()if k not in unconditional}
# Insert after the final signature rule for the same key. All stock fallback
# mappings occur later, and no existing unconditional HD rule is shadowed.
last={}
for i,l in enumerate(lines):
 m=re.match(r'\[[^]]+\]<tile>[^,]+,([^,]+),([^,]+),',l)
 if m and (m[1],m[2])in fallback:last[(m[1],m[2])]=i
for key,i in sorted(last.items(),key=lambda item:item[1],reverse=True):
 atlas,tail=fallback[key];lines.insert(i+1,f'[randyDefeated]<tile>{atlas},{key[0]},{key[1]},{tail}')
p.write_text('\n'.join(lines)+'\n')
(art/'v14_registration.json').write_text(json.dumps({'bracelet_tiles':['74','75','76','77'],'bracelet_palette':'FF160636','bracelet_size':[30,22],'animation':'static pickup; native motion retained','death_fallback_rules':len(fallback),'death_gate':'native health $0440 == 0','fallback_source':'unchanged approved normal/Twin Fire player atlases','preserved':'specific pose rules retain priority'},indent=2)+'\n')
print('Added bracelet rules:',len(bracelet_rules),'HD death fallback rules:',len(fallback))
