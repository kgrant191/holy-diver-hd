from pathlib import Path
from PIL import Image,ImageChops
import argparse,json
p=argparse.ArgumentParser();p.add_argument('--before',required=True);p.add_argument('--after',required=True);p.add_argument('--out',required=True);a=p.parse_args();b=Path(a.before);c=Path(a.after);r={}
for ext in ['ram','ppu','oam']:
 fs=sorted((b/'dumps').glob('*.'+ext));assert len(fs)==450
 assert all(f.read_bytes()==(c/'dumps'/f.name).read_bytes()for f in fs),ext
 r[ext+'_identical_frames']=len(fs)
for name in ['apu.tsv','commands.tsv']:
 assert(b/name).read_bytes()==(c/name).read_bytes(),name;r[name]='identical'
changed=[];same=[]
for f in sorted((b/'frames').glob('*.png')):
 if f.read_bytes()==(c/'frames'/f.name).read_bytes():same.append(int(f.stem));continue
 x=Image.open(f).convert('RGB');y=Image.open(c/'frames'/f.name).convert('RGB');diff=ImageChops.difference(x,y);box=diff.getbbox();assert box and 80<=box[0]<box[2]<=112 and 144<=box[1]<box[3]<=176,(f.name,box)
 changed.append({'frame':int(f.stem),'changed_bounds':box})
assert changed;r.update(unchanged_render_frames=len(same),changed_menu_frames=len(changed),first_changed_frame=changed[0]['frame'],last_changed_frame=changed[-1]['frame'],all_changes_confined_to_bracelet_icon=True,native_pickup_frame=702,controller_start_frame=725,controller_resume_frame=845)
Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
