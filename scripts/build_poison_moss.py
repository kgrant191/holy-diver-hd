"""Give completed Poison Moss Land rooms their own green ruin scenery."""
from pathlib import Path
import json,re,hashlib
import numpy as np
from PIL import Image
r=Path(__file__).resolve().parents[1];pack=r/'build/Holy_Diver_(Tr)';art=r/'art/poison_moss';art.mkdir(exist_ok=True)
text=(pack/'hires.txt').read_text();images=[l[5:]for l in text.splitlines()if l.startswith('<img>')];assert len(images)==45
source=Image.open(r/'art/generated/poison_moss_materials.png').convert('RGB');w,h=source.size
materials={name:source.crop(box).resize((32,32),Image.Resampling.LANCZOS).convert('RGBA')for name,box in{
 'brick':(0,0,w//2,h//2),'ledge':(w//2,0,w,h//2),'stair':(0,h//2,w//2,h),'ceiling':(w//2,h//2,w,h)}.items()}
for name,im in materials.items():im.save(art/(name+'.png'))
atlas=Image.new('RGBA',(512,256));cache={};rules=[];records=[];imagecache={}
def cell(idx,x,y):
 if idx not in imagecache:imagecache[idx]=Image.open(pack/images[idx]).convert('RGBA')
 return imagecache[idx].crop((x,y,x+16,y+16))
for line in text.splitlines():
 m=re.fullmatch(r'\[(l3[^]]+)\]<tile>(.*)',line)
 if not m:continue
 scope,f=m[1],m[2].split(',');t=int(f[1],16);pal=f[2]
 if not 0x700<=t<0x800 or 0x73e<=t<=0x743:continue
 # The approved continuous oak trunk/branch registrations remain wood.
 if ('l3_tree'in scope or'l3_forest'in scope)and pal=='0F091929':continue
 original=cell(int(f[0]),int(f[3]),int(f[4]));alpha=original.getchannel('A')
 if not alpha.getbbox():continue
 kind='brick';x,y=t%2,(t//2)%2
 if 0x734<=t<=0x737:kind='ledge';x,y=(t-0x734)%2,(t-0x734)//2
 elif 0x774<=t<=0x77b:kind='ledge'
 elif 0x77c<=t<=0x787:
  kind='stair';v=(t-0x77c)%4;x,y=1-v%2,1-v//2
 elif 0x792<=t<=0x795 or'l3_shaft'in scope:kind='ceiling'
 im=materials[kind].crop((x*16,y*16,x*16+16,y*16+16));im.putalpha(alpha)
 assert im.getchannel('A').tobytes()==alpha.tobytes()
 key=hashlib.sha256(im.tobytes()).hexdigest()
 if key not in cache:
  n=len(cache);xy=(n%32*16,n//32*16);assert xy[1]+16<=256;cache[key]=xy;atlas.paste(im,xy)
 xx,yy=cache[key];nf=f.copy();nf[0]='45';nf[3:5]=[str(xx),str(yy)];rule='['+scope+']<tile>'+','.join(nf);rules.append(rule)
 records.append(dict(source_rule=line,rule=rule,material=kind,tile=f[1],palette=pal,scope=scope,xy=[xx,yy],alpha_sha256=hashlib.sha256(alpha.tobytes()).hexdigest()))
# New panoramas are separate assets; Stage 1/2 backgrounds remain untouched.
for name in['forest','ruins']:
 im=Image.open(r/f'art/generated/poison_moss_{name}.png').convert('RGB').resize((1024,480),Image.Resampling.LANCZOS)
 # Stock Mesen's horizontal background camera wraps every 512 native pixels.
 # Make that entire 1024-HD-pixel period seamless, including its wrap edge.
 half=im.crop((0,0,512,480));im.paste(half.transpose(Image.Transpose.FLIP_LEFT_RIGHT),(512,0))
 pan=Image.new('RGB',(10240,480))
 for i in range(10):pan.paste(im,(i*1024,0))
 pan.save(pack/f'Poison_Moss_{name.title()}_Background.png');im.save(art/(name+'_preview.png'))
backgrounds=[];lines=[]
for line in text.splitlines(keepends=True):
 m=re.match(r'\[l3[^]]+\]<background>([^,]+),',line)
 if m and m[1]in['Stage3_Forest_Background.png','Nave_Background.png','Stage2_Cave_Background.png']:
  name='Forest'if m[1]=='Stage3_Forest_Background.png'else'Ruins';new=line.replace(m[1],f'Poison_Moss_{name}_Background.png',1)
  backgrounds.append(dict(before=line.rstrip('\n'),after=new.rstrip('\n')));line=new
 lines.append(line)
text=''.join(lines)
def block(part,items):return '# BEGIN POISON_MOSS '+part+'\n'+'\n'.join(items)+'\n# END POISON_MOSS '+part+'\n'
end=text.index('\n',text.rfind('<img>'))+1;text=text[:end]+block('IMAGES',['<img>Poison_Moss_Tiles_2x.png'])+text[end:]
lines=text.splitlines(keepends=True);first=next(i for i,l in enumerate(lines)if '<tile>'in l or'<background>'in l);lines[first:first]=[block('MAPPINGS',rules)]
(pack/'hires.txt').write_text(''.join(lines));atlas.save(pack/'Poison_Moss_Tiles_2x.png');atlas.save(art/'Poison_Moss_Tiles_2x.png')
(art/'registration.json').write_text(json.dumps(dict(tile_rules=len(rules),conditions=0,background_rules=0,background_replacements=backgrounds,mappings=records,atlas_cells=len(cache),preserve_all_alpha_masks=True,previous_artwork_files_unchanged=True,native_gameplay_modified=False),indent=2)+'\n')
print('Poison Moss Land:',len(rules),'green terrain registrations;',len(backgrounds),'scoped backdrop substitutions; original geometry and actors exact.')
